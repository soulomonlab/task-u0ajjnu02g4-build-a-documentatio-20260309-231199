import os
import time
import requests
import pytest

BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8000")
API_KEY = os.environ.get("TEST_API_KEY", "test-key-1")
API_KEY_2 = os.environ.get("TEST_API_KEY_2", "test-key-2")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN")

HEADERS = {"Authorization": f"Bearer {API_KEY}"}
HEADERS_2 = {"Authorization": f"Bearer {API_KEY_2}"}


def reset_rate_limit(api_key):
    if not ADMIN_TOKEN:
        pytest.skip("ADMIN_TOKEN not set; skipping rate-limit reset admin calls")
    resp = requests.post(f"{BASE_URL}/__qa/reset_rate_limit", params={"api_key": api_key}, headers={"Authorization": f"Bearer {ADMIN_TOKEN}"})
    assert resp.status_code == 200


@pytests.fixture(autouse=True)
def ensure_env():
    if not BASE_URL:
        pytest.skip("TEST_BASE_URL not set; skipping tests")


def send_ping(headers):
    return requests.get(f"{BASE_URL}/healthcheck", headers=headers)


def test_rate_limit_per_api_key_and_burst():
    """Send a burst of requests exceeding the allowed burst and ensure 429 + Retry-After for excess requests.

    Assumes rate limit = 60 req/min + burst 10 (i.e., first 10 extra allowed, then 429).
    """
    # Reset token buckets
    if ADMIN_TOKEN:
        reset_rate_limit(API_KEY)
        reset_rate_limit(API_KEY_2)
    else:
        pytest.skip("ADMIN_TOKEN not set; cannot reset token buckets. Set ADMIN_TOKEN to enable this test.")

    # Send 75 quick requests with same API key -> expect 15 429s (beyond 60+10)
    total_requests = 75
    responses = []
    for i in range(total_requests):
        resp = send_ping(HEADERS)
        responses.append(resp)

    status_counts = {}
    for r in responses:
        status_counts[r.status_code] = status_counts.get(r.status_code, 0) + 1

    # Expect at least some 429 responses
    assert 429 in status_counts, f"Expected 429 responses but got counts: {status_counts}"

    # Check Retry-After header on 429s
    for r in responses:
        if r.status_code == 429:
            assert "Retry-After" in r.headers, "429 response missing Retry-After header"
            # should be integer seconds
            assert r.headers["Retry-After"].isdigit(), f"Retry-After not integer: {r.headers['Retry-After']}"

    # Validate per-api-key scoping by sending a request with a different key and expecting it not to be 429
    resp_other = send_ping(HEADERS_2)
    assert resp_other.status_code != 429, "Rate limiting incorrectly shared across API keys"
