# KMS 服务开通与密钥状态

用于 KMS 服务未开通、地域不可用、密钥列表为空、密钥状态异常等问题。

## 前置输入

- Region
- KeyringName / KeyringID
- KeyID / KeyName
- RequestId、错误码、发生时间

## 命令包

### 1. 确认 KMS API 和地域

```text
ve kms DescribeRegions --body '{}'
```

关注字段：

- 返回是否成功：失败且提示服务未开通时，优先判断服务开通/账号资格。
- Region 列表：用户指定地域是否支持 KMS。

### 2. 查询密钥环

```text
ve kms DescribeKeyrings --body '{"CurrentPage":1,"PageSize":10}'
```

关注字段：

- keyring 是否存在。
- 项目或过滤条件是否导致用户找不到 keyring。

### 3. 查询密钥列表

`DescribeKeys` 必须指定 `KeyringName` 或 `KeyringID`。先从 `DescribeKeyrings` 的返回中选取用户目标 keyring；如果用户未提供 keyring，就先向用户说明将抽样查询某个已存在 keyring，避免空参调用。

```text
ve kms DescribeKeys --body '{"CurrentPage":1,"PageSize":10,"KeyringName":"<keyring-name>"}'
```

也可以指定 KeyringID：

```text
ve kms DescribeKeys --body '{"CurrentPage":1,"PageSize":10,"KeyringID":"<keyring-id>"}'
```

### 4. 查询单个密钥

```text
ve kms DescribeKey --body '{"KeyID":"<key-id>"}'
```

或：

```text
ve kms DescribeKey --body '{"KeyringName":"<keyring-name>","KeyName":"<key-name>"}'
```

关注字段：

- KeyState / 状态是否 Enabled。
- KeyUsage、KeySpec、Origin 是否符合调用场景。
- 是否存在 PendingDeletion、Disabled、Archived 等状态。

## 结果解读

| 证据 | 常见结论 |
|---|---|
| `KMS service not open yet` | 服务未开通或账号资格/计费限制，转计费或账号权限 |
| 指定 Region 无返回或不支持 | 地域选错或产品地域限制 |
| keyring 不存在 | 资源定位错误、项目/地域错误 |
| key 存在但 Disabled/PendingDeletion | 生命周期问题，转 `05-key-lifecycle-hsm` |
| key 存在且 Enabled 但调用 AccessDenied | 权限问题，转 `03-key-permission-access-control` |

## 变更边界

本 ref 只做查询；开通服务、创建密钥、启用/禁用密钥、取消删除都必须确认。
