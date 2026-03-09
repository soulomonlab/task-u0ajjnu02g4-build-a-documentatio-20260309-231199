Mobile staging QA run report

Summary
- Test file created: output/tests/test_mobile_staging_checklist.py
- Attempted to run pytest in the sandbox; test run failed because pytest is not installed in the environment.

Actual run output (command executed):
- Command: python -m pytest tests/test_mobile_staging_checklist.py -q (working_dir=output)
- Result: FAILURE to run pytest
- stderr:
  Could not find platform independent libraries <prefix>
  C:\Python313\python.exe: No module named pytest

What I did
- Implemented an automated pytest checklist for mobile-impact verification against the staging backend.
- Tests cover: auth token flow, profile field compatibility, lists pagination, file uploads, notifications list. (Offline flows marked manual.)
- Saved tests at: output/tests/test_mobile_staging_checklist.py

Next actions required (blocking for automated run)
1) #ai-devops: Install pytest (and requests) in the CI/test runner or provide a test environment with pytest available. Minimum packages: pytest>=7.0, requests
   - Recommended: add a simple venv or Docker image used by QA runner with these packages.
2) Provide STAGING_BASE_URL environment variable and optional QA credentials in a secrets store or ephemeral environment variables:
   - STAGING_BASE_URL (e.g. https://staging.example.com)
   - QA_TEST_USER (optional, default used in tests: test_user@example.com)
   - QA_TEST_PASS (optional, default: password123)
3) Once pytest is available, run:
   export STAGING_BASE_URL="https://staging.example.com" && pytest output/tests/test_mobile_staging_checklist.py -q
   (On Windows use setx or set environment accordingly.)

Manual checklist (if automated run cannot be executed immediately)
- Auth: login endpoint returns access_token; token grants access to /api/v1/profile/me. Validate token expiry and refresh if applicable.
- Profile: fetch /api/v1/profile/me; ensure core fields id/email/display_name present. New fields must not cause 5xx.
- Lists: GET /api/v1/lists?limit=10&offset=0 returns items array; pagination meta numeric if present; empty-state handled.
- Uploads: POST small file to /api/v1/uploads (auth required). Expect 200/201 and returned resource URL or id.
- Notifications: GET /api/v1/notifications?limit=10 returns notifications array; missing optional fields should not cause errors.
- Offline flows: perform device/emulator tests for cached data, sync when back online, and conflict resolution flows (manual).

Acceptance criteria for automated run
- pytest completes with exit code 0
- No failing tests
- If failures are found, each failure should be filed as a bug with reproduction steps and device metadata (see bug template recommendation below)

Bug filing recommendation (if regressions found)
- Title: short summary
- Severity: P1 (if crash/data loss/auth broken), P2 (major flow broken), P3 (minor)
- Steps to reproduce: include exact API calls, parameters, sample responses
- Environment: STAGING_BASE_URL, timestamp, headers, auth token if applicable
- Device metadata: OS, app version, emulator vs physical, network type

Files created
- output/tests/test_mobile_staging_checklist.py
- output/reports/mobile_staging_run_report.md (this file)

작업 상태
- Automated run blocked by missing pytest in environment. Manual checklist documented above.
