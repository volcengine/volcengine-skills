# 套餐、订阅与资源包查询

用于处理 Coding Plan、订阅过期、套餐升级不生效、资源包不抵扣、资源包用量耗尽。

## 前置输入

- 套餐/资源包名称，产品名，Region，规格，模型名或实例 ID。
- 错误文本，例如 `valid coding plan subscription`、`subscription expired`。
- 购买/升级时间、订单 ID、用户认为应抵扣的用量。

## 先判断方向

| 现象 | 优先路径 |
|---|---|
| Coding Plan 不存在或过期 | 查资源包/订单，必要时转大模型生态 skill 查模型侧现象 |
| 套餐升级后仍限流 | 先查订单和生效时间，再区分套餐限制和 API 限流 |
| 资源包不抵扣 | 查资源包范围、抵扣明细、账单明细 |
| 套餐内调用次数耗尽 | 查资源包使用明细和产品用量口径 |

## 命令包

### 1. 查询资源包和抵扣明细

```text
ve billing ListResourcePackages --body '{"MaxResults":"5","ResourceType":"Package"}'
ve billing ListPackageUsageDetails --body '{"MaxResults":"5","ResourceType":"Package","DeductBeginTime":"<yyyy-MM-dd>","DeductEndTime":"<yyyy-MM-dd>"}'
```

关注字段：

- 资源包状态、有效期、适用产品、适用地域、剩余量。
- 抵扣明细是否覆盖用户报错的产品、计费项、时间范围。

真实验证提示：当前 CLI 对 `ListResourcePackages` 这类 body 查询可能出现签名兼容问题。若 CLI 失败，优先使用已验证脚本：

```text
python3 scripts/collect_billing_context.py --region cn-beijing --include-packages
```

### 2. 查询订单和可用实例

```text
ve billing ListOrders --body '{"MaxResults":5}'
ve billing GetOrder --body '{"OrderNo":"<order-no>"}'
ve billing ListAvailableInstances
```

关注字段：

- 订单是否支付成功、是否已生效、是否仍在处理中。
- 资源包/订阅是否绑定到当前账号或资源。

### 3. 查询账单明细辅助判断

```text
ve billing ListBillDetail --BillPeriod <yyyy-MM>
ve billing ListBillOverviewByProd --BillPeriod <yyyy-MM>
```

关注字段：

- 费用是否已被资源包抵扣。
- 未抵扣行的产品、计费项、Region、实例 ID 是否与资源包范围匹配。

## 典型 case

```text
400 Your account does not have a valid coding plan subscription, or your subscription has expired.
```

```text
升级套餐后仍旧提示 API rate limit reached. Please try again later.
```

```text
codingplan 充的钱能用吗
```

## 结果解读

| 证据 | 常见结论/下一步 |
|---|---|
| 无有效资源包/订阅 | 提示购买或续订，执行购买需确认 |
| 订单成功但未生效 | 说明生效延迟或等待订单状态流转 |
| 资源包有效但不抵扣 | 对比产品、Region、计费项、规格限制 |
| 套餐有效但 429 | 转 OpenAPI/大模型限流方向，区别于计费 |

## 变更边界

本 ref 不执行购买、升级、续费或退订。涉及资源包购买/续费时必须先确认金额、商品、账号和影响。
