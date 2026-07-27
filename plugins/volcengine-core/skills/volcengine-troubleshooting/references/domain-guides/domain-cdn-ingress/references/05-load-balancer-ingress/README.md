# 负载均衡与流量入口

用于 CLB/ALB 监听器、转发规则、后端服务器、健康检查、会话保持、WebSocket/长连接异常。

## 前置输入

- CLB/ALB 类型、Region、LoadBalancerId。
- ListenerId、ServerGroupId、Backend IP/Port。
- Host、Path、协议、端口、健康检查路径和状态码。

## CLB 命令包

```text
ve clb DescribeLoadBalancers --PageNumber 1 --PageSize 10
ve clb DescribeLoadBalancerAttributes --LoadBalancerId <clb-id>
ve clb DescribeListeners --LoadBalancerId <clb-id> --PageNumber 1 --PageSize 10
ve clb DescribeListenerAttributes --ListenerId <listener-id>
ve clb DescribeListenerHealth --ListenerId <listener-id> --OnlyUnHealthy true --PageNumber 1 --PageSize 20
ve clb DescribeServerGroups --LoadBalancerId <clb-id> --PageNumber 1 --PageSize 10
ve clb DescribeServerGroupAttributes --ServerGroupId <server-group-id>
ve clb DescribeRules --ListenerId <listener-id> --PageNumber 1 --PageSize 20
```

## ALB 命令包

```text
ve alb DescribeLoadBalancers --PageNumber 1 --PageSize 10
ve alb DescribeLoadBalancerAttributes --LoadBalancerId <alb-id>
ve alb DescribeListeners --LoadBalancerId <alb-id> --PageNumber 1 --PageSize 10
ve alb DescribeListenerAttributes --ListenerId <listener-id>
ve alb DescribeListenerHealth --ListenerIds.N <listener-id> --OnlyUnHealthy true
ve alb DescribeServerGroups --LoadBalancerId <alb-id> --PageNumber 1 --PageSize 10
ve alb DescribeServerGroupAttributes --ServerGroupId <server-group-id>
ve alb DescribeServerGroupBackendServers --ServerGroupId <server-group-id> --PageNumber 1 --PageSize 20
ve alb DescribeRules --ListenerId <listener-id> --PageNumber 1 --PageSize 20
```

## 关注字段

- LB 状态、公网/私网地址、VPC、可用区、计费或冻结状态。
- Listener 协议/端口、证书、默认转发、连接超时、会话保持。
- Rule 的 Host/Path 匹配顺序。
- ServerGroup 协议、端口、健康检查开关、路径、状态码。
- Backend 的 IP、端口、权重、健康状态。

## 结果解读

| 证据 | 常见结论 |
|---|---|
| Listener 不存在或端口不符 | 入口监听配置错误 |
| Host/Path 规则不匹配 | ALB/CLB 七层转发规则问题 |
| 只有某些 backend 不健康 | 后端实例/端口/应用/安全组问题 |
| 所有 backend 不健康 | 健康检查配置或源站网络问题 |
| 证书在 listener 上不匹配 | HTTPS 入口证书配置问题 |

## 横向跳转

后端 ECS 服务、端口监听、安全组、路由、NAT、VPC 问题转计算容器网络 skill；证书生命周期回到 `03-ssl-https-certificate`。

## 变更边界

监听、转发规则、后端、权重、健康检查和证书变更都必须确认。
