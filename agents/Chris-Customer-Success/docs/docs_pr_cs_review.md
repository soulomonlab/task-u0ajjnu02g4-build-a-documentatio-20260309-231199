# CS Review — Docs PR Draft: Docs Sync

Summary
- This is a Customer Success (CS) review of `output/docs/docs_pr_update_from_docs_sync.md` (Docs Sync PR draft).
- Purpose: finalize user-facing release notes, confirm clarity of examples, and request engineering confirmations needed to run examples against staging.

Suggested release-note copy (user-facing)
- Short (one-line): "Improved docs: updated canonical API examples and clarified authentication headers — see examples in the API reference for quick start."
- Expanded (paragraph): "We updated the API reference with canonical examples and clearer authentication guidance to help you get started faster. If you use examples from the docs, please note some endpoints require updated header names and environment variables — engineering will confirm exact names before we enable the examples on staging."

Recommended placement and labels
- Put the short copy as the changelog entry and the expanded paragraph in the release notes / What's New section.
- Add a visible note at the top of the examples: "Staging examples will be enabled after engineering confirms API shapes, header names, and environment variables."

User-facing example wording guidance
- Use imperative, action-focused sentences: "Set X to <value>." "Call POST /v1/endpoint with header Authorization: Bearer <token>."
- Show one minimal, copy-paste-ready example and one expanded example with comments.
- Avoid TODO tokens in user-facing examples (replace with explicit placeholders like <API_KEY> or <ENV_VAR_NAME>).

Engineering confirmations we need (from PR TODOs)
1. API shapes: full request/response JSON shapes for each canonical example (including optional fields and defaults).
2. Exact header names and required auth scopes (e.g., Authorization vs X-Api-Key; bearer token vs API key).
3. Exact env var names for staging examples (e.g., STAGING_API_KEY vs API_KEY_STAGING).
4. Any required feature flags or staging-only flags that must be enabled to run examples.
5. Rate limits or special headers that affect example runs.
6. Expected success status codes and sample error responses for test assertions.

CS testing instructions (for Emma to run after engineering confirms)
- Step 1: Engineering replies inline with confirmed API shapes, headers, and env var names.
- Step 2: Create a staging env with the confirmed env var names and credentials.
- Step 3: Run the minimal copy-paste example and verify the response matches the confirmed success JSON.
- Step 4: Run the expanded example and verify edge-case responses (optional fields, error flows).
- Step 5: Report any mismatches back to engineering and update docs accordingly.

Acceptance criteria (for merging the docs PR)
- All TODOs are answered inline in the PR with exact values (API shapes, header names, env var names).
- Emma successfully runs all canonical examples against staging and confirms outputs match the documented responses.
- Release-note wording approved by CS (signed off in this PR or linked issue).
- Reviewer checklist passed (see below).

Reviewer checklist (CS lens)
- [ ] Short and expanded release-note copy present and clear.
- [ ] Examples contain copy-paste-ready code blocks and clear placeholders.
- [ ] No remaining TODOs visible in user-facing examples.
- [ ] QA / engineering confirmations are answered inline.
- [ ] Staging test run results attached or referenced in the PR.

Comments / suggested minor edits
- Replace any remaining "TODO: env var" placeholders with explicit <ENV_VAR_NAME> placeholders and add a one-line explanation for variable purpose.
- If there are long JSON blobs in examples, include a collapsed/expanded view or link to a sample file to keep the docs scannable.

Next steps (proposal)
1. Alex: please coordinate with Marcus to complete the engineering confirmations listed above inline in the PR.
2. Marcus (via Alex): answer each TODO with the exact API shape, header names, env var names, and any staging feature flags.
3. Emma: after confirmations, run the examples on staging and finalize the PR.

CS contact
- Chris (Customer Success) — available to review wording and run a final readthrough after engineering confirms values.

