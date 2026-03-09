# Reviewer Task Templates & PR Comment Scripts

Purpose: Prepare reviewer task descriptions and comment templates that Chris (Customer Success) will use to create reviewer tasks and post initial PR comments once the PR URL is available.

---

## 1) Quick checklist (what Chris will do once PR URL is posted)

- Create reviewer tasks for Marcus (API) and Noah (Runbook/Infra) with 48-hour SLA.
- Post initial reviewer comment in the PR asking reviewers to replace any placeholder API examples and runbook steps and to confirm acceptance criteria.
- Link reviewer tasks back to the PR URL and to Task #129 and Task #144.
- Monitor reviewer responses; escalate to Alex (#ai-product) if either reviewer cannot complete within 48 hours.

---

## 2) Reviewer task templates (copy/paste into tracker)

Title: Review PR for Task #129 — API examples & runbook verification
Assigned to: Marcus
Priority: P1 (48h SLA)
Due: 48 hours from PR creation
Description:
- Verify the PR's API example requests and responses. Replace any placeholder values with accurate examples from the current system.
- Confirm API endpoint paths, request/response field names, and any auth headers match implementation.
- Confirm forward/backward compatibility concerns and note migration steps if necessary.
- Approve PR or leave inline comments pointing to required code/docs updates.

Acceptance criteria:
- No placeholder API examples remain in the PR or docs.
- All endpoints, fields, and auth details are accurate.
- Inline comments from reviewer resolved or marked as blockers.

---

Title: Runbook & infra validation for Task #129
Assigned to: Noah
Priority: P1 (48h SLA)
Due: 48 hours from PR creation
Description:
- Review runbook steps included in the PR for operational accuracy and completeness.
- Replace any placeholder commands, script snippets, or monitoring links with the correct values.
- Confirm required infra changes (if any) and whether a migration window or downtime is needed.
- Verify rollback steps and escalation contacts are correct.

Acceptance criteria:
- Runbook contains no placeholders and is runnable by on-call.
- All infra-level steps validated and any missing infra tasks created.

---

## 3) PR comment templates (post these as the initial comment)

Template A — Initial PR comment (post by Chris)
---
Hi all — linking Task #129 and Task #144.
Please focus review on two items required before merge:
1) Replace placeholder API examples with real request/response examples (Marcus).
2) Validate and replace runbook placeholders (Noah).

Next steps:
- Marcus/Noah: please review and mark "approved" or leave inline comments. This PR has a 48-hour SLA for reviewer responses.
- After you confirm replacements, I will create tracker subtasks for any follow-ups and add the PR link to the Task #129 thread.

Thanks — I will create reviewer tasks and link them to this PR.
---

Template B — Reminder if no response after 24h
---
Gentle reminder: This PR needs your review for placeholder replacements. The 48-hour SLA is in effect. If you need more time, please reply with a new ETA so I can reassign/notify product.
---

Template C — Post-approval checklist comment (to leave before merging)
---
Thanks for the reviews. Before merge, confirm the following are complete:
- All placeholders replaced and inline comments addressed.
- Runbook verified and linked in this PR.
- Migration/rollback steps documented and scheduled if needed.

If all confirmed, please mark as approved and I'll proceed with merge coordination.
---

## 4) PR reviewer creation metadata (what to set when opening tasks)

- Link: add the PR URL in the task description (once available).
- Labels: docs, runbook, api, 48h-sla
- Reviewers to tag in PR: @marcus, @noah
- Reporter: @chris
- Related tasks: #129, #144

---

## 5) Escalation flow (if reviewers can't meet SLA)

- 24h no response: post Template B (reminder) and ping Alex (#ai-product) for prioritization.
- 48h no response: escalate to Alex and open an urgent engineering task for coverage.

---

## 6) Notes / gotchas for reviewers

- If you update API examples, update both request and response bodies and any embedded examples in runbooks.
- Keep changes backward-compatible where possible; if not possible, document migration steps.
- If you change any auth behavior, mark as blocker and notify Security/Product.

---

## 7) Where this file is used

- Copy reviewer task templates into the tracker when PR URL is posted.
- Use PR comment templates verbatim to ensure consistent messaging and SLA awareness.

