# API 覆盖审查矩阵
本文件由 2026-05-22 审查生成，用于证明本 skill 已对 `cli-meta/` 中对应分类的 OpenAPI / CLI / Python SDK 能力做过覆盖盘点。它不是执行顺序清单；Agent 仍应先按主 `SKILL.md` 和章节 reference 选择最小必要证据。
## 审查口径
- 纳入排障优先级：`Describe/List/Get/Query/Check/Search/BatchGet/Verify/Validate/Test/Diagnose/Preview/Estimate` 等只读或诊断型 Action。
- 默认排除自动执行：`Create/Modify/Delete/Update/Attach/Detach/Start/Stop/Run/Invoke/Pay/Renew/Set` 等会改变资源、资金、权限或任务状态的 Action；只能作为解释错误码或 Human-in-the-Loop 建议背景。
- 命令形态：执行时统一写作 `ve <service> <Action> [--Param value...]`；参数不确定时先查 `ve <service> <Action> --help` 或对应 `cli-meta`。
- 凭证边界：只从临时环境读取 `VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、`VOLCENGINE_REGION`，不得写入配置、文档或日志。
## 总览
- 覆盖产品数：24
- 官方文档识别 OpenAPI Action 数合计：594
- 纳入排障候选的只读/诊断 Action 数：534
- 默认不自动执行的写/变更 Action 数：788
- 需人工判断语义的其它 Action 数：141

## 产品级覆盖
### AI 原生 BaaS 平台 Supabase 版
- 官方文档识别 Action 数：1
- 纳入只读/诊断 Action：24
- 排除自动执行的写/变更 Action：40
- 其它需按场景人工判断 Action：ApplyPrivateDNSToPublic, ApplyPrivateDnstoPublic, BranchRestore, DropDatabase, RestartBranch

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAPIKeys` | `aidap` | 身份、权限、密钥或授权证据 |
| `DescribeAccessControlList` | `aidap` | 资源存在性、状态、配置或诊断证据 |
| `DescribeApiKeys` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `DescribeBranchAIFunction` | `aidap` | 资源存在性、状态、配置或诊断证据 |
| `DescribeBranchAiFunction` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeBranchDetail` | `aidap` | 资源存在性、状态、配置或诊断证据 |
| `DescribeBranches` | `aidap` | 资源存在性、状态、配置或诊断证据 |
| `DescribeChildBranches` | `aidap` | 存储、备份或数据库控制面证据 |
| `DescribeComputeDetail` | `aidap` | 资源存在性、状态、配置或诊断证据 |
| `DescribeComputes` | `aidap` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDBAccountConnection` | `aidap` | 存储、备份或数据库控制面证据 |
| `DescribeDBAccounts` | `aidap` | 存储、备份或数据库控制面证据 |
| `DescribeDatabases` | `aidap` | 存储、备份或数据库控制面证据 |
| `DescribeDbAccountConnection` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `DescribeDbAccounts` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `DescribeDefaultBranch` | `aidap` | 资源存在性、状态、配置或诊断证据 |
| `DescribeOperations` | `aidap` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRestorableBranches` | `aidap` | 资源存在性、状态、配置或诊断证据 |
| `DescribeWorkspaceDetail` | `aidap` | 模型、端点、Agent 或工作空间状态证据 |
| `DescribeWorkspaceEndpoint` | `aidap` | 模型、端点、Agent 或工作空间状态证据 |
| `DescribeWorkspaceOverview` | `aidap` | 模型、端点、Agent 或工作空间状态证据 |
| `DescribeWorkspaces` | `aidap` | 模型、端点、Agent 或工作空间状态证据 |
| `GetRestoreWindow` | `aidap` | 存储、备份或数据库控制面证据 |
| `ListWorkspaceUsageTop` | `aidap` | 模型、端点、Agent 或工作空间状态证据 |

### 上下文搜索
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：26
- 排除自动执行的写/变更 Action：11
- 其它需按场景人工判断 Action：AlterTable, CalcTableLimits, DecodeRawKey, DestroyInstance, ExecuteMetaserviceCli, ExecuteQuery, GraphragAddKnowledgeBase, MigrateTabletReplica, TruncateTable

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeInstance` | `graph` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeVegraphConfigInK8s` | `graph` | 资源存在性、状态、配置或诊断证据 |
| `DescribeVegraphConfigInMetamysql` | `graph` | 存储、备份或数据库控制面证据 |
| `DescribeZones` | `graph` | 资源存在性、状态、配置或诊断证据 |
| `GetAddTablesTicketOptions` | `graph` | 资源存在性、状态、配置或诊断证据 |
| `GetConfChecker` | `graph` | 资源存在性、状态、配置或诊断证据 |
| `GetInstanceSpecScope` | `graph` | 资源状态、实例/节点/集群运行态证据 |
| `GetTable` | `graph` | 资源存在性、状态、配置或诊断证据 |
| `GetTableConfig` | `graph` | 资源存在性、状态、配置或诊断证据 |
| `GetTableIOQosOptions` | `graph` | 资源存在性、状态、配置或诊断证据 |
| `GetTableIoQosOptions` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetTableLimit` | `graph` | 资源存在性、状态、配置或诊断证据 |
| `GetTableQuota` | `graph` | 计费、订单、成本、配额或资源包证据 |
| `GetTableSchema` | `graph` | 资源存在性、状态、配置或诊断证据 |
| `GetVegraphInstanceOp` | `graph` | 资源状态、实例/节点/集群运行态证据 |
| `GetVegraphNetworkResource` | `graph` | 资源存在性、状态、配置或诊断证据 |
| `GetVegraphReadAndWriteStatus` | `graph` | 资源存在性、状态、配置或诊断证据 |
| `GetVersionSetAndComponentsInfo` | `graph` | 资源存在性、状态、配置或诊断证据 |
| `ListAllTables` | `graph` | 资源存在性、状态、配置或诊断证据 |
| `ListClusterTables` | `graph` | 资源状态、实例/节点/集群运行态证据 |
| `ListGraphRagService` | `graph` | 资源存在性、状态、配置或诊断证据 |
| `ListInstance` | `graph` | 资源状态、实例/节点/集群运行态证据 |
| `ListTabletServer` | `graph` | 资源状态、实例/节点/集群运行态证据 |
| `ListTabletTask` | `graph` | 资源存在性、状态、配置或诊断证据 |
| `ListTablets` | `graph` | 资源存在性、状态、配置或诊断证据 |
| `ValidateConfChecker` | `graph` | 资源存在性、状态、配置或诊断证据 |

