Engineering KB Confirmation Template

Context
- Product published two P0 Knowledge Base (KB) articles without engineering ETA/owner details.
- Product needs engineering confirmation so KB metadata and any customer-facing messaging can be finalized.
- Reference: output/docs/product_review_kb_published.md (Product review doc created by Alex). Task #175 assigned to Marcus.

Required Engineering Response (fill each section)
1) Owner
   - Name / team / best contact (email/Slack handle)

2) ETA
   - Target date (YYYY-MM-DD) and confidence (High/Medium/Low)
   - If phased, list milestone dates (canary, full rollout)

3) Rollback capability
   - Is rollback supported? (Yes/No)
   - If Yes: describe rollback steps at a high level (commands, feature flag toggle, DB rollback, etc.) and expected RTO/RPO.
   - If No: describe mitigation options and how to minimize user impact.

4) User-visible behavior changes
   - Bullet list of exactly what end-users will see or experience (UI text, error messages, new flows, downtime messages).
   - Include whether changes are immediate or gated by feature flags.

5) Required deploy windows / maintenance
   - Any maintenance window, downtime, or customer-facing availability constraints.
   - Timezone and duration estimate.

6) Dependencies & risks
   - Any dependent services, schema changes, or third-party impacts.
   - Top 3 risks and suggested mitigations.

7) Verification / QA checklist
   - Steps to validate the change post-deploy (end-to-end happy-path + 1-2 critical edge cases).
   - Smoke test commands or URLs.

8) Recommended KB messaging edits (copyable)
   - Short summary for KB metadata (1–2 lines).
   - Suggested customer-facing message or changelog entry (1 paragraph) that Product can paste.

9) Rollback owner & escalation
   - Who will own rollback if needed (name and contact).
   - Escalation path (pager / on-call / manager).

Acceptance criteria (what Product needs to sign off)
- Owner assigned and reachable.
- ETA provided with confidence level.
- Rollback plan or mitigation documented and owners named.
- Clear list of user-visible changes and verification steps.
- Suggested KB messaging provided.

How to respond
- Please copy this file into your reply (or paste the filled answers) either as a comment on Task #175 or directly in the Task thread.
- If you prefer, attach a short runbook for rollback and verification (link or doc).

Example "Recommended KB messaging edits" (copy/paste)
- KB metadata summary: "Resolved: [short summary of fix/change]. Users may see [user-visible change]."
- Customer message:
  "We deployed an update to [feature] on [date]. This update changes [what users notice]. No action is required. If you experience [symptom], please contact support and provide [diagnostic info]."

Notes / Constraints
- If a DB migration or non-reversible change is required, note that Product will need to coordinate a scheduled maintenance window and customer notification.
- Prefer feature flags for gradual rollout where possible to enable quick rollback.

Last updated: 2026-03-09
Author: Taylor (CTO)