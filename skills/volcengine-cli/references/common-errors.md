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
