# QA Test Plan: Rate Limit, Retry, Idempotency, and Canary

Owner: Dana (QA)
Created by: Lisa (ML/AI Engineer)
Purpose: Provide actionable test cases, run instructions, and required test hooks for validating the engineering decisions recorded by Marcus in output/reports/docs_values_confirmation_marcus_response.md

Summary of goals
- Validate per-API-key rate limiting (60 req/min, burst 10) and 429 + Retry-After header behavior.
- Validate retry logic: exponential backoff (start 500ms), max 3 attempts total, only for 502/503/504 and only for idempotent methods or when client supplies Idempotency-Key. Include jitter.
- Validate soft-canary (log-only) vs hard enforcement behavior and the transition.
- Provide test harness skeleton and environment requirements for running automated tests in CI and test/staging environments.

Test environment prerequisites (action items for backend/infra - see "Needed from Backend/Infra")
- A staging/test endpoint base URL (BASE_URL) with the same middleware as prod.
- Test API keys with rate-limit buckets resettable per test (or a way to use distinct API keys per test).
- A "test control" mechanism on the server to simulate transient errors and to disable/enable soft/hard enforcement. Suggested interfaces:
  - Header X-Test-Force-Status: value can be 200, 502, 503, 504 to force the upstream response for the request.
  - Header X-Test-Reset-RateLimit: when set, server resets the token-bucket for the provided API key.
  - Header X-Soft-Canary: when present, server runs in soft-canary (log-only) mode for that request.
- Telemetry hooks: request logs must show rate-limit events and retry events; expose an API or logs to fetch them for assertions.

Test data & configuration
- Create three test API keys: KEY_A, KEY_B, KEY_C. Use unique keys to isolate token-buckets.
- Test clients: use a test client that can set Idempotency-Key header.
- Timing configuration: tests that assert backoff/jitter will allow ±20% tolerance on timing assertions.

Test cases
1) Rate-limit enforcement (per-API-key)
- Purpose: Verify 60 req/min with burst 10 and 429 + Retry-After header.
- Steps:
  a) Ensure token-bucket reset for KEY_A (via X-Test-Reset-RateLimit or new key).
  b) Send 70 requests in a tight loop (concurrency allowed). Expect ~10 429 responses once burst consumed and sustained rate exceeded.
  c) Assert responses that are 429 include Retry-After header with a positive integer.
  d) After waiting Retry-After seconds, next request should succeed (200).
- Acceptance: 429 responses observed when expected; Retry-After header present and honored.

2) Burst behavior
- Purpose: Verify burst=10 is allowed initially.
- Steps:
  a) Reset bucket for KEY_B.
  b) Send 10 requests simultaneously; assert all succeed (200).
  c) Send 1 additional request immediately; expect either 429 or a decrement in sustained capacity depending on timing—document observed outcome.
- Acceptance: First 10 concurrent requests succeed.

3) Retry behavior for transient errors
- Purpose: Ensure client retry semantics meet spec (only 502/503/504, idempotent methods or Idempotency-Key, exponential backoff starting 500ms, max 3 attempts, with jitter).
- Steps:
  a) Use a test endpoint that returns 502 for the first 2 attempts, then 200 on the 3rd when header X-Test-Force-Status is used.
  b) For GET (idempotent), send request and verify client retries up to success and total attempts ≤3.
  c) For POST without Idempotency-Key, server should not have client-side retries: only the initial attempt is made; verify no retries.
  d) For POST with Idempotency-Key, verify retries occur like idempotent methods.
  e) Measure inter-attempt timings to assert exponential backoff: expected delays ≈ 500ms, 1000ms (+/- jitter allowance) between retries.
- Acceptance: Retries happen only under allowed conditions; max attempts 3; timing roughly matches exponential backoff with jitter.

4) Jitter semantics
- Purpose: Ensure jitter is included so retries are not deterministic.
- Steps:
  a) Repeat the transient error test multiple times and assert that measured delays vary and are within expected jitter bounds (±30% of expected backoff).
- Acceptance: Timing variance observed.

5) Soft-enforcement mode (log-only) vs hard enforcement
- Purpose: Verify that when soft-canary is enabled, rate-limit events are logged but do not return 429; on transition to hard enforcement, 429 responses begin.
- Steps:
  a) Enable soft-canary for KEY_C (via X-Soft-Canary header or backend flag).
  b) Send traffic exceeding limits; assert that responses return 200 but logs contain rate-limit events.
  c) Disable soft-canary and enable hard enforcement; repeat traffic and assert 429 responses appear.
- Acceptance: Soft-canary yields no 429 but logs rate-limit decisions; hard enforcement yields 429.

6) Idempotency-Key flow for POST
- Purpose: Verify POST with Idempotency-Key will be retried safely and deduplicated in server.
- Steps:
  a) Send POST with Idempotency-Key and force transient 502; client should retry and final server state must reflect a single logical operation.
  b) Verify server returns same result details for retries (idempotent behavior).
- Acceptance: Server-side idempotency ensured and client retries until success or max attempts reached.

Automation and CI
- Test suite location: output/tests/test_rate_limit_and_retry.py (skeleton provided)
- Required env vars for running tests:
  - BASE_URL
  - API_KEY_A, API_KEY_B, API_KEY_C
  - TEST_CONTROL_TOKEN (if needed to call admin endpoints)
- Run with: pytest -q --maxfail=1
- Tests that depend on precise timing should be marked flaky and optionally skipped in fast CI; run in integration pipeline against staging environment.

Reporting & logs
- On failures, capture request/response pairs and server logs for the test period.
- Store artifacts in CI job artifacts for triage.

Needed from Backend/Infra (action items for #ai-backend / Marcus)
- Provide staging base URL and 3 test API keys.
- Implement/enable test control headers: X-Test-Force-Status, X-Test-Reset-RateLimit, X-Soft-Canary or equivalent admin API.
- Provide access to request logs or an API to query telemetry related to rate-limit and retries.
- Confirm whether test traffic will be considered in SLO metrics or isolated from production monitoring.
- Coordinate on scheduling the 2-week canary rollout window and create an RFC for telemetry/acceptance gating.

Notes & risks
- Tests rely on the server having test-control hooks. Without them, timing-dependent tests will be brittle and may falsely fail.
- Running burst tests against production could disrupt real users. Use isolated staging/test environments.

Appendix: Quick checklist for QA run
- [ ] Get BASE_URL and test API keys from backend.
- [ ] Confirm test control headers or admin API exist.
- [ ] Ensure token-buckets can be reset between tests.
- [ ] Run tests in staging CI job with artifacts enabled.

