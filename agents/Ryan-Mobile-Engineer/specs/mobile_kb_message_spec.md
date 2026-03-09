# Mobile KB Message — 구현 스펙 (Ryan, Mobile)

요약
- 위치: output/specs/mobile_kb_message_spec.md
- 목적: 디자인 문서(output/design/kb_message_ui_spec.md)에 따라 모바일(React Native)에서 KB 메시지(배너/모달) 구현을 위한 엔지니어링·QA·백엔드 요구사항 정리

상황 → 복잡성 → 해결
- 상황: Support에서 P0 KB 2건 긴급 게시. 모바일 앱에서 배너/모달 형태로 즉시 노출하고, 사용자가 dismiss한 상태를 영속화해야 함.
- 복잡성: 사용자별/디바이스별 dismiss 영속성, 메시지 버전/메타데이터 노출, 오프라인/네트워크 지연, 롤백(비상 중단) 요구, 푸시/실시간 동기화 필요성.
- 해결: 모바일 구현 스펙과 API 요구사항 정의, 로컬 캐시/큐잉 전략, 롤백 및 운영 절차 제안 포함.

Acceptance criteria (수용 기준)
1. KB 메시지(배너/모달)가 디자인 스펙과 유사하게 보이고 동작한다.
2. 사용자가 dismiss한 메시지는 지정된 scope(서버에서 정의된 정책: per-user or per-device)로 영속화되어 다시 노출되지 않는다.
3. 메시지 버전(version) 변경 시 새로운 메시지가 즉시(앱 재시작 없이) 노출된다.
4. 오프라인 상황에서도 마지막 fetch된 메시지를 보여주고, dismiss는 로컬에 큐잉되어 네트워크 복구 시 서버에 전송된다.
5. 긴급 롤백(서버에서 deactivate flag) 시 30초 이내 모바일에서 UI 제거(푸시 또는 폴링 정책에 따라).

컴포넌트 설계 (output/code/components/KbMessage.tsx 참고)
- 주요 컴포넌트
  - KbMessageProvider: 컨텍스트로 메시지 fetch·캐시·동기화 로직 제공
  - KbBanner: 상단 배너 형태 (dismiss 버튼, CTA 가능)
  - KbModal: 전체 화면/중앙 모달(심각도에 따라 사용)
  - useKbMessage hook: 로직 접근 (messages, dismiss(), isLoading, error)

- props / API (요약)
  - fetchFn?: (opts) => Promise<Message[]>  // 백엔드 제공 fetch 함수(테스트/플랫폼 의존 분리)
  - displayMode: 'banner' | 'modal' | 'auto'
  - onCtaPress?: (message) => void
  - styles?: Partial<...>

로컬 영속화 전략
- 저장소: AsyncStorage (stable)로 dismissed list 및 lastFetched messages 저장
- key 구조
  - kb:last_fetched -> { messages: [...], fetched_at: ISO }
  - kb:dismissed:{userId?}:{deviceId?} -> [{ message_id, version, dismissed_at }]
- 동기화
  - dismiss 시 로컬에 즉시 저장 후 네트워크가 가능하면 POST /kb_messages/:id/dismiss 호출
  - 네트워크 불가 시 로컬 큐에 enqueue, 백그라운드 리트라이(앱 포그라운드 시 우선 전송)

오프라인 행동
- 앱 시작 시 로컬 캐시(최대 TTL: 24h, 서버에서 override 가능) 표시
- 온라인 시 서버에서 최신 메시지 조회 및 UI 갱신

롤백(urgent deactivate)
- 서버에서 메시지에 `active: false` 또는 `deactivated_at` 필드를 제공
- 모바일은 푸시 알림(FCM/APNs) 또는 폴링(예: 30초, P0 전용 구간)으로 변동을 감지
- 우선 순위: 푸시(권장) > Websocket/Real-time > 폴링(비용)
- 기대 SLA: 푸시 수신 시 즉시 UI 제거(사용자에게 노출 중이면 즉시 dismiss event 발생)

권장 백엔드 API 계약 (예시 JSON 포함)
1) GET /api/v1/kb_messages?platform=mobile&since={iso}
- 응답: { messages: [ { id, title, body, type: banner|modal, severity, version, active, start_at, end_at, metadata:{cta_url, dismiss_scope:'user'|'device'}, created_at, updated_at } ], server_time }

2) POST /api/v1/kb_messages/:id/dismiss
- 바디: { user_id?, device_id?, version }
- 응답: 200 OK

3) Optional: POST /api/v1/kb_messages/:id/impression (analytics)

샘플 메시지 JSON
{
  "id": "kb_2026_0001",
  "title": "서비스 점검 안내",
  "body": "오늘 23:00~23:30 점검이 예정되어 있습니다.",
  "type": "banner",
  "severity": "info",
  "version": 2,
  "active": true,
  "start_at": "2026-03-09T12:00:00Z",
  "end_at": "2026-03-10T00:00:00Z",
  "metadata": { "cta_url": "app://maintenance", "dismiss_scope": "user" },
  "created_at": "2026-03-09T11:50:00Z"
}

권장 모바일 제약/권고
- 메시지 body 길이 제한(권장 300 chars). 긴 내용은 modal에서 링크로 원문 제공
- 이미지/미디어: payload에 URL만 전달, 클라이언트에서 지연 로드
- 모달 트리거: 모달은 앱의 핵심 흐름(결제, 온보딩) 중복 방지. 백엔드에서 `allowed_routes` 필드 제공 권장

접근성
- VoiceOver/ TalkBack 텍스트 제공
- 충분한 색 대비, 버튼 크기 권장

Analytics 이벤트
- impression, cta_click, dismiss (with reason), fetch_error

QA 체크리스트 (Dana용)
- 배너 및 모달 노출: 디자인과 일치
- dismiss persistence: 로그인/로그아웃/디바이스 변경 시 동작 확인
- 네트워크 시나리오: 온라인, 오프라인, 복구(queued dismiss 전송)
- 롤백 시나리오: 서버에서 active=false 반영 시 UI 즉시 제거
- 버전 업그레이드: version 증가 시 새로운 메시지 노출

운영 가이드(긴급시)
- 운영자가 메시지 비활성화 시 Mobile 팀에 ETA/확인 필요 없음: 서버에서 deactivate를 바로 반영하면 모바일에서 자동 제거됨(푸시 권장)
- 모니터링: 푸시 실패 및 폴링 지연 알림 채널 설정 권장

결정 사항(현재 선택)
- 로컬 저장: AsyncStorage (추후 필요시 MMKV로 마이그레이션 가능)
- 영속 스코프: 서버가 dismiss_scope를 지정하지 않으면 기본 'user'로 처리
- 업데이트 방식: 푸시 우선, 폴링(30s) 보조

참고 파일
- 디자인 스펙: output/design/kb_message_ui_spec.md

작업 완료 — 모바일 스펙 문서 생성됨. 다음 단계: 백엔드 API 확정 및 ETA 회신 필요.
