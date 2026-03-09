# Docs values — Confirmation for PR merge

작성자: Alex (Product Owner)
목적: Chris가 정리한 docs PR 병합 전, 기술 항목 B/C/D에 대해 엔지니어링 최종 확정(또는 대체안)을 받아 Emma가 문서 PR을 병합할 수 있도록 함.

요약
- Chris가 작성한 확인서(output/reports/confirmation_request_for_docs_PR.md)에 제안된 임시 기본값:
  1. Feature A: OFF (문서 상 기본값)
  2. Item B (rate limit): 60 req/min
  3. Item C (retry policy): retry on 5xx with exponential backoff starting 500ms, max 3 attempts
  4. Item D (SDK compatibility): SDK >=1.2.0 <2.0.0

결정 요청(확인 필요 항목)
- B (rate limit): 60 req/min 제안 수락 여부, 또는 운영·SLO 영향으로 다른 값 제안
- C (retry policy): 제안된 백오프(초기 500ms, max 3회)가 API/infra 관점에서 적절한지
- D (SDK range): SDK 호환성 범위(>=1.2.0 <2.0.0)가 실제 고객 사용 범위와 릴리즈 정책에 맞는지

간단한 근거(제안의 의도)
- 안전한 기본값 유지: Feature는 기본 OFF로 문서화하여 의도치 않은 활성화를 방지
- rate limit(60/min): 보수적 기본값으로 과부하 위험 최소화(추후 모니터링 후 상향)
- retry 정책: 5xx에 대해 짧은 지수 백오프와 최대 3회로 중복/트래픽 급증 방지
- SDK 호환성: 메이저 버전 미만(2.0.0 미만)으로 깨지는 변경 차단

Acceptance criteria (docs PR 병합 조건)
- [ ] Marcus 또는 엔지니어링 담당자가 B/C/D 각각에 대해 “확정” 응답 또는 대체값 + 이유를 제공
- [ ] 제공된 값이 운영/인프라 제한에 반하지 않음(예: rate limit이 infra quota 초과하지 않음)
- [ ] Emma가 문서 PR에 반영할 최종 텍스트를 받음

제안된 작업 흐름
1) Marcus: B/C/D 기술적 확정 또는 대체안 제시 (이슈 코멘트 또는 아래 슬랙 핸드오프에 응답)
2) Alex(제품): 엔지니어링 결정을 반영하여 docs PR 초안 생성(원하면 Chris가 초안 작성 가능)
3) Marcus: 기술적 사인오프
4) Emma: 최종 병합

일정
- 가능하면 오늘 업무일 내 회신 부탁드립니다(긴급도: P1).

파일 참조
- 원본 요약: output/reports/confirmation_request_for_docs_PR.md (Chris 작성)

추가 컨텍스트/질문
- rate limit 60 req/min은 per-client인가 per-key 인가? (Marcus 확인 필요)
- retry 대상은 모든 5xx인가, 특정 엔드포인트/상태코드만 해당인가?

--
Alex (Product Owner)
