# 3. L2 火山方舟 MaaS 平台排查

用于火山方舟 Endpoint、模型开通、API Key、OpenAI 兼容调用、批量推理、异步推理、精调和方舟知识库问题。

## 前置输入

- Region、ProjectName、Endpoint ID、model id、RequestId、发生时间。
- 调用方式：受支持 Python SDK、OpenAI 兼容请求、控制台、ve CLI。
- 错误码：`ModelNotOpen`、`InvalidEndpointOrModel.NotFound`、`AuthenticationError`、`InvalidParameter`、`429`。

## 命令包

### Endpoint 和模型绑定

```text
ve ark ListEndpoints --body '{"PageNumber":1,"PageSize":10}'
ve ark ListEndpoints --body '{"PageNumber":1,"PageSize":10,"Filter":{"Ids":["<endpoint-id>"]}}'
ve ark GetEndpoint --body '{"Id":"<endpoint-id>"}'
```

关注字段：

- Endpoint 是否存在，状态是否可用。
- 绑定模型、模型版本、项目和标签。
- 用户传入 OpenAI `model` 字段是否应为 Endpoint ID。

### 批量推理和精调

```text
ve ark ListBatchInferenceJobs --body '{"PageNumber":1,"PageSize":10}'
ve ark ListModelCustomizationJobs --body '{"PageNumber":1,"PageSize":10}'
```

关注字段：

- Job 阶段、失败原因、创建时间和绑定模型。
- 精调后的模型是否已发布或可被 Endpoint 绑定。

## 敏感边界

- 不默认执行 `ve ark GetApiKey`，避免读取或回显 API Key。
- 不发起 ChatCompletions 或生成调用，除非用户确认可以消耗额度。
- 不创建、删除、停止、恢复 Endpoint 或精调任务。

## 结果解读

| 证据 | 常见结论 |
|---|---|
| Endpoint 查不到 | ID、Region、ProjectName、账号或权限错误 |
| Endpoint 存在但模型未开通 | 模型开通/授权问题，转账号权限或 Playbook |
| API Key 报错但控制面 CLI 可用 | 区分 Ark API Key 与 AK/SK，转横切鉴权 |
| 批量/精调任务失败 | 先输出任务阶段和失败原因，再判断是否需工单 |
