# Release Notes — CustomerInsights Follow-up

Release: CustomerInsights follow-up
Version: vX.Y.Z
Date: 2026-03-09

Highlights

- New query endpoint improvements: faster summary responses and improved recommendations
- Added 'format' parameter to control summary/timeseries/raw output
- Updated error codes and rate-limiting behavior

Impact

- API clients that parse the previous response structure may need to adjust to the added 'recommendations' field
- No breaking changes to required fields

Migration

- Update clients to handle optional 'recommendations' array
- Respect rate-limiting headers (Retry-After)

Docs

- API reference: output/docs/api_reference_customer_insights.md
- Code samples: output/code/customer_insights_example.py, output/code/customer_insights_example.ts
- Ops runbook: output/docs/ops_runbook_customer_insights.md
