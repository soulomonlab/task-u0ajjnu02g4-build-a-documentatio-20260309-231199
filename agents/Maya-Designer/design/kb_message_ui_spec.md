# KB Messaging & In-App UI Spec

## Situation
Support published two P0 Knowledge Base (KB) articles quickly; Product needs engineering confirmation (ETA, owner, rollback capability, user-visible changes) before finalizing KB metadata and customer messaging.

## Purpose
Provide recommended customer-facing messaging and lightweight in-app UI changes (banner/modal) to surface the KB updates, plus component specs and wireframes. This is a design deliverable to help Product finalize wording and to give Engineering a clear implementation request to confirm feasibility and rollback requirements.

## Assumptions
- KB content is already live in the Help Center.
- We can show in-app banners and modal dialogs via existing frontend components (or create simple ones).
- Engineering can expose a boolean feature flag and content metadata (title, summary, link, version) per KB.

## User personas & contexts
- Customer Support Agents: need clear public-facing messaging.
- End users (logged-in): may be impacted by changes; should be informed non-disruptively.
- Admins: may require rollback or opt-out.

## Recommended customer-facing KB messaging (copy bank)
Use short, plain-language updates at the top of the KB and in the in-app message. Preferred structure: "What changed → Why it matters → What to do (if anything)".

Examples (short):
- Title banner on KB: "Update: [feature/behavior] changed on Mar 5 — details below"
- KB short summary (first paragraph): "We updated [X] to [new behavior]. This affects [who]. If you need the previous behavior, see rollback steps or contact Support."
- In-app banner (non-blocking): "Heads up: [X] updated. Learn what changed → [View KB]"

Tone: factual, concise, no blame, include clear action if user must act.

## User-visible behavior changes (design recommendation)
1. Help Center: Add a short, bolded "Update" header + 1-sentence summary at top of both KBs.
2. In-app non-blocking banner for logged-in users for 7 days (or until dismissed): shows summary + CTA to KB.
3. Optional modal for users performing the exact flow affected (only if critical and likely to cause errors): shows 2-line summary + primary CTA to KB + secondary "Continue (current flow)".

Rationale: Banner == low-friction awareness. Modal == only for high impact flows to prevent disruption.

## Wireframes (ASCII)
KB article top (Help Center):
----------------------------------------
[Update badge] Update • Mar 5, 2026
We updated how [X] behaves. This affects [Y]. Read details below. [View changelog]
----------------------------------------
Article title
Article body...

In-app banner (top of app, persistent until dismissed):
----------------------------------------
⚠️ [Heads up] [Short summary: "[X] updated: [one line]"] [View details →]
[Dismiss]
----------------------------------------

In-app modal (conditional):
----------------------------------------
| Title: "Important update to [X]" |
| Body: "We changed [behavior]. This may affect [your flow]. Read details or continue." |
| [View details] [Continue anyway] |
----------------------------------------

## Component specs
- Banner
  - Placement: fixed under global nav, full-width container (max width: 1200px centered)
  - Height: 56px
  - Background: neutral warning (e.g., #FFF4E5), border-left accent (#FFB020)
  - Text: 14px, medium weight
  - Primary CTA: right-aligned "View details →"
  - Dismiss: small "x" on far right; dismiss persists for 7 days (clientside + server opt-out via API flag)

- Modal
  - Width: 520px, center screen
  - Title: 18px bold
  - Body: 14px regular
  - Primary button: "View details" (primary style)
  - Secondary: "Continue anyway" (link style)
  - Accessibility: trap focus, ESC closes, screen-reader friendly

- KB top banner (Help Center)
  - Bold badge "Update" (accent color), date, 1-line summary
  - Place at top of article body, above title or immediately below depending on existing templates

## Implementation notes for Engineering (what design needs)
- API: feature flag + KB metadata endpoint returning {id, title, summary, link, version, published_at}
- Exposure: frontend needs to know which KBs to show banners for; provide list or boolean per user session
- Dismiss persistence: store per-user dismiss state via API or persistent client cookie + server-side fallback
- Rollback: backend should provide versioned KB content + 'previous version' link; frontend shows "View previous behavior" if available

## Acceptance criteria
- KB pages updated with short 'Update' summary at top.
- In-app banner shown to 100% of logged-in users for 7 days (or until dismissed) with working CTA to KB.
- Modal shown only for targeted flows (engineering to confirm trigger points).
- Dismiss action persists across sessions.

## Open questions for Engineering (Marcus)
1. Can backend provide an endpoint listing KB metadata + versioning and a per-user dismiss API? (needed for persistent dismiss)
2. Can engineering implement a feature flag or boolean to toggle banners and rollbacks quickly? What's ETA and owner?
3. Any constraints that prevent a 7-day banner or per-user persistence?

## Decisions / Trade-offs
- Banner vs Modal: Banner chosen as default to minimize disruption; modal only for high-impact flows. Trade-off: banner may be missed; modal is interruptive.
- Persistence: Prefer server-side dismiss recording for reliability; if not possible, use client cookie with clear expiry.

## Next steps for Product & Engineering
- Product: finalize KB copy (use examples above) and confirm whether modal required.
- Engineering (Marcus): confirm ETA, owner, rollback capability, whether API changes are possible within required timeline.

Document author: Maya (Designer)
