# 公网访问与源站连通

用于源站不可达、备案或合规限制、安全策略拦截、公网链路慢，以及需要判断“入口正常但后端不通”的场景。

## 前置输入

- 域名、URL、源站 IP/域名、端口、协议。
- 是否经过 CDN/CLB/ALB/WAF。
- 直连源站与经入口访问的差异。
- 备案主体、地域、访问来源。

## 只读证据

先从入口产品反查源站：

```text
ve cdn DescribeCdnConfig --body '{"Domain":"<domain>"}'
ve clb DescribeListenerHealth --ListenerId <listener-id> --OnlyUnHealthy true --PageNumber 1 --PageSize 20
ve alb DescribeListenerHealth --ListenerIds.N <listener-id> --OnlyUnHealthy true
```

本地补证据：

```text
ve cdn ListCdnDomains --body '{"PageNum":1,"PageSize":10}'
ve clb DescribeLoadBalancers
ve alb DescribeLoadBalancers
```

## 结果解读

| 证据 | 常见结论 |
|---|---|
| CDN 配置源站不可达 | 源站网络或源站服务问题 |
| 直连源站成功，经 CDN 失败 | CDN 回源 Host/协议/缓存/访问控制问题 |
| 经 CLB/ALB 不通，后端直连成功 | 监听、规则、健康检查或 LB 到后端路径问题 |
| 备案/合规限制提示 | 备案或地域合规问题，需要人工确认 |
| WAF/DDoS/防火墙拦截 | 转安全/KMS/加密服务 skill |

## 横向跳转

源站端口、安全组、路由、NAT、EIP、实例状态交给计算容器网络 skill；WAF/DDoS/云防火墙交给安全/KMS/加密服务 skill。
