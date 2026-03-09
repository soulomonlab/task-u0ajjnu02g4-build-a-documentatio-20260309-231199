import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// k6 load test for per-API-key rate limiting and burst behavior
// Usage (example):
// BASE_URL=https://staging.example.com API_KEYS=key-test-1,key-test-2 k6 run output/tests/qa_rate_limit_k6.js

export let options = {
  vus: 50,
  duration: '2m',
  thresholds: {
    'http_req_failed': ['rate<0.01'],
  },
};

const errors = new Rate('errors');

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';
const API_KEYS = (__ENV.API_KEYS || 'key-test-1').split(',');

export default function () {
  const apiKey = API_KEYS[Math.floor(Math.random() * API_KEYS.length)];
  const url = `${BASE_URL}/v1/resource`;
  const params = {
    headers: {
      'Authorization': `ApiKey ${apiKey}`,
      'Content-Type': 'application/json',
    },
    tags: { api_key: apiKey }
  };

  const res = http.get(url, params);

  const success = check(res, {
    'status is 200 or 429 or 503': (r) => [200, 429, 503].includes(r.status),
  });
  if (!success) errors.add(1);

  // quick pacing to generate bursts
  sleep(Math.random() * 0.5);
}
