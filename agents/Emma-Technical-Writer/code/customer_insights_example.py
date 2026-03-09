"""Python sample for CustomerInsights API

Quickstart: run 'python customer_insights_example.py' after installing requests
"""
import os
import requests

API_URL = os.environ.get('CI_API_URL', 'https://api.example.com/v1/insights/query')
API_KEY = os.environ.get('CI_API_KEY', 'testkey')

payload = {
    "query": "churn_rate",
    "time_range": {"from": "2025-01-01", "to": "2025-02-01"},
    "filters": {"segment": "enterprise"},
    "format": "summary",
    "limit": 10
}

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

resp = requests.post(API_URL, json=payload, headers=headers)
print('Status:', resp.status_code)
print('Response:', resp.json())
