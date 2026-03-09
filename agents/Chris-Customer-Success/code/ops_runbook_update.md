# Ops Runbook Update (Draft - placeholders to be filled by Noah)

## 목적
- 배포/롤백 절차, 모니터링 및 알람 기준, 사전 체크리스트 문서화

## 배포 전 체크리스트 (to be completed)
- Migration required: <yes/no>
- Environment variables to set: <list>
- Secrets changes: <list>
- Required permissions: <accounts/tokens>

## 배포 명령 예시
- Deploy command:
```
<deploy command example>
```
- Rollback command:
```
<rollback command example>
```

## 모니터링 & 알람 기준
- Health check endpoints: <list>
- Key metrics to watch: <e.g., 5xx rate, latency p95>
- Alert thresholds: <e.g., 5xx rate > 1% for 5 minutes>

## 복구 시나리오
- Step 1: <verify>
- Step 2: <rollback if...>
- Contact list: <oncall team>

파일 위치: output/code/ops_runbook_update.md
