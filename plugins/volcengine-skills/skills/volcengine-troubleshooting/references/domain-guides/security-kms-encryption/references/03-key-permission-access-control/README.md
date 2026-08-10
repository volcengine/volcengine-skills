# 密钥权限与访问控制

用于密钥无权限、KMS Action AccessDenied、资源级授权不匹配、STS 角色调用失败等问题。

## 前置输入

- 调用主体：主账号、子用户、角色、STS。
- Action：如 `DescribeKey`、`Encrypt`、`Decrypt`、`GetSecretValue`。
- KeyID / KeyringName / SecretName。
- 错误码、RequestId。

## 命令包

### 1. 先确认密钥是否存在

```text
ve kms DescribeKey --body '{"KeyID":"<key-id>"}'
```

### 2. 查询密钥标签辅助判断资源范围

```text
ve kms ListTagsForResources --body '{"ResourceIds":["<key-id>"]}'
```

### 3. 查询 keyring 范围

```text
ve kms DescribeKeyrings --body '{"CurrentPage":1,"PageSize":10}'
```

## Agent 使用方式

- 如果 `DescribeKey` 本身 AccessDenied：优先转账号权限 skill，检查调用主体是否有 `kms:DescribeKey` 和资源范围。
- 如果 `DescribeKey` 成功但 `Encrypt/Decrypt` AccessDenied：密钥存在，权限缺在数据面 Action 或资源级授权。
- 如果使用 STS：记录 Role、SessionName、过期时间，不要求用户粘贴 token。

## 结果解读

| 证据 | 常见结论 |
|---|---|
| key 不存在 | 不是权限问题，先修正 Region/KeyID |
| key 存在，查询成功，数据面失败 | 缺 `Encrypt` / `Decrypt` / `GenerateDataKey` 等 Action |
| 只有某个 key 失败 | 资源级授权或 keyring 范围不匹配 |
| STS 过期或无权限 | 转账号权限 skill 查角色和临时凭证 |

## 变更边界

本 ref 不修改 IAM 策略，不授权 key，不修改 key policy。权限变更必须转账号权限 skill 并要求人工确认。