### 云备份
- 官方文档识别 Action 数：25
- 纳入只读/诊断 Action：11
- 排除自动执行的写/变更 Action：21

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `CheckExternalAccountRole` | `cbr` | 身份、权限、密钥或授权证据 |
| `DescribeBackupPlans` | `cbr` | 存储、备份或数据库控制面证据 |
| `DescribeBackupPolicies` | `cbr` | 存储、备份或数据库控制面证据 |
| `DescribeBackupResources` | `cbr` | 存储、备份或数据库控制面证据 |
| `DescribeRecoveryPoints` | `cbr` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRegions` | `cbr` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRestoreJobs` | `cbr` | 存储、备份或数据库控制面证据 |
| `DescribeVaults` | `cbr` | 资源存在性、状态、配置或诊断证据 |
| `DescribeZones` | `cbr` | 资源存在性、状态、配置或诊断证据 |
| `ListExternalAccounts` | `cbr` | 资源存在性、状态、配置或诊断证据 |
| `ListTagsForResources` | `cbr` | 资源存在性、状态、配置或诊断证据 |

### 云搜索服务
- 官方文档识别 Action 数：34
- 纳入只读/诊断 Action：11
- 排除自动执行的写/变更 Action：12
- 其它需按场景人工判断 Action：RenameInstance, RestartInstance, RestartNode

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeInstance` | `escloud` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstanceNodes` | `escloud` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstancePlugins` | `escloud` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstances` | `escloud` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeIpAllowList` | `escloud` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNodeAvailableSpecs` | `escloud` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeNodeAvailableSpecsV2` | `escloud` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeScenarios` | `escloud` | 资源存在性、状态、配置或诊断证据 |
| `DescribeZones` | `escloud` | 资源存在性、状态、配置或诊断证据 |
| `ListLogs` | `escloud` | 资源存在性、状态、配置或诊断证据 |
| `ListTagsForResources` | `escloud` | 资源存在性、状态、配置或诊断证据 |

