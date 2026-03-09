API & Ops Documentation Checklist

Purpose
- A single, actionable checklist to ensure every PR that affects APIs or operational behavior includes the necessary documentation updates before merge.

How to use
- Attach this checklist to PRs that change API shape, behavior, deployment, monitoring, or operational runbooks. The PR author fills the Status/Owner columns and attaches links to the updated docs.

Sections
1) PR metadata
- PR URL: 
- Change summary (1-2 sentences):
- Doc owner (name / team):

2) API Reference (mandatory for API surface changes)
- [ ] Endpoint added/removed/changed — Describe changes and rationale. Provide OpenAPI diff or endpoint summary.
- [ ] Request examples (curl/HTTP) — one for success, one for a common failure.
- [ ] Response examples — success payload and error payloads with status codes.
- [ ] Parameters documented (query/path/body) with types and defaults.
- [ ] Authentication & authorization notes updated.
- [ ] Rate limiting and quotas documented (if changed).
- [ ] Pagination / filtering semantics documented.
- [ ] Deprecation windows and migration guidance (if removing/renaming fields).

3) SDK / Client impact
- [ ] Client libraries impacted — list repos and owners.
- [ ] Breaking changes flagged and linked to migration examples.

4) Error codes & troubleshooting
- [ ] Error codes table updated (code, message, HTTP status, cause, remediation).
- [ ] Common support scenarios and suggested debugging steps.

5) User-facing guides & FAQs (if feature affects end users)
- [ ] Quickstart updated (<=5min example)
- [ ] Task-based guide updated (how-to for common workflows)
- [ ] FAQ entries added/updated for expected questions.

6) Ops / Runbooks (for deployment/monitoring changes)
- [ ] Deployment steps updated (staging -> prod).
- [ ] Rollback procedure included and tested in staging.
- [ ] Post-deploy validation checks (health endpoints, smoke tests).
- [ ] Monitoring & alerting: metrics updated, new alerts documented, runbook actions mapped.
- [ ] Required infra changes (DB migrations, feature flags) noted with migration window.

7) Security & compliance
- [ ] Threat model updated (if relevant).
- [ ] Secrets/keys rotation guidance included.
- [ ] Data retention / privacy impact notes updated (if schema/data changes).

8) Accessibility & Localization
- [ ] Text shown to end-users reviewed for accessibility.
- [ ] Strings extracted for localization (if UI changes).

9) Review & Sign-off
- [ ] Engineering review (code owner) — name/date
- [ ] Docs review (technical writer) — name/date
- [ ] Support review (customer success) — name/date
- [ ] Security review (if required) — name/date

Acceptance Criteria (PR cannot merge until these are true)
- API reference pages updated and link included in PR description.
- Ops runbook updated for any change that affects deployment, rollback, or monitoring.
- Quickstart or user guide updated for visible UX changes.
- At least one support FAQ drafted for customer-facing changes.

Owner tips
- Small PRs that change multiple layers should still include minimal doc updates (short note + follow-up task if deeper docs required).
- Use OpenAPI diffs and examples to minimize manual errors.

Template to attach in PR description (copy/paste)
- Docs updated: [yes/no]
- Links to updated docs:
  - API reference: <link>
  - Runbook: <link>
  - User guide/FAQ: <link>
- Docs owner: <name>
- Sign-offs: engineering: <name>, docs: <name>, support: <name>

Version history
- 2026-03-09 — v1.0 — Initial checklist created by Emma (Technical Writer)

