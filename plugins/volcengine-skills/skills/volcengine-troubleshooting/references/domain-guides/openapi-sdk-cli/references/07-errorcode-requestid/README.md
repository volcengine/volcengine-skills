# 错误码与 RequestId 定位

用于用户只有 HTTP 状态码、Code、Message、RequestId 或 LogId 时的标准化定位。

## 前置输入

- HTTP status、Code、Message。
- RequestId、LogId、发生时间、Region、Service、Action、Version。
- 调用入口：Python SDK、CLI、手写 HTTP 请求、API Explorer。

## 判断表

| HTTP / Code | 优先方向 |
|---|---|
| 400 + `InvalidParameter` / `MissingParameter` | 参数与接口版本 |
| 401 + 认证失败 | 签名、Token、代理认证、API Key |
| 403 + `AccessDenied` | 账号权限 skill |
| 404 + `InvalidAction` / `NotFound` | Action/Version 或资源不存在 |
| 429 / Throttling | 计费/配额/限流 skill |
| 5xx / `InternalError` | 保留 RequestId、时间、Region，建议重试并上送后台定位 |

## RequestId 使用方式

- RequestId 必须和时间、Region、Service、Action 一起记录。
- SDK 异常中如果包含 ResponseMetadata，优先提取其中的 RequestId。
- 不要只凭 HTTP status 下结论，必须结合业务 Code。

## 输出建议

当无法本地复现时，输出应包含：

- 调用入口和四元组。
- HTTP status、Code、Message。
- RequestId/LogId 和时间。
- 已排除的机制问题。
- 建议用户带这些信息提交工单或转产品 skill。
