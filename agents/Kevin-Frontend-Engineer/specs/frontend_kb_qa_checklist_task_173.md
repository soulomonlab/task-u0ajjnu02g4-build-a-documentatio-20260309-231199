Frontend KB QA Checklist — Task #173

Purpose
- Frontend-focused acceptance checklist to support the product review of the two published P0 Knowledge Base (KB) articles referenced by Task #173.
- Designed to be run by QA (Dana) after Alex completes content review. Complements: output/specs/product_review_acceptance_checklist.md and output/specs/product_review_response_task_173.md

How to use
- Run each section against both published KB pages.
- For each check, mark: PASS / FAIL / N/A. For FAIL, include: short description, reproduction steps, severity (P0/P1/P2), and screenshot(s).
- Attach automated accessibility report (axe or Lighthouse a11y) and browser/device list.

Acceptance criteria (overall)
- All PASS or P1/P2 items accompanied by low-effort fixes scheduled. No open P0 frontend issues.
- Accessibility: no critical (axe violation level: critical) issues.
- Responsiveness: layout not broken on common breakpoints (mobile/tablet/desktop).
- Performance: First Contentful Paint (FCP) within acceptable range (<2.5s on fast 3G emulation) — note: approximate; not blocking unless content blocks render.

Checklist
1) Page metadata & canonical
   - Title tag matches KB title and is unique. (PASS/FAIL)
   - Meta description present and reflects summary. (PASS/FAIL)
   - Canonical tag present and correct if duplicated content exists.

2) Header / breadcrumbs / navigation
   - Page breadcrumb exists and links to correct parents.
   - Primary nav highlights KB section when viewing a KB.
   - Back / close button behavior works on mobile (doesn't navigate off unexpectedly).

3) Content structure & formatting
   - Headings use semantic H1..H3 order, no skipped levels.
   - Paragraph spacing and line-height match design tokens.
   - Code blocks preserve whitespace and have copy-to-clipboard where applicable.
   - Images render with alt text; large images use responsive sizes.

4) Links & anchors
   - Internal links open in same tab; external links open in new tab with rel="noopener noreferrer".
   - Anchor links jump to correct sections and update URL hash.
   - No 404 links.

5) Table of contents (if present)
   - TOC reflects visible headings and highlights active section on scroll.

6) Search & indexing elements
   - Search snippet/preview shows title, short excerpt, and correct tags if used.
   - Schema.org / structured data present for article where required.

7) Actions & buttons
   - CTA buttons (e.g., "Contact Support", "Give Feedback") are visible, have aria-labels, and keyboard-focusable.

8) Error & empty states
   - If content fails to load (network error), user sees friendly error with retry.
   - If article has no attachments/tags, empty state is sensible.

9) Accessibility (a11y)
   - Keyboard navigation: can tab through headings, links, and interactive controls.
   - Focus visible for all interactive elements.
   - Color contrast meets AA (4.5:1 for normal text).
   - ARIA attributes used correctly; no duplicate IDs.
   - Run automated axe or Lighthouse a11y and attach report.

10) Responsive & cross-browser
   - Test at breakpoints: 375x667 (mobile), 768x1024 (tablet), 1366x768 (desktop).
   - No horizontal scroll on mobile.
   - Visual parity in latest Chrome, Firefox, Safari (macOS), and an Android device (Chrome).

11) Performance & bundle impact (smoke)
   - Page JS size doesn't spike unexpectedly (compare with baseline).
   - Observe network waterfall for large images or third-party scripts.

12) Localization & formatting (if applicable)
   - Dates/times and number formats match locale settings.
   - No untranslated UI strings.

Reporting format (required)
- For each KB URL, provide:
  - Checklist table with PASS/FAIL/N/A for each item.
  - Screenshot set (mobile + desktop) with annotated failures.
  - Axe/Lighthouse a11y JSON export.
  - Short summary: overall verdict (Approve / Request edits), top 3 issues, recommended severity/prio.

Deliverable
- Create report: output/reports/kb_frontend_qa_task_173_dana.md (QA to produce)

Notes & assumptions
- This checklist focuses on frontend/UX/accessibility. Content accuracy remains with Alex's product review.
- If a P0 issue is found (layout break, missing critical CTA, or critical accessibility violation), block publication and escalate to #ai-frontend and #ai-backend.

Contact
- Kevin (Frontend) for clarifications on UI behavior or repro steps.
