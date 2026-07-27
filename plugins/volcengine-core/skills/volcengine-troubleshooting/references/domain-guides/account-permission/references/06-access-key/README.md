# API Key / AccessKey 管理权限

用于处理创建密钥、查看密钥列表、密钥归属、密钥最近使用。

## 前置输入

- 当前主体、目标 UserName、AccessKeyId（可脱敏）。
- 用户说的是 Ark API Key、AccessKey，还是 STS Token。

## 命令包

```text
ve iam ListAccessKeys --UserName <user-name>
ve iam GetAccessKeyLastUsed --AccessKeyId <access-key-id>
```

安全输出要求：

- 不要把 `ListAccessKeys` 的原始 JSON 整段贴给用户。
- `AccessKeyId` 必须脱敏展示，例如 `AKLT...9DGM` 或 `****9DGM`；如需定位多把密钥，只展示状态、UserName、创建时间、最近使用时间和脱敏后的短标识。
- 任何 `SecretAccessKey`、`SecretKey`、会话 Token 或用户提供的测试密钥都不得出现在回答、日志摘录、benchmark 报告或本地文档中。

## 结果解读

| 证据 | 常见结论 |
|---|---|
| 用户把 Ark API Key 和 AccessKey 混用 | 先纠正密钥类型 |
| 当前主体无权管理他人 AccessKey | IAM 管理权限不足 |
| AccessKey 不属于当前账号 | 凭证归属不一致 |

真实验证提示：

- `ListAccessKeys` 可返回 `AccessKeyId`、`Status`、`UserName` 等字段。
- 输出给用户时必须对 `AccessKeyId` 脱敏，只保留前 4 位和后 4 位或仅保留末 4 位；不要粘贴完整 `AccessKeyMetadata`。
- `GetAccessKeyLastUsed` 返回最近使用的 `Service`、`Region`、`RequestTime`，可帮助判断密钥是否仍在使用。

## 变更边界

不执行 `CreateAccessKey`、`DeleteAccessKey`、`UpdateAccessKey`。密钥轮转属于高敏操作，必须确认。
