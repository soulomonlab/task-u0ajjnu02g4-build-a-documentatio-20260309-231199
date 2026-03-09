# QA Test Plan: Docs Values Confirmation (Rate-Limit, Retry, Idempotency, Canary)

Summary
- Purpose: Validate engineering decisions recorded in output/reports/docs_values_confirmation_marcus_response.md
- Scope: Rate-limit enforcement (per-API-key, burst, 429 + Retry-After), retry behavior (only for 502/503/504, idempotent methods or when Idempotency-Key present, exponential backoff with jitter, max 3 attempts), soft-enforcement mode (log-only) and transition to hard enforcement.
- Preconditions: Test environment with controllable test hooks/admin endpoints OR production canary environment with telemetry access. Environment variables used by tests: TEST_BASE_URL, TEST_API_KEY, TEST_API_KEY_2 (for per-key separation), ADMIN_TOKEN (optional for toggling soft/hard mode and forcing responses).

Acceptance criteria
- Rate-limit: When sending a rapid burst of requests exceeding (60 req/min + burst 10), the server returns 429 for excess requests and includes a Retry-After header with an integer (seconds). Per-API-key limits are independent.
- Retry: Retries are applicable only for 502/503/504 responses and for idempotent methods (GET, PUT, DELETE, HEAD, OPTIONS) or POST when Idempotency-Key header is present. Client-side retry attempts must not exceed 3 total attempts. Backoff starts at ~500ms and increases exponentially; jitter is applied.
- Soft enforcement: When soft mode active, server does not return 429 but emits a warning log/metric accessible via admin telemetry endpoint. When switched to hard mode, 429s are enforced.

Test approach
- Automation-first: All test cases will be automated pytest tests (output/tests/...). Tests will be parameterized and will skip with clear messages if required env vars or admin hooks are missing.
- Emulate realistic timing: where possible, tests will wait small durations to observe Retry-After header semantics.
- Isolation: Use separate API keys to validate per-key scoping.

Files created by QA
- output/tests/test_rate_limit.py
- output/tests/test_retry_behavior.py
- output/tests/test_soft_enforcement.py
- output/reports/qa_test_plan_docs_values.md (this file)

Next steps
- Marcus (#ai-backend): Please enable the test hooks in the staging/canary environment or provide ADMIN_TOKEN and endpoints documented below so automated tests can toggle enforcement mode and force response codes for retry tests.
  - Admin endpoints (recommended):
    - POST /__qa/reset_rate_limit?api_key=...  (reset token bucket for api_key)
    - POST /__qa/force_next_response  {"path":"/test/retry","status":502}
    - POST /__qa/set_enforcement_mode {"mode":"soft"|"hard"}
    - GET /__qa/telemetry?metric=rate_limit_warnings
- Once hooks are enabled, run: pytest output/tests -q

QA owner: Dana
