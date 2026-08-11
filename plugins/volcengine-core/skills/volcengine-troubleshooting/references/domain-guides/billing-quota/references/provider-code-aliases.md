# 配额中心 ProviderCode 速查

本文件记录真实验证或高置信来源确认过的配额中心 `ProviderCode`。处理 quota、资源限额、月度用量上限时，先查这里；不确定时再执行 `ve quota ListProducts` 搜索确认。

## 使用原则

- 查询配额必须使用 `--ProviderCode <provider-code>`，不要使用 `--ProductCode`。
- 用户说产品中文名、控制台名、报错里的产品简称时，先映射为 `ProviderCode`。
- 本表没有覆盖时，先执行 `ve quota ListProducts`，再从返回中找最接近的产品项；仍不确定时不要猜。

## 已验证映射

| 用户常说 | 产品/场景 | ProviderCode | 已验证命令 |
|---|---|---|---|
| MaaS、火山方舟、方舟、大模型、模型推理、Endpoint、API Key | 火山方舟 / 大模型服务相关资源配额 | `MaaS` | `ve quota ListProductQuotas --ProviderCode MaaS` |

注意：`ark` 不是配额中心 `ProviderCode`。不要执行 `ve quota ListProductQuotas --ProviderCode ark`。

## 常用命令模板

```text
ve quota ListProducts
ve quota ListProductQuotas --ProviderCode <provider-code>
ve quota ListProductQuotaDimensions --ProviderCode <provider-code>
ve quota GetProductQuota --ProviderCode <provider-code> --QuotaCode <quota-code>
ve quota ListQuotaApplications --ProviderCode <provider-code>
```

## 结果解读

- `ListProductQuotas` 适合先看是否已经超资源配额。
- `GetProductQuota` 适合用户给出明确 `QuotaCode` 或要确认单个配额详情。
- `ListQuotaApplications` 适合用户问“是否已经申请过提额/为什么提额还没生效”。
- 月度调用次数、套餐次数、模型推理上限不一定在配额中心体现；配额中心正常后继续查询资源包/账单/余额，必要时转大模型生态 skill。
