# 排查总入口

用于先回答“失败发生在 API 调用机制、工具链、API 网关/IaC，还是具体产品业务”。

## 前置输入

- 调用入口：OpenAPI、Python SDK、`ve`/`tosutil` CLI、手写 HTTP 请求、API Explorer、API Gateway。
- Method、Host、Path、Action、Version、Service、Region、Endpoint。
- HTTP status、Code、Message、RequestId、LogId、发生时间。
- Python SDK/CLI 版本、语言运行时、是否使用代理、是否使用 STS。

## 命令包

```text
ve sts GetCallerIdentity
ve iam GetAccountSummary
```

关注字段：

- `AccountId`、`IdentityId`、`IdentityType`、`Trn`：当前凭证代表谁。
- 账号摘要：用于判断当前凭证是否能访问 IAM 摘要；权限细节转账号权限 skill。

真实验证提示：`GetCallerIdentity` 无参数。CLI 在本地或沙箱里可能先输出用户目录配置文件读取告警，只要后续 JSON 正常返回，不影响环境变量凭证查询。

## 先判断方向

| 现象 | 下一步 |
|---|---|
| `SignatureDoesNotMatch`、`InvalidCredential` | 进 `03-auth-signature` |
| `InvalidAction`、`InvalidActionOrVersion`、Endpoint/Region 不确定 | 进 `02-openapi-call-model` |
| `InvalidParameter`、`MissingParameter`、序列化失败 | 进 `04-parameters-version` |
| SDK 初始化、导入、超时、异常对象不清楚 | 进 `05-sdk-runtime` |
| CLI/API Explorer 不一致 | 进 `06-cli-api-explorer` |
| 只有 HTTP 状态码、RequestId、InternalError | 进 `07-errorcode-requestid` |
| API Gateway、云控制 API | 进 `08-api-gateway-cloudcontrol-iac` |
| 产品业务 code 明确 | 带上 API 证据转对应产品 skill |

## 结果解读

| 证据 | 常见结论/下一步 |
|---|---|
| 当前 caller 与用户预期不一致 | 先转账号权限 skill 修正身份或凭证 |
| Action/Version/Service 缺失 | 先补齐四元组，无法直接判断产品问题 |
| RequestId 存在但 Code 是产品业务错误 | 保留 RequestId 后转产品 skill |
| API Explorer 成功但本地失败 | 优先排 CLI/Python SDK 参数、代理、签名、环境变量 |
| CLI 成功但 SDK 失败 | 排 SDK 初始化、版本、序列化、异常处理 |
