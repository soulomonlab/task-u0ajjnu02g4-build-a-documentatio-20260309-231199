# Reviewer Tasks (to assign)

Task: Review and confirm API examples
- Assigned to: Marcus (Backend)
- Priority: P1
- Description: Please replace the placeholder API examples in output/docs/docs_followup_pr_actions.md with canonical request/response examples. Ensure authentication, headers, error cases, and sample HTTP status codes are present. If any API behavior changed from implementation, note it in the PR comment.
- Acceptance criteria:
  - All endpoints in the follow-up doc have real request/response examples.
  - Any differences between doc and implementation are documented.
  - Tests or schema pointers added where applicable.

Task: Review and confirm runbook steps
- Assigned to: Noah (DevOps)
- Priority: P1
- Description: Validate and replace runbook placeholders in output/docs/docs_followup_pr_actions.md, ensuring the steps match actual deployment and rollback procedures, monitoring checks, and run commands for the production environment. Add any missing commands or infra references.
- Acceptance criteria:
  - Runbook steps are executable and environment-specific notes are included.
  - Any missing infra steps or permissions are documented.

Suggested comment to paste into PR when opened:
"@Marcus @Noah Please see the follow-up actions doc linked here (output/docs/docs_followup_pr_actions.md). Marcus: confirm API examples. Noah: confirm runbook steps. Chris has created reviewer tasks and will track completion. Please aim to complete within 48 hours."
