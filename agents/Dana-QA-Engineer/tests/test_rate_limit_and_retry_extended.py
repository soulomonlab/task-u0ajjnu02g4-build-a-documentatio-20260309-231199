import os
import time
import uuid
import requests
import pytest

BASE_URL = os.getenv('BASE_URL')
API_KEY = os.getenv('STAGING_API_KEY')

HEADERS = {
    'Authorization': f'Bearer {API_KEY}' if API_KEY else None,
}


def skip_if_no_env():
    if not BASE_URL or not API_KEY:
        pytest.skip('BASE_URL or STAGING_API_KEY not provided; skipping staging-only tests')


@pytest.fixture(scope='module')
def client_headers():
    skip_if_no_env()
    return {k: v for k, v in HEADERS.items() if v}


def post_create_resource(headers, payload, idempotency_key=None):
    h = headers.copy()
    if idempotency_key:
        h['Idempotency-Key'] = idempotency_key
    return requests.post(f"{BASE_URL}/v1/create-resource", json=payload, headers=h)


def get_test_endpoint(headers, params=None):
    return requests.get(f"{BASE_URL}/v1/test-endpoint", headers=headers, params=params)


def reset_rate_limit(headers):
    h = headers.copy()
    h['X-Test-Reset-RateLimit'] = '1'
    return requests.get(f"{BASE_URL}/__test__/reset-rate-limit", headers=h)


def force_status(headers, status_code, count=1):
    h = headers.copy()
    h['X-Test-Force-Status'] = str(status_code)
    h['X-Test-Force-Count'] = str(count)
    return requests.get(f"{BASE_URL}/__test__/force-status", headers=h)


def set_soft_canary(headers, percent):
    h = headers.copy()
    h['X-Soft-Canary'] = str(percent)
    return requests.get(f"{BASE_URL}/__test__/set-soft-canary", headers=h)


@pytest.mark.parametrize('burst_size', [20, 50])
def test_burst_rate_limit_enforcement(client_headers, burst_size):
    """Send a burst of requests after resetting rate limit and assert 429s occur after threshold."""
    reset_rate_limit(client_headers)
    successes = 0
    throttled = 0
    statuses = []

    for i in range(burst_size):
        r = get_test_endpoint(client_headers)
        statuses.append(r.status_code)
        if r.status_code == 200:
            successes += 1
        elif r.status_code == 429:
            throttled += 1

    assert throttled > 0, f"Expected some 429 responses in burst; got none. statuses={statuses}"


def test_steady_state_exceeding(client_headers):
    """Send sustained RPS above limit and ensure server returns consistent 429s."""
    # This is a basic approximation; CI runner should provide timing accuracy.
    reset_rate_limit(client_headers)
    duration = 10  # seconds
    interval = 0.1  # 10 RPS
    end = time.time() + duration
    statuses = []
    while time.time() < end:
        r = get_test_endpoint(client_headers)
        statuses.append(r.status_code)
        time.sleep(interval)

    throttled = statuses.count(429)
    assert throttled > 0, f"Expected throttled responses during sustained high RPS. statuses={statuses}"


def test_retry_behavior_respects_retry_after_and_backoff(client_headers):
    """Force 429s then ensure client backs off and succeeds after retries."""
    reset_rate_limit(client_headers)
    force_status(client_headers, 429, count=3)

    max_retries = 5
    attempt = 0
    backoff = 1
    while attempt < max_retries:
        r = get_test_endpoint(client_headers)
        if r.status_code == 200:
            break
        if r.status_code == 429:
            ra = r.headers.get('Retry-After')
            sleep = backoff
            if ra:
                try:
                    sleep = max(sleep, int(ra))
                except ValueError:
                    pass
            # jitter
            sleep = sleep * (0.5 + (0.5 * (attempt / max_retries)))
            time.sleep(sleep)
            backoff *= 2
        attempt += 1

    assert r.status_code == 200, f"Expected success after retries; last status {r.status_code}"


def test_idempotency_on_post_create(client_headers):
    """POST with same Idempotency-Key should not create duplicate resources."""
    reset_rate_limit(client_headers)
    payload = {'name': 'qa-test-' + str(uuid.uuid4())}
    key = str(uuid.uuid4())

    r1 = post_create_resource(client_headers, payload, idempotency_key=key)
    r2 = post_create_resource(client_headers, payload, idempotency_key=key)

    assert r1.status_code in (200, 201)
    assert r2.status_code in (200, 201, 409)

    # If both 200/201, ids must match
    if r1.status_code in (200, 201) and r2.status_code in (200, 201):
        j1 = r1.json()
        j2 = r2.json()
        assert j1.get('id') == j2.get('id'), f"Idempotent POST returned different ids: {j1} vs {j2}"


def test_soft_canary_routing_distribution(client_headers):
    """Set soft-canary percentage and assert observed proportion within tolerance."""
    set_soft_canary(client_headers, 10)
    N = 200
    canary_count = 0
    for i in range(N):
        r = get_test_endpoint(client_headers)
        if r.headers.get('X-Canary') == '1':
            canary_count += 1

    proportion = (canary_count / N) * 100
    assert abs(proportion - 10) <= 20, f"Observed canary proportion {proportion}% outside tolerance"


if __name__ == '__main__':
    pytest.main(['-q', __file__])
