Docs PR Authoring Guidance — Follow-up for PR docs updates

Situation
- CustomerInsights created an in-depth follow-up report: output/reports/docs_followup_from_pr.md. It lists impacted areas, MECE tasks, acceptance criteria, priority, timeline, and open questions.

Goal
- Turn that report into a concrete docs PR that updates API reference, code samples (priority: Python, JS/TS), ops runbook, and release notes. Obtain backend sign-off and notify Customer Success (Chris) after merge.

What to update (high-level)
1) API Reference
   - Update endpoint descriptions, request/response schemas, and error codes for all endpoints listed in the report.
   - Ensure JSON schema examples match the latest API model (field names/types). Add small sample responses for success and typical errors.
2) Code Samples (priority order)
   - Python: requests/urllib3 and sample SDK usage where relevant.
   - JavaScript/TypeScript: fetch/axios + typed example for TS where applicable.
   - Keep samples minimal (3–8 lines) and runnable. Add a one-line compatibility note if SDKs differ.
3) Ops Runbook
   - Add rollout steps, migration steps (DB or schema changes), monitoring checks, canary criteria, and rollback instructions.
   - Include KB links for feature flags, migration windows, and required infra changes.
4) Release Notes
   - Short summary (1–2 lines), impacted consumers, migration notes, and SDK upgrade guidance.
   - Include a backwards-compatibility statement and highlight any breaking changes.

Acceptance criteria (must be satisfied before merge)
- All sections updated where the report marks them impacted.
- Code samples for Python and JS/TS present, tested, and runnable (or annotated if mock-only).
- Ops runbook includes explicit rollout, monitoring, and rollback steps.
- API reference JSON schemas reflect the final API shape approved by backend and include example success & error payloads.
- Backend sign-off obtained in PR comments (see template below).
- Customer Success (Chris) is notified with the merged PR link and one-line summary.

Checklist for the PR
- [ ] Link to source report: output/reports/docs_followup_from_pr.md
- [ ] Files changed: list in PR description (API ref paths, runbook path, release notes path)
- [ ] Add code samples for Python and JS/TS; add test/verification notes
- [ ] Ops runbook rollout & rollback steps included
- [ ] Add a "Compatibility" subsection in release notes
- [ ] Request backend review & add sign-off comment
- [ ] After merge: notify #ai-support / Chris with link and summary

Backend sign-off comment template (copy into PR thread)
"@backend-team — Please review updated API reference and JSON schemas in this PR. Key files: [list paths]. Changes to confirm: field types for <FIELD>, new error code <CODE>, and any migration steps. Reply with 'LGTM' + note if any API/schema changes remain. Thanks."

Notify CS (post-merge) template
"@Chris — Docs PR merged: <PR link>. Summary: Updated API reference and code samples for <feature>, ops runbook updated with rollout and rollback steps. No customer action required / or migration notes: <if any>."

Timeline & priority
- Priority: P1 (as requested)
- Suggested ETA: draft PR (2 business days), backend review (1–2 business days), merge after sign-off.

Open questions / dependencies to resolve before authoring
- Confirm final API/schema with backend (fields and error codes).
- Confirm target SDK languages and whether sample code should use SDK or raw HTTP.
- Confirm ops owner for runbook review.

Deliverables I created
- This guidance doc: output/docs/docs_pr_author_guidance_for_emma.md
- Reference to the report: output/reports/docs_followup_from_pr.md (already created by CustomerInsights)

Notes / decision rationale
- Prioritize Python and JS/TS samples because they cover the largest portion of integrators per analytics in the product analytics report.
- Keep samples minimal and copy-paste ready to reduce friction for SDK authors and reviewers.

Next step (for Emma)
- Use this guidance + output/reports/docs_followup_from_pr.md to author the docs PR. Obtain backend sign-off (use template) and notify Chris after merge.
