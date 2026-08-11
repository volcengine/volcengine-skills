# VPC Service Notes

## Creation Has Short Consistency Windows

`CreateVpc` can return before the VPC accepts child resources. In a `cn-beijing` ECS+EIP smoke test, creating a subnet immediately after `CreateVpc` failed once with:

```text
InvalidVpc.InvalidStatus: The specified VPC is not in the correct status for the request.
```

Poll `DescribeVpcs --VpcIds.1 "$vpc_id"` until `.Result.Vpcs[0].Status == "Available"` before creating subnets or security groups. Similarly, `CreateSecurityGroup` can return before ingress rules are accepted; wait until `DescribeSecurityGroups --SecurityGroupIds.1 "$sg_id"` returns the group before `AuthorizeSecurityGroupIngress`, or retry `InvalidSecurityGroup.InvalidStatus`.

## Security Group Name Filter Is Indexed

`DescribeSecurityGroups` does not accept `--SecurityGroupName`. Passing it is ignored by the CLI because it is not in help output, so the command returns an unfiltered page and cannot prove cleanup.

Use `--SecurityGroupNames.1` instead:

```bash
ve vpc DescribeSecurityGroups --SecurityGroupNames.1 "cli-skill-test-sg"
```

After deleting a test security group, confirm cleanup with the same indexed filter and require `TotalCount: 0`.

## Security Group Operations Are Async

`CreateSecurityGroup`, `AuthorizeSecurityGroupIngress`, `RevokeSecurityGroupIngress`, and `DeleteSecurityGroup` return `AsyncTaskId`.

`AuthorizeSecurityGroupIngress` uses flat parameters such as `--PortStart`, `--PortEnd`, `--Protocol`, and `--CidrIp`; do not use `--SourceCidrIp` or `Permissions.*` for this CLI command.

For small test resources the next operation usually succeeds immediately, but cleanup verification should still query after delete. The default egress `all` rule is created automatically and does not need to be revoked before deleting the test security group.

Verified lifecycle: created a disposable security group, added/revoked one ingress rule, deleted it, and verified the indexed name filter returned no match.

## EIP Safety

`DescribeEipAddresses` returned existing EIPs attached to NAT gateways in `cn-beijing`. Treat them as user resources; never release or disassociate an EIP unless it was created by the current test run.
