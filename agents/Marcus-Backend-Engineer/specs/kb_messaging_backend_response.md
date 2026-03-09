# KB Messaging — Backend feasibility, ETA, rollback, and constraints

Summary (direct answers to Maya's questions from design doc output/design/kb_message_ui_spec.md)

1) ETA for Banner + dismiss persistence + KB metadata (version) endpoints

- Phase A (MVP, P0 hotfix): Serve/read-only latest KB message + record dismiss action (no versioning, minimal validation, no feature flag).
  - ETA: 1 business day (8 business hours) for API + DB migration + minimal tests.
- Phase B (Recommended, production-safe): Full versioning, message lifecycle (active/inactive), user-dismiss persistence, RBAC for KB creation, feature flag, automated rollback path, observability and tests.
  - ETA: 3 business days (design, migrations, API, unit + integration tests, tracing).
- Phase C (Optional hardening): A/B rollout support, caching optimization, rate limits, analytics events.
  - ETA: +2 business days.

2) Engineering owner (contact)

- Marcus (Backend Engineer) — #ai-backend. I will own the backend implementation and coordinate with Kevin for the frontend contract and Dana for QA.

3) Rollback feasibility & procedure

- Rollback approach (safe, recommended):
  1. Use feature flag (turn off KB_message feature) — immediate disable (seconds).
  2. Mark KB message records as inactive in DB (set active=false on kb_messages) — immediate (seconds).
  3. If a migration requires schema/column changes, implement migrations to be backwards-compatible (add new columns, backfill), and use feature flag to release; rollback involves toggling flag + deploying previous service image.

- Time estimates & risk:
  - Toggling feature flag / marking message inactive: < 1 minute to execute, negligible risk.
  - Rolling back code deployment to previous release: ~5–15 minutes depending on deployment system (requires DevOps coordination).
  - Rolling back destructive DB migrations: potentially hours and higher risk; avoid destructive migrations. If destructive migration happens, restore from DB backup — hours and potentially data loss for recent dismissals.

- Recommendation: avoid destructive migrations. Implement additive migrations and use soft-delete/versioning so rollback is trivial.

4) Design constraints or recommended changes

- Modal trigger limits: avoid automatic modal spam. Backend supports returning a field `display_rules` that the frontend should evaluate (e.g., show_once_per_session, show_once_per_user, cooldown_seconds).
- Dismiss semantics: backend persists per-user dismissals. Frontend MUST call POST /kb_messages/:id/dismiss with user context and idempotency key to ensure exactly-once semantics.
- Timing: if message must appear immediately for all users, use low TTL caching or bypass cache for the "latest" endpoint.

5) Technical constraints / copy guidance

- Plain text or sanitized Markdown only. No embedded scripts or iframes. Backend will sanitize on write and store a sanitized HTML blob per version.
- Max message size: recommend 4096 bytes (4 KB). If longer content is required, use KB article link rather than full text.
- Allow placeholders (e.g., {{user_first_name}}) but require frontend to escape values. Backend will store template variables metadata so frontend can render safely.

---

Detailed implementation proposal

A. DB schema (additive migration)

- kb_messages
  - id: UUID PK
  - title: varchar(255)
  - content: text (sanitized HTML)
  - version: integer
  - active: boolean (default true)
  - created_by: uuid (user)
  - created_at: timestamptz
  - expires_at: timestamptz NULL
  - display_rules: jsonb (e.g., {"show_once_per_user": true, "cooldown_seconds": 86400})

- kb_message_versions (optional, for immutable history)
  - id: UUID PK
  - kb_message_id: UUID FK
  - version: integer
  - content: text
  - created_at
  - changed_by

- user_kb_dismissals
  - id: UUID PK
  - user_id: UUID
  - kb_message_id: UUID
  - version: integer
  - dismissed_at: timestamptz
  - source: varchar(64) (e.g., web, mobile)
  - UNIQUE(user_id, kb_message_id, version)

Notes: Use indexes on (kb_message_id), (user_id, kb_message_id) and on active=true for fast queries.

B. API contract (v1)

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET    | /api/v1/kb_messages/latest | Returns latest active KB message + display_rules + version | Bearer |
| GET    | /api/v1/kb_messages/:id | Get specific KB message (by id, optional version param) | Bearer |
| POST   | /api/v1/kb_messages/:id/dismiss | Persist user dismissal (idempotent) | Bearer |
| POST   | /api/v1/kb_messages/ack | (optional) Bulk ack when UI renders multiple items | Bearer |

Example: GET /api/v1/kb_messages/latest response
{
  "id": "uuid",
  "title": "KB: Incident posted",
  "content": "<p>We deployed hotfix ...</p>",
  "version": 3,
  "display_rules": {"show_once_per_user": true, "cooldown_seconds": 86400},
  "active": true,
  "expires_at": "2026-03-20T12:00:00Z"
}

Example: POST /api/v1/kb_messages/:id/dismiss body
{
  "idempotency_key": "frontend-uuid-123",
  "source": "web",
  "client_ts": "2026-03-09T09:12:00Z"
}

Response 200 OK
{ "status": "dismissed", "message_id": "uuid", "version": 3 }

Idempotency: require Authorization header + idempotency key for dismiss route. Server will return 200 for repeated dismiss with same user_id + kb_message_id + version.

C. Security & validation

- Authenticate all endpoints (Bearer token). Ensure user_id resolved from token; do NOT accept user_id in payload.
- Sanitize content on write (server-side) and validate length.
- RBAC: only admin/support roles can create/activate messages. Expose POST/PUT endpoints for create/update behind RBAC (not detailed here; will add if needed).

D. Observability

- Add OpenTelemetry spans for GET latest and POST dismiss. Emit metrics: dismiss_count, fetch_latency_ms (p95/p99), error_rate.
- Emit events to analytics pipeline for each dismiss (user_id, message_id, version) for audit.

E. Testing

- Unit tests for migration, schema, API contract.
- Integration tests: dismiss idempotency, concurrent dismiss calls, GET latest with active/inactive messages.

F. Operations & rollout

- Deploy behind feature flag. Create migration as additive. Backfill none required for MVP.
- Smoke test: fetch latest as non-admin user, dismiss, verify persisted record.

G. Edge cases & gotchas

- If frontend caches latest message aggressively (e.g., CDN), newly activated KB may not show — recommend bypass caching for /latest or add cache-busting header when message version increments.
- If message expires and a user dismissed older version, frontend should show newer versions regardless; use version in dismissal uniqueness.

---

Acceptance criteria (what I will deliver when I implement)

- DB migrations added and applied.
- Endpoints implemented with OpenAPI schema and unit tests.
- Dismiss persistence with idempotency and unique constraint.
- Feature flag integration + rollback instructions in deploy runbook.
- Observability (OpenTelemetry spans + metrics). 

---

Files to be produced by backend implementation (planned)

- output/code/backend/routers/kb_messages.py
- output/code/backend/models/kb_message.py
- output/code/backend/migrations/xxxx_create_kb_messages.sql
- output/docs/openapi_kb_messages.yaml
- output/reports/kb_messaging_rollback_runbook.md

If you want, I can start Phase A (MVP) immediately and target completion in 1 business day.

