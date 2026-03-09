# Runbook: Apply & Validate Anthropic Worker Mappings

Purpose
Provide step-by-step instructions for operators to apply Anthropic worker mappings and validate them in staging/production.

Prerequisites
- Access to deployment environment (staging or production) with necessary permissions
- API key with mapping write permissions
- CLI or HTTP client (curl, httpie, Postman)
- Access to monitoring dashboards for worker health

Steps: Apply Mapping
1. Prepare payload
   - Use the canonical payload provided in the API docs. Example (placeholder):
     {
       "environment": "staging",
       "mappings": [{"worker_id":"anthropic-001","model":"claude-2","capacity":0.5}]
     }
2. POST mapping to API
   - curl -X POST "https://api.example.com/api/v1/workers/anthropic/mapping" -H "Authorization: Bearer $API_KEY" -H "Content-Type: application/json" -d @payload.json
3. Confirm 200 OK response and review `updated` count
4. Verify worker routing in staging by sending test requests that should be routed to the Anthropic worker

Validation Steps
- Ensure requests are being routed correctly (check logs/traces)
- Check worker health and capacity metrics in monitoring
- Run QA test cases (see QA section below)

Rollback
- If mapping causes errors or degraded performance, revert to previous mapping by reapplying the last-known-good payload.
- Example: POST previous_payload.json

QA Test Cases (for Dana)
1. Create mapping and confirm GET shows the new mapping
2. Send 10 test requests and confirm at least 1 is routed to the designated worker
3. Validate error cases: malformed payload -> 400, unauthorized -> 401

Notes
- Fill in canonical payload shapes after backend confirms field names.
- Coordinate with Marcus for any permission requirements.

