# KB: 429 / DRY_RUN_LIMIT — Immediate Guidance

## Summary
This KB explains the 429 (Too Many Requests) behavior introduced by the PR that enforces a DRY_RUN_LIMIT. It provides customer-facing guidance, temporary mitigations, and support troubleshooting steps.

## Who's affected
- All API consumers making high-frequency requests to affected endpoints.
- SDKs and frontend clients that do not implement retry/backoff or misuse the DRY_RUN flag.

## Technical cause
A recent change introduced a DRY_RUN_LIMIT which returns 429 when the dry-run quota is exceeded. Clients that poll or retry aggressively may hit this limit.

## Customer impact
- Intermittent 429 errors for heavy request patterns.
- Failure modes include aborted pagination flows and failed background syncs.

## Recommended immediate actions for customers (workarounds)
1. Implement exponential backoff with jitter on 429 responses.
2. Honor the Retry-After header when present before retrying.
3. Reduce request frequency (batch calls or increase interval between retries).
4. Where available, disable unnecessary DRY_RUN behavior or reduce the number of dry-run calls.
5. Update SDKs to the patched version (when released) that handles 429s gracefully.

## What Support should tell customers
- Acknowledge: "We’ve identified a rate-limiting behavior causing 429s for certain request patterns. Our engineering team is working on mitigations." 
- Provide the workaround steps above.
- Ask for: endpoint(s) hit, request timestamps, client SDK version, reproduction steps and logs.

## Troubleshooting steps for Support
1. Collect request timestamps, endpoints, and full request headers including Retry-After if present.
2. Confirm whether client is using an older SDK or custom retry logic.
3. Suggest immediate customer-side mitigations (backoff, reduce frequency).
4. If issue persists, escalate to engineering with sample request logs and customer impact.

## Publish checklist
- [ ] Add this KB to Support portal under "Incidents & Rate Limits".
- [ ] Link KB from Status page Incident post.
- [ ] Add short summary tweet/announcement draft for status page.

## References
- Customer insights: output/reports/customer_insights_docs_pr.md
- PR follow-up doc: output/docs/docs_pr_followup.md

## Owner / ETA
Chris (Customer Success) — Drafted. Will publish to Support portal after review by Emma. Target: publish within 2 hours.
