# 6. L5 行业应用与垂直场景排查

用于语音、RAG/知识库、AI IDE、智能客服、行业 Agent、图像/视频/音视频理解等场景化问题。

## 场景入口

| 场景 | 优先证据 |
|---|---|
| TTS/ASR/实时语音 | AppId、Cluster、ResourceId、VoiceType/Speaker、协议、错误码 |
| RAG/知识库检索 | 知识库 ID、Collection、Index、Embedding/Rerank 模型、构建任务 |
| AI IDE / Coding Assistant | Trae 版本、本地模型配置、订阅、错误日志 |
| 智能客服/行业 Agent | Agent ID、工具、知识库、模型、会话 ID、任务链路 |
| 图像/视频生成 | 模型、任务 ID、输入图片/文本摘要、token/尺寸/格式限制 |

## RAG / VikingDB 命令包

必须使用 `--body` 传分页参数。不要写成 `--PageSize 5` 或 `--PageNumber 1`。
在执行下面命令前，Agent 必须已经读取本 reference 或 `query-cli-catalog.md`，避免 RunSkillCLI 因命令不在当前 skill context 中被拒绝。

```text
ve vikingdb ListVikingdbCollection --body '{"PageNumber":1,"PageSize":5}'
ve vikingdb ListVikingdbIndex --body '{"PageNumber":1,"PageSize":5}'
ve vikingdb ListVikingdbTask --body '{"PageNumber":1,"PageSize":5}'
```

关注字段：

- Collection/Index 是否存在、状态是否可检索。
- 构建任务是否失败、排队或未完成。
- Embedding/Rerank 模型不可用时回到方舟模型开通和权限。

## 语音场景

豆包语音、音频技术的 CLI 覆盖有限，不要伪造命令。优先要求：

- 脱敏错误响应、RequestId、发生时间。
- AppId、Cluster、VoiceType/Speaker、ResourceId、音频格式、WebSocket/HTTP 调用方式。
- Python SDK 名称和版本。

常见判断：

- `resource ID is mismatched with speaker related resource`：资源 ID 和 speaker/音色不属于同一资源或未开通。
- WebSocket 断连：先看鉴权、协议、网络代理、心跳和音频格式。
- 鉴权错误：区分语音产品 token/API Key 与 AK/SK。

## 图像/视频/多模态

`cv20240606` 多数接口会提交任务或生成内容，可能消耗额度。默认只解释限制和要求用户提供任务 ID/错误响应，不自动发起生成。已有任务结果读取也需要确认不泄露图片/视频内容。

## 结果解读

| 现象 | 下一步 |
|---|---|
| 知识库无召回 | 先查 VikingDB 资源和构建任务，再查 Embedding/Rerank |
| 语音 resource ID 不匹配 | 核对 ResourceId、Speaker、VoiceType 和开通关系 |
| AI IDE 模型不可用 | 回到 Coding Plan 和方舟模型映射 |
| 多模态 token 超限 | 转 L1 模型能力，减少图片/文本或换模型 |

## 方舟模型开通关联

- VikingDB 资源状态正常，只能说明存储/索引层没有直接异常，不能自动证明 Embedding/Rerank 模型已开通或未开通。
- 未过滤的 `ve ark ListEndpoints` 首页只是样本，不可据此断言某类模型未开通。
- 需要用户提供准确的模型 ID、Endpoint ID 或错误码后，再回到 `03-l2-ark-maas` 做方舟侧确认。
- 如果只有 `ModelNotOpen`、`InvalidEndpointOrModel.NotFound`、`AuthenticationError` 等错误文本，先按 `08-playbooks` 判断，再转权限/计费/OpenAPI skill。
