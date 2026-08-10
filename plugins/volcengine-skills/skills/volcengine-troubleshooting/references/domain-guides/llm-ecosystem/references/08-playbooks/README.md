# 8. 高频问题 Playbook

用于命中固定错误文本时快速进入标准排障卡片。每张卡片都应先识别层级，再给只读证据和下一步动作。

## Playbook 索引

| Playbook | 所属层级 | 首选检查 |
|---|---|---|
| ModelNotOpen 模型未开通 | L2 + 横切权限/开通 | `ark ListEndpoints` / 模型开通关系 |
| InvalidEndpointOrModel | L2 | Endpoint、model 字段、Region、ProjectName |
| AuthenticationError / API key | 横切鉴权 | 区分 Ark API Key 与 AK/SK |
| AccessDenied | 横切权限 | 带模型/Endpoint 上下文转账号权限 |
| InvalidParameter | L1 + OpenAPI | 参数和模型能力、SDK 字段 |
| RateLimit / Quota / 429 | 横切计费/限流 | 时间窗口、QPS/TPM、订阅/额度 |
| Coding Plan / ArkClaw | L3 | ArkClaw 实例、订阅、模型名映射 |
| TTS resource ID mismatched | L5 语音 | ResourceId、Speaker、VoiceType、开通关系 |
| Multimodal token exceed | L1 + L5 | token、图片数量、模型上下文 |
| Embedding/Rerank unavailable | L2 + L5 RAG | 方舟模型、VikingDB Collection/Index |
| InternalServiceError | 横切服务端 | RequestId、时间、Region、最小复现 |
| InfoMissing 信息不足 | 总入口 | 最少必要字段追问 |

## 卡片细则

### ModelNotOpen

```text
ve ark ListEndpoints --body '{"PageNumber":1,"PageSize":10}'
```

判断：

- 如果模型/Endpoint 不在列表中，先确认账号、Region、ProjectName。
- 如果存在但报未开通，保留证据后转权限/开通。

### InvalidEndpointOrModel

```text
ve ark GetEndpoint --body '{"Id":"<endpoint-id>"}'
```

判断：

- 用户传入的是模型 ID 还是 Endpoint ID。
- OpenAI 兼容调用中 `model` 字段是否符合方舟要求。

### AuthenticationError

判断：

- Ark API Key 格式错误或未绑定正确资源。
- AK/SK 签名问题转 OpenAPI / SDK / CLI skill。
- 不读取或回显完整 API Key。

### RateLimit / Quota

判断：

- 不发起压测。
- 需要用户提供发生时间窗口、QPS/TPM、模型、Endpoint 和 RequestId。
- 订阅、额度、欠费转计费 skill。

### Coding Plan / ArkClaw

```text
ve arkclaw ListClawOmniInstances --PageNumber 1 --PageSize 10
```

判断：

- `Unknown model` 先检查模型名映射和订阅。
- 实例状态异常只做只读说明，不执行命令。

### TTS resource ID mismatched

判断：

- ResourceId、Speaker、VoiceType 不匹配或资源未开通。
- 语音产品 CLI 覆盖不足，依赖官方文档和用户脱敏错误响应。

### Embedding / Rerank

```text
ve vikingdb ListVikingdbCollection --body '{"PageNumber":1,"PageSize":5}'
ve vikingdb ListVikingdbIndex --body '{"PageNumber":1,"PageSize":5}'
```

判断：

- Collection/Index 正常但模型不可用：回方舟模型开通。
- 构建任务失败：继续查 `ListVikingdbTask`。
- 不要因为未过滤的方舟 Endpoint 首页没有出现 Embedding/Rerank 就下结论；必须结合准确模型/Endpoint、过滤查询、错误码或控制台证据。
