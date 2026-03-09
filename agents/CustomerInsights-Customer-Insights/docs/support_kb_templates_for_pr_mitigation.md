Support KB Templates — PR Regression Mitigation

Purpose
Provide two ready-to-publish Support knowledge base (KB) articles to quickly inform customers and reduce incoming support volume for regressions introduced by the PR (pagination + 429/DRY_RUN_LIMIT).

References
- Customer insights summary: output/reports/customer_insights_docs_pr.md
- Follow-up notes: output/docs/docs_pr_followup.md

KB 1: 429 / DRY_RUN_LIMIT — "Rate limit (429) when running dry-run operations"

Title
Rate limit error (429) when using dry-run / DRY_RUN_LIMIT — Mitigation and guidance

Summary
Customers may see HTTP 429 (Too Many Requests) errors tied to recent changes that enforce DRY_RUN_LIMIT on certain endpoints. This KB explains why it happens, how to mitigate it immediately, and what to expect from product.

Symptoms
- Requests intermittently return HTTP 429 with error message referencing DRY_RUN_LIMIT.
- Errors appear during bulk or automated dry-run operations (e.g., SDK dry-run calls, CI jobs).

Cause
A code change introduced stricter enforcement of a dry-run rate limit. Some clients execute many dry-run calls in a short period which now exceed the limit.

Immediate user guidance (for Support to publish verbatim)
1. Reduce call frequency: Add a backoff or throttle so dry-run calls are not sent faster than 1 request per X seconds (adjust per customer scale). Example: exponential backoff starting at 500ms.
2. Batch operations where possible: Combine separate dry-run calls into a single operation when the API supports batching.
3. Retry with jitter: If you receive 429, retry after a short delay with jitter up to N attempts.
4. Contact Support: If throttling prevents essential workflows, contact Support and include:
   - Customer org ID and environment
   - Example request timestamps and headers
   - Any SDK versions, CI config or scripts involved

Suggested Support message template to customers
"We’re seeing 429 errors tied to a newly-enforced dry-run rate limit. As a workaround, please reduce the frequency of dry-run calls and add retries with exponential backoff. If you depend on high-frequency dry-runs for critical workflows, please reply with your org ID and examples and we’ll escalate to Engineering for temporary mitigation options."

SDK / Frontend guidance (short)
- Implement automatic 429 handling with exponential backoff + jitter.
- Respect Retry-After header when present.
- Upgrade SDKs when a new release is published with built-in handling.

Publish checklist for Support (must be completed before marking KB published)
- [ ] KB title and summary written
- [ ] Example mitigation steps included
- [ ] Links to engineering notes added (output/reports/customer_insights_docs_pr.md)
- [ ] Add KB to Support portal under "Service disruptions & limits"
- [ ] Add link to public status page incident if applicable
- [ ] Notify customers who reported the issue with personalized guidance

Tags / Severity
- Tags: 429, rate-limit, DRY_RUN_LIMIT, mitigation, KB
- Severity: P0 (customer-impacting)

KB 2: Pagination Migration — "Behavior change in pagination response"

Title
Pagination behavior changed after recent release — How to migrate and avoid missing items

Summary
A pagination change introduced a different cursor/offset behavior causing some customers to observe missing or duplicated items when iterating pages. This KB explains the behavioral change, migration steps, and temporary workarounds.

Symptoms
- Missing results when iterating pages through large result sets.
- Unexpected duplicates across pages in some queries.
- SDKs that relied on the previous cursor semantics may break.

Cause
A PR altered pagination semantics (cursor encoding and/or inclusive/exclusive bounds). Clients that depended on the old semantics now need to adapt or use a compatibility mode.

Immediate user guidance (for Support to publish verbatim)
1. Verify SDK version: Customers using our official SDK should upgrade to the patched SDK (link will be added when SDK release is available).
2. Update pagination loop to use last_item_id cursor (example pseudocode provided below).
3. For short-term mitigation, narrow page size to reduce overlap risk and re-query ranges when deduping is feasible.
4. Share request examples with Support so Engineering can validate reproduction steps.

Suggested Support message template to customers
"We identified a pagination behavior change that can cause missing or duplicate items when iterating large result sets. Please upgrade your SDK when the patch is released or apply the temporary client-side changes below. If you provide example requests and SDK versions we’ll assist directly."

Developer-facing migration snippet (pseudocode)
1. Use the returned cursor token for next_page (do not compute offsets client-side).
2. When deduping, filter by unique item id in client logic.
3. Example loop:
   - fetch page (cursor optional)
   - process items
   - set cursor = response.next_cursor
   - repeat until cursor is null

Publish checklist for Support
- [ ] KB title and summary written
- [ ] Migration steps + pseudocode included
- [ ] Link to SDK patch release (add later)
- [ ] Add KB to Support portal under "Developer docs / API changes"
- [ ] Add link to status page and cross-link with 429 KB if related

Tags / Severity
- Tags: pagination, migration, breaking-change, KB
- Severity: P0

Operational notes for Support editors
- Keep language non-technical at top; include technical migration details in a collapsible section.
- Add a clear date and version when the change shipped.
- Add contact line: "If this change breaks critical automation, please escalate to support@example.com with your org ID."

Quick publish timelines
- Draft + publish (Support can publish as-is): 30–60 minutes
- Add SDK links / engineering addenda once SDK patch is released: update KB and note update timestamp

End of templates
