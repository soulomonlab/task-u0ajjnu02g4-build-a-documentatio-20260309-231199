PR Title: docs: Anthropic worker mapping — API reference + runbook + PR guidance

Summary
- This PR consolidates documentation required to ship Anthropic worker mapping support: API reference, runbook for applying mappings, PR guidance, and the docs opening checklist prepared by Chris.

Files to include
- Please include the three draft artifacts Chris added to the repository (he added them in the docs area of the repo). I did not modify their contents.

Target repo/branch
- Repository: github.com/our-org/platform
- Target branch: docs/anthropic-mappings

Labels and reviewers
- Labels: docs, p1
- Requested reviewers: Marcus (backend), Dana (QA)

PR body (suggested)
- What: Adds API reference for Anthropic worker mapping, operational runbook for applying mappings, and PR guidance + opening checklist.
- Why: Finalize docs so backend and QA can validate API shapes and staging tests before merge.
- Notes for reviewers:
  - API fields/endpoints are currently provisional and require Marcus to confirm canonical request/response shapes.
  - Dana should validate sample requests/responses in staging and confirm runbook steps are reproducible.

Merge criteria (must be met before merge)
1. Marcus (backend) confirms canonical API request/response shapes and signs off in PR comments.
2. Dana (QA) validates sample requests in staging and confirms tests pass; posts a QA approval comment.
3. All PR checklist items are completed and the docs reviewer resolves any comments.

If you want me to open the PR instead
- I can open the PR if you can provide either: (a) a GitHub repo + branch with write permission for me, or (b) invite me as a collaborator with permission to open PRs in the target repo. Otherwise please open the PR using the guidance above.

Suggested commit/PR title
- "docs: Add Anthropic worker mapping API reference and runbook"

Notes
- I created this PR body to make opening the PR one-click for you.
- I did not change the draft artifacts Chris already added; I assume those files are staged in the repo and should be included as-is.
