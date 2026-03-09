Title: Mobile action plan for backend PR changes

Summary
- Purpose: Translate Marcus's backend docs-impact report into concrete mobile implementation tasks and acceptance criteria.
- Location: output/reports/update_docs_from_pr_mobile_action_plan.md

Key Mobile Action Items (MECE)
1) API client & TypeScript models
   - Update client models to match new/changed fields (e.g., `avatar_url`, token fields, pagination tokens).
   - Add strict runtime validation for responses (zod/io-ts) with graceful fallback UI.
   - Acceptance: App compiles; unit tests for models pass; runtime validator logs any schema mismatch.

2) Auth & Token rotation
   - Implement secure refresh token flow using platform secure storage (SecureStore/Keychain/EncryptedSharedPrefs).
   - Centralize auth token handling in an auth hook/session manager. Ensure single-flight refresh (mutex) to prevent token race conditions.
   - On 401 from any request, trigger refresh + retry original request once. If refresh fails → force logout with clear UX.
   - Acceptance: Simulated token rotation tests show no double-refresh and app recovers automatically.

3) 409 Conflict handling & retry strategy
   - On 409 (conflict), apply idempotent retry logic with one immediate retry after refetching the resource. For unsafe ops, surface error with actionable UX.
   - Backoff strategy: linear single retry. Log conflicts to observability.
   - Acceptance: Concurrent update scenario causes retry and resolves without crash in 95% test runs.

4) Pagination validation & robustness
   - Use React Query's useInfiniteQuery for paginated lists. Validate `next_page` tokens and handle malformed/empty pages.
   - Add guardrails: limit page size, dedupe items client-side, detect inconsistent total counts and surface a soft-error state.
   - Acceptance: Scrolling lists handle malformed pagination without UI break; tests for out-of-order/deduped items.

5) Offline, caching & resilience
   - Persist query cache using react-query-persist-client + AsyncStorage for offline reads.
   - Show offline indicator; queue unsafe writes and replay when online, with conflict resolution UX for failed replays.
   - Acceptance: App shows cached content offline and replays queued actions on reconnect.

6) Env vars & observability
   - Ensure mobile config supports new env vars (runtime config via react-native-config or expo-constants). Document required keys.
   - Emit structured logs and errors to Sentry/Datadog. Add metric tags for token_refresh/failures and 409 events.
   - Acceptance: New env vars documented; Sentry events include token/409 metadata.

7) Tests & QA smoke scenarios (for Dana)
   - Device matrix: iOS 14+, iOS 16; Android 9+, Android 12.
   - Smoke tests: login, token refresh (force expired), concurrent update -> 409 handling, paginated list scroll + malformed page, offline read + queued write replay.
   - Automated: Unit tests for models, integration tests for auth flows (mock server), E2E scripts to cover smoke scenarios (Detox or Playwright for native).

Implementation notes & Decisions
- State mgmt: React Query for server state + small Redux slice for session state. Justification: React Query provides built-in caching, retries, and persistence patterns.
- Token storage: SecureStore for Expo / Keychain+EncryptedSharedPrefs for bare RN — reversible decision.
- Retry policy: Single retry on 409 to avoid data duplication; adjustable via config.
- Runtime validation: Use zod. Logs on mismatch to help backend debugging.

Next steps (Mobile)
- I (Ryan) will implement model updates, auth/session manager, and 409 retry logic in mobile codebase. Estimated 3-5 dev days.
- After implementation, notify #ai-qa (Dana) to run device smoke tests and report failures.

Files to be created by mobile implementation (planned)
- output/code/mobile/auth/sessionManager.ts
- output/code/mobile/api/client.ts
- output/code/mobile/hooks/useAuth.ts
- output/code/mobile/screens/PaginatedListScreen.tsx
- tests/mobile/e2e/token_rotation.spec.ts

Contact/Questions
- If API contract changes further (field names, status codes), tag Marcus and I'll pause until clarified.

