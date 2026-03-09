from fastapi import FastAPI, Request, Response, Header, HTTPException
from typing import Optional
import random
import time
from datetime import datetime

app = FastAPI(title="Test Control Endpoints", version="1.0")

# In-memory state for test-only controls. This is intentionally simple for staging/test environments.
_state = {
    "rate_limit_mode": "soft",  # or 'hard'
}


@app.get("/test/rate_limit_mode")
async def get_rate_limit_mode():
    """Return current rate limit enforcement mode."""
    return {"mode": _state["rate_limit_mode"]}


@app.post("/test/rate_limit_mode")
async def set_rate_limit_mode(mode: str):
    """Set rate limit enforcement mode. mode must be 'soft' or 'hard'."""
    if mode not in ("soft", "hard"):
        raise HTTPException(status_code=400, detail="mode must be 'soft' or 'hard'")
    _state["rate_limit_mode"] = mode
    return {"mode": _state["rate_limit_mode"]}


@app.get("/test/retry/{behavior}")
async def test_retry_behavior(
    behavior: str,
    request: Request,
    response: Response,
    x_retry_attempts: Optional[str] = Header(None),
    x_test_id: Optional[str] = Header(None),
):
    """
    Controlled endpoints to simulate transient failures and to expose retry metadata.

    Supported behaviors:
    - always_502 / always_503 / always_504 : always return the specified status code
    - flaky_50 : 50% chance to return 503, 50% success
    - slow_1s : sleep 1 second then return 200
    - slow_3s : sleep 3 seconds then return 200

    Tests can pass header `X-Retry-Attempts` to indicate how many attempts have been made so far.
    The endpoint will echo headers `X-Retry-Attempts` and `X-Retry-TIMESTAMPS` to help QA observe retry behavior.
    """

    # Read incoming retry attempts header (if present)
    try:
        attempts_val = int(x_retry_attempts) if x_retry_attempts is not None else 0
    except ValueError:
        attempts_val = 0

    # Append a timestamp for this attempt
    now_iso = datetime.utcnow().isoformat() + "Z"

    # Build response headers to help tests observe retry behavior
    resp_attempts = str(attempts_val)
    # X-Retry-Timestamps echo: include the existing timestamps (if any) from a request header 'X-Retry-Timestamps'
    incoming_timestamps = request.headers.get("x-retry-timestamps", "")
    outgoing_timestamps = (incoming_timestamps + "," if incoming_timestamps else "") + now_iso
    response.headers["X-Retry-Attempts"] = resp_attempts
    response.headers["X-Retry-TIMESTAMPS"] = outgoing_timestamps
    if x_test_id:
        response.headers["X-Test-Id"] = x_test_id

    # Behavior dispatch
    if behavior in ("always_502", "always_503", "always_504"):
        status_code = int(behavior.split("_")[1])
        raise HTTPException(status_code=status_code, detail=f"Forced {status_code} for testing")

    if behavior == "flaky_50":
        if random.random() < 0.5:
            raise HTTPException(status_code=503, detail="Intermittent 503 for testing")
        return {"status": "ok", "behavior": behavior}

    if behavior == "slow_1s":
        time.sleep(1)
        return {"status": "ok", "latency": "1s"}

    if behavior == "slow_3s":
        time.sleep(3)
        return {"status": "ok", "latency": "3s"}

    # default: echo back
    return {"status": "echo", "behavior": behavior}


@app.get("/test/info")
async def info():
    """Simple info endpoint for smoke checks."""
    return {"service": "test-control", "rate_limit_mode": _state["rate_limit_mode"]}


# Allow running locally for staging usage
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("test_control_endpoints:app", host="0.0.0.0", port=8001, log_level="info")
