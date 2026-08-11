# 用量、配额与调用次数查询

用于处理 `quota`、调用次数耗尽、推理次数上限、资源限额、配额不足和安全用量上限。

## 前置输入

- 产品名、产品编码、Region、资源 ID、模型名。
- 错误文本、RequestId、发生时间。
- 用户想创建/调用/扩容的规格和数量。

## 先判断方向

| 现象 | 优先路径 |
|---|---|
| 创建资源提示配额不足 | 查配额中心产品、维度和当前额度 |
| API 调用次数耗尽 | 查资源包/账单用量，必要时转产品 skill |
| 模型推理上限 | 保留模型上下文，查计费/订阅，同时转大模型生态 skill |
| 429/rate limit | 先区分限流、配额、余额、订阅 |

## 命令包

### 1. 查询支持配额的产品

如果用户问题命中 MaaS、火山方舟、大模型、模型 Endpoint 或 API Key，优先使用已验证映射：

```text
ve quota ListProductQuotas --ProviderCode MaaS
```

不要先调用无 `ProviderCode` 的 `ListProductQuotas`，也不要把参数写成 `ProductCode`。`ark` 不是配额中心 `ProviderCode`，不要执行 `--ProviderCode ark`。

其他产品先查看 `../provider-code-aliases.md`；没有映射时再执行：

```text
ve quota ListProducts
```

关注字段：

- 目标产品是否接入配额中心。
- `ProviderCode`，供后续 `ListProductQuotas` 使用。

### 2. 查询产品配额和维度

```text
ve quota ListProductQuotaDimensions --ProviderCode <provider-code>
ve quota ListProductQuotas --ProviderCode <provider-code>
ve quota GetProductQuota --ProviderCode <provider-code> --QuotaCode <quota-code>
```

真实沙箱验证提示：`ListProductQuotas` 必须使用 `--ProviderCode`。不要把 `ListProducts` 中看到的产品信息直接写成 `--ProductCode` 参数，否则会返回 `JSONInvalid` / `ProviderCode is required`。

关注字段：

- 配额名称、维度、当前值、已用值、可申请上限。
- 维度是否包括 Region、Zone、实例规格、账号类型。

### 3. 查询配额申请和告警

```text
ve quota ListQuotaApplications --ProviderCode <provider-code>
ve quota GetQuotaApplication --ApplicationId <application-id>
ve quota ListQuotaAlarmRules
ve quota ListAlarmHistory
```

关注字段：

- 是否已有申请在审批中或被驳回。
- 告警是否已触达，是否能解释用户看到的资源限制。

## 典型 case

```text
怎么判断套餐内的调用次数/用量已经耗尽
```

```text
You have exceeded the monthly usage quota.
```

```text
Your account has reached the set inference limit for the doubao-seedance-2-0 model.
```

## 结果解读

| 证据 | 常见结论/下一步 |
|---|---|
| 当前配额已达上限 | 说明需要申请更配或释放资源，申请动作需确认 |
| 配额正常但调用失败 | 转产品 skill 或 OpenAPI 限流方向 |
| 有申请审批中 | 告知等待审批，不重复申请 |
| 模型安全上限触发 | 转大模型生态 skill 查模型开通和安全上限 |

## 变更边界

本 ref 不执行 `CreateQuotaApplication`、创建/修改配额告警或模板。需要申请/修改时必须先确认产品、地域、目标额度和业务理由。
