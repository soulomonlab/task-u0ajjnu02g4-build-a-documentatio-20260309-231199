from typing import Callable, Optional
import time
import os
import json

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

import redis

# Config via env
RATE_LIMIT_REDIS_URL = os.getenv("RATE_LIMIT_REDIS_URL", None)
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
RATE_LIMIT_DEFAULT = int(os.getenv("RATE_LIMIT_DEFAULT", "300"))
DRY_RUN_LIMIT = int(os.getenv("DRY_RUN_LIMIT", "10"))

# Initialize Redis client lazily
_redis_client: Optional[redis.Redis] = None


def get_redis_client():
    global _redis_client
    if _redis_client is None and RATE_LIMIT_REDIS_URL:
        _redis_client = redis.Redis.from_url(RATE_LIMIT_REDIS_URL)
    return _redis_client


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple Redis-backed windowed rate limiter with DRY_RUN separation.

    Recognizes dry-run via header 'X-Dry-Run: true' or query param 'dry_run=1'.
    On DRY_RUN_LIMIT exceeded returns 429 with Retry-After and KB link.
    """

    def __init__(self, app, get_client_ip: Optional[Callable[[Request], str]] = None):
        super().__init__(app)
        self.get_client_ip = get_client_ip or (lambda req: req.client.host if req.client else "unknown")

    async def dispatch(self, request: Request, call_next):
        client = get_redis_client()
        is_dry_run = False
        try:
            if request.headers.get("X-Dry-Run", "").lower() == "true":
                is_dry_run = True
            elif request.query_params.get("dry_run") == "1":
                is_dry_run = True
        except Exception:
            is_dry_run = False

        key_prefix = "rate:" if not is_dry_run else "rate:dry:"
        # Identify the rate-limited subject: use api key header if present else client ip
        subject = request.headers.get("X-Api-Key") or self.get_client_ip(request)
        key = f"{key_prefix}{subject}:{int(time.time() // RATE_LIMIT_WINDOW)}"

        limit = DRY_RUN_LIMIT if is_dry_run else RATE_LIMIT_DEFAULT
        remaining = None
        retry_after = None

        try:
            if client:
                # Use INCR on a windowed key, set TTL
                count = client.incr(key)
                client.expire(key, RATE_LIMIT_WINDOW)
                remaining = max(0, limit - int(count))
                if count > limit:
                    # compute retry-after as time until window expires
                    ttl = client.ttl(key)
                    retry_after = ttl if ttl > 0 else RATE_LIMIT_WINDOW
            else:
                # Fallback: in-process naive counter stored on the object: not safe across processes
                if not hasattr(self, "_inproc_counters"):
                    self._inproc_counters = {}
                count = self._inproc_counters.get(key, 0) + 1
                self._inproc_counters[key] = count
                remaining = max(0, limit - int(count))
                if count > limit:
                    retry_after = RATE_LIMIT_WINDOW
        except Exception as e:
            # If Redis fails, log and allow request through (fail-open) but include a warning header
            # For this standalone file we just print, but production should use structured logging
            print("RateLimitMiddleware: redis error", e)
            response = await call_next(request)
            response.headers["X-RateLimit-Note"] = "rate-limit-redis-failure-fail-open"
            return response

        if retry_after is not None and retry_after > 0:
            body = {"error": "DRY_RUN_LIMIT_EXCEEDED" if is_dry_run else "RATE_LIMIT_EXCEEDED",
                    "message": "Your requests exceeded the temporary limit.",
                    "kb": os.getenv("SUPPORT_KB_DRY_RUN", "")}
            headers = {
                "Retry-After": str(retry_after),
                "X-RateLimit-Limit": str(limit),
                "X-RateLimit-Remaining": str(remaining),
            }
            return JSONResponse(status_code=429, content=body, headers=headers)

        # Attach rate limit headers for visibility
        response = await call_next(request)
        if remaining is not None:
            response.headers["X-RateLimit-Limit"] = str(limit)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response
