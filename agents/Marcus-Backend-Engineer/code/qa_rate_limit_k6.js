import http from 'k6/http';
import { check, sleep } from 'k6';
import { Counter } from 'k6/metrics';

// Test for per-API-key rate limiting and burst behavior
// Usage: BASE_URL=https://staging.example.com API_KEYS=key1,key2 k6 run output/tests/qa_rate_limit_k6.js

export let errorCount = new Counter('errors');

let BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';
let API_KEYS = (__ENV.API_KEYS || 'key-test-1').split(',');

export let options = {
    scenarios: {
        sustained: {
            executor: 'constant-arrival-rate',
            rate: 1, // per second per VU group; we'll scale by VUs
            timeUnit: '1s',
            duration: '60s',
            preAllocatedVUs: 50,
            maxVUs: 200,
        },
        burst: {
            executor: 'per-vu-iterations',
            vus: 20,
            iterations: 10,
            maxDuration: '30s',
        }
    },
    thresholds: {
        'http_req_duration{scenario:sustained}': ['p(95)<200'],
        'http_req_failed': ['rate<0.01'],
    }
};

function randomApiKey() {
    return API_KEYS[Math.floor(Math.random() * API_KEYS.length)];
}

export default function () {
    let key = randomApiKey();
    let headers = {
        'Authorization': `Bearer ${key}`,
        'Content-Type': 'application/json'
    };

    // sustained hit to a normal endpoint
    let res = http.get(`${BASE_URL}/api/v1/health`, { headers: headers });
    check(res, {
        'status is 200 or 429': (r) => r.status === 200 || r.status === 429
    }) || errorCount.add(1);

    // quick burst to exercise token-level burst tokens
    if (Math.random() < 0.2) {
        let burstRes = http.get(`${BASE_URL}/api/v1/health`, { headers: headers });
        check(burstRes, {
            'burst status 200 or 429': (r) => r.status === 200 || r.status === 429
        }) || errorCount.add(1);
    }

    sleep(0.1);
}
