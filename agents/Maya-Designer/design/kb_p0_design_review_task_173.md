# KB P0 Design Review — Task #173

Date: 2026-03-09
Author: Maya (Designer)

## Situation
Alex is completing product review for Task #173 (two published P0 KBs). QA will run the acceptance checklist after product review. My role: evaluate the KB user experience and produce a small, actionable design spec with defects, recommended UI changes, and implementation acceptance criteria.

## Complication
P0 KBs must be extremely scannable, unambiguous, and surface actions (proactive notifications, mitigations) clearly. Common UX issues with KBs that risk customer confusion:
- severity/impact unclear on first glance
- long text walls without step-level affordances
- missing quick-actions (e.g., subscribe, view incident timeline)
- inconsistent metadata (author/date/systems affected)
- mobile/tablet layout breakage for long steps

## Resolution (deliverable)
I reviewed the KB presentation patterns and created concrete UI recommendations, component specs, wireframes, and acceptance criteria so frontend can implement them quickly.

Files produced here: this design doc (output/design/kb_p0_design_review_task_173.md)

---

## Design Summary (Top 6 recommendations)
1. Add a prominent P0 header bar (full-width amber/red) with: severity label, short one-line impact summary, confirmed boolean, ETA (if known), and CTA: "Subscribe to updates".
2. Collapse long step lists into numbered steps with expand/collapse per step and inline copyable command blocks.
3. Add a metadata strip beneath the title (published, last-updated, author, affected services, tags) with clear icons.
4. Insert an "Immediate Mitigation" callout (visual emphasis, subtle icon) pinned near top for customers who need first-step actions.
5. Add page-level table-of-contents (TOC) for long KBs on desktop; on mobile, a sticky floating quick-nav button that opens TOC.
6. Accessibility: ensure headings, button targets, and color contrast meet WCAG AA. Keyboard focus order must prioritize Subscribe and Mitigation CTAs.

## User personas & flows
- Persona: Platform Engineer (urgent reader) — needs immediate mitigation steps and subscription to updates.
- Persona: Customer Success / Support — needs full timeline, root cause, and reproducible steps.

Flow A (Engineer, immediate):
1. Land on KB → P0 header visible → read one-line impact
2. Click "Immediate Mitigation" → expands a short step set with copy buttons
3. Click "Subscribe" → modal confirms subscription

Flow B (Support):
1. Land on KB → metadata strip and TOC scanned
2. Jump to timeline section via TOC → review publish/updates
3. Use permalink or copy step blocks for ticket

## Component specs
1. P0 Header Bar
   - Height: 64px desktop, 56px mobile
   - Background: #FFF4E5 (amber 10%) with 1px darker border #FFEDD5; severity chip: background #FF7A59, white text
   - Elements: Severity Chip (left), one-line impact (center, semibold 16/18), CTA group (right): [Subscribe] [View timeline]
   - Behavior: sticky on scroll for first 120px; compresses to 48px after scroll

2. Metadata Strip
   - Layout: horizontal left-to-right, small icons with labels
   - Items: Published (date), Last updated (date), Author, Affected services (chips), Tags
   - Typography: 12px/14px, muted color #6B6B6B

3. Step Block
   - Each numbered step is a card with: step number badge, text, optional code block with copy icon, expand/collapse chevron
   - Code block: monospace, 14px, copy button top-right (visible on hover and keyboard focus)

4. Immediate Mitigation Callout
   - Card with left accent border (#FF7A59), icon (shield/warning), bold title, up to 3 bullet steps
   - Place: directly below metadata strip

5. TOC
   - Desktop: left column sticky for wide screens (> 1024px)
   - Mobile: floating circular button bottom-right opens slide-over TOC

## Wireframes (ASCII)
Desktop (wide):

[Header Nav]
[KB Title]
[P0 Header Bar: [P0] Impact summary ----------------- [Subscribe][Timeline]]
[Metadata strip: date | updated | author | services chips]
[Immediate Mitigation Callout]
[TOC (left column)]  [Content area: steps, timeline, root cause, links]

Mobile:
[Header Nav]
[KB Title]
[P0 Header Bar]
[Metadata strip]
[Immediate Mitigation Callout]
[Content: steps collapsed by default]
[Floating TOC button]

## Acceptance criteria for frontend
- P0 header visible within 1s on page load and is sticky until user scrolls past 120px.
- Subscribe CTA opens modal with success toast; user is added to subscription list (API endpoints TBD).
- Step blocks: expand/collapse works; copy-to-clipboard works on click and keyboard (aria-live for confirmation).
- Mobile TOC accessible and closes on outside tap; focus management returns to triggering control.
- Color contrast for all text >= 4.5:1 (body) and 3:1 for large text.

## Implementation notes (backend dependencies)
- Need fields: severity (enum), confirmed (bool), impact_summary (string 160 chars), affected_services (array), subscribe_enabled (bool).
- If these fields are missing in current KB schema, Marcus needs to add them or provide a mapping.

## Open questions for Alex / Product
1. Should "Subscribe" create accountless email subscription (prompt for email) or require login? Tradeoffs: speed vs. correct user mapping.
2. Is ETA field always provided for P0? If not, show "ETA pending".

---

## Next steps & owners
- Design: this doc (you are reading it).
- Frontend: implement components, confirm API contract with Marcus, add tracking events for subscribe and mitigation clicks.
- Backend: Marcus to confirm availability of metadata fields.
- QA: Dana to run acceptance checklist after implementation and update results.

Decision log:
- Chose numbered step cards (vs continuous text) because they improve scanability and make copy-per-step feasible.

