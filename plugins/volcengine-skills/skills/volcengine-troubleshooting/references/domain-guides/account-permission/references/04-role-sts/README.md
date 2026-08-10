# 角色与 STS 授权

用于处理 `AssumeRole`、`RoleNotExist`、服务角色缺失、临时凭证权限不足。

## 前置输入

- RoleName / RoleArn。
- 调用主体、目标角色、失败 Action、临时凭证到期时间。

## 命令包

```text
ve sts GetCallerIdentity
ve iam ListRoles --Limit 20
ve iam GetRole --RoleName <role-name>
ve iam ListAttachedRolePolicies --RoleName <role-name>
```

## 关注字段

- 目标角色是否存在。
- 当前 caller 是否是预期主体。
- 当前账号下是否能枚举到同名/近似角色，帮助区分“确实不存在”与“角色名/账号写错”。
- 角色信任策略是否允许当前主体扮演。
- 角色附加策略是否覆盖后续目标 Action。

## 结果解读

| 证据 | 常见结论 |
|---|---|
| `ListRoles` 中找不到目标角色 | 角色很可能不存在，或目标账号不是当前账号 |
| `GetRole` 查不到 | Role 不存在或名字/账号错 |
| Role 存在但 `AssumeRole` 被拒绝 | 查 caller 权限和信任策略 |
| AssumeRole 成功但后续产品 Action 被拒绝 | 角色自己的权限策略不足 |

## 典型 case

```text
Action: AssumeRole
Service: sts
AccessDenied
```

```text
RoleNotExist: Role 'trn:iam::ACCOUNT_ID:role/ServiceRoleForVolcObserve' does not exist
```
