# KMS Service Notes

## DescribeKeys Requires a Keyring

`DescribeKeys` requires `KeyringName` or `KeyringID`; omitting both returns `MissingParameter`.

Observed in `cn-beijing`: `DescribeKeyrings` returned an existing keyring, `DescribeKeys` worked when scoped to that keyring, and `DescribeSecrets` returned `TotalCount: 0`.

## Deletion Is Scheduled

KMS keys and secrets are not immediate-delete resources. The current action list exposes `ScheduleKeyDeletion`, `CancelKeyDeletion`, `ScheduleSecretDeletion`, and `CancelSecretDeletion`.

Prefer read/help validation unless the test explicitly accepts scheduled deletion and follow-up cleanup tracking. Disposable tests should use a dedicated keyring name prefix.
