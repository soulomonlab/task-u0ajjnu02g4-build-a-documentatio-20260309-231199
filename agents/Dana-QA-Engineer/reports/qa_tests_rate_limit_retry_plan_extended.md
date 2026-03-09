QA Test Plan — Rate Limit, Retry, Idempotency, and Soft-Canary

Purpose
- Validate backend rate-limiting, retry semantics, idempotency guarantees, jitter/backoff behavior, and soft-canary routing under controlled staging conditions.

Scope
- Endpoints: /v1/test-endpoint (GET), /v1/create-resource (POST) — adjust to real endpoints provided by backend.
- Environments: staging only (require BASE_URL pointing to staging)
- Test-control hooks required from backend/infra to make tests deterministic.

Acceptance Criteria (exit gates)
- No P1 regressions found in automated runs.
- Test coverage: key flows covered by automated tests in output/tests/test_rate_limit_and_retry_extended.py
- Rate limit enforcement: when exceeding configured limit, server returns 429 and includes at least one of: Retry-After, X-RateLimit-Remaining, X-RateLimit-Limit, X-RateLimit-Reset.
- Retry guidance: 429 responses must include Retry-After (seconds) or compliant backoff headers; clients should back off exponentially; server should tolerate well-formed retry attempts (no duplicate side-effects for idempotent requests).
- Idempotency: repeated POST with identical Idempotency-Key creates resource once (same resource id returned or 200 on subsequent calls).
- Soft-canary: header X-Soft-Canary: <bucket-percent> must route a proportionate fraction of traffic to canary; we accept a tolerance of ±20% on small sample sizes.

Environment & Test-Control Requirements (must be provided by backend / infra)
- BASE_URL (staging base URL)
- STAGING_API_KEY (test-only API key with limited scope)
- Test-control headers and endpoints:
  - X-Test-Reset-RateLimit: when set, server resets internal rate-limit counters for the test client (required for deterministic enforcement tests).
  - X-Test-Force-Status: allows forcing a specific status code (e.g., 500, 429) for next N requests to test retries and backoff.
  - X-Soft-Canary: accepts a percentage value (0-100) to route requests to canary path.
- Idempotency support: server must honour Idempotency-Key header for POST resource creation tooling and persist idempotency state for at least test duration.

Test Cases (high-level)
1) Burst test (enforcement)
   - Reset counters via X-Test-Reset-RateLimit.
   - Send N rapid requests (configurable; default N=50) within T seconds.
   - Expect: after threshold, server returns 429s for excess; rate-limit headers present.
   - Metrics recorded: first 429 index, total 429 count, % of 2xx vs 429.

2) Steady-state exceeding
   - Send RPS slightly above limit for M seconds.
   - Expect: sustained 429s; headers show remaining=0 after threshold.

3) Retry behavior
   - Use X-Test-Force-Status to force 429 or 500 responses for first K requests.
   - Client should interpret Retry-After header (if present) and retry respecting exponential backoff + jitter.
   - Validate server responds with success after backoff when limits reset.

4) Jitter & Backoff
   - Verify that retry intervals include jitter; compute variance over multiple retries.
   - Acceptance: observed retry intervals should not be constant (no fixed sleep) — greater than 0 variance.

5) Idempotency
   - POST to create resource with Idempotency-Key set to constant value.
   - Send same POST twice; expect second to return same resource id and not create duplicate resources.

6) Soft-canary routing
   - Use X-Soft-Canary to set a percentage P (e.g., 10%).
   - Send batch of N requests (N >= 100 recommended); count proportion routed to canary (server returns header X-Canary=1 for canary responses).
   - Acceptance: observed proportion within ±20% of P.

7) Error propagation & observability
   - Verify 5xx/429 responses include correlation id header (X-Request-ID) and that logs (provided by backend) include matching ids for investigation.

Automation & Implementation Notes
- Tests implemented in pytest (output/tests/test_rate_limit_and_retry_extended.py).
- Tests skip automatically when BASE_URL or STAGING_API_KEY not provided.
- Tests are designed to be run in staging CI with network access and a rate-limit reset endpoint.
- Tests will produce machine-readable JSON artifact (planned) for ingestion into CI test reports.

Action Items (for Marcus / #ai-backend)
1) Provide staging BASE_URL and STAGING_API_KEY (test-only) to QA.
2) Enable test-control headers: X-Test-Reset-RateLimit, X-Test-Force-Status, X-Soft-Canary for the staging environment and document their behavior.
3) Ensure endpoints support Idempotency-Key for resource creation and persist idempotency records for at least 5 minutes.
4) Provide sample endpoint paths for: /v1/test-endpoint and /v1/create-resource or confirm actual paths.
5) Provide any rate-limit configuration values (limits per minute, per-second bursts) so tests can assert thresholds precisely.
6) Grant temporary access or service account if necessary and confirm retention policy for idempotency state.

Reporting
- QA will run tests in staging CI and produce a results artifact: output/reports/qa_rate_limit_retry_results_<timestamp>.md with pass/fail, logs, and coverage.

Notes & Risks
- Without test-control hooks, tests are non-deterministic and may produce flaky results.
- Soft-canary sampling requires sufficiently large N; small sample sizes increase variance.

Contact
- QA owner: Dana (Senior QA)

