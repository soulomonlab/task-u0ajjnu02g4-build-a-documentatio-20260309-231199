Title: P0 Incident — Frontend blocked by missing backend API details for Task #113
Owner: Incident Response Agent (Incident)
Severity: P0 (blocks development)
Created: 2026-03-09T00:00:00Z
Related files:
- Security checklist: output/reports/security_api_requirements_task_113.md (Isabella)

Summary (conclusion)
- Frontend work (Kevin) is blocked pending backend API contract details required by Task #113. This is a P0 blocker for the sprint.

Why this matters
- Missing endpoint paths, HTTP methods, canonical response/ error JSON, pagination, auth details, and PII classification will cause spec drift, rework, and security regressions.

Blocking questions (MECE checklist for Marcus to answer)
1) Endpoints: List each endpoint path + HTTP method required for Task #113.
2) Response schema: For each endpoint, provide canonical success JSON (full example) and at least one common error JSON (with HTTP status codes).
3) Error format: Confirm global error envelope (fields: code, message, details?) and HTTP status mapping.
4) Pagination: Strategy (limit/offset or cursor), parameter names, default page size, max page size, and example paginated response.
5) Auth: Confirm auth type (JWT bearer, OAuth, API key). If JWT: signing algorithm, expiry, rotation/refresh strategy, required claims (sub, scope, roles), and how to indicate scopes in responses.
6) Idempotency & verbs: Any non-standard idempotency requirements (e.g., POST idempotency key) and safe retries guidance.
7) PII: Which response fields contain PII and whether they should be redacted or returned only for certain roles.
8) Rate limiting / throttling: Per-user or per-key rate limits, headers used to communicate limits and limits for this set of endpoints.
9) Versioning & stability guarantees: API version (v1), deprecation policy, and whether these endpoint shapes will change before release.
10) Contract examples: Attach OpenAPI/JSON Schema fragments (or canonical JSON) for each endpoint (success + error) so frontend can generate models.

Containment / temporary mitigations
- If Marcus cannot finalize schema immediately, provide an OpenAPI v3 stub (best-effort) or mock server URL that returns canonical examples described above so frontend can continue behind a feature flag.
- Alternatively, agree on a minimal stable subset (read-only endpoints + one write endpoint) that frontend can implement now.

Acceptance criteria for unblock
- Marcus provides answers to the 10 blocking questions, and attaches canonical JSON examples for success and common errors into this incident file or as references.
- Backend confirms auth details and PII fields.
- If OpenAPI/Swagger file available, attach and mark as canonical.

Recommended next step (Immediate)
- Marcus: Answer the checklist in Isabella's security file and paste canonical JSON examples into this incident or attach an OpenAPI fragment.

Rollback / containment option
- If backend changes are needed that risk errors, roll back frontend to use mocks and gate feature via feature flag until contract is stable.

Agent notes
- I am the Incident Response Agent. I will escalate if no response within 2 business hours due to P0 severity.
