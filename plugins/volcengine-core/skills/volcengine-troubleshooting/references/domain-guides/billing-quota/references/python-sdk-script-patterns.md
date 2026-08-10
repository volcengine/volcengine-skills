# Python SDK 脚本模式

计费 skill 提供少量只读 Python SDK 脚本。CLI 能覆盖部分单点查询，但真实验证发现 `billing` 的部分 body 查询和 `quota` 查询在当前 CLI 环境下可能出现签名/参数兼容问题；多页聚合、跨账期对比、资源包抵扣归因、费用突增分析优先使用脚本。

## 什么时候需要脚本

| 触发条件 | CLI 不足点 | 脚本应做什么 |
|---|---|---|
| 账单明细跨多页、多产品、多账期 | Agent 手工翻页和比对容易漏项 | 自动分页，按产品/实例/标签聚合费用变化 |
| 资源包是否抵扣某类用量 | 需要同时查资源包、抵扣明细、账单行 | 关联 `ListResourcePackages`、`ListPackageUsageDetails`、`ListBillDetail` |
| 费用突增 | 需要对比日/月粒度、产品、实例、计费项 | 输出增量 TopN 和异常账单项 |
| 配额问题要关联产品配额与申请历史 | `quota` 多接口需要拼接维度 | 归一产品、地域、维度、当前值、申请状态 |

## 脚本安全规范

- 只调用查询 Action。
- 凭证只从环境变量读取，优先使用 `VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、`VOLCENGINE_SESSION_TOKEN`。
- 不接收命令行 AK/SK，不写配置文件，不打印完整凭证。
- 金额、账号、发票、合同等敏感字段只输出排障必要摘要。
- 输出固定包含 `summary`、`findings`、`raw`。

## 暂不需要脚本的场景

- 只查询当前余额：用 `ve billing QueryBalanceAcct`。
- 只查一个订单：用 `ve billing GetOrder`。
- 只查某产品配额：用 `ve quota GetProductQuota` 或 `ListProductQuotas`。
- 只是解释 `AccountOverdueError`、`BalanceNotEnough` 等错误码。

## 候选脚本

| 脚本名 | 状态 | 用途 | 最小输入 |
|---|---|---|---|
| `collect_billing_context.py` | 已实现 | 聚合余额、最近订单、资源包、账单总览/明细摘要 | 无；`--bill-period` 可选 |
| `analyze_cost_spike.py` | 规划中 | 对比账期费用并输出产品/实例 TopN | `--start-period --end-period` |
| `collect_quota_context.py` | 规划中 | 聚合产品配额、维度、申请历史 | `--product`，可选 `--region` |
