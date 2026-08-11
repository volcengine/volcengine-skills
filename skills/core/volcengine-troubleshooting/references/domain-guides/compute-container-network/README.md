# 火山引擎云服务器、容器与网络连通排障技能

这是面向火山引擎计算、容器与网络连通问题的 Agent skill。它对应上层手册 `火山引擎云服务器容器与网络连通问题排查手册`，覆盖 ECS、VKE、容器、VPC、安全组、EIP、NAT、路由、SSH/RDP、公网与私网连通等问题。它的职责不是罗列所有 OpenAPI，而是把用户现象路由到最小必要的查询证据，再基于证据给出排障判断。

## 上层信息

本技能继承的上层设计信息如下：

- 手册定位：面向“计算资源 + 网络路径”的排查场景，常见现象是实例访问失败、服务不通、容器异常、路由不通、端口不通、SSH 登录失败、公网/私网访问异常。
- 横向分工：权限、计费、OpenAPI/Python SDK/CLI 机制不在本 skill 深挖；本 skill 保留产品上下文并转交横向技能或手册。
- 工具优先级：优先使用 `ve` 查询 CLI；TOS 场景使用 `tosutil`；复杂多接口关联再设计 `volc-sdk-python` 或 `volcengine-python-sdk` 只读脚本。VKE Pod 日志、事件和应用侧状态由用户提供，不主动调用集群侧工具。
- 数据来源：产品手册、`火山引擎问题排查手册/README.md` 的产品/Python SDK/CLI 总表、`cli-meta/` 接口元数据、`产品官方文档/` 官方原始文档、`cli/` 和 `python-sdk/` 本地源码。
- 安全边界：默认只做查询；变更、重启、放通、绑定、解绑、扩缩容、删除等动作必须先进行 Human-in-the-Loop 确认。

## 先读这些

处理本领域问题前，先阅读当前目录下的参考文档：

- `references/query-cli-catalog.md`：查询型 CLI 入口索引，按问题域路由到细分 reference。
- `references/api-coverage-matrix.md`：本分类 `cli-meta/` API 覆盖审查矩阵，列出已纳入排障候选的只读/诊断 Action 与默认排除的写操作边界。
- `references/python-sdk-script-patterns.md`：什么时候从 CLI 切换到 Python SDK 脚本，以及只读脚本的安全边界。
- `references/01-overview-routing/README.md`：排查总入口，按用户现象收集证据，以及产品手册和横向手册如何分工。
- `scripts/README.md`：已有脚本的用途、最小必填参数和输出字段。**任何 `RunSkillScript` 调用前都必须先读它或对应 reference 中的完整脚本签名，不能凭脚本名猜参数。**

同时可查阅：

- 产品手册：`火山引擎问题排查手册/火山引擎云服务器容器与网络连通问题排查手册/README.md`
- 产品/Python SDK/CLI 总表：`火山引擎问题排查手册/README.md`
- 接口元数据：`cli-meta/火山引擎云服务器、容器与网络连通问题排查手册/<产品>/接口清单.md`
- 官方原始文档：`产品官方文档/火山引擎云服务器容器与网络连通问题排查手册/<产品>/...`

## 使用边界

Use this skill when the user describes:

- ECS/GPU ECS 创建、启动、状态异常、重启、系统事件、控制台输出、SSH/RDP/VNC 登录失败。
- 公网入站、公网出站、私网互通、跨 VPC、跨地域、VPN、CEN、TR、专线、私网连接、NAT、EIP、路由、安全组、网络 ACL、网卡相关问题。
- VKE 集群、节点池、节点、Pod、Service、Ingress、镜像拉取、CrashLoop、OOMKilled、Pending、集群插件相关问题。
- CLB/NLB/ALB、监听器、后端服务器、健康检查、会话/连接、真实客户端 IP、TLS 握手相关问题。
- 弹性伸缩、镜像仓库、函数服务、消息队列等和计算/网络链路强相关的问题。

Do not use this as the primary skill for pure IAM、计费、OpenAPI 签名、账单、余额、SDK 安装、API 参数格式问题。遇到这些机制问题时，保留产品上下文并转向对应横向技能或手册。

## 强约束

- 默认只执行查询命令。当前阶段只设计读接口，不设计创建、修改、删除、绑定、解绑、启动、停止、重启、运行命令等写操作。
- 查询优先使用 `ve <service> <Action> [--Param value...]`。`cli-meta` 里可能显示历史形态 `volcengine <service> <Action>`，在执行设计中统一写成 `ve`。
- 不执行 `ve configure`、登录、SSO、凭证写入或任何密钥管理命令。凭证只能来自运行环境，不能在 skill 中硬编码 AK/SK。
- 除 `ve`、`tosutil` 和受支持 Python SDK 外，不调用其他本地 CLI 或 SDK；涉及应用修改、资源变更、扩缩容、重启、删除前必须先做 Human-in-the-Loop 确认。
- 如果用户请求修复性动作，先给出将要执行的资源、Action、影响面和回滚/恢复建议，获得用户明确确认后再转入写操作设计。

