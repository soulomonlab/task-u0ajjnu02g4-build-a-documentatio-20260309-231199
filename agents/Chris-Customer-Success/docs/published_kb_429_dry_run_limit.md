# KB: 429 / DRY_RUN_LIMIT Regression (Published)

Summary
- Issue: Customers hit 429 errors with DRY_RUN_LIMIT when running large PR mitigation jobs.
- Impact: P0 regression affecting automated PR mitigation for high-volume customers.

Published: 2026-03-09T15:30:00Z
Status: Published
Tags: P0, regression, rate-limit, pr-mitigation

Customer-facing summary
- We identified a regression causing 429 (DRY_RUN_LIMIT) errors for large PR mitigation jobs. Our engineering team has deployed a mitigation that reduces the frequency of the error for most customers. If you continue to see 429s, please reply to this thread with the job ID and timeframe.

Steps for affected customers
1. Retry the failing PR mitigation job after 5 minutes.
2. If failure persists, capture the job ID and earliest failure timestamp and open a support ticket with that info.
3. In the ticket, mention this KB: https://support.company.com/kb/429-dry-run-limit

Developer notes / remediation guidance (abbreviated)
- Root cause: Regression in rate-limiting logic when DRY_RUN mode batches exceed configured thresholds.
- Short-term mitigation: Backoff and retry with randomized jitter; temporary increase to internal DRY_RUN_LIMIT for affected tenants applied.
- Long-term fix: See internal ticket INT-PR-429 for code patch to pagination in DRY_RUN handler.

Customer message template (support agent)
- "We’ve identified a regression that caused 429 errors for large PR mitigation jobs. Our team has applied a mitigation and is rolling a permanent fix. Please retry after 5 minutes and share the job ID if the issue persists."

Related artifacts
- Template used: output/docs/support_kb_templates_for_pr_mitigation.md
- Follow-up notes: output/reports/customer_insights_docs_pr.md

If you are a developer needing full diagnostic logs, contact the on-call with the job ID and tag 'DRY_RUN_LIMIT'.
