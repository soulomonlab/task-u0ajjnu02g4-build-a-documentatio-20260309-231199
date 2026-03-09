Title: KB Engineering Response — Marcus

Reference: Task #183
Source: output/specs/kb_engineering_request_marcus.md

Situation
- Product supplied an engineering request for KB metadata/messaging and needs engineering ETA, owner, rollback plan, user-visible behaviour changes, messaging edits, and data impact (telemetry, DB migration, backfills, monitoring).

ETA & Owner
- ETA: Initial engineering deliverables (migration scripts, telemetry spec, rollback plan, QA test plan) ready in 48 hours. Full rollout (including safe backfill and verification in prod) targeted within 72 hours after approvals.
- Owner: Marcus (Backend Engineer). Contact: Slack: @marcus (channel #ai-backend) | Email: marcus@example.com

Rollback plan (summary)
1) Feature flag first: All runtime changes gated behind a boolean feature flag (kb_metadata_v2_enabled). Default: off.
2) DB migrations: All schema changes designed to be additive-only where possible. If a destructive migration is required, it will be split into two steps: (A) deploy additive columns/tables and write code to read/write both old & new; (B) backfill data; (C) remove old schema after monitoring window.
3) Code rollback: If runtime issue detected, toggle kb_metadata_v2_enabled -> off for all services (instant rollback of user-visible behavior). If a migration caused corruption, run compensating migration using the preserved audit backup.
4) Backout steps for migration failure:
   - Stop backfill job(s) via orchestration (Celery/Argo).
   - Restore affected rows from pre-migration snapshot (we will take targeted backups of impacted tables before running irreversible migrations).
   - Re-enable previous code path (feature flag off) and open incident.

User-visible behavior changes
- No change until feature flag is enabled.
- When enabled for a cohort/tenant, KB entries will show updated metadata fields (new tags and a short_title). Search and relevance ranking unchanged in v1; front-end will receive additional fields in API responses.
- Minor change: some KB items will display a short_title override where present; otherwise fall back to full title.

Recommended KB messaging edits (copy suggestions for Product)
- Headline for users: "Improved KB metadata for faster discovery"
- Short blurb: "We're rolling out richer metadata (short titles and tags) to help you find relevant articles faster. No action required."
- In-app tooltip: "Try the new short titles — they highlight the core idea of each article."

Data checklist — answers
1) Telemetry
   - Events to add:
     • kb.metadata.v2.enabled (boolean toggle per user/tenant)
     • kb.article.view.metadata_source (enum: old|v2|mixed)
     • kb.metadata.backfill.progress (percent)
     • kb.metadata.backfill.error (error_code)
   - Metrics to track:
     • p95 response time for /api/v1/kb endpoints (existing)
     • proportion of articles served with v2 metadata (gauge)
     • backfill throughput (rows/sec)
   - Tracing: add OpenTelemetry spans around the backfill job and the API branch that populates v2 fields.

2) DB migrations
   - Schema changes (additive):
     • kb_articles table: add columns short_title (varchar(255), nullable), tags jsonb (nullable), metadata_version smallint default 1
     • Add index: GIN index on tags jsonb for tag searches; btree index on metadata_version
   - Migration strategy: Alembic scripts. All additions first. Any large index builds performed concurrently (CONCURRENTLY) to avoid locks.
   - Downtime: none expected. Use online/non-blocking DDL.

3) Backfills
   - Backfill purpose: populate short_title, tags, metadata_version for existing rows.
   - Volume estimate: ~5M rows (estimate pending product confirmation). Plan for batched backfill with controlled concurrency to keep DB p95 < 100ms.
   - Approach:
     • Run backfill as a partitioned job (by created_at or id ranges) via Celery with idempotent workers.
     • Resume checkpoints every N rows (configurable). Persist progress in backfill_jobs table.
     • Run first on staging (full run) then prod during low-traffic window. Use parallelism tuned to target sub-1s avg query latency.
   - Safe-run estimate (prod): 4–12 hours depending on final row count and parallelism. We'll provide a concrete estimate after Product confirms row count.

4) Monitoring & Alerts
   - Dashboards:
     • KB API: p50/p95/p99 latency, error rate, % requests returning v2 metadata
     • Backfill job: progress, throughput, failures per minute
   - Alerts:
     • API error rate > 0.5% (P1)
     • p95 latency increase > 2x baseline (P1)
     • Backfill job failure rate > 1% for 10 minutes (P2)

Acceptance criteria (what Product will sign-off on)
- Migration scripts reviewed and applied on staging without errors.
- Backfill completes on staging and sample of results validated by Product (random 100 rows).
- Telemetry events emitted correctly and visible in analytics dashboards.
- Feature flag toggles behavior without rollback required for canary cohort.

Risks & mitigations
- Risk: Backfill load causing elevated DB latency — Mitigation: run in controlled batches, add read-replicas, throttle.
- Risk: Incomplete metadata extraction — Mitigation: run verification queries and surface rows with metadata_version != expected.

Files delivered
- This response: output/specs/kb_engineering_response_marcus.md

Questions / blocking info needed from Product
- Confirm exact KB row count (estimate in request doc says ~5M — please confirm)
- Confirm preferred rollout window for prod backfill (UTC window)

----
Notes: I will implement Alembic migration scripts and a Celery backfill job once Product confirms row count and approves rollout window.
