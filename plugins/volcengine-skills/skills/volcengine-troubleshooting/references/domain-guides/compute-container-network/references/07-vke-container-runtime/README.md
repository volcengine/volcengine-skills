# VKE / 容器运行查询

用于 VKE 集群、节点池、节点、Pod、Service、Ingress、镜像拉取、CrashLoop、OOMKilled、Pending、插件异常等问题。

## 前置输入

- Cluster ID/Name、Region、Namespace、Pod/Deployment/Service/Ingress 名称。
- 节点 ID、节点池 ID、实例 ID。
- 错误类型：Pending、CrashLoopBackOff、ImagePullBackOff、OOMKilled、Service 不通、Ingress 不通。

## 云上控制面命令包

```text
ve vke ListClusters --Region "<region>"
ve vke ListNodePools --Region "<region>" --ClusterId "<cluster-id>"
ve vke ListNodes --Region "<region>" --ClusterId "<cluster-id>"
ve vke ListAddons --Region "<region>" --ClusterId "<cluster-id>"
ve vke ListScalingEvents --Region "<region>" --ClusterId "<cluster-id>"
ve vke ListScalingPolicies --Region "<region>" --ClusterId "<cluster-id>"
ve vke DescribeSnapshots --Region "<region>"
```

关注字段：

- 集群状态、版本、网络模式、API Server 访问方式。
- 节点池状态、期望/当前节点数、伸缩事件。
- 节点是否 Ready，节点背后的 ECS 实例是否异常。
- CNI、CSI、Ingress Controller、监控等插件状态。

如果问题涉及 Pod/节点/插件联动，优先使用 `scripts/collect_vke_pod_context.py` 聚合 VKE 控制面。Pod 事件、日志、Service/Endpoint/Ingress 等集群内证据由用户提供，不主动调用集群侧工具。

示例：

```text
python3 "${SKILL_ROOT}/references/domain-guides/compute-container-network/scripts/collect_vke_pod_context.py" \
  --region "<region>" \
  --cluster-id "<cluster-id>" \
  --namespace "<namespace>" \
  --pod "<pod>"
```

使用脚本后，先看 `summary.cluster`、`summary.counts`、`raw.nodes` 和 `findings`；如果仍缺 Pod 事件或日志，向用户索取脱敏后的应用侧证据。

## 集群内证据

- `Pending`：需要用户提供调度事件，再结合节点资源、污点、亲和性、PVC、镜像判断。
- `CrashLoopBackOff`：需要用户提供当前日志和上一次崩溃日志，再看退出码、探针、配置。
- `OOMKilled`：需要用户提供容器资源限制、节点内存压力、最近事件。
- `Service 不通`：需要用户提供 Service selector、Endpoint、Pod Readiness、网络策略。
- `Ingress 不通`：需要用户提供 Ingress 规则、Controller 状态、Service/Endpoint，再联动 CLB 后端健康。

## 镜像仓库查询

```text
ve cr ListRegistries --Region "<region>"
ve cr ListNamespaces --Region "<region>" --RegistryId "<registry-id>"
ve cr ListRepositories --Region "<region>" --RegistryId "<registry-id>" --Namespace "<namespace>"
ve cr ListTags --Region "<region>" --RegistryId "<registry-id>" --Namespace "<namespace>" --Repository "<repo>"
ve cr GetVpcEndpoint --Region "<region>" --RegistryId "<registry-id>"
ve cr GetPublicEndpoint --Region "<region>" --RegistryId "<registry-id>"
```

关注字段：

- 镜像 tag 是否存在。
- 节点访问仓库走公网还是 VPC endpoint。
- 鉴权 token/Secret 是否匹配 registry。

## 结果解读

| 证据 | 下一步 |
|---|---|
| VKE 节点 NotReady | 回查 ECS 实例、节点池、CNI/CSI 插件 |
| Pod Pending 且资源不足 | 检查节点资源、伸缩策略、配额/库存 |
| ImagePullBackOff | 检查镜像 tag、Secret、仓库 endpoint、节点出网 |
| Service Endpoint 为空 | 检查 selector、Pod readiness、命名空间 |
| Ingress 后端不健康 | 联动 CLB ref 与安全组 ref |
