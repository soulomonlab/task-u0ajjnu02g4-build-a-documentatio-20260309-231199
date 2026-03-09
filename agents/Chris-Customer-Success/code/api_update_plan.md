# API Update Plan (Draft - placeholders to be filled by Marcus)

## 목적
- 문서화: 변경되는 API 엔드포인트, 요청/응답 예시, 에러 코드, 마이그레이션 가이드

## 영향 범위 (예시)
- /v1/users (GET, POST)
- /v1/orders (POST)

## 엔드포인트 템플릿 (각 항목을 Marcus가 채워주세요)
- Endpoint: <e.g. /v1/example>
- Method: <GET|POST|PUT|DELETE>
- Description: <짧은 설명>
- Request example:
```
<JSON request example>
```
- Success response example:
```
<JSON success response example>
```
- Error responses:
  - HTTP status code: <e.g. 400>
  - Body example:
```
<JSON error response>
```
- Notes: <rate limits, deprecation notes, performance considerations>

## SDK 영향
- Affected SDKs: <list>
- Required SDK changes: <describe>

파일 위치: output/code/pr_stub_files/api_update_plan.md
