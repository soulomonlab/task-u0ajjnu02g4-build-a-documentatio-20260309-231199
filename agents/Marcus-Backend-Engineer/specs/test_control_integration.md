# Test Control Integration Spec (Backend)

Purpose
- Provide staging-only hooks to allow QA to control and assert backend behaviors like forced status codes, rate-limit resets, and soft-canary routing.

Requirements
- Must be disabled in production. Controlled via env var: TEST_CONTROLS_ENABLED=1 in staging
- Minimal surface area: only headers (X-Test-Force-Status, X-Test-Reset-RateLimit, X-Soft-Canary, X-Test-Echo)
- Prefer Redis-backed state for rate-limit resets but allow in-memory fallback for quick staging deploys
- Middleware must not alter production logs or leak secrets

API
- Middleware reads headers and sets request.state attributes:
  - test_control_force_status (int or None)
  - test_control_reset_ratelimit (api_key or 'all' or None)
  - test_control_soft_canary (str or None)

Operational
- Staging team must set TEST_CONTROLS_ENABLED=1 on staging environment
- Provide QA with staging BASE_URL and test API keys
- Redis URL optional: REDIS_URL

Security
- Only enabled when TEST_CONTROLS_ENABLED=1
- Logging should redact API keys
- No persistence of production user data in test control store

Next steps
- #ai-qa (Dana) to collect staging BASE_URL and test API keys; include in QA plan
- #ai-devops (Noah) to enable TEST_CONTROLS_ENABLED in staging and provide REDIS_URL if needed
