# 购买、开通与订单失败查询

用于处理购买失败、开通失败、无购买权限、商品停售、订单支付失败、`CreatePreorder` / `CreateOrder` 相关问题。

## 前置输入

- 商品/产品、规格、Region、购买方式、订单 ID。
- 错误文本、RequestId、logid、发生时间。
- 主账号/子账号、付款账号、认证状态。

## 先判断方向

| 现象 | 优先路径 |
|---|---|
| `BalanceNotEnough` | 同时读余额章节 |
| `用户没有购买该配置的权限` | 查订单/商品，权限机制转账号/IAM |
| `ProductStopSelling` | 商品停售或规格不可购，转产品可售性判断 |
| 支付/开通失败 | 查订单状态、支付状态、可用实例 |

## 命令包

### 1. 查询订单

```text
ve billing ListOrders --body '{"MaxResults":5}'
ve billing GetOrder --body '{"OrderNo":"<order-no>"}'
ve billing ListOrderProductDetails --body '{"OrderNo":"<order-no>"}'
```

关注字段：

- 订单状态、支付状态、失败原因、商品信息、购买账号。
- 订单是否已取消、已支付、处理中、失败。

### 2. 查询可用实例与财务关系

```text
ve billing ListAvailableInstances
ve billing ListFinancialRelation
```

关注字段：

- 实例是否可续费/退订/购买。
- 主子账号或财务托管关系是否影响支付和开通。

### 3. 查询组织账号辅助判断

```text
ve organization DescribeOrganization
ve organization ListAccounts
```

关注字段：

- 当前操作者是否是付款账号或资源拥有账号。
- 是否需要主账号统一购买。

## 典型 case

```text
logid：LOG_ID service：bill_volcano_engine error：用户没有购买该配置的权限
```

```text
ProductStopSelling
```

```text
Operation is denied because create order in one step failed. BalanceNotEnough
```

## 结果解读

| 证据 | 常见结论/下一步 |
|---|---|
| 订单因余额不足失败 | 转余额章节，建议充值后重试 |
| 订单因权限失败 | 转账号/IAM，检查购买/费用中心权限 |
| 商品停售或规格不可购 | 转产品手册，确认可售规格和地域 |
| 支付成功但开通失败 | 查订单产品明细和产品侧开通状态 |

## 变更边界

本 ref 不执行 `PayOrder`、`CommonBuy`、`CancelOrder`、购买或开通。涉及资金和商品状态变更时必须先确认。
