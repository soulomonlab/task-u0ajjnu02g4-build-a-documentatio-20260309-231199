# Confirmation Request for Docs PR (Task #112)

## Purpose
This document summarizes the four ambiguous items identified in output/reports/docs_ambiguities_product_impact.md and provides proposed reversible defaults so the docs PR can proceed. It also lists clear acceptance criteria and asks Product (Alex) to confirm product decisions and coordinate with Engineering (Marcus) for any technical values.

## Reference
- Source analysis: output/reports/docs_ambiguities_product_impact.md

## The four ambiguity items (summary + proposed temporary defaults)
1) Item A — Default behaviour / feature flag
   - Short description: Unclear default state for the new feature toggle (on vs off) in user-facing docs.
   - Proposed temporary default: Feature toggle = OFF (docs explain opt-in flow).
   - Rationale: Minimizes user impact while allowing docs to describe the opt-in path. Reversible by switching the default and updating the docs note.
   - Acceptance criteria for docs PR: Docs show the opt-in flow, include a clear note "Default: OFF (temporary)" and reference the config flag name. Product/Engineering approval captured in PR comments.

2) Item B — API rate-limit / guidance in docs
   - Short description: Recommended API rate-limit guidance not finalized.
   - Proposed temporary default: Recommend "up to 60 requests/minute" in docs with a note that this is a temporary guidance pending engineering confirmation.
   - Rationale: Provides practical guidance to users while being conservative for backend scalability.
   - Acceptance criteria for docs PR: Docs state the guidance and add an inline TODO linking to engineering ticket/confirmation. Engineering must comment on PR to confirm or update.

3) Item C — Error code mapping / recommended retry behaviour
   - Short description: Which server errors should be retried client-side and the suggested retry backoff.
   - Proposed temporary default: Recommend retries for 5xx errors with exponential backoff starting at 500ms, max 3 attempts. Do NOT recommend retry for 4xx errors.
   - Rationale: Conservative, standard client-side retry pattern that lowers accidental load on backend while improving UX.
   - Acceptance criteria for docs PR: Docs include explicit examples and the note "temporary default — awaiting engineering confirmation"; engineering to confirm acceptable retry policy.

4) Item D — CLI/SDK version compatibility statement
   - Short description: Untested compatibility matrix for SDK versions vs API changes.
   - Proposed temporary default: State compatibility for SDK versions `>=1.2.0` and `<2.0.0` (temporary), and include instructions for how to test compatibility and report issues.
   - Rationale: Allows users to get started and keeps the compatibility statement conservative.
   - Acceptance criteria for docs PR: Docs include compatibility statement and a clear "known limitations" section; engineering to confirm the exact supported versions.

## Request / Next actions (for Alex)
- Please confirm each proposed temporary default above for Product, and if any require different values, provide the final values.
- Please coordinate with Marcus to confirm the engineering constraints for Items B, C, and D (rate limits, retry policy, supported SDK versions). If you prefer, I can draft the docs PR using these temporary defaults and tag both you and Marcus for final sign-off.

## Communication & traceability
- Link primary source: output/reports/docs_ambiguities_product_impact.md
- When you provide final values, please either:
  1) Reply in this thread with final values, or
  2) Ask me to draft the docs PR with your chosen values and I'll create the PR draft and tag both you and Marcus.

## Notes
- All proposed defaults are intentionally conservative and reversible. They are intended to unblock docs work while preserving backend stability.
- If Engineering (Marcus) objects to any default, please indicate required alternative and acceptance criteria so docs can be updated before merging.

(Prepared by Chris — Customer Success Engineer)