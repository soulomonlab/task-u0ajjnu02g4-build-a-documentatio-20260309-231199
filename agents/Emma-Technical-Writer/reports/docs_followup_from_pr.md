# Docs Follow-up from PR: Anthropic Worker Mapping

Created by: DocsSync
Date: 2026-03-09

Summary
- This report summarizes Chris's review comments on the Anthropic worker mapping PR and lists the doc actions needed to complete the release.

Impacted Areas
- API Reference: new endpoints to document; request/response examples to add
- SDK samples: update mapping helper functions
- Ops Runbook: include mapping change procedures and validation steps
- Release Notes: mention breaking/non-breaking changes

Recommended Tasks
1. Author API docs for Anthropic worker mapping (GET/POST) — include request/response examples and error codes. (Owner: Emma)
2. Update Python and cURL SDK samples in docs. (Owner: Emma)
3. Add runbook section describing how to apply mappings and validate in staging. (Owner: Emma)
4. Coordinate backend confirmation of exact API diffs (Owner: Marcus) — blockers: field names, endpoint paths, required fields
5. Request QA validation on staging examples (Owner: Dana)

Acceptance Criteria
- API docs: confirmed fields, sample requests/responses tested in staging.
- Runbook: step-by-step apply + validate + rollback instructions.
- Release notes: short summary + migration notes (if any).
- QA: green validation report attached to PR.

Priority & Timeline
- Priority: High (blocking release)
- Timeline: Docs PR authored within 48 hours; backend confirmation within 24 hours of PR opening; QA validation within 24 hours of staging examples being provided.

Open Questions (require backend answers)
- Exact endpoint paths and HTTP verbs
- Final field names and types
- Are there any rate limits or size limits we should document?
- Any auth/permission special cases (e.g., only admin keys can write mappings)?

Next Steps (for Emma/#ai-docs)
- Review this report and author the docs PR containing:
  - API reference file(s)
  - Example code samples (curl, Python)
  - Runbook section for applying mappings
  - Draft release notes
- Tag Marcus for final API confirmation and Dana for QA validation in the PR.

