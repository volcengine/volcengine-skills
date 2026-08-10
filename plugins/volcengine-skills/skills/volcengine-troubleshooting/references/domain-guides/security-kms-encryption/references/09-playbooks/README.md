# 高频 Playbook

## `KMS service not open yet`

1. 执行：

```text
ve kms DescribeRegions --body '{}'
```

2. 如果仍返回服务未开通，判断为服务开通/账号资格/计费限制，转计费或账号权限 skill。
3. 如果 API 可达，再查：

```text
ve kms DescribeKeyrings --body '{"CurrentPage":1,"PageSize":10}'
ve kms DescribeKeys --body '{"CurrentPage":1,"PageSize":10,"KeyringName":"<keyring-name>"}'
```

注意：`DescribeKeys` 必须带 `KeyringName` 或 `KeyringID`，`<keyring-name>` 从 `DescribeKeyrings` 返回中选取。

## 密钥无权限

1. 先确认密钥存在：

```text
ve kms DescribeKey --body '{"KeyID":"<key-id>"}'
```

2. 如果查询也 AccessDenied，转账号权限 skill。
3. 如果查询成功但加解密失败，缺数据面 Action 或资源级授权。

## `KMSEncryptFailed: Plaintext is invalid`

1. 不直接执行 `Encrypt`。
2. 查 key 元数据：

```text
ve kms DescribeKey --body '{"KeyID":"<key-id>"}'
```

3. 检查 Plaintext 编码、长度、是否被重复 base64 或错误 JSON 转义。

## `InvalidEncryptedContent`

1. 查 key 状态。
2. 核对 CiphertextBlob 是否完整、是否来自同一个 key、是否被截断/换行/转码。
3. 如果使用 EncryptionContext，核对加密和解密上下文完全一致。

## WAF 误拦截

1. 查域名接入：

```text
ve waf ListDomain --body '{"Page":1,"PageSize":10,"Region":"<region>","Domain":"<host>"}'
```

2. 查事件：

```text
ve waf QueryAttackSecurityEvent --body '{"StartTime":<start-unix>,"EndTime":<end-unix>,"Page":1,"PageSize":10,"Host":"<host>"}'
```

3. 有命中规则再讨论放行；无事件则转域名入口/源站链路。

## DDoS 清洗后业务不可用

1. 查攻击流量。
2. 查高防域名/端口配置和回源 IP。
3. 如果源站拦截高防回源 IP，转计算网络/源站安全策略。

## 云防火墙拦截

1. 查访问控制策略：

```text
ve fwcenter DescribeControlPolicy --body '{"PageNumber":1,"PageSize":10,"Direction":"in"}'
ve fwcenter DescribeControlPolicy --body '{"PageNumber":1,"PageSize":10,"Direction":"out"}'
```

2. 若有 RuleId：

```text
ve fwcenter DescribeControlPolicyByRuleId --body '{"RuleId":"<rule-id>"}'
```

3. 策略变更必须确认。
