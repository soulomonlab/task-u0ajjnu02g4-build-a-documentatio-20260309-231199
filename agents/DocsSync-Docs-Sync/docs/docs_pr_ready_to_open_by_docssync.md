PR: Open request for Anthropic worker mapping docs

Target repo & branch
- repo: github.com/our-org/platform
- branch: docs/anthropic-mappings (suggested; change if you prefer)

Files to include (already in repo)
- output/docs/pr_chris_api_and_runbook.md
- output/docs/docs_pr_draft_chris.md
- output/reports/docs_pr_opening_checklist.md
- output/docs/api_anthropic_worker_mapping.md (Emma – canonical draft)
- output/docs/runbook_apply_anthropic_mappings.md (Emma – runbook draft)
- output/reports/docs_followup_from_pr.md (Chris – followups)

PR metadata (please copy into GitHub PR form)
- Title: docs(anthropic): Add Anthropic worker mapping API and runbook
- Labels: docs, p1
- Reviewers: @Marcus (backend), @Dana (QA)

Suggested PR description (paste into PR body)
- Summary: Adds documentation for Anthropic worker mappings: API reference, runbook for applying mappings, and supporting follow-ups. Marcus needs to confirm canonical request/response shapes; Dana needs to validate samples in staging before merge.

- Files included:
  - output/docs/api_anthropic_worker_mapping.md
  - output/docs/pr_chris_api_and_runbook.md
  - output/docs/docs_pr_draft_chris.md
  - output/docs/runbook_apply_anthropic_mappings.md
  - output/reports/docs_pr_opening_checklist.md
  - output/reports/docs_followup_from_pr.md

- Acceptance criteria before merge:
  1) Backend (Marcus) confirms and stamps the canonical API shapes in api_anthropic_worker_mapping.md or leaves in-line comments to request changes.
  2) QA (Dana) validates sample requests/responses in staging and adds a QA sign-off comment in the PR. If samples fail, record steps and expected vs actual in the PR comments.
  3) Docs owner (Emma) incorporates any API/behavior changes and updates runbook if the apply steps change.

Reviewer guidance (what Marcus should check)
- Confirm canonical request/response JSON schemas for all endpoints listed.
- Confirm endpoint URLs and auth requirements match implementation.
- Note any unstable/provisional fields using TODOs or an explicit “provisional” tag in the doc.
- If changes are required, suggest text edits or link to the implementation PR/issue.

QA guidance (what Dana should validate)
- Deploy the corresponding backend branch to staging (link to staging env if available).
- Run sample requests from output/docs/api_example_requests.md against staging.
- Validate each sample’s response schema and field semantics; attach sample curl/Postman outputs to PR comments.
- Mark QA sign-off in PR when all samples pass.

Merge conditions & rollback note
- Merge only after BOTH Marcus and Dana sign off.
- Rollback: revert PR and open follow-up ticket linking this PR and the backend change if any post-merge issues arise.

If you want me to open the PR instead
- Tell me which repo/branch to target if different from suggested.
- I will open the PR and assign reviewers as requested.

DocsSync notes
- Chris prepared pr_chris_api_and_runbook.md, docs_pr_draft_chris.md, and reports/docs_pr_opening_checklist.md.
- Emma’s api/runbook drafts exist and are referenced above.
- Key blocker: canonical API shapes still provisional — needs Marcus confirmation.
