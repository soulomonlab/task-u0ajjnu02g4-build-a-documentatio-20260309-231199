Title: QA Test Plan — Rate Limit & Retry Behavior

Purpose
- Validate engineering decisions (rate limit, retry scope, idempotency, soft-canary) and confirm acceptance criteria before canary rollout.

Scope
- Automated + manual tests targeting API gateway layer and client behavior.
- Environments: QA (test), Staging (canary), Production (post-canary).

Acceptance criteria (must pass)
1) Rate limit enforcement: 60 req/min per API key, burst up to 10 tokens. When limit exceeded return 429 with Retry-After header (seconds). Redis token-bucket enforcement active in hard mode.
2) Retry semantics: Clients retry only for 502/503/504. Retries only for idempotent methods (GET, HEAD, PUT, DELETE, OPTIONS) OR any method when client provides Idempotency-Key header. Exponential backoff starting 500ms, up to 3 total attempts (initial + 2 retries), with jitter. Max attempts enforced.
3) Soft-enforcement mode: In soft (log-only) mode no 429s are returned; events are logged and metrics emitted. Transition to hard enforcement flips behavior to reject requests.
4) Canary observability: Metrics and alerts in place for 429 rate, 5xx rate, latency p50/p95, Redis errors, token-bucket drops.

Test data & setup
- API keys: create three test API keys: KEY_A, KEY_B, KEY_C.
- Test clients: use an automated load tool (k6/newman/pytest+requests), and a mock server to return controlled HTTP status codes for retry tests.
- Time sync: ensure test runner and target servers have synchronized clocks (for Retry-After validation).
- Redis: use a test Redis instance that mimics production config (same TTLs, memory limits).

Test cases (detailed)
1) Rate-limit: single-key steady rate
  - Goal: confirm 60 req/min average allowed.
  - Steps: send 60 requests spread evenly over 60s using KEY_A. Expect all 200. Send 61st request -> expect 429 + Retry-After header.
  - Verify Redis token-bucket counters decrement and refill at expected rate.

2) Rate-limit burst behavior
  - Goal: confirm burst up to 10 tokens is allowed.
  - Steps: idle to fill bucket, then send 10 immediate requests -> expect 200 for all. Send 11th immediate request -> expect 429.
  - Verify refill after burst follows token-bucket algorithm.

3) Rate-limit multikey isolation
  - Goal: per-API-key enforcement.
  - Steps: KEY_A sends 60 req/min; KEY_B simultaneously sends 60 req/min. Both should succeed independently.

4) 429 + Retry-After header correctness
  - Goal: header format and semantics.
  - Steps: trigger 429; verify presence of Retry-After (integer seconds) and value equals time until token available (±1s tolerance).

5) Retry behavior — idempotent methods
  - Goal: retries only for 502/503/504 and idempotent methods.
  - Steps: mock server returns 502 on first N attempts then 200. For GET: ensure client retries with backoff (500ms base) and succeeds before max attempts. For PUT/DELETE same.
  - Verify number of attempts <= 3.

6) Retry behavior — non-idempotent POST without Idempotency-Key
  - Goal: no automatic retries.
  - Steps: mock server returns 502; verify client does NOT retry (single attempt). Validate no duplicate side-effects on server.

7) Retry behavior — POST with Idempotency-Key
  - Goal: allow retries when Idempotency-Key provided.
  - Steps: POST with Idempotency-Key header; mock returns 502 then 200; client should retry and operation should be idempotent on server side.
  - Verify server deduplication logic receives same idempotency key and only performs action once.

8) Jitter / backoff semantics
  - Goal: confirm exponential backoff with jitter applied.
  - Steps: instrument client to log timestamps of attempts. For a forced transient error sequence, measure intervals: expect base 500ms, then ~1000ms (±jitter), attempts stop after 3.
  - Acceptance: measured delays follow doubling pattern within jitter range.

9) Max attempts enforcement
  - Goal: ensure attempts do not exceed 3.
  - Steps: force repeated 502 responses; verify client stops after 3 attempts and surfaces final error.

10) Soft-enforcement (log-only)
  - Goal: in soft mode, no 429s are returned; events recorded.
  - Steps: enable soft mode; generate traffic above thresholds. Verify responses remain 200/normal but logs/metrics show token-bucket drops and intended counts. Verify no functional rejection.

11) Transition to hard enforcement
  - Goal: switching to hard enforcement activates 429 behavior without downtime.
  - Steps: flip to hard mode in staging; run the same over-limit traffic and verify immediate 429s + Retry-After. Verify no significant latency spikes or Redis errors.

Automation recommendations
- Implement end-to-end tests in pytest (tests/test_rate_limit.py, tests/test_retry.py) using a controllable mock backend and test Redis instance.
- Use k6 (or similar) for high-volume burst and steady-rate simulations.
- For timing-sensitive tests (backoff), use deterministic test harness or mock sleep to validate algorithm instead of wall-clock waits where possible.

Logging & telemetry checks (during tests)
- Verify metrics emitted: rate_limit.events, rate_limit.drops, retry.attempts, retry.success_after_retry, idempotency.duplicates.
- Validate presence of logs with tags: api_key, enforcement_mode, decision_source (soft/hard).

Test run matrix
- Run all tests in QA. For canary (staging), run a subset focusing on burst, soft->hard transition, and observability.
- Only run full automation in production after canary acceptance criteria met.

Risks & mitigation
- Clock skew affecting Retry-After validation: mitigate by ensuring NTP and using tolerances.
- Flaky timing tests: mock time where possible.
- Redis performance variance: use scaled test Redis and include Redis health checks.

Deliverables from QA
- Automated test scripts (pytest/k6), test run results, screenshots/log extracts proving acceptance criteria.
- A short report mapping failing/passing cases to canary readiness.
