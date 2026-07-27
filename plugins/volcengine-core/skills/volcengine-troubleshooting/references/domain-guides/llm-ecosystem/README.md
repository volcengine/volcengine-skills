# 火山引擎大模型生态排障技能

这是面向火山引擎大模型生态的主入口 skill。它覆盖模型能力、火山方舟 MaaS、智能体开发体系、AI 云原生基础设施、行业应用场景、横切机制和高频错误 Playbook。它不把大模型问题简单等同于 OpenAPI、权限或计费问题，而是先保留模型/产品上下文，再按证据转到横向 skill。

## 上层信息

- 手册定位：对应 `火山引擎问题排查手册/火山引擎大模型生态排查手册/README.md`，按 8 个子类组织。
- 产品范围：火山方舟、豆包语音、音频技术、AgentKit、ArkClaw、扣子、Trae、机器学习平台、VikingDB、Viking AI 搜索、联网搜索/联网问答 Agent、图像生成大模型、即梦 AI、视频/音视频智能处理、客服 Agent、创作 Agent、大模型安全测评、大模型应用防火墙、智能体身份和权限管理平台。
- 横向分工：AK/IAM/AccessDenied 转账号权限 skill；账单、额度、订阅、欠费转计费 skill；签名、Action/Version、Python SDK/CLI 参数转 OpenAPI / SDK / CLI skill；ECS/VPC/VKE/CLB/域名/CDN/TOS 等基础云问题转对应产品 skill。
- 工具优先级：默认 CLI-first，只使用 `ve` 中 `Describe/List/Get/Query/Check` 类只读命令。模型推理、生成、精调、实例执行、启停、授权、创建、删除都必须 Human-in-the-Loop。
- 沙箱兼容性：当前远程沙箱 `ve` 已验证可执行 `ark`、`vikingdb`；`aidap`、`arkclaw` 在本地 CLI 元数据存在，但远程沙箱镜像可能返回 `unknown command`。AgentKit/ArkClaw 场景默认先说明依赖和 fallback，不要把这两个服务当成必然可跑。
- 数据来源：手册、`cli-meta/火山引擎大模型生态排查手册/`、`产品官方文档/火山引擎大模型生态排查手册/`、`cli/volcengine-cli`、`python-sdk/volcengine-python-sdk`、受支持 Python SDK 文档。
- 安全边界：不输出 AK/SK、SessionToken、Ark API Key、OpenAI Bearer Token、用户完整 Prompt、音视频原始内容、业务知识库内容或模型输出敏感片段。

## 先读这些

- `references/query-cli-catalog.md`：按 8 个子类定位最小只读 CLI 查询入口。任何 `RunSkillCLI` 之前都必须先读取本文件或对应章节 reference，不能只凭主 `SKILL.md` 里的摘要直接执行。
- `references/api-coverage-matrix.md`：本分类 `cli-meta/` API 覆盖审查矩阵，列出已纳入排障候选的只读/诊断 Action 与默认排除的写操作边界。
- `references/python-sdk-script-patterns.md`：什么时候才需要 Python SDK 脚本，以及凭证和输出规范。
- `references/01-overview-routing/README.md`：总入口、信息收集和路由规则。
- 当前首版没有可执行 `scripts/`；不要调用 `RunSkillScript`，除非后续 reference 明确提供具体脚本文件名。

同时可查：

- 产品手册：`火山引擎问题排查手册/火山引擎大模型生态排查手册/README.md`
- 接口元数据：`cli-meta/火山引擎大模型生态排查手册/<产品>/接口清单.md`
- 官方文档：`产品官方文档/火山引擎大模型生态排查手册/<产品>/...`

## 使用边界

Use this skill when the user describes:

- 模型未开通、不存在、无访问权、Endpoint 找不到、OpenAI 兼容调用失败、`ModelNotOpen`、`InvalidEndpointOrModel.NotFound`。
- 方舟 API Key、Endpoint、模型 ID、精调、批量推理、异步推理、知识库、Embedding/Rerank、联网搜索问题。
- AgentKit、扣子、HiAgent、ArkClaw、Coding Plan、Trae、智能体工作区、工具调用、知识库检索、工作流运行异常。
- TTS/ASR、豆包语音、音频技术、resource ID 和 speaker 不匹配、WebSocket 连接、实时交互、智能客服。
- 图像/视频生成、多模态 token 超限、音视频理解、即梦 AI、虚拟数字人、内容生产类 AI 能力异常。
- 大模型安全测评、大模型应用防火墙、智能体身份权限等大模型安全产品问题。
- 需要把一个大模型问题同时拆成产品层和横向机制层。

Do not use this as the primary skill for:

