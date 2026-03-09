# Docs PR Draft — CustomerInsights Follow-up

Overview

This document is the drafted documentation PR for the CustomerInsights follow-up report. It packages all required doc changes, code samples, acceptance criteria, PR checklist, backend sign-off & CS notification templates, and a suggested timeline.

Scope (files updated in this PR)

- docs: output/docs/api_reference_customer_insights.md
- code (Python sample): output/code/samples/python/customer_insights_example.py
- code (TS sample): output/code/samples/js/customer_insights_example.ts
- docs (ops/runbook): output/docs/ops_runbook_customer_insights.md
- docs (release notes): output/docs/release_notes_customer_insights.md

Acceptance criteria (must be met before merge)

1. API reference contains updated endpoints, full request/response examples, and all new/changed error codes.
2. Python and JS/TS samples run with current client libraries and produce the expected sample response shown in the API reference.
3. Ops runbook contains deployment checklist, rollback steps, monitoring queries (Datadog/Prometheus examples), and an on-call escalation matrix.
4. Release notes include user impact, migration steps (if any), and exact version/tags to be released.
5. Backend owner (Marcus) has signed off using the sign-off template below.
6. CI checks for docs formatting pass (markdown lint) and sample code lint/run tests pass.

PR Authoring Checklist (do these before opening the PR)

- [ ] Pull latest main and rebase
- [ ] Run docs linter (markdownlint) and fix issues
- [ ] Run Python sample: python -m venv .venv && .venv/bin/pip install -r requirements.txt && python output/code/samples/python/customer_insights_example.py
- [ ] Run TS sample: npm ci && ts-node output/code/samples/js/customer_insights_example.ts
- [ ] Verify examples in API reference match actual outputs
- [ ] Add cross-links to existing docs where relevant
- [ ] Add changelog/release notes entry
- [ ] Tag Marcus for backend sign-off and wait for his explicit approval comment

Backend sign-off template (copy into PR comment)

@Marcus / @ai-backend

Please review the following items and reply with 'LGTM' or list required changes:

- API endpoints in output/docs/api_reference_customer_insights.md (verify schemas & error codes)
- Server-side behavior & edge cases described in the ops runbook
- Sample responses in both code samples (python & ts) — these were generated from the staging API on DATE

Sign-off checklist:
- [ ] Endpoint schemas correct
- [ ] Error codes complete and accurate
- [ ] No behavioural changes missing from the ops runbook

Thank you — Emma

Customer Success notification template (to send after merge)

@Chris / @ai-support

Release: CustomerInsights follow-up docs (PR #XXX merged)
Impact: Briefly describe who is affected and what changed
Action required: Any user-facing instructions (copy from release notes)
Docs links:
- API reference: output/docs/api_reference_customer_insights.md
- Quickstart: (include link to quickstart section in the API reference)
Contact: @Emma (docs), @Marcus (backend)

Timeline & priority

- Priority: P1
- Target draft completion: Today (24 hours)
- Target backend sign-off: +24 hours after draft
- Target merge: +48 hours after sign-off

Open questions

1. Which staging timestamp / sample data set should be used to generate canonical sample responses? (Marcus)
2. Are there any rate-limiting or quota changes to call out in the release notes? (Marcus)
3. Is there a UI/UX change that requires additional user-facing screenshots? (Kevin)

--

This PR draft file is intended to be the single source of truth for the docs PR. After backend sign-off I will open the PR that updates the files listed above and request CS notification after merge.