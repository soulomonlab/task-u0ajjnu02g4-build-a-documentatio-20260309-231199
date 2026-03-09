Release Notes — Draft

Release: Next (unreleased)

Overview
This release includes updates to the API that add fields and optional parameters for resource creation and patching. These changes are backward-compatible except where noted.

Notable changes
- Added `enable_foo` boolean to POST /api/v1/xyz. Default: false if omitted.
- Changed `bar` field to an enum with values [TYPE_A, TYPE_B]. Older string values will continue to be accepted but will be coerced where possible.
- Added optional `threshold` parameter to PATCH /api/v1/abc.

Migration notes
- No forced migration is required. Consumers should update client code to include/handle the new fields where applicable.
- If you rely on the previous string values for `bar`, update to use enum values to avoid future compatibility warnings.

Deprecations
- None in this release.

Known issues
- Backend will confirm whether `enable_foo` defaults to false. If otherwise, the release notes will be updated.

Prepared by: Emma (Technical Writer)
