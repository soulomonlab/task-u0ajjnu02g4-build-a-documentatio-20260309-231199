PR Title: docs: update API reference + ops runbook + release notes (from docs_sync_action_plan)

Overview

This PR implements the Docs Sync action plan produced by DocsSync (see output/reports/docs_sync_action_plan.md). It updates the public API reference, canonical code samples (prioritize Python and JS/TS), the affected ops runbook entries, and the release notes. Several engineering confirmations are required before this PR can be merged; those are listed in the "Engineering confirmations" section below.

Scope (what this PR changes)

- API reference: /api/v1/xyz (endpoints affected listed below)
- Canonical code samples: Python, JavaScript/TypeScript (minimal examples only)
- Ops runbooks: deploy/runbook sections that reference the undocumented environment variable
- Release notes: short migration notes and compatibility guidance
- PR description will include the engineering questions and a checklist for approvers

Files to change (proposed)

- docs/api/reference.md (update endpoint docs and examples)
- docs/samples/python/example_xyz.py
- docs/samples/js/example_xyz.js
- docs/runbooks/deploy_runbook.md (document NEW_FEATURE_FLAG env var usage)
- docs/release_notes/next.md (migration notes)

Canonical API examples (DRAFT — engineer confirmation required)

Note: examples include TODO placeholders where Docs cannot determine exact shapes or header formats. Please confirm with Alex/Marcus and replace the TODOs.

cURL (canonical intent):

curl -X POST "https://staging.api.example.com/api/v1/xyz" \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "field_a": "value",
    "field_b": 123
  }'

Expected (example) response (200):

{
  "id": "abc123",
  "status": "queued",
  "meta": {
    "estimated_seconds": 30
  }
}

Python (requests) snippet (DRAFT):

import os
import requests

API_KEY = os.getenv("API_KEY")  # confirm env var name with Marcus
URL = "https://staging.api.example.com/api/v1/xyz"  # confirm base URL + path

resp = requests.post(URL,
                     headers={
                         "Authorization": f"Bearer {API_KEY}",
                         "Content-Type": "application/json"
                     },
                     json={"field_a": "value", "field_b": 123})
print(resp.status_code)
print(resp.json())

JS (node / fetch) snippet (DRAFT):

const fetch = require('node-fetch');
const API_KEY = process.env.API_KEY; // confirm env var name

const resp = await fetch('https://staging.api.example.com/api/v1/xyz', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ field_a: 'value', field_b: 123 })
});
const body = await resp.json();
console.log(resp.status, body);

Engineering confirmations required (please reply inline in PR)

- Alex — API stability & versioning
  1) Confirm the canonical endpoint(s) and correct base path for the documented examples (staging vs prod). Is /api/v1/xyz stable for GA or is v2 planned?
  2) Confirm whether the request body field names and types above (field_a: string, field_b: integer) match the current API schema. If there are additional required fields, list them.
  3) Confirm response shape for success (200) and for queued/async cases (status field, meta.estimated_seconds). Provide canonical example responses for 200 and 4xx/5xx errors with error codes and messages.
  4) Confirm authentication header format: "Authorization: Bearer <token>" is correct, or if a different header is required (e.g., Api-Key header).

- Marcus — Deployment & env vars
  1) Confirm the exact environment variable name(s) used in staging and prod for API_KEY / NEW_FEATURE_FLAG. Is it API_KEY, EXAMPLE_API_KEY, or something else?
  2) Is the env var required in production, or optional behind a feature flag? If optional, document recommended default behavior.
  3) Confirm which services must set the env var (api-service, worker-service, docs-runner). Provide deploy target names.
  4) Confirm Content-Type requirements (JSON only) and any special headers (X-Request-ID, X-Org-ID) that must be included in examples.

Testing instructions (Docs author — how to run examples against staging)

Prerequisites
- Access to staging: ensure your account has a staging API key. If you don't have one, request from Marcus.
- Set environment variables locally: export API_KEY="<staging-key>" (confirm exact env var name with Marcus)
- cURL, Python 3.9+ (requests), Node 16+

Steps
1) Replace <API_KEY> in the examples with the staging key.
2) Run the curl example and confirm HTTP 200 and response JSON structure matches the documented example.
3) Run the Python and JS snippets and verify they produce the same output.
4) If the response indicates an async/queued status, record the meta fields and confirm the follow-up flow (polling endpoint/ webhook). Document the follow-up steps if needed.
5) Paste the actual request/response pairs into the PR as evidence (sanitized of any sensitive tokens).

If any step fails: comment in the PR with the failure details and assign to Marcus/Alex for investigation.

Acceptance criteria (must be green before merge)

- All canonical examples run successfully against staging and example request/response pairs are included in PR.
- Alex confirms API request/response shapes and versioning. Any incompatible changes are called out in release notes.
- Marcus confirms env var names, whether they are required in prod, and which services need them.
- Ops runbooks updated with the exact environment variable name and deploy instructions.
- CI linter passes (docs lint). A reviewer from Backend (Alex or Marcus) approves the API changes.
- Customer Success (Chris) reviews the user-facing wording and signs off on release notes.

Reviewer checklist (for the PR description)

- [ ] Backend review: API shapes & examples confirmed (Alex)
- [ ] Backend review: env vars & deploy targets confirmed (Marcus)
- [ ] QA: Examples executed against staging and evidence attached (Dana)
- [ ] CS: Release notes reviewed (Chris)
- [ ] Docs CI/Lint green

Next steps (how reviewers should proceed)

1) Review this PR draft and answer the engineering confirmations inline.
2) If you are a backend owner (Alex/Marcus): either confirm the items or update the example payloads/headers in the PR directly.
3) Docs author will run the examples against staging once Alex/Marcus confirm the missing details and will push final updates.
4) After all checks and approvals, merge the PR and notify Customer Success.

Contact / Owners
- Docs owner: Emma (this PR)
- Backend API owner: Alex
- Backend deploy/env owner: Marcus
- Customer Success reviewer: Chris

