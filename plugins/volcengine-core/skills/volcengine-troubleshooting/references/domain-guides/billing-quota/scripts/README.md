# 计费排障脚本

当前提供 1 个只读 Python SDK 脚本，用于绕过 CLI 对部分 billing body 查询的签名/参数兼容问题，并给 Agent 输出结构化 `summary/findings/raw`。

脚本只读取环境变量凭证：

- `VOLCENGINE_ACCESS_KEY`
- `VOLCENGINE_SECRET_KEY`
- `VOLCENGINE_SESSION_TOKEN` 可选

不得通过命令行传入 AK/SK。

## 脚本清单

| 脚本 | 适用入口 | 最小必填参数 | 可选参数 | 输出 |
|---|---|---|---|---|
| `collect_billing_context.py` | 余额/欠费、订单、账单、资源包、费用突增初筛 | 无；默认使用 `--region` 或 `VOLCENGINE_REGION` | `--region`、`--bill-period <yyyy-MM>`、`--max-results <n>`、`--all-pages`、`--max-pages <n>`、`--include-orders`、`--include-packages`、`--include-bill-detail`、`--include-raw` | `summary`、`findings`、`raw` |

## 使用示例

查询余额和最近订单：

```text
python3 scripts/collect_billing_context.py --region cn-beijing --include-orders
```

查询某账期产品账单和资源包：

```text
python3 scripts/collect_billing_context.py --region cn-beijing --bill-period 2026-05 --include-packages
```

查询某账期账单明细，注意明细可能包含敏感资源和金额信息，回复用户时只摘取排障必要字段：

```text
python3 scripts/collect_billing_context.py --region cn-beijing --bill-period 2026-05 --include-bill-detail --max-results 5
```

`--max-results` 只代表每类查询返回的分页样本大小。除非你继续分页并确认拿到全量，否则结论必须写成“当前页/TopN 样本”，不能推导完整账期全量占比。

费用突增、资源包耗尽或用户明确要求“全量/尽量完整”时，使用分页采集：

```text
python3 scripts/collect_billing_context.py --region cn-beijing --bill-period 2026-05 --include-bill-detail --include-packages --all-pages --max-pages 3 --max-results 20
```

必须带 `--all-pages` 才会翻页。只传 `--max-results 100` 是单页查询。

不要传 `--max-results 1000`。费用中心列表接口单页使用 100 作为安全上限，脚本会自动限幅、启用分页并在 `findings` 中说明；Agent 应优先使用 20-100 的页大小。

资源包接口更保守，脚本会把资源包单页大小压到 20 以内。

读取 `summary.*_pagination`：

- `is_complete=true`：当前查询已覆盖脚本可见全量。
- `is_complete=false`：只覆盖前若干页，回答必须注明“已采集前 N 页/样本”。
- `next_token` 或 `expected_total` 可用于判断是否还需要继续分页。

脚本会把 `findings` 和 `headline` 放在输出前部。Agent 先读 `headline.*.pagination` 再展开 `summary`，避免长账单样本截断后误判资源包或账单明细状态。

默认情况下 `raw` 只输出结构摘要，避免完整账单明细直接暴露。只有需要定位字段名或排查脚本问题时，才加 `--include-raw`。

## 失败回落

- 如果脚本提示缺少 `VOLCENGINE_ACCESS_KEY` 或 `VOLCENGINE_SECRET_KEY`，不要要求用户把凭证写入文件；让平台沙箱注入环境变量。
- 如果某个子查询失败，脚本会继续输出其他证据；先看 `summary` 和 `findings`。
- 如果脚本整体失败，回落到章节 reference 中的 CLI 查询：`QueryBalanceAcct`、`ListOrders` 等已经过真实验证。
