# CLB Service Notes

## Zone and EIP Behavior

`DescribeZones` returns master/slave zone pairs, not a flat zone list. Do not feed the raw structure into single-zone fields without choosing the intended master/slave relationship.

For private CLB tests, leave `EipBillingConfig.*` unset. The create API exposes EIP billing fields, so copying a public example can accidentally allocate a public endpoint.

The delete API supports force deletion:

```bash
ve clb DeleteLoadBalancer --LoadBalancerId <clb-id> --ForceDelete true
```

Observed in `cn-beijing`: CLBs, listeners, server groups, and certificates returned empty lists. No lifecycle test was run because CLB is billable and may allocate dependent resources.
