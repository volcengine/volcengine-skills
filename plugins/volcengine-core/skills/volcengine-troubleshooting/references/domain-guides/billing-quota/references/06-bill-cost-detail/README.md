# 账单、成本与消费明细查询

用于处理账单查询、余额查询、成本分析、费用突增、分账账单、摊销成本、资源包抵扣口径解释。

## 前置输入

- 账期：月账期 `yyyy-MM`，或日粒度时间范围。
- 产品、实例 ID、项目、标签、Region、计费模式。
- 用户关注的是账单金额、成本金额、分账金额还是资源包抵扣。

## 先判断方向

| 现象 | 优先路径 |
|---|---|
| 查询余额 | `QueryBalanceAcct` |
| 查某月账单明细 | `ListBillDetail` / `ListBill` |
| 产品汇总费用 | `ListBillOverviewByProd` |
| 成本分析/费用突增 | `ListCostAnalysisOpenApi`、摊销成本账单 |
| 分账/项目/标签口径 | `ListSplitBillDetail`、资源中心/标签查询 |

## 命令包

### 1. 账单明细与汇总

```text
ve billing ListBill --body '{"BillPeriod":"<yyyy-MM>","Limit":5,"Offset":0}'
ve billing ListBillDetail --body '{"BillPeriod":"<yyyy-MM>","Limit":5,"Offset":0}'
ve billing ListBillOverviewByProd --body '{"BillPeriod":"<yyyy-MM>","Limit":5,"Offset":0}'
ve billing ListBillOverviewByCategory --body '{"BillPeriod":"<yyyy-MM>","Limit":5,"Offset":0}'
```

关注字段：

- 产品、计费项、实例 ID、用量、费用、抵扣、应付金额。
- 分页参数，避免只看第一页。

真实验证提示：当前 CLI 对账单 body 查询可能出现签名兼容问题。费用突增、账单明细、资源包抵扣归因优先使用已验证脚本：

```text
python3 scripts/collect_billing_context.py --region cn-beijing --bill-period <yyyy-MM> --include-bill-detail --include-packages --max-results 5
```

脚本判读约束：`--max-results` 控制每类查询的分页样本大小。除非脚本或后续分页已经明确覆盖全量，否则回复用户时只能说“当前页/TopN 样本显示”，不能把 TopN 结果表述成完整账期全量占比。

如果用户问“费用突增到底是谁导致的”“尽量完整归因”“资源包是不是全耗尽”，使用分页模式：

```text
python3 scripts/collect_billing_context.py --region cn-beijing --bill-period <yyyy-MM> --include-bill-detail --include-packages --all-pages --max-pages 3 --max-results 20
```

这个场景必须带 `--all-pages`。只传 `--max-results 100` 仍然只会采集单页，不能满足“完整分页”。

不要传 `--max-results 1000`。费用中心列表接口单页使用 100 作为安全上限，脚本会自动限幅并启用分页；常规排障建议 `--max-results 20`，需要更完整样本时使用 `--max-results 100` 并控制 `--max-pages`。

资源包接口更保守，脚本会自动把资源包查询的单页大小压到 20 以内。

判读 `summary.bill_overview_pagination`、`summary.bill_detail_pagination`、`summary.resource_packages_pagination`：

- `is_complete=true`：脚本已覆盖当前查询可见全量。
- `is_complete=false`：仍有后续页，回答必须注明“当前采集前 N 页”，不要写成全量结论。
- `expected_total` 或 `next_token` 存在时，可用于说明是否还需要继续分页。

脚本输出前部包含 `headline`，优先读取 `headline.bill_overview.pagination`、`headline.bill_detail.pagination`、`headline.resource_packages.pagination`；不要只凭后续样本表格判断是否全量。

### 2. 成本与摊销账单

```text
ve billing ListCostAnalysisOpenApi
ve billing ListAmortizedCostBillMonthly --BillPeriod <yyyy-MM>
ve billing ListAmortizedCostBillDaily --BillPeriod <yyyy-MM>
ve billing ListAmortizedCostBillDetail --BillPeriod <yyyy-MM>
```

关注字段：

- 成本口径是否与账单口径不同。
- 日粒度费用突增的产品、实例、计费项。

### 3. 分账、标签和资源归属

```text
ve billing ListSplitBillDetail --BillPeriod <yyyy-MM>
ve resourcecenter SearchResources --ResourceIds '["<resource-id>"]'
ve tag GetResources
```

关注字段：

- 项目、标签、成本单元、资源归属账号。
- 分账规则是否解释用户看到的费用归属。

## 典型 case

```text
我的账户余额是多少？如何续费？
```

```text
ListCostAnalysisOpenApi
```

```text
ListBillOverviewByProd
```

```text
查询已购商品信息
```

## 结果解读

| 证据 | 常见结论/下一步 |
|---|---|
| 费用集中在某产品/实例 | 转对应产品 skill 分析用量增长原因 |
| 账单与成本金额不同 | 解释账单、摊销、分账口径差异 |
| 资源包抵扣后仍有应付 | 查未覆盖的计费项、地域或规格 |
| 查询账单无权限 | 转账号/IAM，检查费用中心权限 |

## 变更边界

本 ref 不修改预算、标签、成本单元或账单订阅设置。预算/预警变更必须先确认。
