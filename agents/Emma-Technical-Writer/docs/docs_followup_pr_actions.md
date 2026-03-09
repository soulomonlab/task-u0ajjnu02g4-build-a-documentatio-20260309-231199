# Docs: PR Opening and Follow-up Actions

Purpose
- Provide an exact PR template and checklist for opening the documentation PR requested in Task #129.
- Ensure Marcus (backend) and Noah (DevOps) have clear reviewer tasks, SLAs, and acceptance criteria so they can replace placeholder API examples and runbook steps.

Files to link in the PR (already created by Chris):
- output/reports/pr_opening_and_reviewer_plan.md
- output/reports/reviewer_tasks_for_marcus_noah.md

PR metadata (use this exact text when opening the PR)
- Branch: docs/pr/docs-followup-task-129
- Title: docs: finalize API examples & runbook placeholders (Task #129)
- Labels: P1-review, docs, backend, devops
- Reviewers: @Marcus, @Noah
- SLA: 48 hours for reviewer response; set a reminder if no update after 36 hours.

Suggested PR body (copy/paste)

---
This PR finalizes the documentation deliverables for Task #129. It contains placeholder API examples and runbook steps that require confirmation or replacement by the backend and DevOps owners before merge.

Linked reports:
- PR opening & reviewer plan: output/reports/pr_opening_and_reviewer_plan.md
- Reviewer task descriptions and suggested PR comments: output/reports/reviewer_tasks_for_marcus_noah.md

What I need from reviewers (actionable):
- Marcus: Verify and replace the placeholder API request/response examples in docs where applicable. Confirm exact endpoint paths, request/response fields, data types, and add one positive and one error response example per endpoint.
- Noah: Verify and replace the runbook steps that reference environment-specific commands or monitoring checks. Confirm rollback steps and any required secrets or IAM roles.

Acceptance criteria (must be met before merge):
1. Marcus has updated API examples OR left clear line comments with required changes and committed updates to this branch (or pushed a linked branch) within 48 hours.
2. Noah has updated runbook steps OR left clear line comments with required changes and committed updates within 48 hours.
3. All remaining TODOs in docs are resolved or annotated with an owner and ETA.
4. CI/docs build passes and no broken links remain.

Checklist for PR opener (Emma)
- [x] Use branch name above
- [x] Set PR labels and reviewers
- [x] Paste the PR body above
- [x] Attach links to the two report files
- [x] Add this file (output/docs/docs_followup_pr_actions.md) to the PR

Suggested reviewer comment templates (copy from reviewer_tasks_for_marcus_noah.md if needed):
- Marcus: "Review note: I will confirm the API examples. Expect commit by <date 48h from PR open>."
- Noah: "Review note: I will confirm the runbook steps. Expect commit by <date 48h from PR open>."

If reviewers are unavailable
- Escalate to Alex (#ai-product) and Taylor (#ai-tech-lead) after 48 hours if no response.

Post-PR-open actions (Emma)
1. Post a message to Chris: "PR opened: <PR URL> — please create reviewer tasks in the tracker and post the reviewer comments." (Chris will handle creating tracker tasks and monitoring.)
2. Tag Marcus and Noah in the PR and in Slack with the 48h SLA.

Notes
- Keep changes in this single PR to minimize churn: reviewers should either commit direct fixes to this branch or leave clear change requests referencing precise file/line ranges.
- If an endpoint or runbook step is unclear, reviewers should open an issue rather than blocking merge indefinitely; include the issue link in the PR comments.

Files added to this PR
- output/docs/docs_followup_pr_actions.md

EOF
