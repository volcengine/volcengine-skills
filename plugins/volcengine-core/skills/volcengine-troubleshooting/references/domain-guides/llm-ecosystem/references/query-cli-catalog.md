# 大模型生态查询 CLI 索引

本文件是入口索引，不是接口大全。先按问题进入 8 个子类 reference，再选择最小只读命令。

## 通用规则

- CLI 来源：公共 CLI `volcengine-cli`，skill 内统一写成 `ve`。
- 只读优先：默认只执行 `Describe/List/Get/Query/Check` 类命令。
- 运行任何 CLI 前，必须先读取本索引或对应章节 reference，让命令出现在当前 skill context 中；不要只凭主 `SKILL.md` 摘要直接 RunSkillCLI。
- 禁止默认执行：模型推理、生成、精调创建、Endpoint 变更、工作区启停、授权、创建、删除、修改。
- 敏感接口：`ve ark GetApiKey` 可能返回 API Key，不作为默认排障命令。
- 参数不确定时先跑 `ve <service> <Action> --help`，不要猜。

## 子类到 CLI 映射

| 子类 | 主要产品 | CLI 服务 | 优先 reference |
|---|---|---|---|
| L1 基础模型层 | 豆包模型、Embedding、Rerank、多模态 | 主要依赖方舟查询和官方文档 | `02-l1-model-capability` |
| L2 方舟 MaaS | 火山方舟、联网搜索、批量推理、精调 | `ark` | `03-l2-ark-maas` |
| L3 智能体开发 | AgentKit、ArkClaw、扣子、Trae | `coze20250601` 可用性较高；`aidap`、`arkclaw` 为可选元数据命令，当前远程沙箱可能不可用 | `04-l3-agent-development` |
| L4 AI 云原生 | 机器学习平台、推理服务、资源组 | `mlplatform20240701`、`aidap` | `05-l4-ai-native-infra` |
| L5 行业场景 | 语音、RAG、AI IDE、图像/视频 | `vikingdb`、`cv20240606`，语音多依赖官方文档 | `06-l5-vertical-scenarios` |
| 横切专题 | 鉴权、权限、开通、参数、限流、计费、网络 | 先查产品上下文，再转横向 skill | `07-cross-cutting` |
| 高频 Playbook | 固定错误码 | 视错误选择 `ark`、`vikingdb`、`arkclaw` | `08-playbooks` |

## 火山方舟和模型接入

用于 Endpoint 不存在、模型未开通、OpenAI 兼容 model 字段不匹配、批量推理/精调状态确认。

```text
ve ark ListEndpoints --body '{"PageNumber":1,"PageSize":10}'
ve ark ListEndpoints --body '{"PageNumber":1,"PageSize":10,"Filter":{"Ids":["<endpoint-id>"]}}'
ve ark GetEndpoint --body '{"Id":"<endpoint-id>"}'
ve ark ListBatchInferenceJobs --body '{"PageNumber":1,"PageSize":10}'
ve ark ListModelCustomizationJobs --body '{"PageNumber":1,"PageSize":10}'
```

关注字段：

- Endpoint 是否存在、状态是否可用、绑定模型/版本是否符合用户传入值。
- `ProjectName` 和标签是否导致用户在错误项目下查找。
- 批量/精调任务的阶段、失败原因和创建时间。

## VikingDB / 知识库 / Embedding / Rerank

用于知识库检索失败、Embedding/Rerank 模型不可用、Collection/Index 状态异常、构建任务未完成。VikingDB 列表命令必须用 `--body` 传分页参数。

```text
ve vikingdb ListVikingdbCollection --body '{"PageNumber":1,"PageSize":10}'
ve vikingdb ListVikingdbIndex --body '{"PageNumber":1,"PageSize":10}'
ve vikingdb ListVikingdbTask --body '{"PageNumber":1,"PageSize":10}'
```

关注字段：

- Collection 和 Index 是否存在、状态是否可检索。
- Task 是否失败、排队或仍在运行。
- 资源存在但模型调用失败时，回到方舟模型开通和权限链路。
- 不要仅凭方舟 Endpoint 首页没有出现 Embedding/Rerank 就判断未开通。需要用户提供准确模型/Endpoint 后再过滤查询，或结合错误码/控制台证据。

## AgentKit / ArkClaw / 扣子

用于 Agent 工作区、ArkClaw 实例、扣子用户授权和智能体开发链路。

当前沙箱兼容性说明：

- `aidap`、`arkclaw` 在本地 `cli/volcengine-cli` 元数据中存在，但远程沙箱镜像可能未包含对应服务，执行时可能返回 `unknown command`。
- 用户要求在当前沙箱测试时，可以说明该限制；如果失败，不要继续猜其他 service 名，不要转去执行写操作。
- `coze20250601 ListCozeUser` 可作为扣子用户映射的只读查询入口。

```text
ve aidap DescribeWorkspaces --body '{"Limit":10,"Offset":0}'
ve aidap DescribeComputes --body '{"WorkspaceId":"<workspace-id>"}'
ve arkclaw ListClawOmniInstances --PageNumber 1 --PageSize 10
ve arkclaw GetClawOmniInstance --Id <instance-id>
ve coze20250601 ListCozeUser --body '{"PageNumber":1,"PageSize":10}'
```

关注字段：

- Workspace/Compute/Instance 是否存在、状态是否异常。
- ArkClaw Unknown model 先判断模型名映射和 Coding Plan/订阅，再看云端实例状态。
- 扣子授权类接口多为写操作，默认只使用 `ListCozeUser`。

## 机器学习平台和 AI 云原生基础设施

用于推理服务、资源组、部署、资源队列、服务状态和高并发资源问题。

```text
ve mlplatform20240701 ListServices --body '{"PageNumber":1,"PageSize":10}'
ve mlplatform20240701 ListResourceGroups --body '{"PageNumber":1,"PageSize":10}'
```

关注字段：

- 服务状态、资源组状态、ProjectName、Region 和创建/更新时间。
- 启停服务、资源队列暂停/恢复都不是默认排障动作。

## 大模型安全产品

用于大模型安全测评任务、Agent 风险、风险摘要和任务进度。

```text
ve llmscan ListLLMEvalTasks --body '{"PageNumber":1,"PageSize":10}'
```

关注字段：

- 评测任务状态、是否有风险、资产类型和任务类型。
- 防护策略变更、任务创建、模型接入变更必须用户确认。

## 图像/视频/多模态

`cv20240606` 中包含图像/视频类 OpenAPI。多数动作会提交任务或生成内容，可能消耗额度，不作为默认自动排障命令。只在用户明确确认后，才考虑读取已有任务结果或使用只读用量接口。

## 没有可靠 CLI 覆盖的产品

豆包语音、音频技术、Trae、即梦 AI、虚拟数字人、智能视频创作 SDK、客服 Agent、创作 Agent、联网问答 Agent 等场景，首版以官方文档、错误码、RequestId、用户脱敏日志和横向机制判断为主，不伪造 CLI。AgentKit/ArkClaw 在远程沙箱缺少 service 时也按此规则处理。
