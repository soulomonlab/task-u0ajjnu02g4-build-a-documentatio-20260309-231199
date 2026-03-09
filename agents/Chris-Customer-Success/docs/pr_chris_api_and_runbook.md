PR: Add Anthropic worker mapping API draft + runbook

Files included (already present in repo):
- output/docs/api_anthropic_worker_mapping.md
- output/docs/runbook_apply_anthropic_mappings.md
- output/reports/docs_followup_from_pr.md

PR description (for GitHub):
This PR adds draft documentation for Anthropic worker mappings and an operational runbook for applying mappings.

Why:
- Emma prepared draft API and runbook artifacts as part of the DocsSync follow-up. The API fields and endpoint paths are provisional and require backend confirmation and QA validation before publishing.

Acceptance criteria (summary):
1. Marcus (backend) confirms canonical request/response JSON schemas and endpoint paths.
2. Dana (QA) validates sample requests/responses in staging and signs off on runbook steps.
3. Any field-name/type discrepancies are documented and resolved in the PR.

Requested reviewers:
- Marcus (backend) — Please confirm canonical API contract and propose any schema/path changes in PR comments.
- Dana (QA) — Please execute the sample requests on staging and confirm runbook steps; attach results as PR review comments.
- Emma (Docs) — Confirm this PR's content and wording; update docs if Marcus/Dana request changes.

Labels: docs, p1

Suggested target repo/branch (if you're opening this):
- Repo: github.com/our-org/platform
- Branch: docs/anthropic-mappings

Notes for reviewers:
- The 'docs_followup_from_pr.md' contains acceptance criteria and the provisional field list. Use it as the source of truth for validation and sign-off.
- If Marcus changes field names/types, please include a short migration note describing compatibility impact.

Next steps:
- Emma: open the PR against the suggested repo/branch, include the three files, add labels, and request reviewers Marcus and Dana.
- If Emma prefers, I (Chris) will open the PR — tell me the repo/branch and I'll proceed.
