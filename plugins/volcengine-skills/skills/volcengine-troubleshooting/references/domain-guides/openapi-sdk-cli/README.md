# 火山引擎 OpenAPI / SDK / CLI 排障技能

这是面向火山引擎 OpenAPI 调用机制、`ve`/`tosutil` CLI、受支持 Python SDK、API Explorer、API 网关和云控制 API 的横向 skill。它回答的是“调用为什么失败、请求该怎么归因、如何最小复现”，不是替代具体云产品的业务语义排障。

## 上层信息

- 手册定位：覆盖 OpenAPI 基础调用模型、Action/Version/Service/Region/Endpoint、AK/SK/STS 签名、参数和接口版本、受支持 Python SDK 初始化与异常封装、`ve`/`tosutil` CLI、API Explorer、RequestId/错误码定位、API 网关和云控制 API。
- 横向分工：账号、IAM、AK 生命周期和权限策略转账号权限 skill；欠费、配额、限流和库存转计费 skill；具体 ECS/TOS/CDN/KMS/大模型等产品业务错误转对应产品 skill；本 skill 保留 API 调用证据并判断是机制问题还是产品问题。
- 工具优先级：默认 CLI-first，只用 `ve` 和 `tosutil` 的只读命令确认调用主体、API 网关、云控制 API 或产品只读入口；复杂签名复现优先用 API Explorer 和用户提供的脱敏请求信息说明，只有需要多接口联动或结构化解析时才引入受支持 Python SDK 脚本。
- 数据来源：手册、`cli-meta/火山引擎 OpenAPI _ SDK _ CLI 问题排查手册/`、`产品官方文档/火山引擎 OpenAPI SDK CLI 问题排查手册/`、`cli/volcengine-cli`、`python-sdk/volcengine-python-sdk`、`python-sdk/volc-sdk-python`。
- 安全边界：默认只读；不配置、不落盘、不打印 AK/SK/SessionToken、Authorization、CanonicalRequest 中的完整敏感 header、签名值或业务敏感请求体。

## 先读这些

- `references/query-cli-catalog.md`：按问题域定位最小只读命令集合。
- `references/api-coverage-matrix.md`：本分类 `cli-meta/` API 覆盖审查矩阵，列出已纳入排障候选的只读/诊断 Action 与默认排除的写操作边界。
- `references/python-sdk-script-patterns.md`：什么时候才需要 Python 脚本，以及脚本凭证规范。
- `references/01-overview-routing/README.md`：总入口、信息收集和横向跳转。
- 当前首版没有可执行 `scripts/`；不要调用 `RunSkillScript`，除非后续 reference 明确提供了具体脚本文件名。

同时可查：

- 产品手册：`火山引擎问题排查手册/火山引擎OpenAPI-SDK-CLI问题排查手册/README.md`
- 接口元数据：`cli-meta/火山引擎 OpenAPI _ SDK _ CLI 问题排查手册/<产品>/接口清单.md`
- 官方文档：`产品官方文档/火山引擎 OpenAPI SDK CLI 问题排查手册/<产品>/...`

## 使用边界

Use this skill when the user describes:

- `SignatureDoesNotMatch`、`InvalidCredential`、`InvalidAccessKeyId`、STS 临时凭证签名失败、时间偏差、Host/Region/Service 签名不一致。
- `InvalidParameter`、`MissingParameter`、`InvalidAction`、`InvalidActionOrVersion`、Action/Version/Endpoint/Region 不匹配。
- `volc-sdk-python` / `volcengine-python-sdk` 安装、导入、初始化、Region/Endpoint 配置、异常封装、序列化、超时、重试、HTTP 200 但业务 code 失败。
- `ve` / `tosutil` CLI、API Explorer 调用不一致，命令参数、`--body` JSON、shell 转义、代理、TLS/证书链、超时问题。
- API 网关鉴权、消费者、Credential、CustomDomain、Gateway、Service、Upstream、Route 查询和转发链路诊断。
- 云控制 API 资源发现和 OpenAPI 错误归因。
- 需要用 RequestId/LogId、HTTP 状态码、ResponseMetadata 做标准化定位。

Do not use this as the primary skill for:

