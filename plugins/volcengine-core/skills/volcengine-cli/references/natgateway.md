# NAT Gateway Service Notes

## Existing NAT Resources Must Be Treated as User-Owned

`DescribeNatGateways` returned existing account resources in `cn-beijing`, including EIP-backed SNAT configuration. Do not delete or modify them unless they were created by the current test run.

Observed:

- NAT gateway available zones included `cn-beijing-a` through `cn-beijing-d`.
- `DescribeSnatEntries` returned existing SNAT entries.
- `DescribeDnatEntries` returned `TotalCount: 0`.

## EIP-Dependent Paths Are Separate

Public NAT SNAT/DNAT flows usually require EIP allocation or association. If EIP allocation is out of scope, validate only read/discovery behavior or use an explicitly approved test-owned EIP.
