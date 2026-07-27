# 鉴权与签名

用于排查 AK/SK、STS、签名、时间偏差、Host/Region/Service 不一致导致的认证失败。

## 前置输入

- 错误码：`SignatureDoesNotMatch`、`InvalidCredential`、`InvalidAccessKeyId`、`AuthFailure`。
- Method、Host、Path、Query key、SignedHeaders key、Content-Type、Body hash。
- Region、Service、Action、Version、时间戳。
- 是否使用 STS 临时凭证，以及是否传入 SessionToken。

## 命令包

```text
ve sts GetCallerIdentity
ve iam GetAccessKeyLastUsed --AccessKeyId <access-key-id>
```

关注字段：

- `GetCallerIdentity`：当前 AK/SK 是否能完成基础签名调用。
- `GetAccessKeyLastUsed`：只在用户提供 AK ID 且允许查询时使用；不要要求或输出 SK。

不要调用脚本。本 skill 首版没有签名校验脚本，基础签名链路验证直接执行 `ve sts GetCallerIdentity`。

## 签名排查顺序

1. 确认当前 caller 是否为预期账号/子用户/角色。
2. 核对 Host、Service、Region 是否一致；Region 写错会导致签名不匹配。
3. 核对请求时间与本地时钟，尤其容器、CI、离线环境。
4. 核对 Query 编码和排序，空值、数组、特殊字符是否按文档处理。
5. 核对 Body 是否参与签名，JSON 是否被 Python SDK、CLI 或手写 HTTP 请求二次改变。
6. STS 临时凭证必须带 SessionToken，并参与对应签名/请求头。

## 结果解读

| 证据 | 常见结论/下一步 |
|---|---|
| `GetCallerIdentity` 成功但业务 API 签名失败 | 通用凭证有效，重点查 Service/Region/Host/Body/Query |
| `GetCallerIdentity` 也失败 | 凭证或环境变量有问题，转账号权限 skill |
| 手写 HTTP 请求失败但 CLI 成功 | 自己构造签名错误，建议用 API Explorer 或受支持 Python SDK 最小示例对照 |
| SDK 失败但 CLI 成功 | 查 SDK 初始化、Endpoint、Region、STS token 注入 |
| `AccessDenied` 而非签名错误 | 转账号权限 skill，不在本章节深挖授权策略 |

## 安全边界

- 不输出 AK/SK、SessionToken、Authorization、Signature。
- 不要求用户贴完整 CanonicalRequest；只收脱敏字段和字段名。
- 不运行 `sts AssumeRole`，除非用户明确确认且不会回显临时凭证。
