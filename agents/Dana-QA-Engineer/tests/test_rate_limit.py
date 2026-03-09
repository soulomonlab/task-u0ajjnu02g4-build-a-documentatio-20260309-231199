import os
import pytest

SERVICE_URL = os.getenv("SERVICE_URL")
API_KEY = os.getenv("TEST_API_KEY", "test-key")

if not SERVICE_URL:
    pytest.skip("SERVICE_URL not set. Integration tests require running service.", allow_module_level=True)


def _send_request(path, api_key=API_KEY, method='GET', data=None, headers=None):
    import requests
    url = SERVICE_URL.rstrip('/') + path
    hdrs = headers.copy() if headers else {}
    hdrs.setdefault('x-api-key', api_key)
    if method == 'GET':
        return requests.get(url, headers=hdrs)
    elif method == 'POST':
        return requests.post(url, json=data, headers=hdrs)
    else:
        return requests.request(method, url, json=data, headers=hdrs)


def test_rate_limit_per_api_key():
    """
    Per-API-key scope: issue 61 requests in a sliding minute window; expect 60 allowed, 1 rejected with 429 and Retry-After header set.
    Requires SERVICE_URL and TEST_API_KEY env vars.
    """
    allowed = 0
    denied = 0
    last_resp = None
    for i in range(61):
        resp = _send_request('/test/rate-limit')
        last_resp = resp
        if resp.status_code == 200:
            allowed += 1
        elif resp.status_code == 429:
            denied += 1
        else:
            # Non-standard status; still record
            pass

    assert allowed >= 60, f"Expected at least 60 allowed requests, got {allowed}"
    assert denied >= 1, f"Expected at least 1 denied request, got {denied}"
    assert last_resp is not None
    if last_resp.status_code == 429:
        assert ('Retry-After' in last_resp.headers) or ('retry-after' in last_resp.headers), "Retry-After header missing on 429"


def test_burst_behavior():
    """
    Burst behavior: send 12 immediate requests (burst=10); verify initial burst succeeds and subsequent requests are rate-limited per refill.
    """
    results = []
    for i in range(12):
        resp = _send_request('/test/rate-limit')
        results.append(resp.status_code)

    # Expect first 10 mostly 200, the rest may be 429
    first_10 = results[:10]
    tail = results[10:]
    assert sum(1 for s in first_10 if s == 200) >= 8, f"Expected most of first 10 to succeed, got statuses: {first_10}"
    assert any(s == 429 for s in tail), f"Expected rate-limiting in tail, got {tail}"


def test_soft_enforcement_logs_but_allows():
    """
    If enforcement_mode='soft' for this api key, requests exceeding hard limit should still be allowed (200)
    but a corresponding rate_limit_events entry should be available via management endpoint.

    Precondition: an admin has set the policy for TEST_API_KEY to enforcement_mode='soft'
    """
    # Send more than limit
    statuses = []
    for i in range(65):
        r = _send_request('/test/rate-limit')
        statuses.append(r.status_code)

    # All should be allowed if soft enforcement
    assert all(s == 200 for s in statuses), f"When soft, expected all 200 but saw: {set(statuses)}"
    # Verify events are emitted (management endpoint)
    admin_resp = _send_request(f'/admin/rate-limit-events?api_key={API_KEY}')
    assert admin_resp.status_code == 200
    events = admin_resp.json()
    assert isinstance(events, list)
    assert any(e.get('allowed') is False for e in events), "Expected at least one logged event with allowed=false"
