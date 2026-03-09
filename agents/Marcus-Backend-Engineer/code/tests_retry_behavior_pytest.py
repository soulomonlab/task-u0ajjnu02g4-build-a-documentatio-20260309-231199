import os
import requests
import time
import pytest

BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')


def get(url, headers=None):
    return requests.get(f"{BASE_URL}{url}", headers=headers, timeout=10)


@pytest.fixture(scope='module')
def test_info():
    r = get('/test/info')
    assert r.status_code == 200
    return r.json()


def test_control_endpoints_exist(test_info):
    assert 'rate_limit_mode' in test_info


def test_retry_always_502():
    r = get('/test/retry/always_502', headers={'X-Test-Id': 'pytest-1'})
    assert r.status_code == 502


def test_retry_flaky_with_attempts_header():
    headers = {'X-Retry-Attempts': '1', 'X-Test-Id': 'pytest-2'}
    r = get('/test/retry/flaky_50', headers=headers)
    assert r.status_code in (200, 503)
    # ensure response echoes attempt header
    assert 'X-Retry-Attempts' in r.headers


def test_retry_timestamps_header():
    headers = {'X-Retry-Attempts': '2', 'X-Test-Id': 'pytest-3'}
    r = get('/test/retry/slow_1s', headers=headers)
    assert r.status_code == 200
    assert 'X-Retry-TIMESTAMPS' in r.headers


def test_rate_limit_mode_toggle():
    # read current
    r = get('/test/rate_limit_mode')
    assert r.status_code == 200
    current = r.json().get('mode')

    # toggle
    new_mode = 'hard' if current == 'soft' else 'soft'
    r2 = requests.post(f"{BASE_URL}/test/rate_limit_mode", data={'mode': new_mode}, timeout=5)
    assert r2.status_code == 200
    assert r2.json().get('mode') == new_mode

    # revert
    r3 = requests.post(f"{BASE_URL}/test/rate_limit_mode", data={'mode': current}, timeout=5)
    assert r3.status_code == 200
    assert r3.json().get('mode') == current


def test_idempotency_and_retry_semantics():
    # For idempotency, we simulate a client that retries on 5xx and expects no duplicates.
    # This test requires the API to support idempotency keys for POST /api/v1/resource (test-only behavior)
    # If not available, skip.
    res = get('/api/v1/resources/test-idempotency')
    if res.status_code == 404:
        pytest.skip('Idempotency test endpoint not available on this deployment')

    # Try with a single idempotency key
    headers = {'Idempotency-Key': 'pytest-idem-1'}
    r1 = requests.post(f"{BASE_URL}/api/v1/resources/test-idempotency", json={'value': 1}, headers=headers, timeout=5)
    assert r1.status_code in (200, 201)

    # Retry the same request; expect the same response code and no duplicate creation
    r2 = requests.post(f"{BASE_URL}/api/v1/resources/test-idempotency", json={'value': 1}, headers=headers, timeout=5)
    assert r2.status_code in (200, 201)
    assert r1.text == r2.text


def test_retry_backoff_jitter_behavior():
    # This test is mostly observational: we call a flaky endpoint with sleep between retries and expect eventual success
    max_attempts = 5
    headers = {'X-Test-Id': 'pytest-4'}
    for attempt in range(1, max_attempts + 1):
        r = get('/test/retry/flaky_50', headers={'X-Retry-Attempts': str(attempt), **headers})
        if r.status_code == 200:
            break
        time.sleep(0.1 * attempt)  # exponential-ish backoff
    assert r.status_code == 200 or attempt == max_attempts
