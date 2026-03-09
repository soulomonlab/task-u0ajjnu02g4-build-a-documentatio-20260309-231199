Title: Product Impact — Engineering clarifications required for Widgets API docs

Core ask
- Confirm engineering decisions for 4 ambiguous Widgets API items so docs PR can merge with correct examples and runbook updates.

Ambiguities (from output/docs/api_examples_update.md)
1) widget.size type
   - Options: string enum ("small|medium|large") OR numeric (int pixels)
2) metadata schema
   - Options: opaque JSON vs typed object with known fields (owner, created_by, tags)
3) status enum / soft-delete behavior
   - Options: status enum with explicit DELETED value vs boolean `deleted` + soft-delete retention policy
4) WIDGETS_CACHE_TTL env var
   - Details needed: default value, units (seconds/minutes), per-env overrides, and expected eventual consistency windows

User & product impact (MECE)
- Docs correctness & developer experience: wrong type or schema causes integration bugs for SDK users and third-party integrators.
- Migration risk: changing type/schema after launch requires migration guides and breaking-change windows.
- Observability & ops: unclear TTL/soft-delete semantics hinder runbook actions (rollbacks, cache invalidation).
- Security/compliance: metadata typing can surface PII if not constrained; soft-delete retention affects data deletion requests.

Recommended temporary defaults (reversible, low-regret)
- widget.size: adopt string enum (small|medium|large) for v1 — easier for clients; allows future numeric `dimensions` field.
- metadata: document as opaque JSON in examples, but add a recommended typed subset (owner, tags) for search/indexing.
- status/soft-delete: use status enum including "DELETED" with documented retention policy; implement soft-delete semantics server-side.
- WIDGETS_CACHE_TTL: default 300 seconds (5m); units = seconds; allow env override per-deployment; document eventual consistency window = TTL + 2s.

Acceptance criteria for docs PR to merge
- Engineering provides final answers for the 4 questions and confirms no breaking changes planned for next 3 months.
- Examples in output/docs/api_examples_update.md updated with the confirmed values.
- runbook_ops.md includes TTL value, units, and how to force cache invalidation.
- Migration notes for any non-reversible changes.

Next steps / Owner
- Primary: Engineering to confirm specifics (recommended owner: Marcus).
- Product (Alex): prioritize confirmation and decide if the recommended defaults above are acceptable for v1.
- Docs (Emma): update docs PR after confirmation.

Files referenced
- output/docs/api_examples_update.md
- output/docs/docs_pr_changes_summary.md

Why this matters
- Small unresolved tech ambiguities lead to large integration friction and post-release churn. Clear decisions now reduce support load and migration costs.

Created by: Customer Insights Agent
Date: 2026-03-09
