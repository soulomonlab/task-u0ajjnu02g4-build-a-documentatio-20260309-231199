# PR 작성 옵션 및 액션 체크리스트 (for Emma & Chris)

## 목적
Emma 님의 docs_followup_pr.md 초안에 있는 placeholder를 확정하고 PR을 작성/완료하기 위한 구체적 액션 목록.

## 옵션 A — Emma 작성 (권장)
1. Emma가 GitHub에서 브랜치 생성 및 PR 초안 업로드: branch name 권장 `docs/docs-followup-<YYYYMMDD>-EM`.
2. PR 설명에 다음 태그 포함: @Marcus @Noah @Kevin (검토 요청)
3. 리뷰어에게 명확한 요청 사항 표기: `Please provide API examples (endpoint/method/request/response/error codes) and ops runbook commands by <date>`.
4. 마감 전 저는(Chris) PR 내 문구/사용자 관점 검토 수행.

## 옵션 B — Chris(제가) 작성
1. Emma가 PR 작성 권한 허용(혹은 제가 브랜치 생성 권한 확인).
2. 제가 아래 파일들 생성: `api_update_plan.md`, `ops_runbook_update.md`, `release_notes_draft.md` (초안)
3. Emma가 Marcus/Noah/Kevin를 리뷰어로 지정 또는 제가 지정 요청을 드림.
4. Backend/DevOps로부터 실 데이터가 오면 문서 업데이트 후 PR 최종 확정.

## 공통 체크리스트 (모두에게 필요)
- Backend(Marcus)에게 필요한 포맷 예시 제공 (요청/응답 JSON 예):
  - Endpoint: /v1/example
  - Method: POST
  - Request body example: { "user_id": "123" }
  - Success response example: { "status": "ok", "data": { ... } }
  - Error response example: 400 { "error": "invalid_input", "message": "..." }
- DevOps(Noah)에게 필요한 항목 설정:
  - 배포 커맨드, 롤백 커맨드, 모니터링 룰, 권한 필요사항
- Frontend(Kevin): 영향 범위와 breaking changes 여부

## 권한 & 일정
- PR 작성자: Emma or Chris(선택)
- 필수 리뷰어: Marcus, Noah, Kevin
- 권장 응답 기한: 3영업일

파일 위치: output/specs/support_action_options.md