### 云数据库 MySQL 版
- 官方文档识别 Action 数：174
- 纳入只读/诊断 Action：100
- 排除自动执行的写/变更 Action：130
- 其它需按场景人工判断 Action：MigrateToOtherZone, RebuildDBGreenInstance, RebuildDBInstance, RebuildDbGreenInstance, RebuildDbInstance, RebuildDrInstance, RecoveryDBInstance, RecoveryDbInstance, RestartDBInstance, RestartDbInstance, RestoreToCrossRegionInstance, RestoreToExistedInstance, RestoreToNewInstance, SaveAsParameterTemplate, SwitchDBBlueGreen, SwitchDBInstanceHA, SwitchDBPrecheckBlueGreen, SwitchDbBlueGreen, SwitchDbInstanceHa, SwitchDbPrecheckBlueGreen ...

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAllowListDetail` | `rdsmysql, rdsmysqlv2` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAllowLists` | `rdsmysql, rdsmysqlv2` | 资源存在性、状态、配置或诊断证据 |
| `DescribeApplyParameterTemplate` | `rdsmysql, rdsmysqlv2` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAvailabilityZones` | `rdsmysqlv2` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAvailableCrossRegion` | `rdsmysqlv2` | 资源存在性、状态、配置或诊断证据 |
| `DescribeBackupDecryptionKey` | `rdsmysqlv2` | 存储、备份或数据库控制面证据 |
| `DescribeBackupEncryptionStatus` | `rdsmysqlv2` | 存储、备份或数据库控制面证据 |
| `DescribeBackupPolicy` | `rdsmysqlv2` | 身份、权限、密钥或授权证据 |
| `DescribeBackupStats` | `rdsmysqlv2` | 存储、备份或数据库控制面证据 |
| `DescribeBackups` | `rdsmysqlv2` | 存储、备份或数据库控制面证据 |
| `DescribeBinlogFiles` | `rdsmysqlv2` | 资源存在性、状态、配置或诊断证据 |
| `DescribeCrossBackupPolicy` | `rdsmysqlv2` | 身份、权限、密钥或授权证据 |
| `DescribeCrossRegionBackupDBInstances` | `rdsmysqlv2` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeCrossRegionBackupDbInstances` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBAccounts` | `rdsmysqlv2` | 存储、备份或数据库控制面证据 |
| `DescribeDBBlueGreenDifferences` | `rdsmysqlv2` | 存储、备份或数据库控制面证据 |
| `DescribeDBBlueGreenInstance` | `rdsmysqlv2` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBDisasterRecoveryInstances` | `rdsmysqlv2` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstance` | `rdsmysql` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceAttribute` | `rdsmysqlv2` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceChargeDetail` | `rdsmysqlv2` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceConnection` | `rdsmysql` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceDetail` | `rdsmysqlv2` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceEndpoints` | `rdsmysqlv2` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceEngineMinorVersions` | `rdsmysqlv2` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceHAConfig` | `rdsmysqlv2` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceNodes` | `rdsmysqlv2` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceParameters` | `rdsmysqlv2` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceParametersLog` | `rdsmysqlv2` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstancePriceDetail` | `rdsmysqlv2` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceSSL` | `rdsmysqlv2` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceSpecs` | `rdsmysqlv2` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceTDE` | `rdsmysqlv2` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstances` | `rdsmysqlv2` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBNodeParameterDifferences` | `rdsmysqlv2` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBProxy` | `rdsmysqlv2` | 存储、备份或数据库控制面证据 |
| `DescribeDBProxyConfig` | `rdsmysqlv2` | 存储、备份或数据库控制面证据 |
| `DescribeDBProxyPriceDetail` | `rdsmysqlv2` | 存储、备份或数据库控制面证据 |
| `DescribeDBSwitchBlueGreenPrecheck` | `rdsmysqlv2` | 存储、备份或数据库控制面证据 |
| `DescribeDatabases` | `rdsmysqlv2` | 存储、备份或数据库控制面证据 |
| `DescribeDbAccountTableColumnInfo` | `rdsmysqlv2` | 存储、备份或数据库控制面证据 |
| `DescribeDbAccounts` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `DescribeDbBlueGreenDifferences` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `DescribeDbBlueGreenInstance` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbDisasterRecoveryInstances` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstance` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceAttribute` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceChargeDetail` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceConnection` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceDetail` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceEndpoints` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceEngineMinorVersions` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceHaConfig` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceNodes` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceParameters` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceParametersLog` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstancePriceDetail` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceSpecs` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceSsl` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceTde` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstances` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbNodeParameterDifferences` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbProxy` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `DescribeDbProxyConfig` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `DescribeDbProxyPriceDetail` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `DescribeDbSwitchBlueGreenPrecheck` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `DescribeDeletedDBInstances` | `rdsmysqlv2` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDeletedDbInstances` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDiagnosticsInfos` | `rdsmysqlv2` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDisasterRecoveryRegions` | `rdsmysqlv2` | 资源存在性、状态、配置或诊断证据 |
| `DescribeFailoverLogs` | `rdsmysqlv2` | 资源存在性、状态、配置或诊断证据 |
| `DescribeNonWhiteSessionList` | `rdsmysqlv2` | 资源存在性、状态、配置或诊断证据 |
| `DescribeParameterTemplate` | `rdsmysql, rdsmysqlv2` | 资源存在性、状态、配置或诊断证据 |
| `DescribePlannedEvents` | `rdsmysqlv2` | 资源存在性、状态、配置或诊断证据 |
| `DescribeReadOnlyNodeDelay` | `rdsmysqlv2` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeRecoverableTime` | `rdsmysql, rdsmysqlv2` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRegions` | `rdsmysqlv2` | 资源存在性、状态、配置或诊断证据 |
| `DescribeResourcePackageDetail` | `rdsmysqlv2` | 计费、订单、成本、配额或资源包证据 |
| `DescribeResourcePackagePrice` | `rdsmysqlv2` | 计费、订单、成本、配额或资源包证据 |
| `DescribeResourcePackageSpec` | `rdsmysqlv2` | 计费、订单、成本、配额或资源包证据 |
| `DescribeResourceUsage` | `rdsmysqlv2` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTagsByResource` | `rdsmysqlv2` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTaskDetail` | `rdsmysqlv2` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTasks` | `rdsmysqlv2` | 资源存在性、状态、配置或诊断证据 |
| `DescribeUpgradeEngineMajorVersionPrecheckResult` | `rdsmysqlv2` | 资源存在性、状态、配置或诊断证据 |
| `GetBackupDownloadLink` | `rdsmysqlv2` | 存储、备份或数据库控制面证据 |
| `ListAccounts` | `rdsmysql` | 资源存在性、状态、配置或诊断证据 |
| `ListBackups` | `rdsmysql` | 存储、备份或数据库控制面证据 |
| `ListDBInstanceIPLists` | `rdsmysql` | 资源状态、实例/节点/集群运行态证据 |
| `ListDBInstances` | `rdsmysql` | 资源状态、实例/节点/集群运行态证据 |
| `ListDatabases` | `rdsmysql` | 存储、备份或数据库控制面证据 |
| `ListDbInstanceIpLists` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `ListDbInstances` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `ListInstanceParams` | `rdsmysql` | 资源状态、实例/节点/集群运行态证据 |
| `ListInstanceParamsHistory` | `rdsmysql` | 资源状态、实例/节点/集群运行态证据 |
| `ListParameterTemplates` | `rdsmysql, rdsmysqlv2` | 资源存在性、状态、配置或诊断证据 |
| `ListRegions` | `rdsmysql` | 资源存在性、状态、配置或诊断证据 |
| `ListResourcePackages` | `rdsmysqlv2` | 计费、订单、成本、配额或资源包证据 |
| `ListVpcs` | `rdsmysql` | 网络路径、入口、路由或安全策略证据 |
| `ListZones` | `rdsmysql` | 资源存在性、状态、配置或诊断证据 |