- 明确是某个产品资源状态、网络、安全组、对象存储、CDN、KMS、短信、RTC、大模型等业务语义：转对应产品 skill。
- 纯 IAM 权限策略、子用户、角色、AK 创建/禁用/轮转：转账号权限 skill。
- 欠费、余额、账单、配额、库存、API 频控额度：转计费 skill。
- 需要立即执行创建、修改、删除、发布、部署、绑定、解绑、刷新、启停等变更：必须 Human-in-the-Loop，通常转对应产品 skill。

## 强约束

- 默认只执行 `Describe/List/Get/Query/Check` 类查询。
- 公共 CLI 命令统一写成 `ve <service> <Action> [--body '<json>' | --Param value]`；如果 `cli-meta` 中写的是 `volcengine`，在本 skill 中统一转成 `ve`。
- 不运行 `ve configure`、`ve login`、`ve logout`、`ve sso` 等会写配置、登录或变更资源的命令。
- 不要求用户粘贴完整 AK/SK/Token，不把凭证写入文件、配置、报告或日志；新脚本优先读取 `VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、`VOLCENGINE_SESSION_TOKEN`，兼容旧环境变量由平台负责。
- 签名排查只要求用户提供脱敏后的关键字段：Method、Host、Path、Query key、SignedHeaders key、Body hash、Region、Service、Action、Version、时间戳、RequestId。
- API Gateway 的 `GetJwtToken`、身份服务的 `GetRoleCredentials`、`GetResourceApiKey` 等可能返回敏感材料的接口，默认不执行；若用户明确需要，必须先说明脱敏策略。
- 首版没有可执行脚本；不要猜测或调用 `scripts/sts_get_caller_identity.py`、`scripts/signature_check.py` 等不存在的脚本。身份验证直接使用 `ve sts GetCallerIdentity`。

## 交互式确认与 Human-in-the-Loop

| 动作类型 | 示例 | 确认要求 |
|---|---|---|
| 凭证配置/登录 | `ve configure`、`ve login`、`ve sso` | 说明会写本地配置或缓存凭证，等待明确确认 |
| API 网关变更 | `CreateGateway`、`UpdateRoute`、`CreateConsumerCredential`、`AttachGatewayLB` | 说明网关、路由、消费者、上游和影响流量 |
| 云控制 API 变更 | `CreateResource`、`UpdateResource`、`DeleteResource`、`RunPipeline` | 说明资源类型、工作空间、变更内容和回滚方式 |
| 敏感数据读取 | JWT、RoleCredentials、ResourceApiKey、完整请求头/签名串 | 说明脱敏字段，禁止完整回显 |

## 快速路由

| 用户现象 | 优先证据 | 必读 reference |
|---|---|---|
| 不确定是签名、参数、Python SDK、CLI 还是产品业务错误 | Method、URL、Action、Version、Service、Region、Code、RequestId | [`01-overview-routing/README.md`](references/01-overview-routing/README.md) |
| Action/Version/Endpoint/Region 不匹配 | Service、Action、Version、Endpoint、Region、API 文档版本 | [`02-openapi-call-model/README.md`](references/02-openapi-call-model/README.md) |
| `SignatureDoesNotMatch` / `InvalidCredential` | Host、Region、Service、时间戳、SignedHeaders、Body hash、STS token 是否参与签名 | [`03-auth-signature/README.md`](references/03-auth-signature/README.md) |
| `InvalidParameter` / `MissingParameter` / 序列化错误 | 参数名、参数值、Content-Type、Query/Body 位置、SDK 模型字段 | [`04-parameters-version/README.md`](references/04-parameters-version/README.md) |
| SDK 初始化、导入、超时、异常封装 | Python SDK 名称版本、语言运行时、Region/Endpoint、异常对象、ResponseMetadata | [`05-sdk-runtime/README.md`](references/05-sdk-runtime/README.md) |
| CLI/API Explorer 不一致 | `ve --help`、`tosutil help`、`--body` JSON、shell 转义、代理、TLS、环境变量 | [`06-cli-api-explorer/README.md`](references/06-cli-api-explorer/README.md) |
| 只有 RequestId/HTTP 状态码/错误码 | HTTP status、Code、Message、RequestId、LogId、发生时间 | [`07-errorcode-requestid/README.md`](references/07-errorcode-requestid/README.md) |
| API 网关、云控制 API | Gateway/Route/Upstream/Workspace/Resource 配置 | [`08-api-gateway-cloudcontrol-iac/README.md`](references/08-api-gateway-cloudcontrol-iac/README.md) |
| 高频错误需要固定卡片 | 原始错误文本 | [`09-playbooks/README.md`](references/09-playbooks/README.md) |

## 高频固定流程

### SignatureDoesNotMatch

1. 先确认当前调用入口：Python SDK、`ve`/`tosutil` CLI、手写 HTTP 请求或 API Explorer。
2. 只读验证当前凭证可用性：`ve sts GetCallerIdentity`。
3. 核对签名四元组：Service、Region、Host、Endpoint。
4. 核对时间戳、SignedHeaders、Body hash、Query 编码和 STS token 是否参与签名。
5. 如果当前 caller 与预期身份不一致，转账号权限 skill；如果签名正确但产品返回业务错误，转产品 skill。

### InvalidAction / InvalidActionOrVersion

1. 抽取 Action、Version、Service、Endpoint、Region。
2. 用 `ve <service> <Action> --help` 验证 CLI 元数据是否存在该 Action。
3. 如果 CLI 不支持但官方文档支持，记录 Python SDK/CLI 版本差异，建议升级工具或用 API Explorer 兜底。
4. 如果 Action 属于另一个 Service 或 Version，修正路由。

### CLI 参数错误

1. 先读 `ve <service> <Action> --help`。
2. 判断该 Action 使用展开参数还是 `--body '<json>'`。
3. 对复杂对象/数组优先用 `--body`，并要求 JSON 引号和 shell 转义正确。
4. CLI 能跑通后，再把参数映射回 Python SDK 或用户提供的手写 HTTP 请求。

### API 网关鉴权/转发失败

1. 先查 `apig ListGateways` 定位网关和状态。
2. 有 Gateway ID 后查 `GetGateway`、`ListGatewayServices`、`ListUpstreams`、`ListCustomDomains`、`ListPluginBindings`。
3. 路由问题查 `apig20221112 ListRoutes` / `GetRoute`。
4. 后端网络、CLB、域名证书或 WAF 命中转对应产品 skill。

## 章节目录

| 上层章节 | 本 skill reference |
|---|---|
| 1. 排查总入口 | [`01-overview-routing/README.md`](references/01-overview-routing/README.md) |
| 2. OpenAPI 基础调用模型 | [`02-openapi-call-model/README.md`](references/02-openapi-call-model/README.md) |
| 3. 鉴权与签名 | [`03-auth-signature/README.md`](references/03-auth-signature/README.md) |
| 4. 参数与接口版本 | [`04-parameters-version/README.md`](references/04-parameters-version/README.md) |
| 5. SDK 问题 | [`05-sdk-runtime/README.md`](references/05-sdk-runtime/README.md) |
| 6. CLI / API Explorer 问题 | [`06-cli-api-explorer/README.md`](references/06-cli-api-explorer/README.md) |
| 7. 错误码与日志定位 | [`07-errorcode-requestid/README.md`](references/07-errorcode-requestid/README.md) |
| 8. API 网关 / 云控制 API | [`08-api-gateway-cloudcontrol-iac/README.md`](references/08-api-gateway-cloudcontrol-iac/README.md) |
| 9. 高频 Playbook | [`09-playbooks/README.md`](references/09-playbooks/README.md) |

## 工作流

1. 收集入口、Method、Host、Path、Action、Version、Service、Region、Endpoint、HTTP status、Code、Message、RequestId、Python SDK/CLI 版本、发生时间。
2. 先判断机制层：身份/签名、Action/Version、参数、Python SDK/CLI、API Gateway、服务端错误。
3. 打开 `query-cli-catalog` 后只读取当前问题需要的章节 reference。
4. 用最小只读命令确认调用身份、API Gateway/云控制 API 资源或工具元数据。
5. 将 API 机制证据和产品语义分开输出；产品语义明确后跳转对应 skill。

## 输出格式

- `现象归类`
- `调用链路`
- `已查证据`
- `结论`
- `建议动作`
- `横向跳转`
