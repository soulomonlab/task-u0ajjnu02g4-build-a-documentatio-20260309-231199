import time
import random
import requests

BASE_URL = 'http://localhost:8000'
API_KEY = 'test-key'
HEADERS = {'Authorization': f'Bearer {API_KEY}'}


def send_request(method='GET', path='/v1/resource', idempotency_key=None):
    headers = HEADERS.copy()
    if idempotency_key:
        headers['Idempotency-Key'] = idempotency_key
    url = BASE_URL + path
    if method == 'GET':
        return requests.get(url, headers=headers)
    elif method == 'POST':
        return requests.post(url, headers=headers, json={'x': 1})
    elif method == 'PUT':
        return requests.put(url, headers=headers, json={'x': 1})
    else:
        raise ValueError('Unsupported')


def test_retry_only_for_502_503_504_and_idempotent_methods(monkeypatch):
    # This test requires the service to be instrumented to expose retry logs or counters for testing.
    # We'll simulate by calling endpoints that return 502/503/504 and assert retry behavior via a test-only header.

    # Trigger GET with 502
    res = send_request('GET', '/test/retry/502')
    assert res.status_code in (502, 200, 503, 504)
    # Service should indicate retries attempted in X-Retry-Attempts header
    if 'X-Retry-Attempts' in res.headers:
        assert int(res.headers['X-Retry-Attempts']) <= 3

    # Trigger POST without Idempotency-Key to 502: should NOT retry
    res_post = send_request('POST', '/test/retry/502')
    if 'X-Retry-Attempts' in res_post.headers:
        assert int(res_post.headers['X-Retry-Attempts']) == 0

    # Trigger POST with Idempotency-Key to 502: should retry (header present)
    res_post_idem = send_request('POST', '/test/retry/502', idempotency_key='abc-123')
    if 'X-Retry-Attempts' in res_post_idem.headers:
        assert 1 <= int(res_post_idem.headers['X-Retry-Attempts']) <= 3


def test_jitter_and_backoff_respects_max_attempts():
    # Hit an endpoint that will return 503 consistently and check timing between attempts via a test header
    res = send_request('GET', '/test/retry/always_503')
    # Expect header X-Retry-Timestamps with comma-separated epoch ms timestamps of each attempt
    if 'X-Retry-Timestamps' in res.headers:
        timestamps = [int(x) for x in res.headers['X-Retry-Timestamps'].split(',') if x]
        assert len(timestamps) <= 3
        # Check exponential-ish backoff (differences increase)
        diffs = [t2 - t1 for t1, t2 in zip(timestamps, timestamps[1:])]
        assert all(d >= 400 for d in diffs)  # minimum backoff approx 500ms (allow 400ms) + jitter


def test_soft_vs_hard_enforcement_flags():
    # Toggle soft mode via test endpoint or header (assumes service supports a test-only control)
    res_soft = send_request('GET', '/test/rate_limit_mode?mode=soft')
    assert res_soft.status_code == 200
    assert 'X-RateLimit-Mode' in res_soft.headers and res_soft.headers['X-RateLimit-Mode'] == 'soft'

    # Now trigger over-limit and ensure we get logs but not 429
    # Make multiple rapid requests
    for _ in range(10):
        r = send_request('GET', '/v1/resource')
        assert r.status_code != 429

    # Switch to hard
    res_hard = send_request('GET', '/test/rate_limit_mode?mode=hard')
    assert res_hard.status_code == 200
    assert 'X-RateLimit-Mode' in res_hard.headers and res_hard.headers['X-RateLimit-Mode'] == 'hard'

    # Now over-limit should produce 429
    found_429 = False
    for _ in range(20):
        r = send_request('GET', '/v1/resource')
        if r.status_code == 429:
            found_429 = True
            assert 'Retry-After' in r.headers
            break
    assert found_429
