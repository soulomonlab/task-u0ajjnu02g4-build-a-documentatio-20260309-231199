QA Test Plan: Rate-limiting & Retry Behavior

Scope
- Validate engineering decisions recorded in output/reports/docs_values_confirmation_marcus_response.md
- Focus areas: per-API-key rate-limiting (token-bucket + burst), Retry behavior with backoff/jitter/idempotency, soft vs hard enforcement, canary rollout coordination.

Acceptance Criteria
1. Rate-limit enforcement
   - 60 req/min per API key enforced in hard mode; burst of 10 allowed
   - When limit exceeded, server returns 429 with Retry-After header (seconds)
   - Token-bucket semantics: sustained rate limited, short bursts allowed
2. Retry
   - Retries only for 502/503/504 responses
   - Retries limited to idempotent methods (GET, PUT, DELETE) or POST with Idempotency-Key
   - Exponential backoff starting at ~500ms, max 3 attempts total, with jitter
3. Soft vs Hard
   - Soft mode logs events and doesn't return 429
   - Transition to hard mode enforces 429
4. SDK compatibility
   - SDK versions >=1.2.0 <2.0.0 should be accepted by the API (validation is lenient)

Test Cases (high-level)
- TC1: Per-API-key sustained rate test (k6) — ensure limit applied per key
- TC2: Burst behavior (k6) — send burst >10 and verify 429 for excess requests and Retry-After header
- TC3: Retry header verification (pytest) — call test endpoints that simulate 502/503/504 and assert X-Retry-Attempts
- TC4: POST Idempotency-Key path (pytest) — verify POST with Idempotency-Key is retried
- TC5: Soft mode validation (pytest) — set soft mode, exceed limit, ensure no 429 but logs exist
- TC6: Canary readiness checklist — ensure telemetry hooks, monitoring dashboards, and rollback playbook exist

Test Data & Env
- Staging environment with test-only control endpoints: /test/retry/* and /test/rate_limit_mode
- API keys: key-test-1, key-test-2
- Access to logs/metrics (Prometheus/Grafana) for canary verification

Schedule
- Week 0: Implement tests in repo and run locally against staging
- Week 1: Run k6 load tests and pytest suite; iterate with backend to fix issues
- Week 2: Coordinate soft canary rollout (50% traffic) with Marcus; monitor for 2 weeks

Reporting
- Capture k6 output and pytest reports in CI artifacts
- Create a post-test report: output/reports/qa_rate_limit_retry_report.md

