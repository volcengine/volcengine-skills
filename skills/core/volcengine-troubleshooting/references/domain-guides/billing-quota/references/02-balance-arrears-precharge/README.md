# 余额、欠费与预扣费查询

用于处理余额不足、欠费、预扣费失败、代金券不可用、`AccountOverdueError`、`BalanceNotEnough`。

## 前置输入

- 错误码和完整错误文本。
- 发生产品、Action、资源 ID、订单 ID、RequestId。
- 预扣费金额、用户看到的余额、账期。

## 先判断方向

| 现象 | 优先路径 |
|---|---|
| `AccountOverdueError` | 先查账户余额和欠费状态，再解释后付费欠费限制 |
| `BalanceNotEnough` | 查余额、代金券、订单预留金额 |
| `预扣费额度失败` | 对比剩余额度与预扣费额度 |
| 用户问余额/续费 | 查余额；续费动作只给路径，执行需确认 |

## 命令包

### 1. 查询账户余额

```text
ve billing QueryBalanceAcct
```

关注字段：

- 可用余额、现金余额、授信/额度、代金券余额。
- 响应是否指向欠费、冻结或不可用状态。

判读约束：

- 如果 `ArrearsBalance > 0`，可以判断存在历史欠费或逾期账单风险。
- 如果 `ArrearsBalance = 0`，但 `AvailableBalance = 0` 且 `CreditLimit = 0`，不要直接说“已经欠费”；应表述为“当前没有可用余额/授信，容易触发预扣费、开通或新调用失败”，并结合原始错误码、订单或产品侧 RequestId 继续确认。
- 如果报错文本是 `AccountOverdueError`，但余额证据没有欠费金额，要把“产品侧按欠费类错误拒绝”和“账户余额字段显示无历史欠费”同时说明，避免过度归因。

### 2. 查询代金券及使用记录

```text
ve billing ListCoupons --body '{"Limit":5,"Offset":0}'
ve billing ListCouponUsageRecords --body '{"Limit":5,"Offset":0}'
```

关注字段：

- 代金券是否过期、是否适用于目标产品、是否有用量/地域/计费项限制。
- 代金券是否已经被其他订单或账单消耗。

### 3. 查询相关账单和订单

```text
ve billing ListBill --BillPeriod <yyyy-MM>
ve billing ListOrders --body '{"MaxResults":5}'
ve billing GetOrder --body '{"OrderNo":"<order-no>"}'
```

关注字段：

- 欠费是否来自历史账单。
- 订单是否因余额不足、预扣失败、支付失败而失败。

## 典型 case

```text
HTTP 403: 预扣费额度失败, 用户剩余额度: $0.217626, 需要预扣费额度: $0.226494
```

```text
AccountOverdueError: The request failed because your account has an overdue balance.
```

```text
BalanceNotEnough: 您的账户余额及可用代金券低于该商品的下单预留金额，无法开通此服务！
```

## 结果解读

| 证据 | 常见结论/下一步 |
|---|---|
| 可用余额低于预扣金额 | 余额不足，建议充值或降低购买/调用规格 |
| 现金余额足够但代金券不可用 | 检查代金券产品/地域/计费项限制 |
| 后付费欠费 | 先处理欠费账单，恢复后再重试业务调用 |
| 无历史欠费但可用余额/授信为 0 | 优先按预扣费/新消费可用额度不足解释，保留产品侧欠费错误码作为待确认线索 |
| 查询余额无权限 | 转账号/IAM，检查计费读权限 |

## 变更边界

本 ref 不执行充值、支付、续费、购买。涉及资金动作时，只能在用户确认后转入对应变更流程。
