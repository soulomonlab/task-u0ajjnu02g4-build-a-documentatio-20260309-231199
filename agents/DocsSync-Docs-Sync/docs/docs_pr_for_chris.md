Summary
-------
This artifact packages Emma's drafted docs and the follow-up report and requests that Chris open the docs PR and coordinate backend + QA sign-offs.

Files to include in the PR
-------------------------
- output/docs/api_anthropic_worker_mapping.md
- output/docs/runbook_apply_anthropic_mappings.md
- output/reports/docs_followup_from_pr.md

Background / context
--------------------
- Emma produced the draft API doc and runbook (paths above).
- API endpoint paths and request/response fields are still provisional and must be confirmed by Marcus (backend).
- QA (Dana) must validate sample requests/responses in staging before we finalize docs.
- Acceptance criteria and follow-up actions are documented in output/reports/docs_followup_from_pr.md — include these in the PR description.

Requested PR actions (step-by-step)
-----------------------------------
1. Create a docs PR that adds the three files above.
   - Suggested PR title: "docs: add Anthropic worker mapping API + runbook"
   - Copy the acceptance criteria section from output/reports/docs_followup_from_pr.md into the PR description.
2. Tag reviewers: Marcus (backend) and Dana (QA). Assign Emma as primary docs author in the PR or add her as a reviewer.
3. In the PR description, explicitly call out which API fields are provisional and request Marcus to confirm canonical request/response shapes by commenting with confirmed shapes or pushing a follow-up commit.
4. Ask Dana to validate the sample requests/responses in staging and comment on the PR with pass/fail and any sample corrections.
5. Once Marcus and Dana sign off, merge the PR and update the CHANGELOG / release notes (if applicable).

Optional: If you prefer Emma to open the PR, reply with repo and branch target and she will prepare the PR content.

Acceptance criteria (at merge time)
-----------------------------------
- Marcus has confirmed canonical API endpoint paths and request/response shapes (explicit comment or commit in PR).
- Dana has validated samples in staging and left QA approval in PR.
- PR includes the runbook and follow-up report and links to any related Jira/issue IDs.

Notes / gotchas
---------------
- Do not finalize API path strings until Marcus confirms; document interim placeholders as "PROVISIONAL" in the PR body.
- If Marcus requests changes to the docs, prefer small follow-up commits to keep history clear.

If you need me (DocsSync) to add any missing doc sections before opening the PR, I can update the files — just specify what’s missing.
