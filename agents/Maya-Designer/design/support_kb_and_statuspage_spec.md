Title: Support KB & Status-Page / In-App Migration UX Spec

Purpose
- Provide Support with ready-to-publish KB templates for the two P0 issues (429/DRY_RUN_LIMIT and pagination migration) and provide frontend specs for status page banners and in-app migration notices.
- Ensure messaging is clear, actionable, and consistent across Support portal, status page, and product UI.

Audience
- Primary: Support (Chris) — publish KBs using the provided templates and copy.
- Secondary: Frontend (Kevin) — implement status page banners, in-app migration modal/toast and SDK-friendly error UI.

Files produced
- output/design/support_kb_and_statuspage_spec.md (this file)

1) KB Article Template (use for both KBs)

Structure (recommended order):
- Title (short + explicit)
- TL;DR (one-sentence summary)
- Severity / Impact (who is affected)
- Symptoms / How to identify (logs, API responses, examples)
- Root cause (short, non-technical summary + link to engineering issue)
- Immediate mitigation (what customers can do now)
- Migration / long-term fix steps (if applicable)
- SDK / frontend recommended handling (copy + code pointers)
- Support / contact instructions (what Support should ask/collect)
- References (links to related docs, epic, PRs)

Copy guidance (tone):
- Be concise, empathetic, and action-oriented.
- Start with what to do now (TL;DR + immediate mitigation).
- Use bullets, bold key actions, and provide copy snippets customers can paste.

Sample KB copy — 429 / DRY_RUN_LIMIT
- Title: "API 429: DRY_RUN_LIMIT exceeded — What to do"
- TL;DR: "Some requests may return HTTP 429 (DRY_RUN_LIMIT). If you see 429s, please implement exponential backoff and increase pagination window as described below."
- Severity: P0. Affects clients making high-volume DRY_RUN requests.
- Symptoms: Example response body + headers. Note: include exact header name for rate limit.
- Immediate mitigation:
  1) Retry with exponential backoff (suggest 100ms * 2^n, cap 2s, max 5 attempts).
  2) If using SDK, upgrade to version X which respects server 'Retry-After'.
- SDK/frontend handling:
  - Show a non-blocking toast: "Server busy — retrying..." and a subtle loader on the affected button.
  - Provide an opt-in "manual retry" button if operation is user-facing.
- Support troubleshooting checklist: request timestamps, example request IDs, SDK version, frequency.

Sample KB copy — Pagination Migration
- Title: "Pagination migration: change X → Y (Breaking change)"
- TL;DR: "We changed pagination semantics. Action required: update your client to use new 'page_token' param OR follow migration steps to avoid duplicate/missing data."
- Immediate mitigation:
  - Short-term: use legacy param (if available) or reduce page size to avoid overlapping results.
  - Long-term: update parsing logic to handle next_page_token; see code sample.
- Migration steps (developer-friendly): include 3-step code sample in JS/Python showing how to handle tokens and detect end-of-list.

2) Status Page & Public Notices

Placement & Priority
- Use the status page banner for global incidents (P0). Short headline + link to KB.
- Banner structure: [Severity Icon] [Short headline — 1 line] [CTA link "Read support advisory"] [Subtle timestamp]

Example banner copy:
- "P0: Pagination migration may affect list endpoints — Read advisory"
- Link target: published KB URL (Support must publish then update status page with link).

Accessibility & UX rules
- Banners must be keyboard focusable, have ARIA role="status".
- Provide high-contrast colors for severity.
- Include last-updated timestamp and link to a timeline entry.

3) In-Product Messaging (Frontend)

Use-cases
- Notify users inside the app who are taking actions that could surface the issues (e.g., exporting lists, running heavy DRY_RUN calls).

Components
- Non-blocking toast (for transient 429 retries): short message, auto-dismiss 4s, manual Dismiss action and optional "Retry".
- Migration modal (for migration guidance): shown once per user per account until acknowledged. Contains:
  - Title (Migration needed)
  - 2-line summary
  - Key steps (1–3 bullets)
  - Primary CTA: "View migration guide" (opens KB in new tab)
  - Secondary CTA: "Remind me later" (snooze 24 hours)

Wireframes (ASCII)
- Toast:
  [icon] Server busy — retrying... [Retry] [Dismiss]

- Migration modal:
  +------------------------------------------------+
  | Migration required                             |
  | We changed pagination behavior; update client. |
  |                                                |
  | • What to change                              |
  | • When to expect fix                           |
  |                                                |
  | [View migration guide]   [Remind me later]     |
  +------------------------------------------------+

Behavior rules
- Modal shown only to users who perform list operations that returned a pagination-related error OR on account-level rollout (feature-flagged).
- Avoid showing modal to background API consumers (non-interactive clients). Only in UI.
- Toasts for 429 should not block user flows; allow manual retry.

4) Component Specs (Tokens)

Colors
- P0 Banner background: #FFF4E5 (warning orange 10%) — ensure contrast for text.
- Toast background: #323232 (dark) with white text.

Typography
- Title: 16px / 600 weight
- Body: 14px / 400

Spacing
- Modal: 24px padding, 16px gap between bullets

5) Acceptance Criteria (for Support & Frontend)
- Support: KBs published with required sections and a public URL for each KB.
- Frontend: Status page banner shows with link to KB; In-product toast and migration modal implemented behind feature flags and tested on staging.
- QA: Provide list of flows where UI must be validated (toasts on 429, modal trigger, status page link).

6) Handoff Notes & Next Steps
- Support (Chris): Use the KB templates above to publish the two P0 KBs and paste public URLs into the status page. Once KBs are live, update the status page link.
- Frontend (Kevin): Implement status page banner, toast, and modal per this spec. Use feature flags to control rollout; coordinate with Support to fetch KB URLs after publishing.
- Engineering: Provide SDK guidance snippets and indicate SDK version that includes automatic backoff.

Design Decisions (short)
- Prefer non-blocking toasts for 429 because user flows often continue; blocking modals create frustration during transient rate-limiting.
- Use modal for migration because it requires user action and steps to change client code.
- Provide Support-ready copy to minimize time to publish.

References
- output/reports/customer_insights_docs_pr.md
- output/docs/docs_pr_followup.md
- GitHub Epic: https://github.com/soulomonlab/slack_bot/issues/155

Document owner: Maya (UX)
Last updated: 2026-03-09

