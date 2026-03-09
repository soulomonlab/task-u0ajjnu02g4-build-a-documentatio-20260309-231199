# Backend Mitigation Plan: 429 (DRY_RUN_LIMIT) & Pagination Regression

Status: Draft
Owner: Marcus (Backend)
Date: 2026-03-09

## 1) Summary
Provide immediate backend mitigations to stop customer-facing regressions caused by: (A) uncontrolled 429s tied to a DRY_RUN_LIMIT, and (B) recent pagination behavior changes that broke clients. Deliver a fast, reversible patch plus tests and a short rollout plan.

## 2) Goals
- Stop customer-facing 429 spikes and provide deterministic Retry-After semantics.
- Restore backward-compatible pagination defaults and add feature-flagged opt-in for stricter behavior.
- Be low-risk and reversible; instrument heavily for observability.

## 3) Background / References
- Epic spec: output/specs/epic_docs_pr_mitigation.md
- Customer insights: output/reports/customer_insights_docs_pr.md
- Docs followup: output/docs/docs_pr_followup.md

## 4) Proposed Backend Mitigation (short-term, P0)
A. Rate-limit / DRY_RUN mitigation
- Deploy a RateLimitMiddleware that recognizes a DRY_RUN context (header: `X-Dry-Run: true` or query param `?dry_run=1`) and applies a separate, low-capacity counter (DRY_RUN_LIMIT).
- When the DRY_RUN_LIMIT is exceeded, return 429 with:
  - JSON body: {"error": "DRY_RUN_LIMIT_EXCEEDED", "message": "Your dry-run requests exceeded the temporary limit.", "kb": "<support_kb_url>"}
  - Headers: `Retry-After` (seconds), `X-RateLimit-Limit`, `X-RateLimit-Remaining`.
- Use Redis-based counters (preferred) with an in-process fallback (warn in logs). Config via env: RATE_LIMIT_REDIS_URL, RATE_LIMIT_WINDOW=60, RATE_LIMIT_DEFAULT=300, DRY_RUN_LIMIT=10.
- Add OpenTelemetry spans and metrics (counter + histograms).

B. Pagination mitigation
- Restore previous default page size (e.g., default=20) and max page size cap (e.g., max=100). Add a compatibility header `X-Pagination-Mode: legacy|strict` so clients can opt in.
- Implement a feature flag `FEATURE_PAGINATION_STRICT` (env) to gate stricter behavior. Default OFF until support/SDK updated.
- Add warning header `X-Pagination-Deprecated: true` when client requests strict mode during the migration window.

## 5) API & Implementation Notes
- Endpoints: middleware-based rate limiting — no endpoint changes required.
- Responses standardized: application/json error shape {"error": "CODE", "message": "...", "kb": "..."}
- Idempotency & retry: ensure 429 responses include `Retry-After` and a human-friendly KB link.

## 6) Rollout Plan
1. Implement and unit-test middleware + pagination guard in backend. (This PR)
2. Deploy behind feature flag and enable metrics/tracing. Monitor p95/p99 and 429 rate for 1 hour.
3. If stable, release feature flag ON to all traffic. If issues, rollback (feature flag toggle or revert PR).

## 7) Acceptance Criteria
- On simulated high dry-run traffic, 429 is returned with Retry-After and KB URL.
- Pagination endpoints default to legacy page size and cap; strict mode only when env flag ON.
- Observability: traces for rate limit hits, metric exported `backend.rate_limit.hits`.
- Performance: p95 < 100ms for routes after middleware (Redis cold-start excluded).

## 8) QA / Testing
- Unit tests: token-bucket logic, Redis fallback, headers on 429.
- Integration: simulate concurrent clients hitting DRY_RUN_LIMIT and verify metrics+429.
- Regression: pagination tests for legacy default, strict mode, caps, and headers.

## 9) Support / Docs notes for KB authors
- Include exact error code: DRY_RUN_LIMIT_EXCEEDED and sample cURL showing Retry-After header.
- For pagination KB, include migration steps: explicit page & size params, SDK changes, and examples.
- Reference this spec and: output/reports/customer_insights_docs_pr.md

## 10) Risks
- In-process fallback can under-count in multi-replica deployment. Mark as temporary and prefer Redis.
- KB URL placeholder must be replaced by Support when links are published.

