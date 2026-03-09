Engineering response — Published KBs (Task #175)

Overview
- Owner: Marcus (Backend Engineer)
- Task: Confirm engineering impact, ETA, rollback plan, user-visible changes, and recommend KB messaging edits so Product can sign off.

ETA
- Initial confirmation (this document): immediate (today).
- If only KB metadata/messaging changes are required: implementation & verification estimate = 1 business day.
- If a backend fix (rare) is required: estimate = 2-3 business days (investigation + QA).

Owner Contact
- Marcus (Backend) — Slack: @Marcus (channel #ai-backend), Email: marcus@ourcompany.internal
- Escalation: Taylor (Tech Lead) in #ai-tech-lead if any architectural blockers.

Summary of findings
- From initial review of the KBs in product_review_kb_published.md, there are no required code changes to the public API or DB schema. The KBs are content/metadata updates in the CMS.
- Engineering involvement is limited to: (1) updating/search indexing metadata if Product requests changes to metadata fields; (2) publishing-related rollout/rollback steps; (3) monitoring user-facing behaviour after publish.

Rollback plan (engineer-executable)
Pre-requisites: article IDs and timestamps for the published KB versions; admin credentials for CMS; access to Redis and search index.

1) Identify affected article IDs
   - Query CMS or DB: SELECT id, current_version, status FROM kb_articles WHERE slug IN (...);
2) Revert to previous version
   - If CMS supports versioning: use admin UI to restore previous version (preferred).
   - If manual SQL required (last-resort):
     a) BEGIN TRANSACTION;
     b) UPDATE kb_articles SET content = previous_content, metadata = previous_metadata, version = previous_version WHERE id = <id>;
     c) INSERT INTO audit_log(...)
     d) COMMIT;
3) Set visibility/status
   - Set status = 'draft' (if removing from public) or restore previous published state.
4) Clear caches
   - Redis: DEL kb:article:<id> and any related listing caches.
5) Reindex search (if applicable)
   - Trigger search reindex for the article(s). Depending on our indexer, this could be an async job (may take up to 30–60 minutes to propagate).
6) Post-rollback verification
   - Smoke test: GET /api/v1/kb/:slug and confirm content matches expected previous version.
   - Monitor logs and 5-min metrics for errors.

Estimated rollback time
- Quick revert via CMS UI: 5–30 minutes.
- Manual DB + reindex + verification: 30–120 minutes.

User-visible behavior changes
- Users will see updated KB content and metadata immediately after publish (subject to CDN/edge cache TTLs).
- Potential minor search latency or stale results for up to TTL/reindex window (expected max 60 minutes).
- No API contract changes expected (no client-breaking changes).

Monitoring and acceptance criteria
- After publish, we will monitor the following for 4 hours:
  - KB GET API success rate (should remain > 99.9%)
  - Error logs related to KB read endpoints
  - Search index consistency for the affected slugs
- Acceptance: Product signs off when content/messages are approved and smoke tests pass.

Recommended KB messaging edits (suggested copy)
- Headline (short): "Updated: [KB Title] — [Date]"
- Summary (1–2 lines): "We updated this article to clarify [topic] and include steps for [action]. No action is required from customers."
- What changed (bullet list):
  - Clarified step 2 for [feature]
  - Added note about [edge-case]
  - Updated screenshots to match UI vX
- If rollback possible: "If you experience any unexpected behavior after this update, contact Support and we can revert to the previous version within 2 hours."
- Contact line: "Need help? Open a support ticket here: <support_link>"

Suggested KB metadata edits
- Add a short changelog field: "engineer_note: reverted_possible"
- Add publish timestamp in ISO8601 and the publisher contact (support@company)

Next steps for Product
1) Review and approve the messaging template above or provide edits.
2) Confirm whether you want us to: (A) proceed with metadata-only changes (we execute), or (B) require an engineering PR for backend changes (we'll estimate and schedule).

Notes / Risks
- If Product requests changes to metadata that require search schema changes, reindexing may increase latency and add 30–60 minutes to rollout time.
- If any unexpected client-side issues are reported, follow the rollback plan and escalate to #ai-tech-lead.

Output
- Engineering confirmation document created by Marcus as requested.

