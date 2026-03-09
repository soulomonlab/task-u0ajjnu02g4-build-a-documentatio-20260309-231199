상황
- Emma가 PR 문서상의 모호함 해결을 위해 API 예시 및 변경 요약을 생성했습니다 (output/docs/api_examples_update.md, output/docs/docs_pr_changes_summary.md).

문제/요청
- 머지 전 엔지니어 확인이 필요합니다. 확인해야 할 4가지 핵심 질문:
  1) widget.size 타입: 숫자(int) vs 문자열(enum). (권장: enum으로 제한하면 프론트/밸리데이션이 쉬움)
  2) metadata 스키마: 자유형 JSON vs 명시적 키셋(예: {created_by, tags, source}). (권장: 필수/선택 키 정의 후 확장 가능한 additionalProperties 허용)
  3) status enum 및 soft-delete 동작: 단순 enum + deleted 플래그 vs soft-delete 상태값 포함. (권장: status enum에 DELETED 포함 + deleted_at timestamp — 쿼리 편의성과 일관성 고려)
  4) WIDGETS_CACHE_TTL 환경변수: 기본값, 단위(초/분), 런타임 변경 허용 여부. (권장: 기본 300초, 초 단위, 런타임 변경 가능)

참고
- 상세 요청/예시: output/docs/api_examples_update.md (Emma가 작성)
- 문서 업데이트 이후: output/docs/api_reference.md, output/docs/runbook_ops.md에 반영 예정

요청사항(액션 아이템)
- Alex: 위 4가지 질문에 대해 Marcus와 함께 기술적 확인을 부탁드립니다. 각 항목별로
  - 최종 결정(간단 문장)
  - 이유(한 줄)
  - 마이그레이션/부작용(있다면 한 줄)
  형식으로 회신해 주세요.
- 회신 방법: 이 파일(output/reports/engineer_confirmation_request.md) 상단에 'Confirmed by Alex: YYYY-MM-DD' 형식으로 기록하거나, 직접 슬랙으로 회신해주셔도 됩니다.

다음 단계
- 엔지니어 확인 완료되면 Emma가 docs를 최종 수정하고 PR을 생성합니다.

파일 작성자: Chris (Customer Success)
