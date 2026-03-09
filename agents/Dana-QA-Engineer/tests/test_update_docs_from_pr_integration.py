import os
import requests
import time
import pytest

BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:8000")

# Helpers
def refresh_token(refresh_token):
    url = f"{BASE_URL}/api/v1/auth/refresh"
    return requests.post(url, json={"refresh_token": refresh_token})

def create_item(payload, idempotency_key=None):
    headers = {}
    if idempotency_key:
        headers["Idempotency-Key"] = idempotency_key
    url = f"{BASE_URL}/api/v1/items"
    return requests.post(url, json=payload, headers=headers)

def get_items(params=None):
    url = f"{BASE_URL}/api/v1/items"
    return requests.get(url, params=params)

def get_users():
    url = f"{BASE_URL}/api/v1/users"
    return requests.get(url)

# Tests
@pytest.mark.integration
def test_refresh_happy_path():
    # Requires TEST_REFRESH_TOKEN env var
    token = os.getenv("TEST_REFRESH_TOKEN")
    assert token, "Set TEST_REFRESH_TOKEN to run this test"
    r = refresh_token(token)
    assert r.status_code == 200, f"Expected 200, got {r.status_code} - {r.text}"
    data = r.json()
    assert "access_token" in data and data["access_token"], "access_token missing"

@pytest.mark.integration
def test_refresh_invalid_token():
    r = refresh_token("bad-token")
    assert r.status_code == 401, f"Expected 401 for invalid refresh, got {r.status_code} - {r.text}"

@pytest.mark.integration
def test_refresh_race_condition_simultaneous_requests():
    token = os.getenv("TEST_REFRESH_TOKEN")
    assert token, "Set TEST_REFRESH_TOKEN to run this test"
    # Fire two near-simultaneous refresh requests
    from concurrent.futures import ThreadPoolExecutor
    def do_refresh():
        return refresh_token(token)
    with ThreadPoolExecutor(max_workers=2) as ex:
        futures = [ex.submit(do_refresh) for _ in range(2)]
        results = [f.result() for f in futures]
    statuses = [r.status_code for r in results]
    assert all(s == 200 for s in statuses), f"Expected both 200, got {statuses}"
    # Ensure tokens are present and not identical (rotated)
    tokens = [r.json().get("access_token") for r in results]
    assert all(tokens), f"Missing tokens: {tokens}"
    assert len(set(tokens)) == len(tokens), "Expected rotated tokens (distinct), got identical tokens"

@pytest.mark.integration
@pytest.mark.parametrize("page_size", [0, -1, 999999, "abc"])
def test_pagination_invalid_page_size(page_size):
    r = get_items(params={"page_size": page_size})
    assert r.status_code == 422, f"Expected 422 for invalid page_size={page_size}, got {r.status_code} - {r.text}"

@pytest.mark.integration
def test_pagination_boundary_values():
    # Assuming defaults: default_page_size=20, max_page_size=100
    r = get_items(params={"page_size": 20})
    assert r.status_code == 200
    data = r.json()
    assert "items" in data and isinstance(data["items"], list)
    assert "page" in data and "page_size" in data
    r2 = get_items(params={"page_size": 100})
    assert r2.status_code == 200

@pytest.mark.integration
def test_create_item_idempotency_retry():
    payload = {"name": "test-item-retry", "value": 1}
    key = f"test-key-{int(time.time())}"
    r1 = create_item(payload, idempotency_key=key)
    # Accept either 201 or 409 as first response depending on race; handle accordingly
    if r1.status_code == 201:
        created = r1.json()
    elif r1.status_code == 409:
        # Retry with exponential backoff
        backoff = 0.1
        created = None
        for _ in range(5):
            time.sleep(backoff)
            r = create_item(payload, idempotency_key=key)
            if r.status_code == 201:
                created = r.json()
                break
            backoff *= 2
        assert created, f"Expected eventual 201 after retries; last status {r.status_code}"
    else:
        pytest.fail(f"Unexpected status code {r1.status_code} - {r1.text}")

@pytest.mark.integration
def test_users_new_optional_field():
    r = get_users()
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list), "Expected list of users"
    # Check that items accept presence or absence of is_archived
    for u in data[:5]:
        assert isinstance(u, dict)
        # No assertion that is_archived must exist; but if exists it should be boolean
        if "is_archived" in u:
            assert isinstance(u["is_archived"], bool), f"is_archived must be boolean, got {u['is_archived']}"

