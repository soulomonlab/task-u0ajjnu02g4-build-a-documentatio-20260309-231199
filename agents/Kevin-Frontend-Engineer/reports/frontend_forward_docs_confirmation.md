요약
- 목적: Alex/Chris가 생성한 docs_values_confirmation.md 내용을 Marcus(백엔드)에게 공식 확인 요청 및 회신 촉구하기 위함.

참고 문서
- output/reports/docs_values_confirmation.md (기존 PR 초안/요약)

요청 사항 (확인/회신 필요)
1) Rate limit: 기본값 60 req/min 수락 여부
   - 이 값이 per-client(사용자 기준)인지 per-key(API 키/계정 기준)인지 명시해주세요.
   - 제안 변경이 있다면 대체값 + 간단 근거(인프라/SLO 영향)를 남겨주세요.

2) Retry 정책: 초기 500ms, 지수 백오프, 최대 3회 수락 여부
   - 이 정책을 모든 5xx(500~599) 에 적용하나요, 특정 코드(예: 502, 503, 504)만 적용하나요?
   - 재시도 시 idempotency 고려사항(특정 엔드포인트는 재시도 불가 등)이 있다면 알려주세요.

3) SDK 호환성: >=1.2.0 <2.0.0 수락 여부
   - 마이너/메이저 호환성 우려가 있으면 간단히 기술해주세요.

우선순위: P1 — 가능한 오늘 중 회신 부탁드립니다. 회신 내용은 Chris/Emma가 docs PR 최종 병합 시 사용할 예정입니다.

컨텍스트/제약
- 제품(Chris/Alex)은 기본값을 Feature OFF, rate limit 60 req/min, retry(초기 500ms, max 3회, exponential) 및 SDK >=1.2.0 <2.0.0으로 제안해두었습니다.
- 엔지니어링(Marcus) 확인 필요: 인프라/SLO 영향, per-client vs per-key 결정, 어떤 5xx에 재시도 적용할지 등.

회신 형식(권장)
- 항목별: (확정/대체값) + (간단한 근거: infra/SLO/안전성)
- 예: 1) rate limit: "확정(60 req/min) — per-key. 이유: X. 영향: Y"  2) retry: "대체(초기 300ms, max 4회) — 적용 대상: 502,503,504" 3) SDK: "확정"

감사합니다.
