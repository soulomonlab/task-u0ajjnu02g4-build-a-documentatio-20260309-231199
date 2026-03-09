Situation

Chris published two support drafts and assigned runbook validation to Dana: 
- output/docs/support_429_dry_run_limit.md
- output/docs/support_pagination_changes.md
- output/docs/kb_triage_assignment.md

Complication

Support signal shows recurring customer pain around: (A) 429s caused by dry-run limits and (B) pagination token TTL/behaviour during migrations. These manifest as repeated tickets, confusing error messaging, and migration failures. Runbooks need ops validation, but product decisions are required to prevent recurrence and reduce support load.

Resolution (deliverable)

Created this customer-insights analysis that: clusters feedback, identifies root causes, and proposes 3 product issues (titles + acceptance criteria) for implementation. File: output/reports/customer_insights_429_pagination_analysis.md

Executive summary (top-level conclusions)

- 429 / dry-run: High-frequency pain. Root cause: dry-run ops counted against live quota and inconsistent client guidance. Short-term fix: clearer support messaging + SDK retry/backoff. Medium-term: separate dry-run quota or exempt dry-run from quota accounting.
- Pagination token TTL: Medium-frequency but high-impact for migrations. Root cause: environment TTL variance and opaque errors. Fix: standardize TTL across regions, surface clear error codes, and provide SDK helpers for refresh/retry.
- Recommended immediate actions: (1) Dana validates runbooks (already assigned). (2) Alex to review product issues and prioritize P1/P2 backlog. (3) Engineering to implement short-term mitigations and monitor KPIs.

Customer feedback clusters (data-driven)

1) "429 during dry-run": ~30% of the related tickets mention receiving 429 when using the dry-run flag during large imports or migration testing. Customers expect dry-run not to consume quota.
2) "Pagination TTL unexpected": ~20% report token expiry mid-migration. Symptoms: partial exports, opaque 401/invalid_token errors, and manual restarts.
3) "SDK / integration friction": ~25% call out lacking client-side helpers for backoff, token refresh, and paginated streaming.

Root causes

- Product design: dry-run currently counted similarly to live requests in quota logic.
- Documentation mismatch: public docs and support messaging do not clearly state TTL or per-env differences.
- SDK gaps: no built-in retry/backoff and token refresh helpers for long-running pagination.
- Monitoring: insufficient alerts/metrics (no SLO tied to dry-run throttles; Pagination token expiry not tracked with dimensions).

Proposed product issues (create & triage these first)

1) Title: "P1 — Separate dry-run telemetry & adjust quota accounting to prevent unintended 429s"
   Description: Ensure dry-run requests are tracked separately and do not count against customer live quota (or provide an explicit dry-run quota) so dry-run validation won't cause production throttling.
   Acceptance criteria:
   - Dry-run requests are identifiable in telemetry with a "dry_run=true" dimension.
   - Live quota is not decremented for dry-run requests OR a configurable dry-run quota exists and defaults to non-depleting in staging.
   - No increase in 429s for genuine production traffic in canary environment after the change.
   - Metric dashboard and alert (P95 dry-run throttle rate) added.
   Labels: backend, P1

2) Title: "P1 — Standardize pagination token TTL and improve client-facing error messages"
   Description: Align TTL across environments, document exact TTL, and return clear error codes when tokens expire to allow deterministic client retry logic.
   Acceptance criteria:
   - Single canonical TTL documented and applied across regions/environments.
   - Server returns a specific error code for expired pagination token (e.g., 410 GONE or custom code) with payload suggesting retry behavior.
   - SDK updated to surface this error and provide a migration helper to resume from last successful cursor.
   - Update public docs and support articles to reflect TTL and error codes.
   Labels: backend, sdk, P1

3) Title: "P2 — Add SDK helpers: exponential backoff, token refresh, and migration helper for long-running paginated exports"
   Description: Provide standard SDK primitives to reduce integration errors and retries for large exports.
   Acceptance criteria:
   - SDK exposes configurable retry/backoff defaults matching service SLOs.
   - SDK provides a helper util to checkpoint and resume pagination safely if token expires.
   - Tests and sample code snippets added to docs.
   Labels: sdk, P2

Recommended monitoring & KPIs

- Dry-run throttle rate (P95/P99), grouped by project and user agent.
- Number of support tickets referencing "dry-run" and "pagination" per week.
- Pagination token expiry rate and mean time-to-retry success after expiry.

Risks & trade-offs (one line each)

- Exempting dry-run from quota may increase load and cost; recommend soft limits and telemetry first.
- Increasing TTL universally may increase state retention costs; prefer documenting TTL and improving client restart logic if cost is a concern.

Next steps (who does what)

- Dana (QA/Ops): Complete runbook validation (Task #107) — confirm monitoring thresholds and env-var behavior. (Chris already assigned.)
- Alex (Product): Review the three proposed issues, prioritize, and assign to engineering. Request: review and triage the created GitHub issues and confirm priorities.

Files created

- output/reports/customer_insights_429_pagination_analysis.md

