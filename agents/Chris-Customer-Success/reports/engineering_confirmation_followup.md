Summary: Follow-up for engineering confirmation on 4 blocking items for the widgets docs PR.

Situation
- Docs team created a short engineering confirmation request outlining 4 blocking questions needed before merging the docs PR.

Complication
- Docs PR cannot merge until canonical behaviors are confirmed for:
  1) widget.size semantics
  2) metadata schema shape and required fields
  3) status vs soft-delete behavior and lifecycle
  4) WIDGETS_CACHE_TTL canonical default and eviction guarantees

Resolution / Action requested (what I created)
- I collected the 4 questions and proposed temporary answers below so we have a single place to confirm.
- File created: output/reports/engineering_confirmation_followup.md (this file)

Questions + suggested temporary answers (please confirm or override)
1) widget.size
   - Suggested temp: size is an integer representing pixel length on the long edge; allowed values: {0, 32, 64, 128, 256}; 0 means 'auto' (responsive).
   - Acceptance: Backend returns consistent numeric value in all endpoints and includes unit (px) in schema example.

2) metadata schema
   - Suggested temp: metadata is a free-form object with optional fields: title (string), description (string), tags (string[]). All other keys allowed but non-guaranteed.
   - Acceptance: Schema example in docs shows optional fields; consumers should treat metadata as opaque beyond documented fields.

3) status vs soft-delete
   - Suggested temp: status = {active, archived, deleted}; soft-delete implemented by setting status=deleted and retaining resource for 30 days before hard delete.
   - Acceptance: API responses include status field; soft-deleted resources return 410 on fetch after 30 days; list endpoints exclude status=deleted unless ?include_deleted=true.

4) WIDGETS_CACHE_TTL
   - Suggested temp: default TTL = 300s (5 minutes); cache is best-effort (no strong consistency guarantees); services must accept eventual consistency.
   - Acceptance: Docs state default TTL and that cache is eventual; include config name WIDGETS_CACHE_TTL and environment example.

Next steps (specific asks)
- Alex: Please coordinate with Marcus (backend) to confirm the canonical behaviors above OR instruct me to proceed with drafting the docs PR using these temporary answers and tag Marcus/Alex for final sign-off.
- If confirmed, please reply in this thread with explicit confirmation per item. If not confirmed, give corrections inline.

Why this matters
- Docs merge is blocked. Having either engineering confirmations or an agreed set of temporary answers will unblock the docs PR and keep release timelines intact.

Contact
- Created by: Chris (Customer Success Engineer)
- Timestamp: (see task in handoff)

