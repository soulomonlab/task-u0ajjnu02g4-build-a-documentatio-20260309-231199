import os
import pytest
import requests

STAGING_URL = os.getenv("STAGING_URL")

pytest.skip_reason = "STAGING_URL not set; skipping integration tests against staging"

@pytest.fixture
def base_url():
    if not STAGING_URL:
        pytest.skip(pytest.skip_reason)
    return STAGING_URL.rstrip("/")

def test_rate_limit_endpoint_exists(base_url):
    """Verify test-only rate limit endpoint exists and returns 200 and expected fields."""
    url = f"{base_url}/test-only/rate_limit_status"
    resp = requests.get(url, timeout=10)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
    data = resp.json()
    assert "rate_limit" in data, f"Missing 'rate_limit' in response: {data}"
    assert isinstance(data["rate_limit"], dict)

def test_retry_endpoint_triggers_retry_logic(base_url):
    """Verify test-only retry endpoint returns retry metadata and eventual success."""
    url = f"{base_url}/test-only/retry_test"
    # The endpoint should return a JSON with 'attempts' and 'status'
    resp = requests.post(url, json={"simulate_failures": 2}, timeout=20)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
    data = resp.json()
    assert "attempts" in data and "status" in data
    assert data["status"] == "ok", f"Expected status 'ok', got {data['status']}"
    assert data["attempts"] >= 1

def test_rate_limit_behavior_under_burst(base_url):
    """Basic check: when sending a small burst, some 429s may be returned but service remains responsive."""
    url = f"{base_url}/api/health"
    # Send a small burst of requests
    results = []
    for _ in range(10):
        r = requests.get(url, timeout=5)
        results.append(r.status_code)
    # At least one 2xx or 429 expected; fail if all 5xx
    assert any(200 <= s < 300 for s in results) or any(s == 429 for s in results), f"Unexpected statuses: {results}"
