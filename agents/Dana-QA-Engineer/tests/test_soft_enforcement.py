import os
import requests
import pytest
import time

BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8000")
API_KEY = os.environ.get("TEST_API_KEY", "test-key-1")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}


def set_enforcement_mode(mode):
    if not ADMIN_TOKEN:
        pytest.skip("ADMIN_TOKEN not set; skipping enforcement mode tests")
    resp = requests.post(f"{BASE_URL}/__qa/set_enforcement_mode", json={"mode": mode}, headers={"Authorization": f"Bearer {ADMIN_TOKEN}"})
    assert resp.status_code == 200


def get_telemetry(metric):
    if not ADMIN_TOKEN:
        pytest.skip("ADMIN_TOKEN not set; skipping telemetry checks")
    resp = requests.get(f"{BASE_URL}/__qa/telemetry", params={"metric": metric}, headers={"Authorization": f"Bearer {ADMIN_TOKEN}"})
    assert resp.status_code == 200
    return resp.json()


def test_soft_vs_hard_enforcement_behavior():
    # Set soft mode
    set_enforcement_mode("soft")

    # Reset rate limit
    resp = requests.post(f"{BASE_URL}/__qa/reset_rate_limit", params={"api_key": API_KEY}, headers={"Authorization": f"Bearer {ADMIN_TOKEN}"})
    assert resp.status_code == 200

    # Send a burst > limit
    for i in range(75):
        r = requests.get(f"{BASE_URL}/healthcheck", headers=HEADERS)
        assert r.status_code == 200, "In soft mode server should not return 429"

    # Check telemetry shows warnings
    telemetry = get_telemetry("rate_limit_warnings")
    assert telemetry.get("count", 0) > 0, "Expected telemetry warnings in soft mode"

    # Switch to hard mode
    set_enforcement_mode("hard")

    # Reset
    resp = requests.post(f"{BASE_URL}/__qa/reset_rate_limit", params={"api_key": API_KEY}, headers={"Authorization": f"Bearer {ADMIN_TOKEN}"})
    assert resp.status_code == 200

    # Send burst again and expect 429s
    got_429 = False
    for i in range(75):
        r = requests.get(f"{BASE_URL}/healthcheck", headers=HEADERS)
        if r.status_code == 429:
            got_429 = True
            assert "Retry-After" in r.headers
            break
    assert got_429, "Hard enforcement did not produce any 429 responses"
