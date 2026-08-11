# 排查总入口

用于先回答“当前是谁在调用、失败发生在哪一层”。

## 前置输入

- 错误码、原始错误文本、RequestId、发生时间。
- Service、Action、Resource、Region、Project。
- 用户自述身份：主账号、IAM 子用户、Role、STS、服务角色。

## 命令包

```text
ve sts GetCallerIdentity
ve iam GetAccountSummary
```

关注字段：

- `AccountId` / `IdentityType` / `Trn`：当前凭证代表谁。
- IAM 账号摘要：用户、组、角色、策略数量是否符合预期。

真实验证提示：`GetCallerIdentity` 的当前返回字段为 `AccountId`、`IdentityId`、`IdentityType`、`Trn`。CLI 在本地可能先输出用户目录配置文件读取告警，只要后续 JSON 正常返回，不影响环境变量凭证查询。

## 先判断方向

| 现象 | 下一步 |
|---|---|
| 认证/风控错误文本 | 进 `02-account-verification-risk` |
| `AccessDenied` 且有明确用户 | 进 `03-iam-user-policy` |
| `AssumeRole` / `RoleNotExist` | 进 `04-role-sts` |
| 产品 Action 被拒绝 | 进 `05-product-resource-access` |
| 创建/查看 AccessKey 失败 | 进 `06-access-key` |

## 结果解读

| 证据 | 常见结论 |
|---|---|
| 当前 caller 与用户以为的身份不同 | 先修正凭证/主体，再谈授权 |
| 没有 Action / Resource | 证据不足，先补失败 API 和资源范围 |
| 产品 Action 明确 | 保留产品 skill 入口，本 skill 只补权限链 |
