"""
Staging-only Test Control Middleware for FastAPI
- Enables QA to drive test scenarios via special headers:
  - X-Test-Force-Status: force the response status code (int)
  - X-Test-Reset-RateLimit: reset rate-limiter state for a given API key (string or 'all')
  - X-Soft-Canary: set a routing hint (percentage or 'on')

Usage:
- Mount in FastAPI app: app.add_middleware(TestControlMiddleware)
- Enable with environment variable TEST_CONTROLS_ENABLED=1 (default: disabled)
- Optional Redis integration: set REDIS_URL to use Redis instead of in-memory store

NOT FOR PRODUCTION: intended for staging only.
"""
from __future__ import annotations

import os
import threading
from typing import Optional, Dict, Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi.responses import JSONResponse

# Try to import Redis; if not available we'll fall back to in-memory store.
try:
    import redis
except Exception:  # pragma: no cover - optional dependency
    redis = None


class TestControlStore:
    """Abstracts storage for test-control state. Uses Redis if REDIS_URL is set, else in-memory dict."""

    def __init__(self, redis_url: Optional[str] = None):
        self._use_redis = bool(redis and redis_url)
        self._lock = threading.Lock()
        if self._use_redis:
            self._client = redis.Redis.from_url(redis_url)
        else:
            self._store: Dict[str, Any] = {}

    def reset_rate_limit(self, api_key: Optional[str] = None) -> None:
        """Reset rate limiter state for a specific api_key or all keys if api_key is None or 'all'."""
        if self._use_redis:
            if api_key in (None, "all"):
                # WARNING: This is simplistic. In production, you'd delete specific keys or use a namespace.
                for key in self._client.scan_iter(match="ratelimit:*"):
                    self._client.delete(key)
            else:
                self._client.delete(f"ratelimit:{api_key}")
        else:
            with self._lock:
                if api_key in (None, "all"):
                    self._store.clear()
                else:
                    self._store.pop(f"ratelimit:{api_key}", None)

    def set_metadata(self, key: str, value: Any) -> None:
        if self._use_redis:
            self._client.hset("test_control:meta", key, str(value))
        else:
            with self._lock:
                self._store[f"meta:{key}"] = value

    def get_metadata(self, key: str) -> Optional[Any]:
        if self._use_redis:
            v = self._client.hget("test_control:meta", key)
            return v.decode() if v else None
        else:
            with self._lock:
                return self._store.get(f"meta:{key}")


class TestControlMiddleware(BaseHTTPMiddleware):
    """FastAPI middleware to interpret staging-only test-control headers.

    Behaviour:
    - If X-Test-Force-Status is present: short-circuit and return that status with JSON body.
    - If X-Test-Reset-RateLimit is present: reset the rate-limit state for that API key (or 'all').
    - If X-Soft-Canary is present: attach routing hint to request.state for downstream handlers.

    Environment variables:
    - TEST_CONTROLS_ENABLED=1 to enable middleware in staging
    - REDIS_URL (optional) to persist test-control state and operate on rate-limit keys
    """

    def __init__(self, app, redis_url: Optional[str] = None):
        super().__init__(app)
        self.enabled = os.getenv("TEST_CONTROLS_ENABLED", "0") in ("1", "true", "True")
        self.store = TestControlStore(redis_url=redis_url)

    async def dispatch(self, request: Request, call_next):
        if not self.enabled:
            # Pass-through when disabled
            return await call_next(request)

        headers = {k.lower(): v for k, v in request.headers.items()}
        # 1) Force status code (immediate short-circuit)
        force_status = headers.get("x-test-force-status")
        if force_status:
            try:
                status_code = int(force_status)
            except ValueError:
                return JSONResponse({"error": "invalid X-Test-Force-Status value"}, status_code=400)

            # Helpful JSON body for QA to assert on
            return JSONResponse({"test_control": "forced_status", "status": status_code}, status_code=status_code)

        # 2) Reset rate limit
        reset_rl = headers.get("x-test-reset-ratelimit")
        if reset_rl:
            # If value is 'all' or empty -> reset global
            api_key = reset_rl if reset_rl.strip() else None
            if api_key == "":
                api_key = None
            self.store.reset_rate_limit(api_key=api_key)
            # attach flag for downstream logging
            request.state.test_control_reset_ratelimit = api_key or "all"

        # 3) Soft canary hint
        soft_canary = headers.get("x-soft-canary")
        if soft_canary:
            # Expect value to be 'on', 'off', or a percentage '10' (means 10%)
            request.state.test_control_soft_canary = soft_canary

        # Attach raw test-control headers for handlers to consult
        request.state.test_control_headers = {
            "x-test-force-status": force_status,
            "x-test-reset-ratelimit": reset_rl,
            "x-soft-canary": soft_canary,
        }

        response = await call_next(request)

        # Expose minimal debug info in staging responses if requested
        if headers.get("x-test-echo") == "1":
            # be careful not to leak sensitive info
            response.headers["x-test-control-applied"] = ",".join(k for k, v in request.state.test_control_headers.items() if v)

        return response


# Helper: convenience function to generate a stable test API key (UUID4 suffix)
def generate_test_api_key(prefix: str = "stg-test") -> str:
    import uuid

    return f"{prefix}-{uuid.uuid4().hex[:12]}"


# If file executed directly, print sample usage
if __name__ == "__main__":
    print("TestControlMiddleware module loaded.")
    print("Enable by setting TEST_CONTROLS_ENABLED=1 and adding middleware to your FastAPI app.")
