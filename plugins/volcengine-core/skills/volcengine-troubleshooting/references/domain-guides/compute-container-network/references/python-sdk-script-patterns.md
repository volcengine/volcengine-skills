# Python SDK 脚本规范

本技能优先使用 CLI 查询。只有当问题需要多接口联动、分页聚合、拓扑关系拼接或复杂字段解析时，才设计 Python SDK 脚本。

## 调用前检查

在调用已有脚本前，Agent 必须先确认：

1. 已阅读当前 reference 中的脚本段落或 `../scripts/README.md`。
2. 已拿到脚本的所有必填参数；没有时先补问或先用 CLI 查询，不要先运行脚本试错。
3. 已确认这是多接口联动问题，而不是单条 CLI 就足够的问题。

最小必填签名：

| 脚本 | 最小必填参数 |
|---|---|
| `collect_ecs_network_context.py` | `--region <region> --instance-id <instance-id>` |
| `collect_vke_pod_context.py` | `--region <region> --cluster-id <cluster-id>` |
| `collect_clb_backend_context.py` | `--region <region> --type <clb|alb> --load-balancer-id <lb-id>` |

## 适用场景

- 用户只给了一个 ECS 实例 ID，需要自动展开实例、网卡、VPC、子网、安全组、EIP、路由表、NAT/CLB 关系。
- 需要批量检查多个实例、多个 Pod、多个安全组或跨地域资源。
- 需要把 CLI JSON 输出归一成排障报告，例如找出没有默认路由、未放通端口、健康检查失败的后端。
- 需要分页拉取 `Describe/List` 结果并筛选异常字段。

## 已提供脚本

### `scripts/collect_ecs_network_context.py`

适用问题：ECS 公网/私网不通、SSH/RDP 不通、端口放通后仍不通、需要同时查看实例、网卡、安全组、子网和路由表的场景。

使用方式：

```text
python3 "${SKILL_ROOT}/references/domain-guides/compute-container-network/scripts/collect_ecs_network_context.py" \
  --region "<region>" \
  --instance-id "<instance-id>"
```

脚本来源：新版公共 Python SDK `volcengine-python-sdk`，使用 `volcenginesdkecs` 与 `volcenginesdkvpc`。

安全边界：只调用 `DescribeInstances`、`DescribeNetworkInterfaces`、`DescribeSecurityGroupAttributes`、`DescribeSubnets`、`DescribeRouteTableList`、`DescribeRouteEntryList`；只从环境变量读取 AK/SK；不执行任何写操作。

### `scripts/collect_vke_pod_context.py`

适用问题：VKE Pod `Pending`、`CrashLoopBackOff`、`ImagePullBackOff`、`OOMKilled`、节点 `NotReady`、Service/Ingress 不通，需要同时看 VKE 控制面和 Kubernetes 对象状态。

使用方式：

```text
python3 "${SKILL_ROOT}/references/domain-guides/compute-container-network/scripts/collect_vke_pod_context.py" \
  --region "<region>" \
  --cluster-id "<cluster-id>" \
  --namespace "<namespace>" \
  --pod "<pod>"
```

脚本来源：新版公共 Python SDK `volcengine-python-sdk` 的 `volcenginesdkvke`。

安全边界：只调用 VKE `ListClusters`、`ListNodePools`、`ListNodes`、`ListAddons`；不执行集群侧工具或云资源写操作。

### `scripts/collect_clb_backend_context.py`

适用问题：CLB/ALB 后端 `unhealthy`、公网入口不通、监听器配置与后端服务状态需要联动判断。

使用方式：

```text
python3 "${SKILL_ROOT}/references/domain-guides/compute-container-network/scripts/collect_clb_backend_context.py" \
  --region "<region>" \
  --type "<clb|alb>" \
  --load-balancer-id "<lb-id>" \
  --listener-id "<listener-id>"
```

脚本来源：新版公共 Python SDK `volcengine-python-sdk` 的 `volcenginesdkclb`、`volcenginesdkalb`、`volcenginesdkecs`。

安全边界：只调用负载均衡和 ECS 查询接口；不修改监听器、转发规则、后端服务器组、健康检查或 ECS。

调用约束：`--type` 和 `--load-balancer-id` 都是必填；如果用户只说“CLB”或“ALB”，`--type` 直接取对应字面值；如果用户只给了域名或业务名，先用 CLI 定位 LB ID，再运行脚本。

## 来源

可使用的 SDK 以项目 README 为准：

- 公共新版 Python SDK：`python-sdk/volcengine-python-sdk`
- 旧版 Python SDK：`python-sdk/volc-sdk-python`
- 产品专用 SDK：以 `火山引擎问题排查手册/README.md` 和 `cli-meta/<分类>/<产品>/接口清单.md` 中记录为准。

本 skill 只支持 `ve`、`tosutil` 两类 CLI，以及 `volc-sdk-python`、`volcengine-python-sdk` 两类 Python SDK。若排查需要其它 CLI/SDK 或集群侧工具，只说明限制并收集用户提供的脱敏证据，不在本地执行。

## 只读脚本约束

- 只调用 `Describe/List/Get/Query/Check/Search` 等查询接口。
- 禁止调用 `Create/Modify/Delete/Attach/Detach/Associate/Start/Stop/Reboot/Run/Invoke` 等写接口。
- 禁止硬编码 AK/SK/Token；凭证只从环境变量或运行时默认凭证链读取。
- 默认输出 JSON 或 Markdown 摘要，保留原始 RequestId 和关键资源 ID。
- 对分页、地域、项目、过滤条件显式声明，避免“查不到”被误判为“资源不存在”。
- 脚本执行前说明将查询哪些服务和资源；如果可能产生大量请求，先让用户确认范围。

## 建议目录

后续新增脚本放在当前 skill 的 `scripts/` 目录：

```text
scripts/
  collect_ecs_network_context.py
  collect_vke_pod_context.py
  collect_clb_backend_context.py
```

每个脚本开头需要写清楚：

- 使用的 SDK 来源。
- 调用的只读 Action。
- 必填参数。
- 输出字段。
- 不会执行的写操作。
