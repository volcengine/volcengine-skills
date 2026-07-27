# 公网与私网连通查询

用于公网访问 ECS/服务不通、ECS 无法访问公网、同 VPC/跨 VPC 不通、跨地域慢、丢包、抖动等问题。

## 前置输入

- 源端和目的端：IP/域名、实例/Pod/CLB/EIP ID。
- 协议、端口、访问方向、公网/私网。
- Region、VPC、Subnet、发生时间、是否偶发。

## 证据梯度

1. 先定位源端和目的端资源。
2. 再检查安全策略：安全组、网络 ACL。
3. 再检查路径：路由表、EIP、NAT、CLB、CEN/TR/VPN/专线。
4. 最后看质量：网络智能中心诊断、流量指标。

## 命令包

### 1. 资源定位

```text
ve ecs DescribeInstances --Region "<region>" --InstanceIds.1 "<instance-id>"
ve vpc DescribeNetworkInterfaces --Region "<region>" --InstanceId "<instance-id>"
ve vpc DescribeVpcs --Region "<region>" --VpcId "<vpc-id>"
ve vpc DescribeSubnets --Region "<region>" --SubnetIds.1 "<subnet-id>"
```

如果问题入口是 ECS 实例 ID，且需要连带判断安全组、子网和路由表，优先调用 `scripts/collect_ecs_network_context.py` 生成聚合 JSON，再按输出里的 `summary` 和 `findings` 下结论。

### 2. 公网入站

```text
ve vpc DescribeEipAddresses --Region "<region>"
ve clb DescribeLoadBalancers --Region "<region>"
ve clb DescribeListeners --Region "<region>" --LoadBalancerId "<lb-id>"
ve clb DescribeListenerHealth --Region "<region>" --ListenerId "<listener-id>"
ve clb DescribeServerGroups --Region "<region>"
ve clb DescribeServerGroupAttributes --Region "<region>" --ServerGroupId "<server-group-id>"
```

如果入口是 CLB/ALB，且问题涉及监听器、健康检查、后端服务器组、后端 ECS 状态联动，优先使用 `scripts/collect_clb_backend_context.py`。

示例：

```text
python3 "${SKILL_ROOT}/references/domain-guides/compute-container-network/scripts/collect_clb_backend_context.py" \
  --region "<region>" \
  --type "<clb|alb>" \
  --load-balancer-id "<lb-id>" \
  --listener-id "<listener-id>"
```

使用脚本后，先看 `summary.listener_count`、`summary.server_group_ids`、`summary.backend_instance_ids` 和 `findings`，再进入 `raw.listener_health`、`raw.server_group_attributes`、`raw.backend_ecs` 定位证据。

关注字段：

- 入口是 EIP 直连还是 CLB/NLB/ALB。
- 监听器协议/端口是否匹配。
- 后端健康检查是否失败，失败后端对应哪个 ECS/端口。

### 3. 出公网

```text
ve vpc DescribeRouteTableList --Region "<region>" --VpcId "<vpc-id>"
ve vpc DescribeRouteEntryList --Region "<region>" --RouteTableId "<route-table-id>"
ve natgateway DescribeNatGateways --Region "<region>"
ve natgateway DescribeSnatEntries --Region "<region>" --NatGatewayId "<nat-gateway-id>"
ve vpc DescribeBandwidthPackages --Region "<region>"
```

关注字段：

- 子网默认路由是否指向 NAT 或网关。
- SNAT 是否覆盖源子网/源网段。
- NAT/EIP/带宽包状态是否正常。

### 4. 网络质量与路径诊断

```text
ve na DescribeDiagnosisInstances --Region "<region>"
ve na DescribeDiagnosisInstanceDetail --Region "<region>" --DiagnosisInstanceId "<diagnosis-id>"
ve na GetAnalysisPathReport --Region "<region>" --DiagnosisInstanceId "<diagnosis-id>"
ve na GetNetworkTrafficMetrics --Region "<region>"
ve na GetNetworkTrafficTopN --Region "<region>"
```

关注字段：

- 是否存在路径不可达、路由黑洞、ACL/安全组拦截。
- 哪段链路延迟或丢包异常。
- 流量是否打满带宽或存在异常突增。

## 判断模板

| 现象 | 常见根因 |
|---|---|
| 公网访问 timeout | EIP/CLB 未绑定、SG/ACL 拦截、后端未监听、路由缺失 |
| 出公网失败 | 无默认路由、SNAT 未覆盖、NAT/EIP 状态异常、DNS 问题 |
| 私网不通 | 双向安全组/ACL/路由缺失、源目的 VPC 不一致 |
| 跨地域慢 | CEN/TR/VPN/专线带宽或质量问题，进入网关类 ref |