- 纯 AK/SK、IAM 策略、子用户、角色扮演、STS 临时凭证：转账号权限 skill。
- 纯账单、余额、订阅、配额、按量扣费、欠费停服：转计费 skill。
- 纯 OpenAPI 签名、SDK 安装、CLI 参数、Action/Version、Region/Endpoint 机制错误：转 OpenAPI / SDK / CLI skill。
- 纯 ECS/VPC/VKE/CLB/CDN/DNS/TOS/KMS 等基础云产品问题：转对应产品 skill。

## 强约束

- 默认只执行 `Describe/List/Get/Query/Check` 类查询。
- 公共 CLI 命令统一写成 `ve <service> <Action> [--body '<json>' | --Param value]`；如果 `cli-meta` 中写的是 `volcengine`，在本 skill 中统一转成 `ve`。
- 不执行模型推理、图片/视频/语音生成、精调启动、批量任务创建、实例启停、授权、创建、删除、修改等动作，除非用户明确确认。
- `ve ark GetApiKey`、OpenAI Bearer Token、API Key 查询、完整 Prompt/Response、知识库文档内容都属于敏感数据，默认不读取或不回显。
- 复杂对象参数优先使用 `--body '<json>'`；参数不确定时先要求查看 `ve <service> <Action> --help` 或 `cli-meta`，不要猜。
- 当前首版没有脚本；如果 Agent 认为需要脚本，先说明为什么 CLI 不够，并引用 `python-sdk-script-patterns.md`。

## 交互式确认与 Human-in-the-Loop

| 动作类型 | 示例 | 确认要求 |
|---|---|---|
| 模型推理/生成 | ChatCompletions、图片生成、视频生成、TTS 合成 | 说明会消耗额度或产生内容，只在用户确认后执行 |
| 方舟变更 | 创建/删除 Endpoint、启动/终止精调、批量推理任务创建 | 说明资源、模型、费用、影响面和回滚方式 |
| Agent/工作区变更 | AgentKit 工作区启停、ArkClaw 实例操作、扣子授权 | 说明实例/用户/工作区、命令内容和风险 |
| 基础设施变更 | 机器学习平台服务启停、资源队列暂停/恢复 | 说明影响的服务、流量、资源和恢复方式 |
| 敏感读取 | API Key、Prompt、知识库原文、音视频内容 | 说明脱敏策略，禁止完整回显 |

## 快速路由

| 用户现象 | 优先证据 | 必读 reference |
|---|---|---|
| 不确定属于哪一层 | 产品名、模型/Endpoint、错误码、RequestId、时间、Python SDK/CLI | [`01-overview-routing/README.md`](references/01-overview-routing/README.md) |
| 模型能力、模态、上下文、参数不支持 | model id、模态、参数、token 数、调用方式 | [`02-l1-model-capability/README.md`](references/02-l1-model-capability/README.md) |
| 方舟 Endpoint、API Key、模型开通、OpenAI 兼容、批量/精调 | Endpoint ID、model id、Ark RequestId、ProjectName | [`03-l2-ark-maas/README.md`](references/03-l2-ark-maas/README.md) |
| AgentKit、扣子、ArkClaw、Coding Plan、Trae | 工作区/实例/用户、模型配置、工具、知识库、订阅 | [`04-l3-agent-development/README.md`](references/04-l3-agent-development/README.md) |
| 高并发、推理服务、网关、超时、WebSocket、观测 | 服务/资源组、QPS、超时、日志、RequestId、Region | [`05-l4-ai-native-infra/README.md`](references/05-l4-ai-native-infra/README.md) |
| 语音、知识库/RAG、AI IDE、行业 Agent、多模态 | 场景、资源 ID、音色/模型/知识库/任务 ID | [`06-l5-vertical-scenarios/README.md`](references/06-l5-vertical-scenarios/README.md) |
| 鉴权、权限、参数、限流、计费、网络、服务端错误 | 错误码、身份、额度、账单、网络、ResponseMetadata | [`07-cross-cutting/README.md`](references/07-cross-cutting/README.md) |
| 命中高频错误文本 | 原始错误文本或用户截图摘要 | [`08-playbooks/README.md`](references/08-playbooks/README.md) |

## 高频固定流程

### ModelNotOpen / InvalidEndpointOrModel

1. 区分用户传的是模型 ID、Endpoint ID 还是第三方 OpenAI `model` 字段。
2. 方舟场景先用 `ark ListEndpoints` / `ark GetEndpoint` 只读确认 Endpoint 是否存在、状态和绑定模型。
3. 如果资源存在但仍报无权限，保留模型/Endpoint 证据后转账号权限 skill。
4. 如果模型能力不支持当前模态或参数，转 L1 模型能力 reference。