### 云数据库 PostgreSQL 版
- 官方文档识别 Action 数：10
- 纳入只读/诊断 Action：42
- 排除自动执行的写/变更 Action：77
- 其它需按场景人工判断 Action：CloneDatabase, CloneParameterTemplate, RestartDBInstance, RestartDbInstance, RestoreToExistedInstance, RestoreToNewInstance, SaveAsParameterTemplate, UnifyNewAllowList, UpgradeAllowListVersion

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAllowListDetail` | `rdspostgresql` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAllowLists` | `rdspostgresql` | 资源存在性、状态、配置或诊断证据 |
| `DescribeApplyParameterTemplate` | `rdspostgresql` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAvailabilityZones` | `rdspostgresql` | 资源存在性、状态、配置或诊断证据 |
| `DescribeBackupPolicy` | `rdspostgresql` | 身份、权限、密钥或授权证据 |
| `DescribeBackups` | `rdspostgresql` | 存储、备份或数据库控制面证据 |
| `DescribeDBAccounts` | `rdspostgresql` | 存储、备份或数据库控制面证据 |
| `DescribeDBEngineVersionParameters` | `rdspostgresql` | 存储、备份或数据库控制面证据 |
| `DescribeDBInstanceDetail` | `rdspostgresql` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceParameters` | `rdspostgresql` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceParametersLog` | `rdspostgresql` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstancePriceDetail` | `rdspostgresql` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstancePriceDifference` | `rdspostgresql` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceProxyParameters` | `rdspostgresql` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceSSL` | `rdspostgresql` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceSpecs` | `rdspostgresql` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstances` | `rdspostgresql` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDatabases` | `rdspostgresql` | 存储、备份或数据库控制面证据 |
| `DescribeDbAccounts` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `DescribeDbEngineVersionParameters` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `DescribeDbInstanceDetail` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceParameters` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceParametersLog` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstancePriceDetail` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstancePriceDifference` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceProxyParameters` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceSpecs` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceSsl` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstances` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDetachedBackups` | `rdspostgresql` | 存储、备份或数据库控制面证据 |
| `DescribeFailoverLogs` | `rdspostgresql` | 资源存在性、状态、配置或诊断证据 |
| `DescribeParameterTemplate` | `rdspostgresql` | 资源存在性、状态、配置或诊断证据 |
| `DescribePlannedEvents` | `rdspostgresql` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRecoverableTime` | `rdspostgresql` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRegions` | `rdspostgresql` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSchemas` | `rdspostgresql` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSlots` | `rdspostgresql` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTasks` | `rdspostgresql` | 资源存在性、状态、配置或诊断证据 |
| `DescribeWALLogBackups` | `rdspostgresql` | 存储、备份或数据库控制面证据 |
| `DescribeWalLogBackups` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `GetBackupDownloadLink` | `rdspostgresql` | 存储、备份或数据库控制面证据 |
| `ListParameterTemplates` | `rdspostgresql` | 资源存在性、状态、配置或诊断证据 |

### 云数据库 SQL Server 版
- 官方文档识别 Action 数：42
- 纳入只读/诊断 Action：21
- 排除自动执行的写/变更 Action：32
- 其它需按场景人工判断 Action：RestartDBInstance, RestartDbInstance, RestoreToExistedInstance

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAllowListDetail` | `rdsmssql` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAllowLists` | `rdsmssql` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAvailabilityZones` | `rdsmssql` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAvailableCrossRegion` | `rdsmssql` | 资源存在性、状态、配置或诊断证据 |
| `DescribeBackupDetail` | `rdsmssql` | 存储、备份或数据库控制面证据 |
| `DescribeBackups` | `rdsmssql` | 存储、备份或数据库控制面证据 |
| `DescribeCrossBackupPolicy` | `rdsmssql` | 身份、权限、密钥或授权证据 |
| `DescribeDBAccounts` | `rdsmssql` | 存储、备份或数据库控制面证据 |
| `DescribeDBInstanceDetail` | `rdsmssql` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceParameters` | `rdsmssql` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceSpecs` | `rdsmssql` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstances` | `rdsmssql` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbAccounts` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `DescribeDbInstanceDetail` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceParameters` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceSpecs` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstances` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstanceAllowLists` | `rdsmssql` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeRegions` | `rdsmssql` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTosRestoreTaskDetail` | `rdsmssql` | 存储、备份或数据库控制面证据 |
| `DescribeTosRestoreTasks` | `rdsmssql` | 存储、备份或数据库控制面证据 |

