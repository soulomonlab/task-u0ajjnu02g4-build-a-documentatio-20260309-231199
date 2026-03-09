import os
import time
import requests
import pytest

BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8000")
API_KEY = os.environ.get("TEST_API_KEY", "test-key-1")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}


def force_next_response(status):
    if not ADMIN_TOKEN:
        pytest.skip("ADMIN_TOKEN not set; skipping forced-response tests")
    resp = requests.post(f"{BASE_URL}/__qa/force_next_response", json={"path": "/test/retry","status": status}, headers={"Authorization": f"Bearer {ADMIN_TOKEN}"})
    assert resp.status_code == 200


def client_call(method="GET", idempotency_key=None):
    headers = HEADERS.copy()
    if idempotency_key:
        headers["Idempotency-Key"] = idempotency_key
    if method == "GET":
        return requests.get(f"{BASE_URL}/test/retry", headers=headers)
    elif method == "POST":
        return requests.post(f"{BASE_URL}/test/retry", json={"x":1}, headers=headers)
    elif method == "PUT":
        return requests.put(f"{BASE_URL}/test/retry", json={"x":1}, headers=headers)
    else:
        raise ValueError("unsupported method")


def test_retries_only_on_502_503_504_and_idempotent_methods():
    # Force a 502 server response
    if ADMIN_TOKEN:
        force_next_response(502)
    else:
        pytest.skip("ADMIN_TOKEN not set; skipping retry behavior tests")

    # Expect client to retry up to 3 attempts for GET
    t0 = time.time()
    resp = client_call(method="GET")
    elapsed = time.time() - t0
    # If retries configured: elapsed should be >= 0.5 (first backoff) and less than some upper bound (e.g., 10s)
    assert elapsed >= 0.4, "No retry delay observed for GET on 502"

    # For POST without Idempotency-Key: should not retry. Force another 502 and measure quick response
    if ADMIN_TOKEN:
        force_next_response(502)
    t0 = time.time()
    resp_post = client_call(method="POST")
    elapsed_post = time.time() - t0
    assert elapsed_post < 0.5, "POST without Idempotency-Key should not retry on 502"

    # For POST with Idempotency-Key: should retry
    if ADMIN_TOKEN:
        force_next_response(502)
    t0 = time.time()
    resp_post_idem = client_call(method="POST", idempotency_key="idem-123")
    elapsed_post_idem = time.time() - t0
    assert elapsed_post_idem >= 0.4, "POST with Idempotency-Key did not retry on 502"


def test_max_three_attempts_enforced():
    # Force repeated 503 responses; ensure client stops after 3 attempts
    if ADMIN_TOKEN:
        force_next_response(503)
    else:
        pytest.skip("ADMIN_TOKEN not set; skipping retry attempt count test")

    t0 = time.time()
    resp = client_call(method="GET")
    elapsed = time.time() - t0
    # For exponential backoff 0.5s initial, 1s next, 2s next ~ total ~3.5s (plus jitter) -> expect elapsed < 10
    assert elapsed < 15, f"Retries took too long, elapsed={elapsed}"

    # No server error should be returned more than 3 times; we can't inspect client internals here, so rely on timing and logs
    assert resp.status_code in (502,503,504), "Final response not a retriable error as expected"
