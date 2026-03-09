Title: 429 / DRY_RUN_LIMIT — What customers will see and how to resolve

Summary
- New error code introduced: 429 with subcode DRY_RUN_LIMIT. Returned when a client exceeds the allowed number of `dry_run` operations in a rolling window.
- Affects customer-facing API endpoints that accept the `dry_run` flag. Behavior change is intentional to protect system stability.

Who is impacted
- Customers using `dry_run=true` at high frequency (batch jobs, CI pipelines, automated testing).
- SDKs that automatically retry `dry_run` calls without backoff.

Customer-facing symptom
- API responses with HTTP 429 and a JSON body {"error": "DRY_RUN_LIMIT", "retry_after_seconds": <n>}.
- Client sees immediate failure on `dry_run` requests; production (non-dry-run) calls unaffected.

Root cause
- Rate-limiting of `dry_run` operations to prevent system abuse and ensure capacity for real (non-dry-run) traffic.

Immediate mitigation for customers
1. Implement exponential backoff and respect `retry_after_seconds` header/value.
2. Reduce frequency of `dry_run` calls; accumulate inputs into larger batches where possible.
3. For test environments, use local mocks or a dedicated test quota if available — contact support to request quota adjustments.

Recommended support response template
- Brief explanation: This error means your application exceeded the allowed number of dry-run requests. Production calls are not blocked.
- Actionable steps: Reduce dry-run frequency, add backoff, optionally request a quota increase with use-case details.
- Escalation: If customer needs immediate allowance for scheduled test runs, escalate to #ai-ops and include the customer’s account ID, expected traffic pattern, and justification.

Operational impact & rollback note
- No rollback required for code: this is an operational limit enforced server-side.
- If unintended customer disruption occurs, temporary exceptions can be issued per-account by Ops while engineering reviews quota thresholds.

Acceptance criteria for publishing
- Support article published to KB and linked from API reference and PR description.
- Response template and troubleshooting steps validated by Support (Chris) and Ops (Noah).
- SDK owners (Kevin) notified to add client-side retry guidance.

Related files / PRs
- Reference: output/docs/docs_pr_followup.md (mapping and priority)

Last updated: by DocsSync agent