## 交互式确认与 Human-in-the-Loop

### 概述

本 skill 默认只执行查询动作。`Describe/List/Get/Query/Check/Search` 类 OpenAPI 和受支持 Python SDK 只读脚本可以作为证据采集自动执行；任何会改变云资源、集群对象或业务流量的动作必须先获得用户明确确认。

### 需要确认的动作

| 动作类型 | 示例 | 确认要求 |
|---|---|---|
| ECS 生命周期变更 | `StartInstance`、`StopInstance`、`RebootInstance`、重置密码、绑定/解绑 EIP | 说明资源 ID、Region、影响面和恢复方式，等待用户确认 |
| 网络策略变更 | 新增/删除安全组规则、修改 ACL、修改路由、调整 NAT/SNAT/DNAT | 说明协议、端口、CIDR、目标资源和潜在暴露面 |
| VKE/Kubernetes 写操作 | 节点扩缩容、修改 Service/Ingress、重启工作负载 | 说明 namespace、对象、变更内容和回滚方式 |
| CLB/入口变更 | 修改监听器、后端组、健康检查、证书或转发规则 | 说明入口、后端、流量影响和回滚方式 |

## 快速路由

| 用户现象 | 优先证据 | 先查产品/工具 |
|---|---|---|
| 不确定属于实例、容器、网络、安全组、路由、登录还是横向问题 | 资源 ID、方向、时间、错误码、RequestId | [`01-overview-routing/README.md`](references/01-overview-routing/README.md) |
| ECS 创建、启动、停止、重启、实例状态异常 | 实例状态、任务、系统事件、控制台输出、伸缩活动 | [`02-ecs-lifecycle-state/README.md`](references/02-ecs-lifecycle-state/README.md) |
| ECS 无法访问、SSH/RDP 失败 | 实例状态、控制台输出、EIP/公网 IP、网卡、安全组、路由 | [`03-login-os-access/README.md`](references/03-login-os-access/README.md) |
| 公网无法访问服务 | EIP/CLB、监听器、后端、健康检查、安全组、ACL、实例端口 | [`04-public-private-connectivity/README.md`](references/04-public-private-connectivity/README.md) |
| ECS 无法出公网 | 实例子网、路由表、NAT/SNAT、EIP、带宽包 | [`04-public-private-connectivity/README.md`](references/04-public-private-connectivity/README.md) |
| 安全组或 ACL 放通后仍不通 | 入/出方向规则、源/目的 CIDR、端口、协议、子网 ACL | [`05-security-policy-port/README.md`](references/05-security-policy-port/README.md) |
| 同 VPC / 跨 VPC 不通 | 源/目的网卡、子网、路由、安全组、CEN/TR/VPN/专线 | [`06-eip-nat-route-gateway/README.md`](references/06-eip-nat-route-gateway/README.md) |
| VKE Pod 异常 | 集群、节点池、节点、插件、Pod 事件、日志、Service/Endpoint | [`07-vke-container-runtime/README.md`](references/07-vke-container-runtime/README.md) |
| 镜像、cloud-init、用户数据、初始化失败 | 镜像状态、用户数据、控制台输出、云助手状态 | [`08-image-init-cloudassistant/README.md`](references/08-image-init-cloudassistant/README.md) |
| 负载均衡后端异常 | CLB/监听器/转发规则/健康检查/后端服务器/安全组 | [`04-public-private-connectivity/README.md`](references/04-public-private-connectivity/README.md) |
| 弹性伸缩不符合预期 | 伸缩组、伸缩配置、策略、活动、实例、配额 | [`02-ecs-lifecycle-state/README.md`](references/02-ecs-lifecycle-state/README.md) |
| 网络质量差 | 诊断实例、路径报告、流量指标、源/目的地域和链路 | [`04-public-private-connectivity/README.md`](references/04-public-private-connectivity/README.md) |

## 章节目录

