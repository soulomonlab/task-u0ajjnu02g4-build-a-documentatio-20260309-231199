# KB: Pagination Migration Regression (Published)

Summary
- Issue: Pagination behavior changed after the migration, causing missing results for some queries and unexpected duplicates.
- Impact: P0 regression affecting list endpoints used by PR mitigation workflows.

Published: 2026-03-09T15:40:00Z
Status: Published
Tags: P0, regression, pagination, pr-mitigation

Customer-facing summary
- We discovered a pagination regression introduced during the recent migration. Our team has implemented a rollback on affected endpoints and is validating data consistency. If you notice missing or duplicate results, please provide the query and timeframe.

Steps for affected customers
1. Re-run the query or workflow after 10 minutes.
2. If results still appear missing or duplicated, collect the query parameters and timeframe and open a support ticket referencing this KB: https://support.company.com/kb/pagination-migration

Developer notes / remediation guidance (abbreviated)
- Root cause: Off-by-one changes in cursor handling after migration, and inconsistent sort keys.
- Short-term mitigation: Rollback migration for affected endpoints and enable consistency checks.
- Long-term fix: Apply cursor normalization and add end-to-end pagination tests (see INT-PAG-001).

Customer message template (support agent)
- "We found a pagination regression after a recent migration. We’ve rolled back the change for affected endpoints and are validating results. Please retry in 10 minutes and share query details if you still have issues."

Related artifacts
- Template used: output/docs/support_kb_templates_for_pr_mitigation.md
- Follow-up notes: output/reports/customer_insights_docs_pr.md

If you are a developer needing full diagnostic logs, contact the on-call with query parameters and tag 'PAGINATION_MIGRATION'.