### AuthenticationError / API key

1. 不要求用户贴完整 API Key，只看脱敏前缀、调用入口、Region、Endpoint、Python SDK/CLI。
2. 方舟 API Key 和 AK/SK 分开判断：Ark OpenAI 兼容 API 通常用 Bearer API Key，控制面 CLI 用 AK/SK。
3. 如是公共 OpenAPI 签名失败，转 OpenAPI / SDK / CLI skill；如是 API Key 未授权模型，转账号权限 skill。

### 429 / RateLimit / Quota

1. 不发起模型推理压测。
2. 收集模型、Endpoint、时间窗口、QPS/TPM、错误码、RequestId、账单/订阅状态。
3. 区分瞬时限流、配额不足、欠费/订阅过期、服务端拥塞。
4. 配额/账单明确后转计费 skill。

### Coding Plan / ArkClaw

1. 先判断是云端 ArkClaw 实例/订阅问题，还是模型名/Endpoint 映射问题。
2. 云端只读查询可选使用 `ve arkclaw ListClawOmniInstances` / `ve arkclaw GetClawOmniInstance`，但当前沙箱的 `ve` 可能不包含 `arkclaw` service；如果用户要求在当前沙箱验证，应先说明可能不可用，并在失败时直接转为本地日志/订阅/模型名映射排查。
3. 不执行 `ExecuteClawOmniInstanceCommand`、Pause、Resume、Reset 等动作。
4. 订阅过期或额度问题转计费 skill；模型名映射问题回到方舟/模型能力。

### TTS / ASR resource ID

1. 收集 AppId、Cluster、VoiceType/Speaker、ResourceId、音频格式、协议、错误码。
2. 判断是音色资源和 speaker 不匹配、资源未开通、鉴权错误还是 WebSocket/网络问题。
3. 语音产品 CLI 覆盖不足时，优先走官方文档和用户提供的错误响应，不强行调用不存在的 CLI。

### Embedding / Rerank / 知识库检索

1. 判断错误发生在模型调用、VikingDB Collection/Index、知识库构建、检索召回还是 Agent 编排。
2. VikingDB 资源可用 `vikingdb ListVikingdbCollection` / `ListVikingdbIndex` / `ListVikingdbTask` 做只读确认，必须先读取 `query-cli-catalog.md` 或 `06-l5-vertical-scenarios/README.md`，并使用 `--body '{"PageNumber":1,"PageSize":5}'` 这种 JSON 形式，不要把 `PageSize` 展开为顶层 CLI 参数。
3. 模型不可用或无权限时回到方舟模型开通和权限链路。不能仅凭未过滤的 `ark ListEndpoints` 首页没有出现 Embedding/Rerank Endpoint 就断定模型未开通；必须有用户提供的准确模型/Endpoint、过滤查询结果、错误码或控制台证据。

## 章节目录

| 上层章节 | 本 skill reference |
|---|---|
| 1. 排查总入口与全局框架 | [`01-overview-routing/README.md`](references/01-overview-routing/README.md) |
| 2. L1 基础模型层排查 | [`02-l1-model-capability/README.md`](references/02-l1-model-capability/README.md) |
| 3. L2 火山方舟 MaaS 平台排查 | [`03-l2-ark-maas/README.md`](references/03-l2-ark-maas/README.md) |
| 4. L3 智能体开发体系排查 | [`04-l3-agent-development/README.md`](references/04-l3-agent-development/README.md) |
| 5. L4 AI 云原生基础设施排查 | [`05-l4-ai-native-infra/README.md`](references/05-l4-ai-native-infra/README.md) |
| 6. L5 行业应用与垂直场景排查 | [`06-l5-vertical-scenarios/README.md`](references/06-l5-vertical-scenarios/README.md) |
| 7. 横切专题排查 | [`07-cross-cutting/README.md`](references/07-cross-cutting/README.md) |
| 8. 高频问题 Playbook | [`08-playbooks/README.md`](references/08-playbooks/README.md) |

## 工作流

1. 收集产品名、生态层、错误码、RequestId、发生时间、Region、ProjectName、模型/Endpoint/工作区/实例/知识库/任务 ID、调用入口和 Python SDK/CLI 版本。
2. 先按用户现象进入 8 个子类之一，再打开对应 reference。
3. 打开 `query-cli-catalog` 后只选择当前问题需要的最小只读命令。
4. 用查询结果区分产品层事实和横向机制事实。
5. 输出诊断时保留不确定性，明确下一步需要用户补充哪些脱敏证据。

## 输出格式

- `现象归类`
- `生态层级`
- `已查证据`
- `初步结论`
- `建议动作`
- `横向跳转`
