# 安全组、网络 ACL 与端口查询

用于“安全组放通后仍不通”“端口不通”“某个源 IP 被拒绝”“换安全组后访问异常”“多网卡/多安全组规则不一致”等问题。

## 前置输入

- 源 IP/CIDR、目的 IP、协议、端口、方向。
- ECS/ENI ID、VPC/Subnet ID、安全组 ID。
- 最近是否改过安全组、ACL、路由、实例网卡。

## 命令包

### 1. 实例到网卡到安全组

```text
ve ecs DescribeInstances --Region "<region>" --InstanceIds.1 "<instance-id>"
ve vpc DescribeNetworkInterfaces --Region "<region>" --InstanceId "<instance-id>"
ve vpc DescribeSecurityGroups --Region "<region>" --VpcId "<vpc-id>"
ve vpc DescribeSecurityGroupAttributes --Region "<region>" --SecurityGroupId "<sg-id>"
```

Agent 使用方式：

1. 从实例结果拿 `NetworkInterfaces` 和 `SecurityGroupIds`。
2. 对每个安全组查 attributes。
3. 同时检查入方向和出方向，不能只看入方向。
4. 规则匹配要同时满足协议、端口、源/目的 CIDR。

### 2. 网络 ACL

```text
ve vpc DescribeSubnets --Region "<region>" --SubnetIds.1 "<subnet-id>"
ve vpc DescribeNetworkAcls --Region "<region>" --VpcId "<vpc-id>"
ve vpc DescribeNetworkAclAttributes --Region "<region>" --NetworkAclId "<acl-id>"
```

Agent 使用方式：

- 先确认子网是否关联网络 ACL。
- 检查入方向和出方向是否存在拒绝规则。
- ACL 是子网级策略，可能解释“同安全组其他实例正常，但这个子网不通”。

### 3. 端口与后端健康

```text
ve clb DescribeListeners --Region "<region>" --LoadBalancerId "<lb-id>"
ve clb DescribeListenerHealth --Region "<region>" --ListenerId "<listener-id>"
ve clb DescribeServerGroupAttributes --Region "<region>" --ServerGroupId "<server-group-id>"
```

用于判断：

- CLB 监听端口与后端端口是否一致。
- 健康检查端口/路径是否配置错误。
- 后端实例安全组是否允许 CLB 访问。

## 结果解读

| 证据 | 结论 |
|---|---|
| 入方向无规则 | 外部到实例被安全组拦截 |
| 出方向无回包规则 | TCP 建连可能表现为 timeout |
| ACL 有拒绝规则 | 即使安全组允许，子网级 ACL 仍会拦截 |
| CLB 健康检查失败 | 继续检查后端端口、服务监听和后端安全组 |

## 变更边界

本 ref 只做查询。新增/删除安全组规则、更新 ACL、调整 CLB 后端都属于写操作，必须先让用户确认具体资源、协议、端口、CIDR 和影响面。