### 云数据库 veDB MySQL 版
- 官方文档识别 Action 数：80
- 纳入只读/诊断 Action：37
- 排除自动执行的写/变更 Action：66
- 其它需按场景人工判断 Action：ApplyParameterTemplate, RestartDBInstance, RestartDbInstance, RestoreTable, RestoreToNewInstance, SaveAsParameterTemplate

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAllowListDetail` | `vedbm` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAllowLists` | `vedbm` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAvailabilityZones` | `vedbm` | 资源存在性、状态、配置或诊断证据 |
| `DescribeBackupPolicy` | `vedbm` | 身份、权限、密钥或授权证据 |
| `DescribeBackups` | `vedbm` | 存储、备份或数据库控制面证据 |
| `DescribeCrossRegionBackupDBInstances` | `vedbm` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeCrossRegionBackupDbInstances` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeCrossRegionBackupPolicy` | `vedbm` | 身份、权限、密钥或授权证据 |
| `DescribeDBAccounts` | `vedbm` | 存储、备份或数据库控制面证据 |
| `DescribeDBEndpoint` | `vedbm` | 存储、备份或数据库控制面证据 |
| `DescribeDBInstanceDetail` | `vedbm` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceParameterChangeHistory` | `vedbm` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceParameters` | `vedbm` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstancePriceDetail` | `vedbm` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceSpecs` | `vedbm` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceVersion` | `vedbm` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstances` | `vedbm` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDatabases` | `vedbm` | 存储、备份或数据库控制面证据 |
| `DescribeDbAccounts` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `DescribeDbEndpoint` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `DescribeDbInstanceDetail` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceParameterChangeHistory` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceParameters` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstancePriceDetail` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceSpecs` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceVersion` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstances` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeExistDBInstancePrice` | `vedbm` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeExistDbInstancePrice` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstanceAllowLists` | `vedbm` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeModifiableParameters` | `vedbm` | 资源存在性、状态、配置或诊断证据 |
| `DescribeParameterTemplateDetail` | `vedbm` | 资源存在性、状态、配置或诊断证据 |
| `DescribeParameterTemplates` | `vedbm` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRecoverableTime` | `vedbm` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRegions` | `vedbm` | 资源存在性、状态、配置或诊断证据 |
| `DescribeScheduleEvents` | `vedbm` | 资源存在性、状态、配置或诊断证据 |
| `DescribeStoragePayablePrice` | `vedbm` | 资源存在性、状态、配置或诊断证据 |

### 向量数据库 Milvus 版
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：10
- 排除自动执行的写/变更 Action：11
- 其它需按场景人工判断 Action：MSCreateInstance, MSCreateInstanceOneStep, MSDescribeInstance, MSDescribeInstances, MSModifyEndpointAllowGroup, MSModifyPublicDomain, MSReleaseInstance, ScaleInstance

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAvailableSpec` | `milvus` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAvailableVersion` | `milvus` | 资源存在性、状态、配置或诊断证据 |
| `DescribeConfigModules` | `milvus` | 资源存在性、状态、配置或诊断证据 |
| `DescribeInstanceConfig` | `milvus` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstanceDetail` | `milvus` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstances` | `milvus` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeNodeInfo` | `milvus` | 资源状态、实例/节点/集群运行态证据 |
| `DescribePrice` | `milvus` | 资源存在性、状态、配置或诊断证据 |
| `DescribeZones` | `milvus` | 资源存在性、状态、配置或诊断证据 |
| `ListTagsForResources` | `milvus` | 资源存在性、状态、配置或诊断证据 |

### 大数据文件存储
- 官方文档识别 Action 数：28
- 纳入只读/诊断 Action：2
- 排除自动执行的写/变更 Action：2

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeNamespaces` | `cfs` | 资源存在性、状态、配置或诊断证据 |
| `GetNamespaceQuota` | `cfs` | 计费、订单、成本、配额或资源包证据 |

### 存储迁移服务
- 官方文档识别 Action 数：27
- 纳入只读/诊断 Action：2
- 排除自动执行的写/变更 Action：5

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `ListDataMigrateTask` | `dms` | 资源存在性、状态、配置或诊断证据 |
| `QueryDataMigrateTask` | `dms` | 资源存在性、状态、配置或诊断证据 |

### 对象存储
- 官方文档识别 Action 数：15
- 纳入只读/诊断 Action：15
- 排除自动执行的写/变更 Action：19
- 其它需按场景人工判断 Action：AbortMultipartUpload, AppendObject, CompleteMultipartUpload, GeneratePresignedUrl, HeadBucket, HeadObject

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `GetIndex` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetObject` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `GetObjectAcl` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |
| `GetVectorBucket` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `GetVectorBucketPolicy` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `GetVectors` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListBuckets` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `ListIndexes` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListMultipartUploads` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListObjectVersions` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `ListObjects` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `ListParts` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListVectorBuckets` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `ListVectors` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `QueryVectors` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |

### 弹性块存储
- 官方文档识别 Action 数：1
- 纳入只读/诊断 Action：11
- 排除自动执行的写/变更 Action：25
- 其它需按场景人工判断 Action：ApplyAutoSnapshotPolicy, CalculatePriceV2, ExtendVolume, ReInitializeVolume, RollbackSnapshotGroup, RollbackVolume

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAutoSnapshotPolicy` | `storageebs` | 身份、权限、密钥或授权证据 |
| `DescribePlacementGroupDetails` | `storageebs` | 资源存在性、状态、配置或诊断证据 |
| `DescribePlacementGroups` | `storageebs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeReservedStorageCapacity` | `storageebs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSnapshotChains` | `storageebs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSnapshotGroups` | `storageebs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSnapshots` | `storageebs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSnapshotsUsage` | `storageebs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTags` | `storageebs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeVolumeType` | `storageebs` | 存储、备份或数据库控制面证据 |
| `DescribeVolumes` | `storageebs` | 存储、备份或数据库控制面证据 |

