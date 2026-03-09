# Support Article: 429 / DRY_RUN_LIMIT

Summary
- Users may see HTTP 429 responses with an error code DRY_RUN_LIMIT when a service-side dry-run quota is exceeded.
- This article explains causes, customer-visible symptoms, short-term mitigations, and suggested next steps for support agents.

When customers see this
- API responses return HTTP 429 with body:
  {
    "error": "DRY_RUN_LIMIT",
    "message": "Dry-run request limit exceeded. Try again later."
  }
- Common surfaces: API client calls using dry-run/testing flags, automated CI test suites that repeatedly call dry-run endpoints.

Cause
- Server-side rate/quota limit applies specifically to requests marked as dry-run. A new quota was introduced in the recent PR to prevent abuse of dry-run endpoints.
- This limit is separate from standard per-user rate limits.

Impact
- Non-destructive test calls may be rejected even when regular requests succeed.
- Customers using heavy automated testing or CI may see intermittent failures in pipelines.

Immediate troubleshooting steps (for Support agents)
1. Confirm the response is 429 with error code DRY_RUN_LIMIT.
2. Ask the customer whether they are using any dry-run/test flag or a sandbox environment.
3. If reproducible, request: timestamps, request IDs (if present), client IP, and sample request payloads.
4. Suggest short-term mitigations:
   - Reduce dry-run call frequency or batch tests to fewer requests per minute.
   - Temporarily run some tests without dry-run flag if safe for the customer.
   - Stagger CI jobs or add exponential backoff/retries with jitter.
5. Escalate to Engineering/Rate-Limits team if the customer claims usage well under expected quotas and can provide logs.

Recommended customer messaging
- Clear, empathetic message explaining this is a protection limit for dry-run endpoints.
- Example: "We're seeing that your requests hit a dry-run quota limit (DRY_RUN_LIMIT). This prevents excessive non-destructive calls. Please reduce dry-run frequency or stagger test runs. If you think this is an error, provide timestamps and sample request IDs and we'll investigate."

Product/Docs actions (from docs PR follow-up)
- Short-term: publish a Support Article (this page) and update KB to include mitigations and messaging templates.
- Medium-term: add the dry-run quota to the public Rate Limits documentation and to the API reference error codes table.
- Long-term: update SDKs to surface a clear exception for DRY_RUN_LIMIT with guidance for automatic retries/backoff.

Acceptance criteria
- Support article published in KB: output/docs/support_429_dry_run_limit.md
- Support team has messaging templates and triage checklist included above.
- Doc owners assigned for API reference and SDK changes (see KB triage file).

Related files
- docs PR follow-up: output/docs/docs_pr_followup.md

