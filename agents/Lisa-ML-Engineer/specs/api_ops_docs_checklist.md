Title: API & Ops Docs Checklist (Post-PR)

Situation
- A recent PR from provider 'anthropic' mapped code changes that affect API and operational docs (per Alex's update). We need a deterministic checklist to ensure docs fully reflect code and ops changes before merging follow-up PRs.

Complication
- PRs often update implementation but miss: OpenAPI spec, client SDKs, deployment runbooks, migration steps, monitoring/playbooks, and release notes. Missing docs cause on-call confusion and deployment/regression risk.

Resolution — Checklist (use this to drive follow-up PRs)
1) API Surface & Contracts
   - Update OpenAPI (openapi.yaml / swagger.json) to reflect added/removed endpoints, param changes, response schema changes.
   - Add API changelog entry with commit hash and rationale.
   - Update client SDK docs and example requests where applicable.
   - Acceptance: curl/postman examples run against staging, unit tests for schema changes pass.

2) Integration & Backward-compatibility
   - Document breaking changes and migration steps for clients (versioning strategy: major/minor tags).
   - Add deprecation notice and timeline if endpoints are removed.
   - Acceptance: compatibility smoke tests (old client → new server) pass.

3) Environment & Config
   - List new/changed env vars and their defaults (runtime, CI, k8s secrets).
   - Update deployment manifests and Helm values documentation.
   - Acceptance: deployment to staging with documented env vars succeeds.

4) Ops Runbook & Monitoring
   - Update runbook: deployment steps, rollback steps, common errors after change, mitigation steps.
   - Update monitoring dashboards and alerts affected by changes (metric names, tags).
   - Add playbook steps for on-call (who to page, commands to run).
   - Acceptance: simulated alert triggers documented remediation steps.

5) Security & Compliance
   - Document any new sensitive data flows, required encryption, or updated access controls.
   - Update IAM roles/policies docs if applicable.
   - Acceptance: security review sign-off (if sensitive) or short approval note.

6) QA & Testing Docs
   - Update test plan: unit/integration/e2e tests impacted, new test cases to add.
   - Add regression checklist for QA to validate in staging.
   - Acceptance: QA checklist marked green in staging run.

7) Release Notes & Changelog
   - Draft release notes: short summary, impact, migration steps, targeted audience.
   - Ensure release version and date are set.

8) Ownership & Reviewers
   - Assign: Backend owner (Marcus) for API contract changes; DevOps (Noah) for deployment/config; Docs owner (Emma) for PR text; QA (Dana) for test validation.

9) PR Template Additions (for follow-up PR)
   - "Docs impact" section: list files to update and checklist items completed.
   - Attach staging verification logs/screenshots where relevant.

10) Acceptance Criteria (final)
   - All affected doc files updated and reviewed by owners.
   - Staging verification passed and QA sign-off.
   - Handoff to Release/DevOps for deployment.

Notes
- Keep checklist items atomic and reference specific files (openapi.yaml, docs/api/*.md, ops/runbook.md). Use this checklist in PR description and mark completed items as checkboxes.