### 弹性文件存储
- 官方文档识别 Action 数：66
- 纳入只读/诊断 Action：12
- 排除自动执行的写/变更 Action：23

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `CheckDir` | `efs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAccessPoints` | `efs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeFileSystems` | `efs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeMountPoints` | `efs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeNamespaces` | `cfs` | 资源存在性、状态、配置或诊断证据 |
| `DescribePermissionGroups` | `efs` | 身份、权限、密钥或授权证据 |
| `DescribePermissionRules` | `efs` | 身份、权限、密钥或授权证据 |
| `DescribeQuotas` | `efs` | 计费、订单、成本、配额或资源包证据 |
| `DescribeRegions` | `efs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeZones` | `efs` | 资源存在性、状态、配置或诊断证据 |
| `GetNamespaceQuota` | `cfs` | 计费、订单、成本、配额或资源包证据 |
| `ListTagsForResources` | `efs` | 资源存在性、状态、配置或诊断证据 |

### 弹性极速缓存
- 官方文档识别 Action 数：8
- 纳入只读/诊断 Action：10
- 排除自动执行的写/变更 Action：21

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `CheckDir` | `efs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAccessPoints` | `efs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeFileSystems` | `efs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeMountPoints` | `efs` | 资源存在性、状态、配置或诊断证据 |
| `DescribePermissionGroups` | `efs` | 身份、权限、密钥或授权证据 |
| `DescribePermissionRules` | `efs` | 身份、权限、密钥或授权证据 |
| `DescribeQuotas` | `efs` | 计费、订单、成本、配额或资源包证据 |
| `DescribeRegions` | `efs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeZones` | `efs` | 资源存在性、状态、配置或诊断证据 |
| `ListTagsForResources` | `efs` | 资源存在性、状态、配置或诊断证据 |

### 数据库传输服务
- 官方文档识别 Action 数：5
- 纳入只读/诊断 Action：21
- 排除自动执行的写/变更 Action：30
- 其它需按场景人工判断 Action：CrossRegionUpsertValidationTask, GenerateValidationResultFile, PreCheckAsync, RetryTransmissionTask, RetryTransmissionTasks, RetryValidationTask, RetryValidationTasks, SpawnSwimmingLane, SuspendTransmissionTask, SuspendTransmissionTasks, SuspendValidationTask, SuspendValidationTasks

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeDataSource` | `dts` | 资源存在性、状态、配置或诊断证据 |
| `DescribePriceDifferences` | `dts` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSubscriptionGroup` | `dts` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSubscriptionGroupProgress` | `dts` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSubscriptionGroups` | `dts` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSupportedValidationTypes` | `dts` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTagsByResource` | `dts` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTransmissionTaskInfo` | `dts` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTransmissionTaskProgress` | `dts` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTransmissionTasks` | `dts` | 资源存在性、状态、配置或诊断证据 |
| `DescribeValidationTaskInfo` | `dts` | 资源存在性、状态、配置或诊断证据 |
| `DescribeValidationTaskResult` | `dts` | 资源存在性、状态、配置或诊断证据 |
| `DescribeValidationTasks` | `dts` | 资源存在性、状态、配置或诊断证据 |
| `GetAsyncPreCheckResult` | `dts20180101` | 资源存在性、状态、配置或诊断证据 |
| `GetDBTableDiffDetails` | `dts` | 存储、备份或数据库控制面证据 |
| `GetDbTableDiffDetails` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `ListDataSource` | `dts` | 资源存在性、状态、配置或诊断证据 |
| `ListVPC` | `dts20180101` | 网络路径、入口、路由或安全策略证据 |
| `ListVPCSubnets` | `dts20180101` | 网络路径、入口、路由或安全策略证据 |
| `ListVpc` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |
| `ListVpcSubnets` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |

### 数据库工作台
- 官方文档识别 Action 数：2
- 纳入只读/诊断 Action：10
- 排除自动执行的写/变更 Action：3
- 其它需按场景人工判断 Action：AgreeUserProtocol, ExecuteSQL, ExecuteSql, GenerateSQLFromNL, GenerateSqlFromNl, ManualExecuteTicket, SlowQueryAdviceTaskHistoryApi

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAuditLogConfig` | `dbw` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAuditLogDetail` | `dbw` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSlowLogs` | `dbw` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTicketDetail` | `dbw` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTickets` | `dbw` | 资源存在性、状态、配置或诊断证据 |
| `DescribeWorkflow` | `dbw` | 资源存在性、状态、配置或诊断证据 |
| `GetTableInfo` | `dbw` | 资源存在性、状态、配置或诊断证据 |
| `ListDatabases` | `dbw` | 存储、备份或数据库控制面证据 |
| `ListSlowQueryAdviceApi` | `dbw` | 资源存在性、状态、配置或诊断证据 |
| `ListTables` | `dbw` | 资源存在性、状态、配置或诊断证据 |

