# 排查总入口

本文件对应上层手册第 1 章“排查总入口”。它把用户现象转换为排障证据集合。执行时先选一个最贴近的场景，再到 `../query-cli-catalog.md` 取对应查询 reference。

## 通用输入

优先向用户索取或从上下文提取：

- 地域、账号/项目、时间范围、资源 ID、RequestId。
- 源 IP、目的 IP/域名、协议、端口、访问方向。
- ECS 实例 ID、ENI ID、VPC/Subnet ID、安全组 ID、EIP、NAT 网关、CLB/监听器、VKE 集群/节点/Pod。
- 错误现象：超时、拒绝连接、403/5xx、健康检查失败、Pending、CrashLoop、OOMKilled、镜像拉取失败、AccessDenied。

## 场景到证据

| 场景 | 必查证据 | 常用产品 |
|---|---|---|
| SSH/RDP 登录失败 | ECS 状态、控制台输出/截图、EIP、网卡、安全组入方向、子网路由、系统事件 | 云服务器、私有网络、公网 IP |
| 实例启动/重启异常 | 实例状态、任务、系统事件、镜像、云助手状态、控制台输出 | 云服务器/GPU 云服务器 |
| 公网入站不通 | EIP/公网 IP 绑定、CLB 监听器、后端健康、安全组、ACL、路由、实例监听端口 | 公网 IP、负载均衡、私有网络、云服务器 |
| 出公网失败 | 实例网卡、子网路由、NAT 网关、SNAT、EIP/带宽包、IPv6 网关 | 云服务器、私有网络、NAT 网关、IPv6 网关 |
| 私网互通失败 | 双端 ENI、子网、VPC、路由表、安全组、网络 ACL | 私有网络、云服务器 |
| 跨 VPC / 跨地域不通 | CEN/TR/VPN/专线附件、路由、带宽包、对端网关、双向安全策略 | 云企业网、中转路由器、VPN、专线连接 |
| VKE 节点异常 | 集群、节点池、节点、伸缩事件、节点 ECS 状态、Pod 事件 | 容器服务、云服务器、弹性伸缩 |
| Pod CrashLoop/OOM/Pending | 用户提供的 Pod 日志/事件、节点资源、镜像仓库、Service/Endpoint | 容器服务控制面、镜像仓库 |
| 镜像拉取失败 | Registry、Namespace、Repository、Tag、认证 token、VPC endpoint、节点网络 | 镜像仓库、VKE、VPC |
| CLB 后端异常 | LoadBalancer、Listener、ServerGroup、Backend、HealthCheck、安全组 | 负载均衡、云服务器、私有网络 |
| 弹性伸缩失败 | ScalingGroup、Policy、Activity、Instance、生命周期钩子、配额/库存 | 弹性伸缩、云服务器、计费/配额横向手册 |
| 网络质量问题 | 网络智能中心诊断、路径报告、流量指标、CEN/TR/VPN/专线状态 | 网络智能中心、私有网络、云企业网、中转路由器 |

## 横向问题转交

- `AccessDenied`、`NoPermission`、角色扮演、STS、资源级授权：转平台账号与权限手册。
- 欠费、冻结、配额不足、库存不足、购买/续费失败：转计费手册。
- `SignatureDoesNotMatch`、Action/Version、参数格式、Python SDK/CLI 安装和命令语法：转 OpenAPI / SDK / CLI 手册。
