# Support Publish Plan — 429 DRY_RUN_LIMIT & Pagination Migration KBs

Summary
- Owner: Chris (Customer Success Engineer)
- Purpose: Stage, review, and publish two P0 KB articles to the customer-facing portal and ensure cross-team follow-up for API, SDK, and runbook updates.
- Files created:
  - output/docs/kb_429_dry_run_limit.md
  - output/docs/kb_pagination_migration.md

Timeline & ETA
- Chris (me) will stage both KBs into the CMS as drafts within 6 hours (ETA: today +6h).
- Emma (Technical Writer) to review content, apply editorial fixes, and publish to the customer portal within 24 hours after staging (ETA: staging +24h).
- Notify customers and update release notes once published (target: immediately after publish).

Tasks & Owners
1. Stage KB drafts in CMS (Chris) — include metadata (tags: "breaking-change", "migration", "rate-limit"), add links to API docs and support contact. (P0)
2. Editorial review & publish (Emma) — check tone, clarity, compliance, and publish publicly. (P0)
3. Update API reference & add schema examples (API docs owner / Alex to assign) — link from KBs. (P1)
4. Coordinate SDK/frontend updates (Kevin / SDK owners) — ensure code samples and SDKs reflect cursor pagination and 429 handling. (P1)
5. Create Ops/Security runbook for 429 incidents (Ops/Security owners) — link to KB and monitoring playbook. (P0 via Alex coordination)

Acceptance Criteria
- KBs published and accessible from support portal with correct metadata and links.
- API reference contains links to KB and response schema added.
- Notification sent to customers and internal teams (SDKs, Support, Ops).
- QA checklist: verify sample responses render correctly, code blocks copyable, links not broken.

Notes & Dependencies
- Link to customer_insights report and Emma's follow-up: output/reports/customer_insights_docs_pr.md and output/docs/docs_pr_followup.md (Task #92).
- Alex already received a handoff to create the tracked epic (Task #118).

Contact
- Chris: chris@example.com
- Emma: (please confirm preferred contact)