### 数据闪送服务
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 文件存储 vePFS
- 官方文档识别 Action 数：48
- 纳入只读/诊断 Action：19
- 排除自动执行的写/变更 Action：35
- 其它需按场景人工判断 Action：ConfigDataFlowBandwidth, ExpandFileSystem

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAudits` | `vepfs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDataFlowBandwidth` | `vepfs` | 网络路径、入口、路由或安全策略证据 |
| `DescribeDataFlowTasks` | `vepfs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeFileSystemOverview` | `vepfs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeFileSystemStatistics` | `vepfs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeFileSystems` | `vepfs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeFilesets` | `vepfs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeLensPolicies` | `vepfs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeLensServices` | `vepfs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeLensTasks` | `vepfs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeMountServiceClients` | `vepfs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeMountServiceNodeTypes` | `vepfs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeMountServiceTaskResults` | `vepfs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeMountServiceTasks` | `vepfs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeMountServices` | `vepfs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRegions` | `vepfs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeZones` | `vepfs` | 资源存在性、状态、配置或诊断证据 |
| `ListTagsForResources` | `vepfs` | 资源存在性、状态、配置或诊断证据 |
| `VerifyMountServiceClients` | `vepfs` | 资源存在性、状态、配置或诊断证据 |

### 文档数据库 MongoDB 版
- 官方文档识别 Action 数：5
- 纳入只读/诊断 Action：35
- 排除自动执行的写/变更 Action：49
- 其它需按场景人工判断 Action：ApplyDbInstanceParamTpl, MigrateAvailabilityZones, RestartDBInstance, RestartDbInstance, RestoreToNewInstance, SwitchDBMaster, SwitchDbMaster

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAllowListDetail` | `mongodb` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAllowLists` | `mongodb` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAvailabilityZones` | `mongodb` | 资源存在性、状态、配置或诊断证据 |
| `DescribeBackups` | `mongodb` | 存储、备份或数据库控制面证据 |
| `DescribeCreateInstanceProgress` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBAccounts` | `mongodb` | 存储、备份或数据库控制面证据 |
| `DescribeDBEndpoint` | `mongodb` | 存储、备份或数据库控制面证据 |
| `DescribeDBInstanceBackupPolicy` | `mongodb` | 身份、权限、密钥或授权证据 |
| `DescribeDBInstanceBackupURL` | `mongodb` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceDetail` | `mongodb` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceParameters` | `mongodb` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceParametersLog` | `mongodb` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceSSL` | `mongodb` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstances` | `mongodb` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDatabaseDetail` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `DescribeDbAccounts` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `DescribeDbEndpoint` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `DescribeDbInstanceBackupPolicy` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `DescribeDbInstanceBackupUrl` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceDetail` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceParamTplDetail` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceParamTpls` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceParameters` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceParametersLog` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceSsl` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstances` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstanceAllowLists` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeMultiDbInstanceParameters` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeNodeSpecs` | `mongodb` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeNormalLogs` | `mongodb` | 资源存在性、状态、配置或诊断证据 |
| `DescribePlannedEvents` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRecoverableTime` | `mongodb` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRegions` | `mongodb` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSlowLogs` | `mongodb` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTemplateParameter` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |

### 日志服务
- 官方文档识别 Action 数：9
- 纳入只读/诊断 Action：51
- 排除自动执行的写/变更 Action：71
- 其它需按场景人工判断 Action：ActiveTlsAccount, ApplyRuleToHostGroups, BatchBindTopics, ConsumeLogs, ConsumerHeartbeat, ExecProcessor, ManualShardSplit, OperateProcessor, WebTracks, WithApiKey

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `CheckSchemeAndEndpoint` | `Python SDK-only/未匹配 CLI` | 模型、端点、Agent 或工作空间状态证据 |
| `DescribeAlarmContentTemplates` | `Python SDK-only/未匹配 CLI` | 密钥、安全策略、风险或告警证据 |
| `DescribeAlarmNotifyGroups` | `Python SDK-only/未匹配 CLI` | 密钥、安全策略、风险或告警证据 |
| `DescribeAlarmWebhookIntegrations` | `Python SDK-only/未匹配 CLI` | 密钥、安全策略、风险或告警证据 |
| `DescribeAlarms` | `Python SDK-only/未匹配 CLI` | 密钥、安全策略、风险或告警证据 |
| `DescribeCheckpoint` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeConsumerGroups` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeCursor` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDownloadTasks` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDownloadUrl` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeEtlTask` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeEtlTasks` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeHistogram` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeHistogramV1` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeHostGroup` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeHostGroupRules` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeHostGroups` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeHosts` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImportTask` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImportTasks` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeIndex` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeKafkaConsumer` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeLogContext` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeProcessor` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeProcessorBindings` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeProcessorByTopic` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeProcessorFunctions` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeProcessors` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeProject` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeProjects` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRule` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRules` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeScheduleSqlTask` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeScheduleSqlTasks` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeShards` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeShipper` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeShippers` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTopic` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTopics` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTopicsByProcessor` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTrace` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTraceInstance` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeTraceInstances` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `GetAccountStatus` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetRegion` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetRetryPolicy` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `GetServiceInfo` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListTagsForResources` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `SearchLogs` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `SearchLogsV2` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `SearchTraces` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |

