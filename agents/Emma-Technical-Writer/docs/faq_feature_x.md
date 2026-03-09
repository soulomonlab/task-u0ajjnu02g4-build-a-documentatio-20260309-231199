FAQ: Feature X

Q: What is Feature X?
A: Feature X is a capability that can be enabled per-tenant to provide [short description].

Q: How do I enable Feature X?
A: Use the API endpoint POST /v1/feature-x/activate with tenant_id and resource_id. See quickstart for example.

Q: I get a 422_FEATURE_INACTIVE error. What does it mean?
A: This means a business precondition prevents activation (e.g., missing subscription tier, unpaid invoices). Steps:
  1) Verify tenant meets prerequisites (billing, subscription tier).
  2) Check activation prerequisites via GET /v1/feature-x/status.
  3) Contact support if prerequisites are met but activation still fails.

Q: Will enabling Feature X require downtime?
A: No downtime is expected. A DB migration adds a nullable column and backfills false; deploy during low-traffic window is recommended.

Q: How can I test activation in staging?
A: Use the staging API base URL and run the POST then GET flow. Ensure test tenant has required subscription.

Q: Who do I contact for issues?
A: Support: Chris (#ai-support). Backend: Marcus (#ai-backend). DevOps: Noah (#ai-devops).

