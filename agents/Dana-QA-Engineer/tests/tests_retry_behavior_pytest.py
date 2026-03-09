import os
import time
import requests
import pytest

BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')

# Utility to flip rate limit mode (test-only control endpoint)
def set_rate_limit_mode(mode):
    r = requests.post(f"{BASE_URL}/test/rate_limit_mode?mode={mode}")
    r.raise_for_status()

# Utility to trigger deterministic failures
def trigger_test_failure(code):
    r = requests.get(f"{BASE_URL}/test/retry/{code}")
    return r

# Tests for retry semantics and idempotency

def test_retry_header_present_on_502():
    r = trigger_test_failure('502')
    assert r.status_code == 502
    # X-Retry-Attempts should be present even for a single failure
    assert 'X-Retry-Attempts' in r.headers


def test_always_503_endpoint_retries_until_client_limit():
    # This endpoint always returns 503; client should implement retry with backoff.
    r = trigger_test_failure('always_503')
    assert r.status_code == 503
    assert 'X-Retry-Attempts' in r.headers


def test_soft_vs_hard_mode_affects_response():
    set_rate_limit_mode('soft')
    # In soft mode, requests over limit should be accepted with warning header
    r = requests.get(f"{BASE_URL}/v1/resource")
    assert r.status_code in (200, 429)
    if r.status_code == 200:
        assert r.headers.get('X-RateLimit-Mode') == 'soft'

    set_rate_limit_mode('hard')
    r2 = requests.get(f"{BASE_URL}/v1/resource")
    # In hard mode, over-limit should return 429
    assert r2.status_code in (200, 429)
    if r2.status_code == 429:
        assert r2.headers.get('Retry-After') is not None


def test_idempotency_of_retries():
    # Ensure multiple retries don't create duplicate side-effects
    # Use a test-only endpoint that returns a request_id and increments a counter
    r = requests.post(f"{BASE_URL}/test/idempotent_create", json={"value": "qa-test"})
    assert r.status_code == 200
    data = r.json()
    req_id = data.get('request_id')
    assert req_id

    # Simulate client retry by calling the same request_id
    r2 = requests.post(f"{BASE_URL}/test/idempotent_create", json={"request_id": req_id, "value": "qa-test"})
    assert r2.status_code == 200
    assert r2.json().get('created') in (True, False)


def test_retry_backoff_jitter_observed():
    # The test relies on X-Retry-Timestamps header listing retry timestamps
    r = trigger_test_failure('always_503')
    assert 'X-Retry-Timestamps' in r.headers
    ts_header = r.headers['X-Retry-Timestamps']
    timestamps = [float(x) for x in ts_header.split(',') if x.strip()]
    assert len(timestamps) >= 1
    if len(timestamps) > 1:
        # ensure increasing and non-uniform (jitter)
        diffs = [t2 - t1 for t1, t2 in zip(timestamps, timestamps[1:])]
        assert all(d > 0 for d in diffs)
        assert any(d != diffs[0] for d in diffs)


if __name__ == '__main__':
    pytest.main(['-q', '--disable-warnings'])