### 缓存数据库 Redis 版
- 官方文档识别 Action 数：8
- 纳入只读/诊断 Action：52
- 排除自动执行的写/变更 Action：79
- 其它需按场景人工判断 Action：DecreaseDBInstanceNodeNumber, DecreaseDbInstanceNodeNumber, ExecutePlannedEvent, FlushDBInstance, FlushDbInstance, IncreaseDBInstanceNodeNumber, IncreaseDbInstanceNodeNumber, InterruptKeyScanJob, RestartDBInstance, RestartDBInstanceProxy, RestartDbInstance, RestartDbInstanceProxy, RestoreDBInstance, RestoreDbInstance, SwitchOver, SwitchoverBlueGreenDeployment, UpgradeAllowListVersion

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAllowListDetail` | `redis` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAllowLists` | `redis` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAvailableCrossRegion` | `redis` | 资源存在性、状态、配置或诊断证据 |
| `DescribeBackupPlan` | `redis` | 存储、备份或数据库控制面证据 |
| `DescribeBackupPointDownloadUrls` | `redis` | 存储、备份或数据库控制面证据 |
| `DescribeBackups` | `redis` | 存储、备份或数据库控制面证据 |
| `DescribeBigKeys` | `redis` | 密钥、安全策略、风险或告警证据 |
| `DescribeBlueGreenDeployments` | `redis` | 资源存在性、状态、配置或诊断证据 |
| `DescribeCrossRegionBackupPolicy` | `redis` | 身份、权限、密钥或授权证据 |
| `DescribeCrossRegionBackups` | `redis` | 存储、备份或数据库控制面证据 |
| `DescribeDBEngineVersions` | `redis` | 存储、备份或数据库控制面证据 |
| `DescribeDBInstanceAclCategories` | `redis` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceAclCommands` | `redis` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceBandwidthPerShard` | `redis` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceDetail` | `redis` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceParams` | `redis` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceShards` | `redis` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstanceSpecs` | `redis` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstances` | `redis` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbEngineVersions` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `DescribeDbInstanceAclCategories` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceAclCommands` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceBandwidthPerShard` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceDetail` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceParams` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceShards` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceSpecs` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstances` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeEnterpriseDBInstanceDetail` | `redis` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeEnterpriseDBInstanceParams` | `redis` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeEnterpriseDBInstanceSpecs` | `redis` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeEnterpriseDbInstanceDetail` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeEnterpriseDbInstanceParams` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeEnterpriseDbInstanceSpecs` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeEnterpriseZones` | `redis` | 资源存在性、状态、配置或诊断证据 |
| `DescribeHotKeys` | `redis` | 密钥、安全策略、风险或告警证据 |
| `DescribeKeyScanJobs` | `redis` | 密钥、安全策略、风险或告警证据 |
| `DescribeNodeIds` | `redis` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeParameterGroupDetail` | `redis` | 资源存在性、状态、配置或诊断证据 |
| `DescribeParameterGroups` | `redis` | 资源存在性、状态、配置或诊断证据 |
| `DescribePitrTimeWindow` | `redis` | 资源存在性、状态、配置或诊断证据 |
| `DescribePlannedEvents` | `redis` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRegions` | `redis` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSlowLogs` | `redis` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTagsByResource` | `redis` | 资源存在性、状态、配置或诊断证据 |
| `DescribeZones` | `redis` | 资源存在性、状态、配置或诊断证据 |
| `ListDBAccount` | `redis` | 存储、备份或数据库控制面证据 |
| `ListDbAccount` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `TestFailoverDBInstanceZone` | `redis` | 资源状态、实例/节点/集群运行态证据 |
| `TestFailoverDbInstanceZone` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `TestShutDownDBInstanceNodes` | `redis` | 资源状态、实例/节点/集群运行态证据 |
| `TestShutDownDbInstanceNodes` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |

### 表格数据库 HBase 版
- 官方文档识别 Action 数：5
- 纳入只读/诊断 Action：7
- 排除自动执行的写/变更 Action：15
- 其它需按场景人工判断 Action：RestartDBInstance, RestartDbInstance

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAllowListDetail` | `hbase` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAllowLists` | `hbase` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDBInstanceDetail` | `hbase` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDBInstances` | `hbase` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstanceDetail` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDbInstances` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeTagsByResource` | `hbase` | 资源存在性、状态、配置或诊断证据 |

### 记忆库 Mem0
- 官方文档识别 Action 数：1
- 纳入只读/诊断 Action：5
- 排除自动执行的写/变更 Action：11

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAPIKeyDetail` | `mem0` | 身份、权限、密钥或授权证据 |
| `DescribeApiKeyDetail` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `DescribeMemoryProjectDetail` | `mem0` | 资源存在性、状态、配置或诊断证据 |
| `DescribeMemoryProjects` | `mem0` | 资源存在性、状态、配置或诊断证据 |
| `ListTagsForResources` | `mem0` | 资源存在性、状态、配置或诊断证据 |

## 使用建议
- 优先使用章节 reference 中已经编排好的命令包；当用户问题落在未细化章节时，再从本矩阵选择最小只读 Action 补充证据。
- 如果某个只读 Action 需要分页、跨产品联动或深层字段归一，再考虑新增 `scripts/` 只读脚本，并同步更新脚本说明。
- 如果只读证据指向写操作修复，必须先输出影响面、资源 ID、回滚/恢复建议，并等待用户确认。
