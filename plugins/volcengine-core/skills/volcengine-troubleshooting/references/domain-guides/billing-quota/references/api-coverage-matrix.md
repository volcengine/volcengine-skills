# API 覆盖审查矩阵
本文件由 2026-05-22 审查生成，用于证明本 skill 已对 `cli-meta/` 中对应分类的 OpenAPI / CLI / Python SDK 能力做过覆盖盘点。它不是执行顺序清单；Agent 仍应先按主 `SKILL.md` 和章节 reference 选择最小必要证据。
## 审查口径
- 纳入排障优先级：`Describe/List/Get/Query/Check/Search/BatchGet/Verify/Validate/Test/Diagnose/Preview/Estimate` 等只读或诊断型 Action。
- 默认排除自动执行：`Create/Modify/Delete/Update/Attach/Detach/Start/Stop/Run/Invoke/Pay/Renew/Set` 等会改变资源、资金、权限或任务状态的 Action；只能作为解释错误码或 Human-in-the-Loop 建议背景。
- 命令形态：执行时统一写作 `ve <service> <Action> [--Param value...]`；参数不确定时先查 `ve <service> <Action> --help` 或对应 `cli-meta`。
- 凭证边界：只从临时环境读取 `VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、`VOLCENGINE_REGION`，不得写入配置、文档或日志。
## 总览
- 覆盖产品数：6
- 官方文档识别 OpenAPI Action 数合计：135
- 纳入排障候选的只读/诊断 Action 数：87
- 默认不自动执行的写/变更 Action 数：52
- 需人工判断语义的其它 Action 数：13

## 产品级覆盖
### 售后技术支持
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 消息中心
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 账号相关
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 费用中心
- 官方文档识别 Action 数：57
- 纳入只读/诊断 Action：43
- 排除自动执行的写/变更 Action：13
- 其它需按场景人工判断 Action：CommonBuy, UnsubscribeInstance

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `GetFilterInfoForCostAnalysis` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `GetOrder` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `GetServiceInfo` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListAmortizedCostBillDaily` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListAmortizedCostBillDetail` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListAmortizedCostBillMonthly` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListAvailableInstances` | `billing` | 资源状态、实例/节点/集群运行态证据 |
| `ListBill` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListBillDetail` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListBillOverviewByCategory` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListBillOverviewByProd` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListBudget` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListBudgetAmountByBudgetID` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListBudgetAmountByBudgetId` | `Python SDK-only/未匹配 CLI` | 计费、订单、成本、配额或资源包证据 |
| `ListBudgetFilterBillingMode` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListBudgetFilterOwnerID` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListBudgetFilterOwnerId` | `Python SDK-only/未匹配 CLI` | 计费、订单、成本、配额或资源包证据 |
| `ListBudgetFilterPayerID` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListBudgetFilterPayerId` | `Python SDK-only/未匹配 CLI` | 计费、订单、成本、配额或资源包证据 |
| `ListBudgetFilterProduct` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListBudgetFilterProject` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListBudgetFilterRegionCode` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListBudgetFilterSubjectInfo` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListBudgetFilterTagKey` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListBudgetFilterTagValue` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListBudgetFilterZoneCode` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListCostAnalysisOpenApi` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListCouponUsageRecords` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListCoupons` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListFinancialRelation` | `billing` | 资源存在性、状态、配置或诊断证据 |
| `ListInvitation` | `billing` | 资源存在性、状态、配置或诊断证据 |
| `ListOrderProductDetails` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListOrders` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListPackageUsageDetails` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListRecipientInformation` | `billing` | 资源存在性、状态、配置或诊断证据 |
| `ListResourcePackages` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `ListSplitBillDetail` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `QueryBalanceAcct` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `QueryBudgetDetail` | `billing` | 计费、订单、成本、配额或资源包证据 |
| `QueryPriceForPayAsYouGo` | `billing` | 资源存在性、状态、配置或诊断证据 |
| `QueryPriceForRenew` | `billing` | 资源存在性、状态、配置或诊断证据 |
| `QueryPriceForSubscription` | `billing` | 资源存在性、状态、配置或诊断证据 |
| `QueryTagValueByTagKey` | `billing` | 密钥、安全策略、风险或告警证据 |

### 资源管理
- 官方文档识别 Action 数：58
- 纳入只读/诊断 Action：33
- 排除自动执行的写/变更 Action：31
- 其它需按场景人工判断 Action：AcceptInvitation, AcceptQuitApplication, ExecuteSQLQuery, ExecuteSqlQuery, InviteAccount, MoveAccount, QuitOrganization, ReInviteAccount, RejectInvitation, RejectQuitApplication, RetryChangeAccountSecureContactInfo

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAccount` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAccountInvitation` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `DescribeOrganization` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `DescribeOrganizationalUnit` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `DescribeQuitApplication` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `GetAccountSecureContactInfo` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `GetExampleQuery` | `resourcecenter` | 资源存在性、状态、配置或诊断证据 |
| `GetMultiAccountResourceCenterStatus` | `resourcecenter` | 资源存在性、状态、配置或诊断证据 |
| `GetMultiAccountResourceCounts` | `resourcecenter` | 资源存在性、状态、配置或诊断证据 |
| `GetQuery` | `resourcecenter` | 资源存在性、状态、配置或诊断证据 |
| `GetResourceCenterStatus` | `resourcecenter` | 资源存在性、状态、配置或诊断证据 |
| `GetResourceCounts` | `resourcecenter` | 资源存在性、状态、配置或诊断证据 |
| `GetResources` | `tag` | 资源存在性、状态、配置或诊断证据 |
| `GetServiceControlPolicy` | `organization` | 身份、权限、密钥或授权证据 |
| `GetServiceControlPolicyEnablement` | `organization` | 身份、权限、密钥或授权证据 |
| `GetTagKeys` | `tag` | 密钥、安全策略、风险或告警证据 |
| `GetTagValues` | `tag` | 资源存在性、状态、配置或诊断证据 |
| `GetTags` | `tag` | 资源存在性、状态、配置或诊断证据 |
| `ListAccounts` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `ListExampleQueries` | `resourcecenter` | 资源存在性、状态、配置或诊断证据 |
| `ListInvitations` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `ListOrganizationalUnits` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `ListOrganizationalUnitsForParent` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `ListPoliciesForTarget` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `ListQueries` | `resourcecenter` | 资源存在性、状态、配置或诊断证据 |
| `ListResourceTypes` | `resourcecenter, tag` | 资源存在性、状态、配置或诊断证据 |
| `ListServiceControlPolicies` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `ListTagResources` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `ListTagsKeys` | `organization` | 密钥、安全策略、风险或告警证据 |
| `ListTagsValues` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `ListTargetsForPolicy` | `organization` | 身份、权限、密钥或授权证据 |
| `SearchMultiAccountResources` | `resourcecenter` | 资源存在性、状态、配置或诊断证据 |
| `SearchResources` | `resourcecenter` | 资源存在性、状态、配置或诊断证据 |

### 配额中心
- 官方文档识别 Action 数：20
- 纳入只读/诊断 Action：11
- 排除自动执行的写/变更 Action：8

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `GetAlarmRule` | `quota` | 密钥、安全策略、风险或告警证据 |
| `GetProductQuota` | `quota` | 计费、订单、成本、配额或资源包证据 |
| `GetQuotaApplication` | `quota` | 计费、订单、成本、配额或资源包证据 |
| `GetQuotaTemplateServiceStatus` | `quota` | 计费、订单、成本、配额或资源包证据 |
| `ListAlarmHistory` | `quota` | 密钥、安全策略、风险或告警证据 |
| `ListProductQuotaDimensions` | `quota` | 计费、订单、成本、配额或资源包证据 |
| `ListProductQuotas` | `quota` | 计费、订单、成本、配额或资源包证据 |
| `ListProducts` | `quota` | 资源存在性、状态、配置或诊断证据 |
| `ListQuotaAlarmRules` | `quota` | 计费、订单、成本、配额或资源包证据 |
| `ListQuotaApplicationTemplates` | `quota` | 计费、订单、成本、配额或资源包证据 |
| `ListQuotaApplications` | `quota` | 计费、订单、成本、配额或资源包证据 |

## 使用建议
- 优先使用章节 reference 中已经编排好的命令包；当用户问题落在未细化章节时，再从本矩阵选择最小只读 Action 补充证据。
- 如果某个只读 Action 需要分页、跨产品联动或深层字段归一，再考虑新增 `scripts/` 只读脚本，并同步更新脚本说明。
- 如果只读证据指向写操作修复，必须先输出影响面、资源 ID、回滚/恢复建议，并等待用户确认。
