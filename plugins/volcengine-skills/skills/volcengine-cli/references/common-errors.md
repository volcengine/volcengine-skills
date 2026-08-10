# Common Error Handling

Use this reference when a Volcengine response includes `ResponseMetadata.Error`, especially for account state, real-name verification, purchase limits, service activation, or permission-looking errors.

## Real-Name Verification

Check the account verification state before assuming a request-format bug:

```bash
python3 scripts/call_extend_api.py --api GetVerifyInfo
```

Treat the account as not real-name verified when the derived summary contains:

```text
verification.is_verified: false
```

The console authentication page is:

```text
https://console.volcengine.com/user/authentication/detail/
```

Do not write real account IDs, request IDs, TRNs, personal names, certificate numbers, phone numbers, or resource IDs into shared troubleshooting notes.

## Error Classification

| Error code | Classification | Confirmed contexts | Handling |
| --- | --- | --- | --- |
| `AccountNotVerified` | Explicit real-name verification blocker | Organization `CreateOrganization` | Ask the user to complete console authentication, then retry. |
| `ErrNotVerifiedAccount` | Explicit real-name verification blocker | PrivateZone `ListPrivateZones` | Ask the user to complete console authentication, then retry. |
| `OperationDenied.InvalidAccount` with message containing `Account not verified yet or may not exist` | Explicit real-name verification blocker | CR `ListRegistries`, `GetPublicEndpoint`, `GetVpcEndpoint`, `ListNamespaces`, `ListRepositories`, `ListTags`, `CreateRegistry` | Check `GetVerifyInfo`; if unverified, ask the user to authenticate before retrying. |
| `Forbidden.PurchaseLimited` | Account purchase qualification or risk-control blocker | VPC `AllocateEipAddress` | Do not classify as real-name verification without `GetVerifyInfo` or product documentation. Escalate as account purchase eligibility. |
| `AccountPrivilegeInsufficient` | Account privilege blocker | RDS MySQL `CreateDBInstance` | Do not classify as real-name verification without another source. Check product/account permissions. |
| `AccountNoPermission` | Product permission blocker | Extension APIs `StartCloudServer`, `StopCloudServer`, `RebootCloudServer` | Do not classify as real-name verification without another source. Check product permission or entitlement. |
| `ProductUnsubscribed`, `ServiceNotActivated`, `KMS_ServiceNotOpen`, `OperationDenied.ServiceStopped` | Service not enabled or stopped | Multiple service activation checks | Treat as service activation/account service state, not as request-format bugs. |

## Remote Login Process Exited

The following helper error means the `ve login --remote` process is no longer running:

```text
ERROR: no running ve login subprocess.
Call './scripts/ve_login_remote.sh start-wait <region>' first (default) and keep that invocation running; use './scripts/ve_login_remote.sh start <region>' only if the runtime is known to preserve background descendants.
```

Older helper versions may mention only `start` or `start-wait`. In every case, the error means that the PKCE-owning login process is no longer alive.

This commonly happens in managed command runners that terminate background descendants when the launching command returns. The authorization URL and code are bound to the terminated PKCE process and cannot be reused.

Recovery:

1. Run `scripts/ve_login_remote.sh abort` to remove stale state.
2. Start a new flow with `scripts/ve_login_remote.sh start-wait <region> [profile]` as a long-running tool call. Keep its process session active; do not detach it with shell `&`. If unsure which subcommand to use, use `start-wait`.
3. Only if the runtime is explicitly known to preserve background descendants after the launching tool call returns, you may instead use `scripts/ve_login_remote.sh start <region> [profile]` via a normal (foreground) tool call.
4. Pass the new authorization code verbatim to `scripts/ve_login_remote.sh complete <code> [profile]` in a separate invocation.
5. If `start-wait` was used, drain its tool session after `complete` returns.

If the runtime cannot keep a long-running tool session active and is not explicitly known to preserve background descendants, do not guess — fall back to another authentication method (AK/SK, STS token, or SSO).

Do not retry `complete` with a code generated from an exited login process.
