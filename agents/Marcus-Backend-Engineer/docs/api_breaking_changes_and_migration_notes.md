Breaking changes and migration notes (backend review by Marcus)

Summary:
- No breaking changes introduced in this OpenAPI update. Changes are additive: new examples, clarified parameters, idempotency header documented.

Decisions made:
- Pagination params default set to page=1, size=20. These defaults are enforced in the service layer.
- Idempotency-Key header added to POST /api/v1/items. Not required but recommended. Backend will accept and store idempotency keys for up to 24 hours.
- Security: BearerAuth retained; token expiry: access 15min, refresh 7d (see auth.md)

Migration notes:
- Clients using list endpoint unaffected; if they relied on implicit default page size different from 20, they must pass size explicitly.
- No database migrations required.

Action items for Docs PR:
- Include example showing Idempotency-Key usage and explain behavior on duplicate requests.
- Document pagination defaults and max page size (max 200).
- Reference auth token lifetimes and refresh flow.

If any of the above decisions need to change, comment here and I will update the OpenAPI/specs accordingly.
