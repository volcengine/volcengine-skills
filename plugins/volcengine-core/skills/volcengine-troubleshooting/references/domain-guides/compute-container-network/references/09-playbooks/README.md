# 高频 Playbook

本文件给 Agent 快速套用，不替代细分 reference。执行时仍然只做查询；涉及变更时必须确认。

## ECS SSH 连接超时

1. 读 [`03-login-os-access/README.md`](../03-login-os-access/README.md)。
2. 查实例：`ve ecs DescribeInstances`。
3. 查 EIP/网卡/安全组：`ve vpc DescribeEipAddresses`、`DescribeNetworkInterfaces`、`DescribeSecurityGroupAttributes`。
4. 查路由和 ACL：`DescribeRouteEntryList`、`DescribeNetworkAclAttributes`。
5. 查控制台输出：`ve ecs GetConsoleOutput`。

## CLB/ALB 后端不健康

1. 先确认入口类型是 `clb` 还是 `alb`。
2. 只有在拿到负载均衡类型和 ID 后再运行脚本；最小调用签名：
   `scripts/collect_clb_backend_context.py --region <region> --type <clb|alb> --load-balancer-id <lb-id>`。
3. 先看 `findings` 和 `summary.backend_instance_ids`。
4. 如果后端 ECS 存在，再转 `03-login-os-access` 或 `04-public-private-connectivity` 检查实例、安全组和路由。

## VKE Pod / Service / Ingress 异常

1. 先确认 Cluster ID、Namespace、Pod/Service/Ingress 名称。
2. 用 `scripts/collect_vke_pod_context.py` 聚合 VKE 控制面。
3. 向用户索取 Pod 事件、日志和 Service/Endpoint/Ingress 的脱敏摘要。
4. 如果 Ingress 后端不健康，再联动 `collect_clb_backend_context.py`。
6. 输出结论：入口 IP 是否正确、安全策略是否允许、实例系统是否正常。

## 公网访问 ECS 服务不通

1. 读 [`04-public-private-connectivity/README.md`](../04-public-private-connectivity/README.md) 和 [`05-security-policy-port/README.md`](../05-security-policy-port/README.md)。
2. 判断入口是 EIP 直连还是 CLB。
3. EIP 直连：查 EIP、实例网卡、安全组、ACL、路由。
4. CLB 入口：查 LB、Listener、ServerGroup、ListenerHealth、后端 ECS 安全组。
5. 如果健康检查失败，优先定位后端端口、服务监听、后端安全组。

## ECS 无法访问公网

1. 读 [`04-public-private-connectivity/README.md`](../04-public-private-connectivity/README.md) 和 [`06-eip-nat-route-gateway/README.md`](../06-eip-nat-route-gateway/README.md)。
2. 查实例子网和路由表。
3. 查 NAT 网关、SNAT 条目、EIP/带宽包。
4. 如果出口 IP 不符合预期，检查 SNAT 覆盖范围和 EIP 绑定。

## 安全组放通后仍不通

1. 读 [`05-security-policy-port/README.md`](../05-security-policy-port/README.md)。
2. 检查实例是否多网卡、多安全组。
3. 同时检查入方向和出方向。
4. 检查网络 ACL 是否对子网额外拦截。
5. 如果走 CLB，检查后端健康和 CLB 到后端的安全组规则。

## VKE Pod CrashLoop

1. 读 [`07-vke-container-runtime/README.md`](../07-vke-container-runtime/README.md)。
2. 向用户索取 Pod 事件、退出码、探针结果。
3. 向用户索取上一次崩溃日志摘要。
4. 查节点状态、资源压力、VKE 节点池和插件。
5. 若涉及镜像，查镜像仓库 tag、endpoint 和 Secret。

## 容器镜像拉取失败

1. 读 [`07-vke-container-runtime/README.md`](../07-vke-container-runtime/README.md)。
2. 查 Pod 事件中的 registry、repo、tag、错误类型。
3. 查 CR registry/namespace/repository/tag。
4. 查节点是否能访问公网或 VPC endpoint。
5. 判断是 tag 不存在、鉴权失败、网络不通，还是仓库 endpoint 配置问题。
