# 计费排查总入口

用于不知道问题属于余额、订阅、配额、订单、账单还是权限时的第一层分流。

## 前置输入

- 错误文本、错误码、RequestId、发生时间。
- 产品名、资源 ID、Region、实例规格或模型名。
- 主账号/子账号、付款账号、资源归属账号。
- 订单 ID、账期、套餐/资源包名称。

## 先判断方向

| 现象 | 优先路径 |
|---|---|
| `AccountOverdueError`、欠费、余额不足、预扣费失败 | 读 `02-balance-arrears-precharge` |
| `valid coding plan subscription`、订阅过期、资源包不抵扣 | 读 `03-subscription-package` |
| `quota`、调用次数耗尽、推理上限、资源限额 | 读 `04-usage-quota-limit` |
| 下单失败、商品不可购、无购买权限、CreatePreorder | 读 `05-order-purchase-activation` |
| 费用突增、账单明细、成本分析、余额查询 | 读 `06-bill-cost-detail` |
| `AccessDenied`、无权查账单/无权购买 | 保留计费上下文，转账号/IAM skill |
| API 签名、SDK 参数、CLI 命令报错 | 保留计费 Action，转 OpenAPI/Python SDK/CLI skill |

## 最小查询包

### 1. 余额与账户商业状态

```text
ve billing QueryBalanceAcct
```

关注字段：

- 可用余额、现金余额、代金券余额、欠费相关字段。
- 如果 API 返回权限错误，转账号/IAM；如果余额为 0 或不足，继续 `02`。

### 2. 资源归属与主子账号关系

```text
ve organization DescribeOrganization
ve organization ListAccounts
ve resourcecenter SearchResources --ResourceIds '["<resource-id>"]'
```

关注字段：

- 资源属于哪个账号、项目、标签、Region。
- 付款账号和资源拥有账号是否一致。

### 3. 配额产品列表

```text
ve quota ListProducts
```

关注字段：

- 目标产品是否接入配额中心。
- 产品名和产品编码，后续查 `ListProductQuotas`。

## 结果解读

| 证据 | 常见结论/下一步 |
|---|---|
| 余额不足或欠费 | 进入余额/欠费排查，给出充值、续费、释放欠费限制路径 |
| 有资源包但仍扣费 | 查资源包范围、抵扣明细和账单明细 |
| 有 quota 错误但余额正常 | 查配额中心或产品级调用上限，不按欠费处理 |
| 查询账单 API AccessDenied | 转账号/IAM 手册，检查计费相关权限 |
| 订单失败且 BalanceNotEnough | 同时进入订单和余额章节 |

## 变更边界

本 ref 只做查询。充值、支付、购买、退订、续费、配额申请和预算变更都需要用户明确确认。
