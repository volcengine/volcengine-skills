# 计费问题 Playbook

用于高频计费错误的快速排查卡片。每张卡片都要先确认错误文本和产品上下文，再执行最小查询。

## AccountOverdueError

触发信号：

```text
The request failed because your account has an overdue balance.
```

路径：

1. `ve billing QueryBalanceAcct`
2. `ve billing ListBill --BillPeriod <yyyy-MM>`
3. 如果查询无权限，转账号/IAM。

结论：

- 欠费导致服务调用被拒绝，优先处理欠费账单。

## BalanceNotEnough / 预扣费失败

触发信号：

```text
BalanceNotEnough
预扣费额度失败, 用户剩余额度不足
```

路径：

1. `ve billing QueryBalanceAcct`
2. `ve billing ListCoupons`
3. 如果和订单相关，补 `ve billing GetOrder --OrderNo <order-no>`。

结论：

- 可用余额或可用代金券低于商品预留金额。

## Coding Plan 订阅过期

触发信号：

```text
Your account does not have a valid coding plan subscription, or your subscription has expired.
```

路径：

1. `ve billing ListResourcePackages`
2. `ve billing ListOrders`
3. 保留模型/ArkClaw 上下文，必要时转大模型生态 skill。

结论：

- 无有效订阅、订阅过期、订阅未在当前账号生效，或错误被模型层包装。

## 套餐升级后仍 rate limit

触发信号：

```text
升级套餐后仍旧提示 API rate limit reached.
```

路径：

1. `ve billing GetOrder --OrderNo <order-no>`
2. `ve billing ListResourcePackages`
3. 如果订阅已生效，转 OpenAPI/大模型限流排查。

结论：

- 需要区分套餐生效延迟、产品限流和模型侧 QPS/TPM/RPM 限制。

## 资源包不抵扣

路径：

1. `ve billing ListResourcePackages`
2. `ve billing ListPackageUsageDetails`
3. `ve billing ListBillDetail --BillPeriod <yyyy-MM>`

结论：

- 对比资源包的产品、地域、计费项、规格和账单行。

## 无购买权限

触发信号：

```text
service：bill_volcano_engine error：用户没有购买该配置的权限
```

路径：

1. `ve billing ListOrders`
2. `ve billing ListFinancialRelation`
3. `ve organization ListAccounts`
4. 转账号/IAM 检查购买和费用中心权限。

结论：

- 可能是商品资格、账号认证、主子账号财务关系或 IAM 权限问题。

## 账单查询无权限

路径：

1. 确认用户要查余额、账单、成本还是订单。
2. 尝试对应只读 Action。
3. 如果返回 `AccessDenied`，转账号/IAM。

结论：

- 业务入口是计费，但根因是权限机制。
