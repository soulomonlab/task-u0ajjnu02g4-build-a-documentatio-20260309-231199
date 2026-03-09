Title: Pagination behavior changes — What customers need to know

Summary
- Pagination semantics for several customer-facing APIs were updated: cursor tokens are now opaque and shorter-lived; page_size defaults changed from 100 to 50 for certain endpoints.
- Some endpoints may now return fewer items per page and require clients to rely on cursor tokens for iteration.

Who is impacted
- Clients that parse or construct cursor tokens (assumed format) instead of treating them as opaque strings.
- Integrations that rely on stable page sizes for batch processing.

Customer-facing symptom
- Unexpected fewer results per request; previously working pagination clients may break if they attempted to parse cursor tokens.
- Edge case: clients depending on cursor token stability across data mutations may see duplicate or missing items if they cache cursors.

Root cause
- Tokens changed to an opaque, signed format for security and to support cursor invalidation on significant data changes.
- Default page_size lowered to reduce load spikes and improve latency for hot endpoints.

Recommended migration steps for customers
1. Treat cursor tokens as opaque; do not parse or generate tokens client-side.
2. Always use the returned `next_cursor` value to fetch subsequent pages; do not assume numeric offsets.
3. Update batch logic to handle variable page sizes and implement deduplication when merging pages.
4. If your integration requires stable page sizes, request a custom quota or endpoint variant from Support.

Support response template
- Explain the change succinctly and confirm whether the customer parsed cursor tokens or relied on fixed page_size.
- Provide migration steps and offer assistance updating examples in SDKs.
- If a customer's flow is broken, escalate to SDK owners and product engineering with the customer’s example request/response.

Operational impact & rollback note
- Rollback would require reverting token format and increasing default page_size — non-trivial; preferred path is customer migration and SDK updates.
- Ops can provide temporary higher page_size on a per-account basis if needed while migration occurs.

Acceptance criteria for publishing
- KB article published and cross-linked from API reference and migration guide.
- SDK/Frontend owners (Kevin) notified to update client libraries and examples.
- QA to validate pagination behavior with customer-provided examples.

Related files /PRs
- Reference: output/docs/docs_pr_followup.md (mapping and priority)

Last updated: by DocsSync agent