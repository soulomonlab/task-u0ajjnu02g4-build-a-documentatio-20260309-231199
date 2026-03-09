# Mobile KB Test Cases — Task #173

Purpose
- Specific, actionable test cases QA (Dana) should execute on mobile for the two published P0 KBs.

Test Environment
- Devices: iPhone 12 (iOS 16), Pixel 5 (Android 13) — if not available, equivalent.
- App build: latest staging with KB sync enabled.
- Network: Wi-Fi and Airplane mode tests.
- Tools: adb, Xcode device logs, Flipper (optional), screen recorder.

Test Case Template
- KB ID:
- KB Title:
- Device/OS:
- Test steps:
- Expected result:
- Actual result:
- Pass/Fail:
- Evidence (path to screenshots/video/logs):
- Notes:

Test Cases
1) Render test
   - Steps: Open KB list, open article.
   - Expect: Correct rendering of title, body, images, no HTML artifacts.

2) Deep link test
   - Steps: Trigger deep link on device.
   - Expect: App opens the KB article.

3) Offline cache test
   - Steps: Open article, enable airplane mode, reopen article.
   - Expect: Article content still accessible if caching required; else graceful error.

4) Search visibility test
   - Steps: Search for a unique term in the KB.
   - Expect: Article appears and clicking opens it.

5) Notification open test (if notifications approved)
   - Steps: Send test push with kb_id and deep_link.
   - Expect: Tapping notification opens the KB article and analytics event fires.

6) Accessibility test
   - Steps: Enable VoiceOver/TalkBack and navigate to the article.
   - Expect: Screen reader reads title and body; images labelled.

7) Performance test
   - Steps: Open list and scroll; open article.
   - Expect: No jank, acceptable open times.

8) Analytics test
   - Steps: Perform views and clicks.
   - Expect: kb_view and kb_click events recorded with kb_id.

Reporting
- Use the provided Test Case Template per KB and upload artifacts to the shared QA folder.

