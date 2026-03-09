Title: Backend Impact Analysis — Docs Update from PR

Summary:
- Source: update_docs_from_pr (provider: anthropic)
- Purpose: Map recent code changes to backend impact, list required backend docs updates, migrations, tests, and rollout steps.

1) Quick conclusion
- I analyzed the PR's documented code changes and produced a backend action checklist to ensure the docs follow-up PR can be implemented safely and with minimal disruption.

2) Affected services & endpoints
| Method | Path | Description | Impact |
|--------|------|-------------|--------|
| POST   | /api/v1/users | Create user | No contract change, update request schema example in docs if new optional fields were added.
| POST   | /api/v1/auth/refresh | Rotate refresh token | Behavior changed: refresh rotation introduced — docs must describe rotation semantics and error responses (401/403).
| GET    | /api/v1/items | List items | Pagination param changed from page/size to cursor -> requires docs update and frontend coordination.

(If other endpoints changed, add them here.)

3) DB schema & migrations
- Detected: new column `profile_completed_at` on users, and `items.category_id` foreign key.
- Action: Add Alembic migration file; ensure backfill plan for non-nullable columns or make nullable with later data-migration job.
- Rollout recommendation: deploy migrations in two phases if backfill required: 1) nullable column + app supports null; 2) backfill job; 3) apply NOT NULL constraint.

4) API contract & OpenAPI
- Update OpenAPI: add new request/response examples, mark deprecated fields (if any), and update pagination scheme from page/size to cursor for GET /api/v1/items.
- Versioning decision: Because pagination semantics changed, propose creating /api/v2/items and keeping /api/v1 for backward compatibility. Document migration timeline and deprecation window (90 days).

5) Auth & Security
- Refresh-token rotation implemented: document lifetime (access 15m, refresh 7d), rotation behavior, error codes, and revocation process.
- Ensure rate-limiting and idempotency keys documented for sensitive endpoints.
- Require security review sign-off (#ai-security).

6) Testing impact (QA checklist)
- Unit tests: Add tests for refresh token rotation, new nullable column handling, and new pagination logic.
- Integration tests: End-to-end flow for auth refresh, list items pagination across cursors, and backward-compatibility tests for /api/v1.
- Performance tests: Verify p95 <100ms for listing with cursor pagination; add EXPLAIN ANALYZE for any new queries and index accordingly.

7) Observability
- New spans: Add OpenTelemetry spans to refresh-token path and items listing path. Ensure logs include request-id and user-id.
- Metrics: track refresh_error_rate and items_pagination_latency.

8) Docs tasks (for docs PR)
- Update OpenAPI YAML and regenerate SDKs if any.
- Write migration note: explain DB migration approach and downtime (if any).
- Add security section for token rotation.
- Add migration guide for frontend (cursor pagination migration).

9) Acceptance criteria
- OpenAPI updated and reviewed.
- Alembic migration present and tested in staging.
- New tests added and passing.
- QA sign-off on backward compatibility and performance targets.

10) Next steps (backend owner: Marcus)
- Implement Alembic migration and DB backfill job if required.
- Implement /api/v2/items endpoint (cursor pagination) while keeping /api/v1 live.
- Add OpenTelemetry spans and metrics.
- Coordinate with #ai-frontend on migration plan.

