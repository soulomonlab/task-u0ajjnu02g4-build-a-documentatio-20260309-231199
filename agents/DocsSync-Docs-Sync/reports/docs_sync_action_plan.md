Title: Docs Sync Action Plan for PR "update_docs_from_pr"

Source: output/reports/docs_update_from_pr_summary.md (Chris)
Prepared by: Docs Sync Agent (DocsSync)
Date: (auto)

Purpose
- Provide a clear, migration-safe action plan and draft doc updates so Emma can open the docs PR and get engineering confirmation for ambiguous items.

Scope
- Update public API examples in the docs
- Add or clarify required environment variable documentation in ops runbook
- Draft release notes and rollback guidance
- Produce a docs PR checklist and specific questions for engineering

Summary of issues to resolve (from Chris)
1) API examples ambiguous: missing or inconsistent request/response examples, unclear auth header usage, and inconsistent Content-Type in examples.
2) One environment variable requirement mentioned in the feature PR but not documented: name, default value, required/optional status, and where it must be set (build vs runtime).

Detailed action items
1) API examples (docs/public-api/*.md)
   - Replace existing examples with canonical templates for each endpoint: HTTP method, full request URL, required headers (Authorization, Content-Type), sample request body (JSON schema), and sample 200/4xx/5xx responses.
   - Add curl and node-fetch examples for each endpoint (kept small; not full SDK code). Include one minimal successful example and one error example per endpoint.
   - Acceptance criteria: each example is copy-paste runnable (curl or fetch) against the staging mock server and returns the documented response shape.

2) Environment variable (OPERATIONS)
   - Document env var: NAME TBD (engineering to confirm). For docs, include: variable name, expected type (string|bool|int), example value, whether it is required, default if any, where to set (docker-compose/K8s/CI/CD), and potential impact if mis-set.
   - Add an ops note: after deploy, verify using the health endpoint or by checking the application logs for a specific startup message.
   - Acceptance criteria: env var documented in ops runbook with example K8s manifest snippet and rollback note.

3) Ops runbook & release notes
   - Ops runbook: include pre-deploy checks (migrations, schema compatibility), config changes, environment variable steps, and rollback steps (how to revert config and code and how to re-run migrations safely if applicable).
   - Release notes: create a short user-facing paragraph + technical bullet list for SRE/deploy teams.
   - Acceptance criteria: ops runbook contains exact commands and manifests for production; release notes succinct and linked from the changelog.

4) QA and migration safety
   - Add a doc QA checklist item: test each API example against staging mock or real staging environment.
   - Add a rollback note: document the minimal steps to revert the change and where stateful migration risks exist.

Open engineering questions (please confirm with Alex/Marcus)
- API examples
  1. Which endpoints are considered stable v1 vs experimental for the release? (affects wording and examples)
  2. Exact request/response shapes for the ambiguous endpoints (attach sample JSON schema or example payloads).
  3. Auth header format: "Authorization: Bearer <token>" vs custom header? Is an API key allowed?
  4. Expected Content-Type for POST/PUT (application/json vs multipart/form-data)

- Environment variable
  5. Exact env var name and allowed values. Is there a default fallback? Is it required at runtime or only during build?
  6. Which deploy targets need this var set (k8s, lambda env, CI)? Any special provisioning steps?

Implementation notes (suggested wording and templates)
- Provide a small canonical example template for docs (place these directly into the docs PR):
  - Endpoint header (method + path)
  - Short description
  - curl example (single-line) + node-fetch example
  - Request JSON schema (minimal) and 200 response example
  - Errors: list of possible 4xx/5xx with sample codes

- For the env var documentation, include a K8s example snippet (ConfigMap/Secret) and docker-compose env example.

Docs PR checklist (for Emma)
- [ ] Replace ambiguous API examples with canonical templates (see above)
- [ ] Add code samples (curl + fetch) and test them against staging
- [ ] Add env var docs with examples and defaults
- [ ] Update ops runbook with pre-deploy checks and rollback steps
- [ ] Draft release notes and add changelog entry
- [ ] Request engineering confirmations inline on the PR for any remaining unknowns

Rollback note
- If this change requires DB migrations or stateful changes, include an explicit pre-release backup step and test rollback path; otherwise document the safe revert steps for config-only changes.

Next steps (recommended)
1) Emma: Open a docs PR using this action plan as the PR description, implement the doc changes, and mark each engineering question as TODOs in the PR.
2) Emma: Request direct confirmation from Alex for API stability and from Marcus for env var & deploy specifics. Tag them in the PR and paste these exact questions.
3) Engineering: Provide JSON samples and confirm env var name/values.

Owner: Emma (docs)

Files produced by this agent
- output/reports/docs_sync_action_plan.md (this file)
