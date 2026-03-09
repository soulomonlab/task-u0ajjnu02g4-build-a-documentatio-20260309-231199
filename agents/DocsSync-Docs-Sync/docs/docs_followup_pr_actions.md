Title: PR Opening & Follow-up Actions

Purpose
- Provide step-by-step actions for Emma to open the PR, link the two reviewer reports, assign reviewers, set SLAs/labels, and notify Chris so reviewer tasks can be tracked.

Files to link in the PR
- output/reports/pr_opening_and_reviewer_plan.md
- output/reports/reviewer_tasks_for_marcus_noah.md

PR metadata (use these exactly)
- Suggested PR title: "Finalize docs & runbook placeholders — [feature-name]"
- Labels to add: needs-backend-review, needs-devops-review, sla-48h, docs
- Reviewers to add: Marcus (Backend), Noah (DevOps)

PR description template (paste into PR body)

Summary:
- Short one-line summary of what this PR aims to finalize.

Context / Links:
- Decision & timeline: see output/reports/pr_opening_and_reviewer_plan.md
- Reviewer tasks & suggested comments: see output/reports/reviewer_tasks_for_marcus_noah.md

What I need from reviewers (Acceptance criteria - ALL required):
1. Marcus (Backend): confirm or replace the placeholder API examples with final endpoints, request/response JSON, and any migration notes.
2. Noah (DevOps): confirm or replace runbook steps, validate rollout/rollback commands, and add any infra-specific prerequisites.
3. Both reviewers must leave explicit ACK comments in the PR and mark which files they changed or require changes to.

SLA and process
- SLA: 48 hours from PR opening. If a reviewer cannot complete within SLA, they must comment with expected ETA and notify Chris.
- If both reviewers approve within 48h, PR owner (Emma) should merge according to merge policy.
- If unresolved after 48h, revert PR to draft and tag Chris for escalation.

Checklist for PR opener (tick before opening)
- [ ] Insert the PR description template and link the two report files above.
- [ ] Add Marcus and Noah as reviewers.
- [ ] Apply labels: needs-backend-review, needs-devops-review, sla-48h, docs.
- [ ] Attach any additional runbook artifacts if available.
- [ ] Paste the suggested reviewer comment (below) into the PR to make review action explicit.

Suggested reviewer comment to paste (so Chris can automate later):
"@Marcus / @Noah — Please confirm or replace the placeholders in the PR within 48 hours. See the reviewer tasks here: output/reports/reviewer_tasks_for_marcus_noah.md. If you need more time, reply with ETA and @Chris for escalation."

Post-PR opening actions (what Emma does after opening)
1. Post the PR link in the Chris thread and ping @Chris (Chris will create reviewer tasks in the tracker and post reviewer comments on the PR).
2. Monitor reviewer responses for 48 hours and update labels accordingly.

Rollback & escalation note
- If review blockers are discovered that prevent merging, mark PR as draft and escalate to Chris with a summary of the blocker, impacted systems, and next steps.

Contact
- Chris (Owner of reviewer coordination and monitoring)

