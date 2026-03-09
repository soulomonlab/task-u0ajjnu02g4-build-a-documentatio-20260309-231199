Title: Frontend Implementation Plan for PR #113

Situation
- Emma created an implementation guide (output/docs/update_docs_from_pr.md) translating Marcus's backend PR impact into frontend/QA/Support tasks and assigned task #113 to frontend.

Objective
- Implement frontend changes required by PR #113. Blocked until backend endpoint names and response field names are confirmed by Marcus to avoid spec drift.

Deliverables (frontend)
1. New/updated components:
   - FeatureListPage (list + pagination)
   - FeatureItemCard
   - FeatureDetailModal (or page)
   - API client hooks: useFeatures, useFeature
2. Typescript types for API responses (auto-generated from confirmed shapes)
3. Integration smoke tests for Dana to run
4. Accessibility and loading/error states

Suggested TS interfaces (TO BE CONFIRMED BY MARCUS)
- interface Feature { id: string; title: string; description?: string; created_at: string; updated_at?: string; }
- interface FeaturesListResponse { total_count: number; items: Feature[]; page: number; per_page: number; }

Frontend implementation notes / decisions
- State: use React Query for fetching and caching (reversible: can swap to Zustand later if needed).
- Styling: Tailwind + existing design tokens (Maya to confirm visuals separately).
- Errors: show inline error banner with retry button for list fetch failures.
- Pagination: client-driven controls; backend should provide total_count (needed for page count calculation).

Acceptance criteria (frontend)
- Feature list loads and renders items for first page
- Pagination controls allow navigating pages and correctly request new pages
- Detail modal opens and shows selected feature fields
- Loading and error states present and keyboard accessible
- TypeScript types match actual API response (no any)

QA smoke/integration checklist (for Dana)
- Fetch first page: expect 200 and non-empty items
- Pagination: navigate to page 2, confirm request includes page param and UI updates
- Network error: simulate 500 on list endpoint → UI shows error banner and retry works
- Auth: if endpoint requires auth, verify unauthorized 401 behavior

Blocking questions for Marcus (need exact answers before frontend work)
1) Exact endpoint paths and HTTP methods:
   - List features: e.g., GET /api/v1/features  (CONFIRM)
   - Get feature: e.g., GET /api/v1/features/:id  (CONFIRM)
2) Response field names and types for list & detail responses — provide full example JSON for happy path
   - Confirm field names: total_count vs total, items vs data, created_at vs createdAt
3) Pagination params and format
   - Query params names: page & per_page? offset & limit? Cursor-based?
   - Does response include total_count or next_cursor?
4) Error response shape
   - Standard error format (e.g., { code: string, message: string, details?: any })
5) Auth requirements
   - Bearer token header name and expected status codes for invalid tokens
6) Rate limits / pagination limits (max per_page)
7) Any feature flags or rollout conditions we should be aware of

Required artifacts from Marcus
- Example JSON responses for list and detail (happy path + sample 4xx/5xx error response)
- Exact endpoint paths and param names
- Any field rename mappings if PR renames fields
- Expected response codes for edge cases (e.g., empty list, not found)

Next steps for frontend (upon Marcus confirmation)
1) Implement API client hooks and types (use axios / fetch wrapper)
2) Build FeatureListPage and FeatureDetailModal
3) Add unit tests + integration smoke tests
4) Notify #ai-qa (Dana) to run smoke tests and follow QA checklist

Files referenced
- input: output/docs/update_docs_from_pr.md (created by Emma)
- this spec: output/specs/frontend_task_113.md

Notes
- This is blocking work; frontend will not implement until Marcus confirms the API shapes to avoid rework.
- If Marcus prefers, provide a swagger/openapi snippet and frontend will generate types from it.
