Title: Engineering confirmation needed — docs sync (DocsSync Agent)

Purpose
- Summarize the four engineering questions blocking the docs PR and provide suggested temporary answers so engineering can confirm quickly.
- Reference: output/docs/api_examples_update.md and output/docs/docs_pr_changes_summary.md (Emma).

Background
- Emma prepared proposed request/response examples and a docs-change summary. Before we merge the docs PR we need engineering confirmation on four implementation details that affect API examples, validation, and ops runbook.

Questions for engineering (one per bullet). See output/docs/api_examples_update.md for context/examples.

1) widget.size type
- Question: What is the canonical type and value set for widget.size? (string enum like "small|medium|large" OR integer codes OR free-form string)
- Consequence: Determines example payloads, input validation, and potential migration if changing.
- Suggested (temporary) docs text: "widget.size: string enum. Allowed values: 'small', 'medium', 'large'." If backend actually uses ints, DocsSync will map int->label in examples but we need canonical type.

2) metadata schema
- Question: Is 'metadata' a free-form JSON blob (no enforced schema) or a typed object with required/optional keys? Are there size limits or validated keys? Should unknown keys be rejected (400) or allowed?
- Consequence: Affects example requests, validation guidance, and runbook notes about payload size/validation errors.
- Suggested (temporary) docs text: "metadata: free-form JSON object. Recommended keys: 'displayName' (string), 'tags' (array of strings). Server accepts arbitrary keys; unknown keys are ignored, not rejected. Max serialized size: 64KB." (Please confirm/adjust.)

3) status enum & soft-delete behavior
- Question: What are the allowed status values? Does soft-delete set status to 'deleted' (persist record) or is deletion hard? Do list endpoints exclude deleted items by default? Is there a restore endpoint?
- Consequence: Affects example responses, tutorials (delete vs restore), and runbook for data retention.
- Suggested (temporary) docs text: "status: enum ['ACTIVE','DELETED']. DELETE performs a soft-delete and sets status='DELETED'. List endpoints exclude deleted items by default; a query param include_deleted=true will return them. Deleted items can be restored via POST /widgets/{id}/restore." (Please confirm/adjust.)

4) WIDGETS_CACHE_TTL env var
- Question: What is the canonical env var name, unit (seconds/minutes), default value, and whether it is per-process or shared across instances? Any recommended production values or burst behaviour to watch for?
- Consequence: Affects runbook_ops.md, deployment/release notes, and example .env used in docs.
- Suggested (temporary) docs text: "WIDGETS_CACHE_TTL (integer, seconds). Default: 300 (5 minutes). Per-process in-memory cache. For high-update workloads set to 60 or disable caching by setting to 0. Monitor cache_hit_ratio and event lag metrics when tuning." (Please confirm/adjust.)

Acceptance criteria for engineering confirmation
- For each of the four questions: an explicit canonical answer (e.g., type + allowed values + default), any migration notes if the current implementation differs from docs, and any runbook steps (e.g., how to clear cache on deploy).
- If the implementation is undecided or changing soon, signal whether docs should be postponed, include a migration warning, or document the current behavior with a clear "subject to change" flag.

Next steps for Chris (requested action)
- Confirm the four answers above with Marcus (backend) and Alex (PO). Either:
  a) Reply with the confirmed canonical answers, or
  b) Ask DocsSync to draft the docs PR with the suggested temporary answers and tag Marcus/Alex for review.

Impact and rollback note
- If a docs merge documents a different type/behavior than the implementation, clients may send invalid requests or mis-handle deleted items. If we later change docs, add an explicit migration note and contact support channels. For WIDGETS_CACHE_TTL, mismatched units/defaults can cause perf regressions.

Files referenced
- output/docs/api_examples_update.md (proposed examples + explicit engineering questions)
- output/docs/docs_pr_changes_summary.md (what will change, acceptance criteria, migration notes)

DocsSync contact
- DocsSync (me) will update output/docs/api_reference.md and output/docs/runbook_ops.md and create the docs PR after engineering confirmation.
