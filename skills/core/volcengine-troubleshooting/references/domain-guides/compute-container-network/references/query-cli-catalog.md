# 查询 CLI 入口索引

本文件是渐进式披露入口，不再承载完整接口罗列。Agent 先根据用户现象选择一个细分 reference，再在该 reference 中按“命令包 + 结果解读”执行。

命令来源：

- 产品接口元数据：`cli-meta/火山引擎云服务器、容器与网络连通问题排查手册/<产品>/接口清单.md`
- 官方原始文档：`产品官方文档/火山引擎云服务器容器与网络连通问题排查手册/<产品>/...`
- 公共 CLI 源码：`cli/volcengine-cli`
- 公共 Python SDK 源码：`python-sdk/volcengine-python-sdk`

约定：`cli-meta` 中历史命令形态是 `volcengine <service> <Action>`，本 skill 执行设计统一写成 `ve <service> <Action>`。

## 路由表

| 用户问题 | 必读 reference | 主要查询产品 |
|---|---|---|
| 无法判断是实例、容器、网络、安全组、路由、登录还是横向问题 | [`01-overview-routing/README.md`](01-overview-routing/README.md) | 总入口 |
| ECS 创建、启动、停止、重启、实例状态异常、系统事件、控制台输出 | [`02-ecs-lifecycle-state/README.md`](02-ecs-lifecycle-state/README.md) | 云服务器/GPU 云服务器、弹性伸缩 |
| SSH/RDP/VNC 登录失败、系统无法进入、sshd 异常 | [`03-login-os-access/README.md`](03-login-os-access/README.md) | 云服务器、VPC、公网 IP、安全组 |
| 公网入站不通、ECS 出公网失败、私网互通失败、跨地域慢/丢包 | [`04-public-private-connectivity/README.md`](04-public-private-connectivity/README.md) | ECS、VPC、EIP、CLB、网络智能中心 |
| 安全组、网络 ACL、端口放通后仍不通 | [`05-security-policy-port/README.md`](05-security-policy-port/README.md) | 私有网络、安全组、网络 ACL、网卡 |
| EIP、NAT、路由、IPv6、VPN、CEN、TR、专线、私网连接 | [`06-eip-nat-route-gateway/README.md`](06-eip-nat-route-gateway/README.md) | 公网 IP、NAT、路由、VPN、CEN、TR、专线 |
| VKE、Pod、节点、Service/Ingress、镜像拉取、CrashLoop/OOM/Pending | [`07-vke-container-runtime/README.md`](07-vke-container-runtime/README.md) | 容器服务控制面、镜像仓库、ECS |
| 镜像、cloud-init、用户数据、云助手、初始化失败 | [`08-image-init-cloudassistant/README.md`](08-image-init-cloudassistant/README.md) | 云服务器、镜像、云助手 |
| 高频问题需要直接套用流程 | [`09-playbooks/README.md`](09-playbooks/README.md) | 组合查询 |

## 全局执行守则

- 只执行 `Describe/List/Get/Query/Check/Search` 等查询动作。
- 如果用户要求修复，先完成只读证据收集，再列出变更动作、资源、影响面，等待用户确认。
- 如果命令参数不确定，先运行对应 `ve <service> <Action> --help` 或查 `cli-meta`，不要猜字段。
- 如果一个场景需要跨多个服务查询，先执行 CLI 命令包；当需要分页聚合、拓扑拼接或批量比对时，再参考 [`python-sdk-script-patterns.md`](python-sdk-script-patterns.md) 设计只读脚本。
