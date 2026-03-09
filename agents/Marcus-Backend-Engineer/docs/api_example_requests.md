API Example Requests

Base URL: https://api.example.com
Auth: Bearer <access_token>

1) List items
GET /api/v1/items?page=1&size=20
Headers:
  Authorization: Bearer <token>
Response: 200
{
  "items": [
    {
      "id": "11111111-1111-1111-1111-111111111111",
      "title": "Sample item",
      "description": "A sample item",
      "created_at": "2026-01-01T12:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 20
}

2) Create item
POST /api/v1/items
Headers:
  Authorization: Bearer <token>
  Idempotency-Key: <uuid>
Body:
{
  "title": "New item",
  "description": "Details"
}
Response: 201
{
  "id": "22222222-2222-2222-2222-222222222222",
  "title": "New item",
  "description": "Details",
  "created_at": "2026-02-02T10:00:00Z"
}

3) Get item
GET /api/v1/items/22222222-2222-2222-2222-222222222222
Headers:
  Authorization: Bearer <token>
Response: 200
{
  "id": "22222222-2222-2222-2222-222222222222",
  "title": "New item",
  "description": "Details",
  "created_at": "2026-02-02T10:00:00Z"
}
