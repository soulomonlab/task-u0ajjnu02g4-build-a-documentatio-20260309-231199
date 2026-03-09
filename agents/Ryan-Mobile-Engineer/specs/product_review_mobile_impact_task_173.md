# Mobile Impact Review — Task #173

Purpose
- Surface mobile-specific acceptance criteria and test steps for the two published P0 knowledge base (KB) articles under Product Review Task #173.

Context
- Alex created: output/specs/product_review_response_task_173.md and asked QA to run the acceptance checklist.
- This document adds the mobile engineering perspective so QA validates mobile behavior (in-app KB, notifications, offline, deep links, accessibility).

Scope
- Validate the two published P0 KBs on iOS and Android in the app (React Native mobile client).
- Focus areas: rendering, deep links, offline availability, search, push notifications (if proactive notification is recommended), analytics, accessibility, performance.

Mobile Acceptance Checklist (Pass/Fail for each)
1) In-app rendering
   - KB title, summary, and body render correctly on iOS and Android (no truncated text, no HTML artifacts).
   - Images load and scale appropriately; tapping images opens viewer (if supported).
   - Code blocks, lists, headings maintain formatting.
   - Evidence: screenshots of full article on both platforms.

2) Deep links & navigation
   - KB deep link opens app to the article when app is installed (use app link / universal link and intent testing).
   - If app not installed, link falls back to web (confirm behavior if applicable).
   - Back navigation returns to previous screen without losing state.
   - Evidence: device logs or screenshot showing deep link success.

3) Search & discovery
   - Article appears in in-app search results (if search indexing is used) within one sync cycle.
   - Search snippet highlights query terms.
   - Evidence: screenshot of search results on both platforms.

4) Offline availability & caching
   - If KBs should be available offline: verify article is cached after viewing and accessible offline (airplane mode).
   - If not required, confirm graceful error message when offline.
   - Evidence: video or screenshot with device in airplane mode showing article availability or graceful error.

5) Proactive push notifications (if Alex recommends proactive customer notifications)
   - Verify notification payload fields required by mobile client: title, body, kb_id, deep_link, sent_at.
   - Confirm tapping notification opens the article in-app.
   - Confirm opt-in/opt-out respects user notification settings.
   - Evidence: captured notification on-device and navigation screenshots.

6) Performance
   - Article list and article open times meet budget: list render < 200ms on recent mid-tier devices; full article open < 500ms (network-dependent).
   - No jank during scroll (60fps target where device permits).
   - Evidence: profiling screenshots or summary (Flipper or Android Profiler traces optional).

7) Accessibility
   - Screen reader (VoiceOver/TalkBack) reads title and body; images have alt text or labelled.
   - Tap targets meet 44x44pt guideline.
   - Evidence: short screen-recording with VoiceOver/TalkBack or checklist items noted.

8) Analytics & attribution
   - Verify analytics events fire: kb_view, kb_search_result_click, kb_notification_open. Include kb_id and platform fields.
   - Evidence: analytics event payloads or console logs.

9) iOS / Android edge checks
   - iOS: Verify dynamic type scaling, Safe Area handling, no clipped UI.
   - Android: Verify back-button behavior and intent handling.
   - Evidence: screenshots demonstrating correct behavior.

Test Steps (concise)
1) On iOS and Android devices (physical preferred): open app, navigate to KB list, open article #1, take screenshots; repeat for article #2.
2) Test deep link: trigger deep link on device (adb intent / Notes link on iOS) and confirm navigation.
3) Toggle airplane mode and confirm offline behavior per checklist.
4) If push notifications are in-scope: send test notification containing kb_id and deep_link; confirm open behavior.
5) Run lightweight performance checks during scroll and open (record timings if possible).
6) Capture accessibility checks with VoiceOver/TalkBack.
7) Collect logs/screenshots/video and provide Pass/Fail per checklist item.

Dependencies (backend / product)
- Backend must provide KB API fields: kb_id, title, summary, body (sanitized HTML or markdown), images (URLs), last_updated, deep_link, notification_allowed flag.
- Notification service must be able to send a test payload containing deep_link and kb_id.
- Product decision: confirm whether KBs should be available offline (caching requirement).

Reporting format
- For each KB, supply a table: checklist item, pass/fail, evidence (attach file paths / links), notes.
- Provide a single-line recommendation whether proactive customer notification is appropriate for mobile users (Yes/No) with brief rationale.

Timeline
- QA run for mobile checks: 1-2 business days (can run in parallel with Alex's web review).

Contact
- Owner (mobile): Ryan (Mobile Engineer) — I can triage any mobile-specific failures or unblock backend fields.

