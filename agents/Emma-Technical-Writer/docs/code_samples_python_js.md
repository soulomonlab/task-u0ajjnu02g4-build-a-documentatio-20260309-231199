Code Samples — Python and JavaScript (Draft)

Overview
This file contains runnable minimal examples for the updated endpoints. These are drafts — backend must confirm exact parameter names and auth model.

Python example (requests)

```python
import requests
API_URL = "https://api.example.com/api/v1/xyz"
API_KEY = "REPLACE_WITH_KEY"

payload = {
    "name": "example",
    "enable_foo": True,
    "bar": "TYPE_A"
}

resp = requests.post(API_URL, json=payload, headers={"Authorization": f"Bearer {API_KEY}"})
print(resp.status_code)
print(resp.json())
```

JavaScript example (node-fetch)

```javascript
const fetch = require('node-fetch');
const API_URL = 'https://api.example.com/api/v1/xyz';
const API_KEY = 'REPLACE_WITH_KEY';

const payload = {
  name: 'example',
  enable_foo: true,
  bar: 'TYPE_A'
};

fetch(API_URL, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${API_KEY}`
  },
  body: JSON.stringify(payload)
})
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);
```

Notes
- Replace API_KEY and endpoint with environment-specific values.
- Confirm SDK-specific guidance if there is a maintained SDK for Python/JS.

Prepared by: Emma (Technical Writer)
