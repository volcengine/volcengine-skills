# 密钥生命周期与云加密机

用于密钥禁用、待删除、轮转、归档、专属密钥库、自带密钥材料、云加密机 Secret 等问题。

## 前置输入

- KeyID / KeyName / KeyringName
- KeyState、Rotation、DeletionWindow
- CustomKeyStoreID、SecretName
- 发生时间、RequestId

## 命令包

### 1. 查询密钥状态

```text
ve kms DescribeKey --body '{"KeyID":"<key-id>"}'
```

关注字段：

- 状态：Enabled / Disabled / PendingDeletion / Archived。
- KeySpec、KeyUsage、Origin。
- 轮转或主地域信息。

### 2. 查询专属密钥库

```text
ve kms DescribeCustomKeyStores --body '{}'
```

### 3. 查询 Secret / 云加密机元数据

```text
ve metakms DescribeSecrets --body '{}'
ve metakms DescribeSecret --body '{"SecretName":"<secret-name>"}'
```

## 结果解读

| 证据 | 常见结论 |
|---|---|
| Disabled | 调用失败符合预期，需确认是否允许启用 |
| PendingDeletion | 删除等待期内不可按普通密钥使用，恢复需确认 |
| 轮转后失败 | 调用方缓存 KeyID/版本或上下文处理异常 |
| CustomKeyStore 异常 | 专属密钥库/HSM 连通或状态问题 |
| metakms Secret 不存在 | SecretName/地域/产品混用 |

## 变更边界

启用、禁用、轮转、取消删除、导入密钥材料、连接/断开专属密钥库均为高风险动作，必须确认。