| 上层章节 | 本 skill reference |
|---|---|
| 1. 排查总入口 | [`01-overview-routing/README.md`](references/01-overview-routing/README.md) |
| 2. ECS 实例生命周期与状态 | [`02-ecs-lifecycle-state/README.md`](references/02-ecs-lifecycle-state/README.md) |
| 3. SSH / RDP / 操作系统访问 | [`03-login-os-access/README.md`](references/03-login-os-access/README.md) |
| 4. 公网与私网连通 | [`04-public-private-connectivity/README.md`](references/04-public-private-connectivity/README.md) |
| 5. 安全组、网络 ACL 与端口 | [`05-security-policy-port/README.md`](references/05-security-policy-port/README.md) |
| 6. EIP / NAT / 路由 / 网关 | [`06-eip-nat-route-gateway/README.md`](references/06-eip-nat-route-gateway/README.md) |
| 7. VKE / 容器运行问题 | [`07-vke-container-runtime/README.md`](references/07-vke-container-runtime/README.md) |
| 8. 云盘、镜像与初始化 | [`08-image-init-cloudassistant/README.md`](references/08-image-init-cloudassistant/README.md) |
| 9. 高频 Playbook | [`09-playbooks/README.md`](references/09-playbooks/README.md) |

## 脚本调用协议

脚本是复杂场景的提效层，不是跳过 reference 的捷径。使用脚本时必须遵守：

1. 先读取 `scripts/README.md` 或当前问题 reference 中的脚本段落，确认用途、必填参数和可选参数。
2. 只有在已拿到脚本的最小必填参数时才调用；缺参数时先向用户补问或先用 CLI 定位资源，不能先试错。
3. 调用失败时，先判断是缺参、凭证、上下文还是云资源错误；能用 CLI 补证据时回落到对应 reference 的命令包，不要直接结束排查。
4. 脚本返回后，先读 `summary` 和 `findings`，再按需展开 `raw`；不要把完整 JSON 原样倾倒给用户。

| 脚本 | 适用入口 | 最小必填参数 | 可选参数 |
|---|---|---|---|
| `scripts/collect_ecs_network_context.py` | ECS/SSH/端口/实例链路问题 | `--region <region> --instance-id <instance-id>` | 无 |
| `scripts/collect_vke_pod_context.py` | VKE 集群、节点、Pod、Service、Ingress 问题 | `--region <region> --cluster-id <cluster-id>` | `--namespace <ns> --pod <pod> --node <node>` |
| `scripts/collect_clb_backend_context.py` | CLB/ALB 监听器、健康检查、后端问题 | `--region <region> --type <clb|alb> --load-balancer-id <lb-id>` | `--listener-id <listener-id>` |

## 工作流

1. 明确问题的源端、目的端、协议、端口、时间范围、地域、账号/项目、资源 ID。
2. 判断这是实例态、系统态、容器态、入口态、网络路径态、安全策略态，还是横向机制问题。
3. 打开 `references/query-cli-catalog.md`，路由到一个细分 reference；只读取当前问题必要的 reference。
4. 如果命令不在清单里，查看对应 `cli-meta/.../<产品>/接口清单.md` 和官方文档后再补充。
5. 对跨产品链路问题，按资源关系汇总 JSON 输出：ECS -> ENI -> Subnet/VPC -> SG/ACL -> Route -> EIP/NAT/CLB/CEN/TR/VPN。
   - 如果入口是 ECS 实例 ID，且已拿到 `region + instance-id`，优先使用 `scripts/collect_ecs_network_context.py --region <region> --instance-id <instance-id>` 聚合 ECS/VPC 只读证据，再补查 EIP/NAT/CLB/CEN/TR/VPN。
6. 对 VKE 问题，收集 VKE 控制面信息，并让用户补充 Pod 事件、日志和应用侧现象，避免只看云上集群列表就下结论。
   - 如果涉及 Pod、Service、Ingress、节点或插件联动，且已拿到 `region + cluster-id`，优先使用 `scripts/collect_vke_pod_context.py --region <region> --cluster-id <cluster-id>`；可补 `--namespace`、`--pod`、`--node` 记录用户上下文，但脚本不会调用集群侧工具。
7. 如果需要多接口关联、分页聚合、字段归一或拓扑拼接，按 `references/python-sdk-script-patterns.md` 设计只读 Python SDK 脚本。
   - 如果入口是 CLB/ALB 且涉及健康检查或后端 ECS，只有在已确认 `type` 和 `load-balancer-id` 后，才使用 `scripts/collect_clb_backend_context.py --region <region> --type <clb|alb> --load-balancer-id <lb-id>`；不得漏传 `--type`。
8. 输出诊断结论时分层说明：已确认事实、最可能根因、还缺哪些证据、下一步安全动作。

## 输出格式

排障回复应优先给出可执行的判断，而不是堆命令：

- `现象归类`：这是哪类计算/网络问题。
- `已查证据`：列出关键资源状态和异常字段。
- `结论`：最可能根因，必要时给置信度。
- `建议动作`：只读补查、用户侧验证、或需要确认的变更动作。
- `横向跳转`：如果根因是 IAM、计费、OpenAPI/Python SDK/CLI 机制，明确转到哪个横向手册。
