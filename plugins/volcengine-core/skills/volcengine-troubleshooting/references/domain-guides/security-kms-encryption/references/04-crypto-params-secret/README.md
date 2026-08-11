# 加密/解密参数与 Secret

用于 `KMSEncryptFailed`、Plaintext 参数非法、密文无法解密、加密上下文不一致、Secret 元数据异常。

## 前置输入

- 错误文本：`InvalidParameter`、`InvalidEncryptedContent`、`InvalidCiphertext` 等。
- KeyID、算法、加密上下文是否使用。
- SecretName、SecretVersion。
- Python SDK/CLI 调用方式和 RequestId。

## 只读命令包

### 1. 查询密钥状态

```text
ve kms DescribeKey --body '{"KeyID":"<key-id>"}'
```

### 2. 查询非对称公钥

```text
ve kms GetPublicKey --body '{"KeyID":"<key-id>"}'
```

仅用于确认 key 类型和公钥元数据，不输出业务私密材料。

### 3. 查询 Secret 元数据

```text
ve kms DescribeSecrets --body '{"CurrentPage":1,"PageSize":10}'
ve kms DescribeSecret --body '{"SecretName":"<secret-name>"}'
ve kms DescribeSecretVersions --body '{"SecretName":"<secret-name>"}'
```

云加密机 / metakms Secret：

```text
ve metakms DescribeSecrets --body '{}'
ve metakms DescribeSecret --body '{"SecretName":"<secret-name>"}'
ve metakms DescribeSecretVersions --body '{"SecretName":"<secret-name>"}'
```

## 不默认自动执行

以下命令会处理敏感材料，不能作为首轮自动查询：

```text
ve kms Encrypt
ve kms Decrypt
ve kms GenerateDataKey
ve kms GetSecretValue
ve metakms GetSecretValue
```

只有用户明确要求并确认脱敏方式后，才允许继续。

## 结果解读

| 证据 | 常见结论 |
|---|---|
| Plaintext invalid | 明文编码、长度或类型不符合 API 要求 |
| InvalidEncryptedContent | CiphertextBlob 不完整、不是同一密钥产生、被错误转码 |
| 加密上下文不一致 | 加密和解密时的 context 不一致 |
| key 类型不匹配 | 对称/非对称、签名/加密用途混用 |
| Secret 元数据存在但取值失败 | 权限、版本状态或 SecretValue 敏感读取边界 |

## 变更边界

不输出 SecretValue、明文、密文原文。需要用户提供样本时，要求脱敏或使用测试材料。
