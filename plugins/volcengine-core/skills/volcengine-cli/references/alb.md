# ALB Service Notes

## Flat Parameter Mode

ALB create APIs use flat CLI parameters, not JSON body mode. Nested arrays use indexed dot notation such as `--ZoneMappings.1.ZoneId`.

For private ALB smoke tests, keep all EIP/public address fields unset unless public exposure is explicitly under test:

```bash
ve alb CreateLoadBalancer \
  --RegionId cn-beijing \
  --LoadBalancerName cli-skill-test-alb \
  --Type private \
  --VpcId vpc-xxxx \
  --SubnetId subnet-xxxx \
  --ZoneMappings.1.ZoneId cn-beijing-b \
  --ZoneMappings.1.SubnetId subnet-xxxx \
  --LoadBalancerBillingType 1 \
  --LoadBalancerEdition Basic \
  --Tags.1.Key publish-by \
  --Tags.1.Value deploy-skill
```

Observed in `cn-beijing`: a private Basic ALB created with `publish-by=deploy-skill` appeared in `DescribeLoadBalancers` with the tag attached, then `DeleteLoadBalancer` removed it. ALB creation is billable and depends on real VPC/subnet choices, so keep lifecycle tests short and delete the test load balancer after validation.
