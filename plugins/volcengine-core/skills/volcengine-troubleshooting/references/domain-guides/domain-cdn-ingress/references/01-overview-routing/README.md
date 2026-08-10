# 排查总入口

用于快速判断入口链路异常落在哪一段：DNS、证书、CDN、负载均衡、源站或公网合规。

## 前置输入

- 域名、完整 URL、状态码、错误文本。
- 发生时间、客户端地域/运营商、是否所有用户都异常。
- 是否经过 CDN/DCDN/GA、CLB/ALB、WAF。
- 源站地址、回源 Host、端口、协议。

## 先判断方向

| 现象 | 优先路径 |
|---|---|
| 域名解析不到或解析到旧地址 | DNS / CNAME / TTL |
| 浏览器提示证书错误 | 证书中心 + CDN/CLB/ALB 证书绑定 |
| CDN 403/404/5xx | CDN 域名状态 -> CDN 配置 -> 边缘/源站指标 |
| 刷新预热失败 | 任务状态、URL 范围、配额、权限 |
| CLB/ALB 健康检查失败 | LB -> Listener -> ServerGroup -> Backend |
| 直连源站失败 | 后端 ECS/VPC/安全组/路由，转计算网络 skill |
| WAF/DDoS/云防火墙拦截 | 转安全/KMS/防护 skill |

## 入口证据

先用产品只读 CLI 确认入口资源是否存在，再判断是否需要本地网络工具：

```text
ve cdn ListCdnDomains --body '{"PageNum":1,"PageSize":10,"Domain":"<domain>"}'
ve dns ListZones --body '{"PageNumber":1,"PageSize":10,"Key":"<domain>"}'
ve clb DescribeLoadBalancers --PageNumber 1 --PageSize 10
ve alb DescribeLoadBalancers --PageNumber 1 --PageSize 10
```

本地工具只用于补证据，不替代云上配置查询：

```text
ve dns ListZones
ve dns ListRecords
ve cdn ListCdnDomains --body '{"PageNum":1,"PageSize":10}'
```

## 横向跳转

- `AccessDenied`：账号权限 skill。
- 刷新预热配额、服务冻结、欠费：计费 skill。
- 源站网络、安全组、路由、NAT：计算容器网络 skill。
- WAF/DDoS/云防火墙：安全/KMS/加密服务 skill。
