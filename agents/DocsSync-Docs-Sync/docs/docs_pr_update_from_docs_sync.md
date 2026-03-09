Docs PR Update — Ready for CS review and engineering confirmations

Summary
- I updated the PR draft with canonical examples, testing instructions, and a checklist. Several TODOs remain where exact API shapes, headers, and env var names are required from engineering. CS review needed for user-facing wording and rollout notes.

Files updated
- output/docs/docs_pr_update_from_docs_sync.md (original PR draft by Emma)
- This file: output/docs/docs_sync_cs_review_request.md (DocsSync — CS review request and suggested release-note wording)

What I need from CS (Chris / #ai-support)
1) Review the suggested release-note wording and pick Short or Expanded (or edit).
2) Tag Alex & Marcus in the PR and request they answer the engineering confirmations listed in docs_sync_cs_review_request.md.
3) Confirm any CS-specific test accounts, feature flags, or rollout notes that must be included in the PR before publishing.

Engineering confirmations required (copy from docs_sync_cs_review_request.md)
- API endpoints and method(s)
- Request header names and auth scheme
- Response shapes (success and errors)
- Environment variable names (staging placeholders)
- Required query params or body fields
- Rate limits and expected response times for staging
- Staging test instructions (test tenant, flags)
- Rollback / operational impact details

Next steps (what I'll do after confirmations)
- Update the PR examples with exact headers, env vars, and response shapes.
- Run the canonical examples against staging and record output in the PR.
- Remove all TODOs and mark the PR ready for final review and merge.

Acceptance criteria
- All engineering confirmations answered inline in PR.
- CS-approved release-note wording.
- Examples successfully executed in staging and updated in the PR.
- Docs linter and reviewer checklist passed.

Output files created by DocsSync
- output/docs/docs_sync_cs_review_request.md — CS review package and suggested wording

Please confirm you can take the handoff and I'll route the request to you.
