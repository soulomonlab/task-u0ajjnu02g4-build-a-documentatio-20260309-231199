# KB: Pagination Migration Guide

Summary
- Purpose: Guide customers through the pagination changes introduced in the PR, including API response format changes, migration steps, and code samples.
- Audience: API consumers, SDK maintainers, frontend engineers, and support agents.

What changed
- The API now uses cursor-based pagination instead of page-number based pagination for the following endpoints:
  - GET /v1/items
  - GET /v1/search
- Responses now include a `next_cursor` field and remove `page` and `total_pages` in paginated endpoints.

Why this matters to customers
- Existing clients using page numbers will receive unexpected results or may ignore new fields, causing incomplete data retrieval.
- SDKs and frontend components need updates to store and pass the cursor between requests.

Response example

{
  "data": [ ... ],
  "next_cursor": "eyJ0b2tlbiI6ICJ...",
  "has_more": true
}

Migration steps
1. Identify affected endpoints and clients
   - Search logs for usage of page= or page_number parameters.
2. Update SDKs or client code
   - Replace page number param with next_cursor handling:
     - First request: omit cursor
     - Subsequent requests: include ?cursor=<next_cursor>
3. Update UI components
   - For infinite scroll: fetch using next_cursor, append results.
   - For paged UI: implement next/previous logic using cursors. Store last-cursor stack for previous.
4. Testing
   - Verify full dataset retrieved by iterating until has_more is false.
   - Confirm edge cases: empty results, rapid cursor expiry.

Code samples
- JS (fetch):
  async function fetchAll() {
    let cursor = null;
    const results = [];
    while (true) {
      const url = '/v1/items' + (cursor ? `?cursor=${cursor}` : '');
      const res = await fetch(url);
      const json = await res.json();
      results.push(...json.data);
      if (!json.has_more) break;
      cursor = json.next_cursor;
    }
    return results;
  }

Edge cases & notes
- Cursor expiry: Cursors may expire after X minutes (document actual TTL). If expired, clients should restart from the beginning or surface an error.
- Sorting & consistency: Ensure clients specify stable sort fields to avoid missing items between pagination requests.

Support & Troubleshooting
- For migration assistance, collect:
  - API key/client id (do NOT share secrets)
  - Example failing requests and responses
  - SDK versions in use

Acceptance criteria for KB
- Clear migration steps, code samples, and testing checklist.
- Published to customer-facing KB and referenced from API docs.

Contact
- Support: support@example.com
- For complex migrations, request a migration support ticket with usage patterns and expected data volumes.
