# 7. 横切专题排查

用于鉴权、权限、开通、参数、限流、计费、网络、服务端错误等跨层机制问题。

## 横向分工

| 机制 | 保留的大模型上下文 | 转向 |
|---|---|---|
| AK/SK、IAM、AccessDenied、STS | 产品、model/Endpoint、RequestId、Action | 账号权限 skill |
| 余额、订阅、额度、配额、429 | 模型、Endpoint、QPS/TPM、时间窗口 | 计费 skill |
| 签名、Action/Version、Python SDK/CLI 参数 | Service、Action、Version、Region、Endpoint | OpenAPI / SDK / CLI skill |
| VPC、代理、TLS、DNS、WebSocket 网络 | 调用入口、域名、错误、时间 | 计算网络或域名 CDN skill |
| 服务端错误、InternalServiceError | RequestId、时间、Region、产品和模型 | 先产品证据，必要时升级工单 |

## 高频机制判断

### 鉴权

- 方舟 OpenAI 兼容 API Key 不等于 AK/SK。
- 控制面 `ve` CLI 使用 AK/SK 或 STS。
- 不要求用户贴完整密钥，只看脱敏格式和错误响应。

### 权限和开通

- 资源存在但调用报无权限：账号/IAM 或模型授权。
- Endpoint 查不到：可能是 Region/ProjectName/账号错误，也可能是权限不足。
- 模型未开通：先用方舟证据确认，再转权限/开通。

### 参数和模型能力

- 参数报错不一定是 SDK 问题，可能是模型能力不支持。
- OpenAI 兼容请求字段和方舟兼容层字段要单独核对。

### 限流和计费

- 429 可能是瞬时限流、RPM/TPM、并发、账号额度、订阅或欠费。
- 不做压测，不发起额外推理请求。

### 服务端错误

- `InternalServiceError` 要收集 RequestId、时间、Region、模型/Endpoint、输入规模。
- 如果只有偶发错误，先建议重试策略和最小复现；持续错误需要升级工单。

## 输出要求

- 先说明大模型生态层级，再说明横向机制。
- 不把横向 skill 当成替代，而是带着上下文跳转。
- 对敏感输入只描述结构和脱敏摘要。
