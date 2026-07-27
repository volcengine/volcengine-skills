# Redis Service Notes

## Swagger/Explorer Gaps

`scripts/fetch_swagger.py --service redis --action <Action>` can fail with OpenAPI Explorer HTTP 500 for Redis actions including allow-list and instance lifecycle APIs. Fall back to `ve redis <Action> --help` for the JSON body schema.

## Allow-List Cleanup Ordering

Calling `DeleteAllowList` immediately after `DeleteDBInstance` can fail with `AllowListBindInstanceCannotDelete` because the instance has not been fully removed. Wait until `DescribeDBInstanceDetail` returns not found, then delete the allow list.

`DescribeAllowLists` requires `RegionId` and has no useful name filter in CLI help. Passing `AllowListName` can still return an unfiltered list, so it cannot prove cleanup.

Correct cleanup proof: query the deleted allow-list ID directly and expect `AllowListNotExist`.

```bash
ve redis DescribeAllowListDetail --body '{"AllowListId":"acl-xxx"}'
```

Observed lifecycle note: creating an allow list with `AllowListType` set to `IPv4` returned detail output with `AllowListType` shown as `DualStack`; do not use that field alone as an echo check.

## Parameter Groups Need Pagination

`DescribeParameterGroups` requires `RegionId`, `PageNumber`, and `PageSize`. Calling it with only `RegionId` fails with:

```text
Missing Params: PageNumber,PageSize
```

Observed in `cn-beijing`: the paginated call returned system default parameter groups for Redis 4.0, 5.0, 6.0, and 7.0.

## Minimal Instance Parameters That Were Easy to Get Wrong

For the disposable Redis instance lifecycle test, the following details mattered:

- `NoAuthMode` uses `close`, not `disabled`.
- `ConfigureNodes` must include the subnet AZ, for example `{"AZ":"cn-beijing-b"}`.
- Deletion protection must be disabled for disposable tests.
- Poll `DescribeDBInstanceDetail` through `Deleting` until the detail API returns not found; only then clean dependent allow lists.

Verified lifecycle: created a minimal postpaid Redis 6.0 instance with one 512 MB shard, deleted it, confirmed `DescribeDBInstances` had no test instance, then deleted the associated allow list and verified `AllowListNotExist`.

## Shell Cleanup Trap

With `set -o pipefail`, password snippets like `tr -dc ... | head -c 14` can exit with code 141 because `head` closes the pipe. If used inside a cleanup-protected resource test, this can abort after prerequisites are created.

Use a generator that does not rely on an early-closing pipe, or temporarily disable `pipefail` around password generation. Do not print Redis passwords in logs.
