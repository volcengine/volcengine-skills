# Scripts

本目录只放计算、容器与网络连通排障的只读 Python SDK 脚本。脚本不得硬编码 AK/SK，不得写入凭证文件，只能从环境变量读取 `VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、`VOLCENGINE_REGION`。

新增或修改脚本前，先阅读 `../references/python-sdk-script-patterns.md`。

## 调用规则

- 运行脚本前，先确认脚本的最小必填参数已经齐全；缺参时先补问或先用 CLI 定位资源，不要先运行脚本试错。
- `RunSkillScript` 只接收相对路径，例如 `scripts/collect_clb_backend_context.py`；参数放在 `args` 中。
- 复杂脚本返回后，优先读取 `summary` 和 `findings`，再按需展开 `raw`。

| 脚本 | 最小必填参数 |
|---|---|
| `collect_ecs_network_context.py` | `--region <region> --instance-id <instance-id>` |
| `collect_vke_pod_context.py` | `--region <region> --cluster-id <cluster-id>` |
| `collect_clb_backend_context.py` | `--region <region> --type <clb|alb> --load-balancer-id <lb-id>` |

## `collect_ecs_network_context.py`

用途：当 ECS 连通性问题需要同时关联实例、网卡、安全组、子网和路由表时，用新版公共 Python SDK 聚合只读上下文，减少多条 CLI 手工拼接的遗漏。

来源：`python-sdk/volcengine-python-sdk` 中的 `volcenginesdkecs`、`volcenginesdkvpc`。

示例：

```text
python3 "${SKILL_ROOT}/references/domain-guides/compute-container-network/scripts/collect_ecs_network_context.py" \
  --region cn-beijing \
  --instance-id i-xxxxxxxx
```

输出：JSON，包含 `summary`、`raw.describe_instances`、`raw.describe_network_interfaces`、`raw.security_groups`、`raw.subnets`、`raw.route_tables` 和初步 `findings`。

## `collect_vke_pod_context.py`

用途：当 VKE / Kubernetes 问题需要同时关联集群、节点池、节点、插件和用户提供的 Pod/Service/Ingress 上下文时，用新版公共 Python SDK 聚合 VKE 控制面。

来源：`python-sdk/volcengine-python-sdk` 中的 `volcenginesdkvke`。

示例：

```text
python3 "${SKILL_ROOT}/references/domain-guides/compute-container-network/scripts/collect_vke_pod_context.py" \
  --region cn-beijing \
  --cluster-id cdxxxxxxxx \
  --namespace default \
  --pod web-xxxxx
```

输出：JSON，包含 `summary.cluster`、`summary.counts`、`raw.clusters`、`raw.node_pools`、`raw.nodes`、`raw.addons`。

使用边界：只查询 VKE 控制面，不查询 Pod 事件和日志；Pod 事件、日志和应用侧现象由用户提供。

## `collect_clb_backend_context.py`

用途：当 CLB/ALB 后端不健康或公网入口不通时，聚合负载均衡实例、监听器、健康检查、后端服务器组和后端 ECS 状态。

来源：`python-sdk/volcengine-python-sdk` 中的 `volcenginesdkclb`、`volcenginesdkalb`、`volcenginesdkecs`。

示例：

```text
python3 "${SKILL_ROOT}/references/domain-guides/compute-container-network/scripts/collect_clb_backend_context.py" \
  --region cn-beijing \
  --type clb \
  --load-balancer-id clb-xxxxxxxx
```

ALB 示例：

```text
python3 "${SKILL_ROOT}/references/domain-guides/compute-container-network/scripts/collect_clb_backend_context.py" \
  --region cn-beijing \
  --type alb \
  --load-balancer-id alb-xxxxxxxx \
  --listener-id lsn-xxxxxxxx
```

输出：JSON，包含 `summary.listener_count`、`summary.server_group_ids`、`summary.backend_instance_ids`、`raw.load_balancers`、`raw.listeners`、`raw.listener_health`、`raw.server_group_attributes` 和 `raw.backend_ecs`。

使用边界：只读；不修改监听器、转发规则、后端服务器组、健康检查或 ECS。

调用提醒：`--type` 是必填参数，CLB 场景传 `clb`，ALB 场景传 `alb`；只有在需要收窄到某个监听器时才补 `--listener-id`。
