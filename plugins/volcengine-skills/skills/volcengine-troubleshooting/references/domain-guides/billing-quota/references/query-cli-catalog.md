# 计费查询 CLI 入口索引

本文件只做入口索引，不承载完整接口清单。处理具体问题时先根据用户现象跳到章节 reference，再按最小证据集调用查询 CLI。

公共约定：

- 执行形态统一写成 `ve <service> <Action> [--Param value...]`。
- `cli-meta` 中展示的 `volcengine <service> <Action>` 是来源形态，执行设计中统一映射为 `ve`。
- 只默认使用查询 Action：`Describe/List/Get/Query/Search/Check`。
- 配额中心真实 CLI 参数使用 `ProviderCode`：例如 `ve quota ListProductQuotas --ProviderCode MaaS`。不要写成 `--ProductCode`。
- 不允许调用无 `--ProviderCode` 的 `ve quota ListProductQuotas`、`GetProductQuota`、`ListQuotaApplications`。
- 配额中心产品编码先看 `provider-code-aliases.md`；没有映射再执行 `ve quota ListProducts`。
- 写操作如 `PayOrder`、`RenewInstance`、`UnsubscribeInstance`、`CommonBuy`、`CreateQuotaApplication`、`CreateBudget` 必须先 Human-in-the-Loop 确认。

## 快速入口

| 问题域 | 必读 reference | 主要服务 | 典型查询 Action |
|---|---|---|---|
| 总入口与分流 | `01-overview-routing/README.md` | `billing`、`quota`、`resourcecenter`、`organization` | `QueryBalanceAcct`、`ListProducts`、`SearchResources` |
| 余额、欠费、预扣费 | `02-balance-arrears-precharge/README.md` | `billing` | `QueryBalanceAcct`、`ListCoupons`、`ListCouponUsageRecords`、`ListBill` |
| 套餐、订阅、资源包 | `03-subscription-package/README.md` | `billing` | `ListResourcePackages`、`ListPackageUsageDetails`、`ListAvailableInstances`、`GetOrder` |
| 用量、配额、调用次数 | `04-usage-quota-limit/README.md` | `quota`、`billing` | `ListProducts`、`ListProductQuotas --ProviderCode <provider-code>`、`GetProductQuota --ProviderCode <provider-code>`、`ListQuotaApplications --ProviderCode <provider-code>` |
| 购买、开通、订单失败 | `05-order-purchase-activation/README.md` | `billing`、`organization` | `ListOrders`、`GetOrder`、`ListOrderProductDetails`、`ListFinancialRelation` |
| 账单、成本、消费明细 | `06-bill-cost-detail/README.md` | `billing`、`resourcecenter`、`tag` | `ListBillDetail`、`ListBillOverviewByProd`、`ListCostAnalysisOpenApi`、`SearchResources` |
| 高频 Playbook | `07-playbooks/README.md` | 视 case 而定 | 按错误码映射 |

## 来源

- `cli-meta/火山引擎计费问题排查手册/费用中心/接口清单.md`
- `cli-meta/火山引擎计费问题排查手册/配额中心/接口清单.md`
- `cli-meta/火山引擎计费问题排查手册/资源管理/接口清单.md`
- `产品官方文档/火山引擎计费问题排查手册/费用中心/费用中心/_目录.md`
- `产品官方文档/火山引擎计费问题排查手册/配额中心/配额中心/_目录.md`
