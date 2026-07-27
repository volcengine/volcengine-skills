# API 覆盖审查矩阵
本文件由 2026-05-22 审查生成，用于证明本 skill 已对 `cli-meta/` 中对应分类的 OpenAPI / CLI / Python SDK 能力做过覆盖盘点。它不是执行顺序清单；Agent 仍应先按主 `SKILL.md` 和章节 reference 选择最小必要证据。
## 审查口径
- 纳入排障优先级：`Describe/List/Get/Query/Check/Search/BatchGet/Verify/Validate/Test/Diagnose/Preview/Estimate` 等只读或诊断型 Action。
- 默认排除自动执行：`Create/Modify/Delete/Update/Attach/Detach/Start/Stop/Run/Invoke/Pay/Renew/Set` 等会改变资源、资金、权限或任务状态的 Action；只能作为解释错误码或 Human-in-the-Loop 建议背景。
- 命令形态：执行时统一写作 `ve <service> <Action> [--Param value...]`；参数不确定时先查 `ve <service> <Action> --help` 或对应 `cli-meta`。
- 凭证边界：只从临时环境读取 `VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、`VOLCENGINE_REGION`，不得写入配置、文档或日志。
## 总览
- 覆盖产品数：14
- 官方文档识别 OpenAPI Action 数合计：642
- 纳入排障候选的只读/诊断 Action 数：379
- 默认不自动执行的写/变更 Action 数：238
- 需人工判断语义的其它 Action 数：109

## 产品级覆盖
### DDoS防护
- 官方文档识别 Action 数：53
- 纳入只读/诊断 Action：4
- 排除自动执行的写/变更 Action：5
- 其它需按场景人工判断 Action：BatchAddFwdRule, BatchAddHostRule, BatchDelHostRule, BatchDeleteFwdRule, BatchSwitchBackupServers, BatchUpdHostRule, DelHostRule, DelWebDefCcRule, DescAtkAlarmThreshold, DescCertificate, DescWebAtkOverview, DescWebAtkStatistics, DescWebAtkTopSrcIp, DescWebAtkTopUrl, DescWebBpsFlow, DescWebQpsFlow, DescWebRespCode, UpdHostRule, UpdWebDefCcRule

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAttackFlow` | `advdefence20230308` | 资源存在性、状态、配置或诊断证据 |
| `DescribeBizFlowAndConnCount` | `advdefence20230308` | 资源存在性、状态、配置或诊断证据 |
| `GetFwdRuleLipList` | `advdefence` | 资源存在性、状态、配置或诊断证据 |
| `GetHostDefStatus` | `advdefence` | 资源存在性、状态、配置或诊断证据 |

### Web应用防火墙
- 官方文档识别 Action 数：75
- 纳入只读/诊断 Action：41
- 排除自动执行的写/变更 Action：55
- 其它需按场景人工判断 Action：BatchUpdateTLSFieldsConfig, BatchUpdateTlsFieldsConfig

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `CheckLLMPrompt` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `CheckLLMResponseStream` | `waf` | 域名、证书、CDN、直播或入口链路证据 |
| `CheckLlmPrompt` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `CheckLlmResponseStream` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `GetDomainInfo` | `waf` | 域名、证书、CDN、直播或入口链路证据 |
| `GetInstanceCtl` | `waf` | 资源状态、实例/节点/集群运行态证据 |
| `GetReqQPSAnalysis` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `GetReqQpsAnalysis` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetTLSConfig` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `GetTlsConfig` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetVulnerabilityConfig` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `ListAclRule` | `waf` | 网络路径、入口、路由或安全策略证据 |
| `ListAllIpGroups` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `ListAllowRule` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `ListAreaBlockRule` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `ListBlockRule` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `ListBotAnalyseProtectRule` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `ListBotAnalyseProtectRulePriorityAvailable` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `ListCCRule` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `ListCcRule` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListCertificateServices` | `waf` | 域名、证书、CDN、直播或入口链路证据 |
| `ListCustomBotConfig` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `ListCustomPage` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `ListDomain` | `waf` | 域名、证书、CDN、直播或入口链路证据 |
| `ListHostGroup` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `ListIpGroup` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `ListLoadBalancer` | `waf` | 计费、订单、成本、配额或资源包证据 |
| `ListProhibition` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `ListSystemBotConfig` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `ListTamperProof` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `ListVulWhiteField` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `ListVulnerabilityRule` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `ListWafServiceCertificate` | `waf` | 域名、证书、CDN、直播或入口链路证据 |
| `QueryAttackAnalysisTermsAggLb` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `QueryAttackAnalysisWithRuleAggLb` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `QueryAttackSecurityEvent` | `waf` | 网络路径、入口、路由或安全策略证据 |
| `QueryCertificateIfReplace` | `waf` | 域名、证书、CDN、直播或入口链路证据 |
| `QueryFlowOverviewLb` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `QueryLLMGenerate` | `waf` | 资源存在性、状态、配置或诊断证据 |
| `QueryLlmGenerate` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `QueryProtectionOverviewLb` | `waf` | 资源存在性、状态、配置或诊断证据 |

### 业务风险识别
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 云信任中心
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：2

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 云加密机
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：5
- 排除自动执行的写/变更 Action：0

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `BatchGetSecretValue` | `metakms` | 密钥、安全策略、风险或告警证据 |
| `DescribeSecret` | `metakms` | 密钥、安全策略、风险或告警证据 |
| `DescribeSecretVersions` | `metakms` | 密钥、安全策略、风险或告警证据 |
| `DescribeSecrets` | `metakms` | 密钥、安全策略、风险或告警证据 |
| `GetSecretValue` | `metakms` | 密钥、安全策略、风险或告警证据 |

### 云堡垒机
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 云安全中心
- 官方文档识别 Action 数：376
- 纳入只读/诊断 Action：268
- 排除自动执行的写/变更 Action：103
- 其它需按场景人工判断 Action：AllAssetScan, AssetScan, BanAlarmIP, BanAlarmIp, BaselineChecklistWhite, BatchAddHostToGroup, BatchCreateRepoRegistryVpcAuth, BatchDeleteVarmorPolicies, BatchDetectWeakPassword, BatchInstallVarmorApps, BatchUninstallVarmorApps, BatchUpgradeVarmorApps, CalculateRepoImageScanQuota, ControlMonitorPolicy, CreatFileScanTask, DetectBaseline, DetectBaselineByCheckConfig, DetectVuln, DetectVulnForAI, DetectVulnForAi ...

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `CheckAlarmSupportBanIP` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `CheckAlarmSupportBanIp` | `Python SDK-only/未匹配 CLI` | 密钥、安全策略、风险或告警证据 |
| `CheckInstallAgentClient` | `seccenter20240508` | 模型、端点、Agent 或工作空间状态证据 |
| `CheckInstallRasp` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `CheckMonitorPolicy` | `seccenter20240508` | 身份、权限、密钥或授权证据 |
| `DescribeFileChangeTrendTop5` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `DescribeFileMonitorOverview` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `DescribeLastWeekFileChangeTrends` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetAIAlarmJudgeConfig` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `GetAIApplicationSyncConfig` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetAIFingerprintApp` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetAIFingerprintPort` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetAIFingerprintProcess` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetAIFingerprintRefreshStatus` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetAIFingerprintSoftware` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetAIFingerprintStatistics` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetAIFingerprintTop5` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetAISessionVulnInfo` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetAIVulnDetectProgressDetail` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetAiAlarmJudgeConfig` | `Python SDK-only/未匹配 CLI` | 密钥、安全策略、风险或告警证据 |
| `GetAiApplicationSyncConfig` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetAiFingerprintApp` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetAiFingerprintPort` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetAiFingerprintProcess` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetAiFingerprintRefreshStatus` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetAiFingerprintSoftware` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetAiFingerprintStatistics` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetAiFingerprintTop5` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetAiSessionVulnInfo` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetAiVulnDetectProgressDetail` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetAlarmBySmithKey` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `GetAlarmRuleList` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `GetAlarmTrace` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `GetAlarmTraceRawData` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `GetAlarmVirusStatistics` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `GetAllMonitorSuffixList` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetArmorProfile` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetAssetClusterStatistic` | `seccenter20240508` | 资源状态、实例/节点/集群运行态证据 |
| `GetAssetClustersSyncEnd` | `seccenter20240508` | 资源状态、实例/节点/集群运行态证据 |
| `GetAssetWorkloadStatistic` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetAutoIsolateAgentList` | `seccenter20240508` | 模型、端点、Agent 或工作空间状态证据 |
| `GetAutoProtectConfig` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetBaselineDetectProgressDetail` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetBaselineGroupStatistics` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetBruteForceBanCapParams` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetBruteForceBanConfig` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetBruteForceBanStatistics` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetCisDetail` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetClusterStatistics` | `seccenter20240508` | 资源状态、实例/节点/集群运行态证据 |
| `GetClustersPermissionResult` | `seccenter20240508` | 身份、权限、密钥或授权证据 |
| `GetCustomWeakPasswords` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetDevAssetOverview` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetDevDetail` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetDevFingerprintPort` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetDevFingerprintProcess` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetDevFingerprintSoftware` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetDevFingerprintStatistics` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetDownloadStatus` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetFingerprintApp` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetFingerprintAppGroup` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetFingerprintCron` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetFingerprintEnv` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetFingerprintIntegrity` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetFingerprintKmod` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetFingerprintPort` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetFingerprintProcess` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetFingerprintRefreshStatus` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetFingerprintService` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetFingerprintSoftware` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetFingerprintStatistics` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetFingerprintTop5` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetFingerprintUser` | `seccenter20240508` | 身份、权限、密钥或授权证据 |
| `GetFingerprintWeb` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetGeoLocation` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetGroupCheckStatus` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetHidsAlarmInfo` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `GetHidsAlarmStatistics` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `GetHidsAlarmSummaryInfo` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `GetHostAssetOverview` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetHostBasicInfo` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetHostImportantProtectState` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetHostVolume` | `seccenter20240508` | 存储、备份或数据库控制面证据 |
| `GetHostVulnInfo` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetIntrusionRealTimeUpdates` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetIntrusionRiskTrends` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `GetK8sAssetStatistic` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetLayeredGroups` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetMLPAssetSyncTaskDetail` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetMLPAssetSyncTaskStatus` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetManualSyncAIApplicationStatus` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetManualSyncAiApplicationStatus` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetMlpAlarmStatistics` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `GetMlpAlarmSummaryInfo` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `GetMlpAssetSyncTaskDetail` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetMlpAssetSyncTaskStatus` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetMlpUpdateSoftwareTaskDetail` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetMonitorPolicyDirectory` | `seccenter20240508` | 身份、权限、密钥或授权证据 |
| `GetMultiLevelAuthDetail` | `seccenter20240508` | 身份、权限、密钥或授权证据 |
| `GetMultiLevelHostAssetOverview` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetMultiLevelInstitutionDetail` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetNeighboringAlarm` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `GetOfflineNotificationConfig` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetOfflineNotificationList` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetOneRaspAlarm` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `GetPolicyStatistics` | `seccenter20240508` | 身份、权限、密钥或授权证据 |
| `GetRaspAlarmStatistics` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `GetRaspAlarmSummaryInfo` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `GetRaspAuthorizationStatistics` | `seccenter20240508` | 身份、权限、密钥或授权证据 |
| `GetRaspConfigStatistics` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetRaspProcessDetail` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetRaspProtectStatistics` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetRegistriesPermissionResult` | `seccenter20240508` | 身份、权限、密钥或授权证据 |
| `GetRegistryImageDetail` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetRegistryImagesSyncStatus` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetRegistrySyncConfig` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetRegularClean` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetRegularVirusScanConfig` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetRegularVirusTaskStatus` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetRepoImageRiskCnt` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `GetRepoImageScanCron` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetRepoImageScanScope` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetRepoRegistrySummary` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetRepoRegistryVpcAuthCreateInfo` | `seccenter20240508` | 身份、权限、密钥或授权证据 |
| `GetSOCAssetAlarmStats` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `GetSOCAssetInstanceProtectStatus` | `seccenter20240508` | 资源状态、实例/节点/集群运行态证据 |
| `GetSOCAssetSecurityScore` | `seccenter20240508` | 网络路径、入口、路由或安全策略证据 |
| `GetSOCAssetVulnStats` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetSOCPrecautionBaselineStats` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetSecurityOverview` | `seccenter20240508` | 网络路径、入口、路由或安全策略证据 |
| `GetSecurityOverviewScoreStats` | `seccenter20240508` | 网络路径、入口、路由或安全策略证据 |
| `GetSocAssetAlarmStats` | `Python SDK-only/未匹配 CLI` | 密钥、安全策略、风险或告警证据 |
| `GetSocAssetInstanceProtectStatus` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `GetSocAssetSecurityScore` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |
| `GetSocAssetVulnStats` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetSocPrecautionBaselineStats` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetStackTrace` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetTLSInfo` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetTenantQuota` | `seccenter20240508` | 计费、订单、成本、配额或资源包证据 |
| `GetTlsInfo` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetUserBatchScanStatus` | `seccenter20240508` | 身份、权限、密钥或授权证据 |
| `GetVarmorConfigYAML` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetVarmorConfigYaml` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetVarmorPolicy` | `seccenter20240508` | 身份、权限、密钥或授权证据 |
| `GetVarmorTLSInfo` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetVarmorTlsInfo` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetVirusAlarmSummaryInfo` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `GetVirusDatabaseUpdateTime` | `seccenter20240508` | 存储、备份或数据库控制面证据 |
| `GetVirusTaskInfo` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetVirusTaskStatistics` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetVulnCheckStatus` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetVulnCheckStatusForAI` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetVulnCheckStatusForAi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetVulnDetail` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetVulnInfo` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetVulnInfoForAI` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetVulnInfoForAi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetVulnScanConfig` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetVulnStatistics` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetVulnStatisticsForAI` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `GetVulnStatisticsForAi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetWhiteListField` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListAIApplicationBasicInfo` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListAgentProxies` | `seccenter20240508` | 模型、端点、Agent 或工作空间状态证据 |
| `ListAgentProxyServers` | `seccenter20240508` | 资源状态、实例/节点/集群运行态证据 |
| `ListAgentkitSessionIDs` | `seccenter20240508` | 模型、端点、Agent 或工作空间状态证据 |
| `ListAgentkitSessionIds` | `Python SDK-only/未匹配 CLI` | 模型、端点、Agent 或工作空间状态证据 |
| `ListAiApplicationBasicInfo` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListAlarmArchiveRecords` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `ListAlarmNameList` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `ListAlarmTags` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `ListAllCntrStaticDict` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListAssetCenterDevs` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListAssetCenterHosts` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListAssetClusters` | `seccenter20240508` | 资源状态、实例/节点/集群运行态证据 |
| `ListAssetGroups` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListAssetNamespaces` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListAssetPodsLinkedWorkload` | `seccenter20240508` | 资源状态、实例/节点/集群运行态证据 |
| `ListAssetPodsLinkedWorkloadWithNoPage` | `seccenter20240508` | 资源状态、实例/节点/集群运行态证据 |
| `ListAssetTags` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListAssetWorkloads` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListAutoDefenseHosts` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListAutoDefenseRules` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListBanIPList` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListBanIpList` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListBaselineBasicInfo` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListBaselineCheckConfig` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListBaselineCheckDetail` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListBaselineCheckItemHosts` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListBaselineCheckItems` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListBaselineCheckRes` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListBaselineForGroupPolicy` | `seccenter20240508` | 身份、权限、密钥或授权证据 |
| `ListBaselineGroups` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListBaselineHostItemHosts` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListBaselines` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListBatchEndpointHandleMethods` | `seccenter20240508` | 模型、端点、Agent 或工作空间状态证据 |
| `ListCheckConfigRelatedBaseline` | `seccenter20240508` | 存储、备份或数据库控制面证据 |
| `ListCleanHistory` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListCloudEnvs` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListCloudPlatforms` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListClusterVarmorVersionHistory` | `seccenter20240508` | 资源状态、实例/节点/集群运行态证据 |
| `ListClustersAndVarmorApps` | `seccenter20240508` | 资源状态、实例/节点/集群运行态证据 |
| `ListDevAssetIDs` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListDevAssetIds` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListDevBasicInfos` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListDevPlatform` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListDevRegion` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListEndpointHandleMethods` | `seccenter20240508` | 模型、端点、Agent 或工作空间状态证据 |
| `ListFileMonitorAlarms` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `ListFingerprintCollectConfig` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListGroupRelatedAgent` | `seccenter20240508` | 模型、端点、Agent 或工作空间状态证据 |
| `ListHidsAlarms` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `ListHostPlatform` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListHostRegion` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListHostVpc` | `seccenter20240508` | 网络路径、入口、路由或安全策略证据 |
| `ListHostsAgentIDs` | `seccenter20240508` | 模型、端点、Agent 或工作空间状态证据 |
| `ListHostsAgentIds` | `Python SDK-only/未匹配 CLI` | 模型、端点、Agent 或工作空间状态证据 |
| `ListHostsBasicInfos` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListInstallCommands` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListIsolationFiles` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListLayeredGroupRelatedHost` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListLayeredGroupsDetail` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListLoginConfigs` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListMLPAssetTasks` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListMlpAlarmTags` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `ListMlpAlarms` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `ListMlpAssetTasks` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListMonitorPolicies` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListMultiLevelAssetHosts` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListMultiLevelInstitution` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListOrderedHostsBasicInfos` | `seccenter20240508` | 计费、订单、成本、配额或资源包证据 |
| `ListRaspAlarms` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `ListRaspConfigAgentInfos` | `seccenter20240508` | 模型、端点、Agent 或工作空间状态证据 |
| `ListRaspConfigs` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListRaspProcesses` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListRegistries` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListRegistryImages` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListRegistryNamespaceIDs` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListRegistryNamespaceIds` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListRegistryNamespaces` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListRepoImageCompl` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListRepoImageLayer` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListRepoImageLayerSenfile` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListRepoImageLayerVirus` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListRepoImageLayerVuln` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListRepoImagePackage` | `seccenter20240508` | 计费、订单、成本、配额或资源包证据 |
| `ListRepoImageSenfile` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListRepoImageVirus` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListRepoImageVuln` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListRiskComplAffectRepoImage` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `ListRiskVulnAffectRepoImage` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `ListScanSubTasks` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListScanTaskHosts` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListScanTasks` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListTagRelatedAgent` | `seccenter20240508` | 模型、端点、Agent 或工作空间状态证据 |
| `ListTagsDetail` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListVarmorPolicies` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListVirusAlarms` | `seccenter20240508` | 密钥、安全策略、风险或告警证据 |
| `ListVulByPod` | `seccenter20240508` | 资源状态、实例/节点/集群运行态证据 |
| `ListVulDetail` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListVulHostByPod` | `seccenter20240508` | 资源状态、实例/节点/集群运行态证据 |
| `ListVulnAffectAISession` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListVulnAffectAiSession` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListVulnForAI` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListVulnForAi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListVulnHosts` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListVulns` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListWeakPasswordCheckDetail` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |
| `ListWhiteLists` | `seccenter20240508` | 资源存在性、状态、配置或诊断证据 |

### 云工作负载保护平台
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：8
- 排除自动执行的写/变更 Action：6
- 其它需按场景人工判断 Action：DelSyslogConfig, EditIMConfig, EditIMConfigStatus, EditImConfig, EditImConfigStatus, GenLogStashConfig, UpsertAlarmFeedbackWithRag

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `CheckIMConfig` | `secagent` | 资源存在性、状态、配置或诊断证据 |
| `CheckIMConfigParams` | `secagent` | 资源存在性、状态、配置或诊断证据 |
| `CheckImConfig` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `CheckImConfigParams` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAlarmStatOverviewV2` | `secagent` | 密钥、安全策略、风险或告警证据 |
| `GetAlarmDetail` | `secagent` | 密钥、安全策略、风险或告警证据 |
| `GetResourceAuthConfig` | `secagent` | 身份、权限、密钥或授权证据 |
| `ListSyslogConfig` | `secagent` | 资源存在性、状态、配置或诊断证据 |

### 云防火墙
- 官方文档识别 Action 数：62
- 纳入只读/诊断 Action：20
- 排除自动执行的写/变更 Action：40
- 其它需按场景人工判断 Action：AssetList, UseAclBackup

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAclBackup` | `fwcenter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeAddressBook` | `fwcenter` | 资源存在性、状态、配置或诊断证据 |
| `DescribeControlPolicy` | `fwcenter` | 身份、权限、密钥或授权证据 |
| `DescribeControlPolicyByRuleId` | `fwcenter` | 身份、权限、密钥或授权证据 |
| `DescribeControlPolicyPriorUsed` | `fwcenter` | 身份、权限、密钥或授权证据 |
| `DescribeDnsControlPolicy` | `fwcenter` | 身份、权限、密钥或授权证据 |
| `DescribeNatFirewallControlPolicy` | `fwcenter` | 身份、权限、密钥或授权证据 |
| `DescribeNatFirewallControlPolicyPriorityUsed` | `fwcenter` | 身份、权限、密钥或授权证据 |
| `DescribeNatFirewallList` | `fwcenter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTransitRouterResourcesList` | `fwcenter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeVpcFirewallAclRuleList` | `fwcenter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeVpcFirewallAclRulePriorUsed` | `fwcenter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeVpcFirewallList` | `fwcenter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeVpcFirewallRoutePolicyList` | `fwcenter` | 身份、权限、密钥或授权证据 |
| `DescribeVpcs` | `fwcenter` | 网络路径、入口、路由或安全策略证据 |
| `GetPolicyAnalyzeDetail` | `fwcenter` | 身份、权限、密钥或授权证据 |
| `GetPolicyAnalyzeOverview` | `fwcenter` | 身份、权限、密钥或授权证据 |
| `GetPolicyAnalyzeResult` | `fwcenter` | 身份、权限、密钥或授权证据 |
| `GetPolicyCheckResult` | `fwcenter` | 身份、权限、密钥或授权证据 |
| `QueryUserAlarmConfig` | `fwcenter` | 身份、权限、密钥或授权证据 |

### 可信隐私计算平台
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：7
- 排除自动执行的写/变更 Action：1
- 其它需按场景人工判断 Action：BuyPoolPackage, BuyResourcePackage, ClearDeviceLongMemory, PushMsgToDevice, TopActionDispatch

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `GetAgentList` | `tis` | 模型、端点、Agent 或工作空间状态证据 |
| `GetDeviceBindTcOrderID` | `tis` | 计费、订单、成本、配额或资源包证据 |
| `GetDeviceBindTcOrderId` | `Python SDK-only/未匹配 CLI` | 计费、订单、成本、配额或资源包证据 |
| `GetPoolDetailList` | `tis` | 资源存在性、状态、配置或诊断证据 |
| `GetPoolQuotaInfo` | `tis` | 计费、订单、成本、配额或资源包证据 |
| `GetQuotaInfo` | `tis` | 计费、订单、成本、配额或资源包证据 |
| `GetSpeakerList` | `tis` | 资源存在性、状态、配置或诊断证据 |

### 多云安全平台
- 官方文档识别 Action 数：21
- 纳入只读/诊断 Action：10
- 排除自动执行的写/变更 Action：0
- 其它需按场景人工判断 Action：BanAlertIPCallback, BanAlertIpCallback, PostApiV1AlarmDescribeOverview, PostApiV1AssetDescribeDetail, PostApiV1OverviewDescribeAssetInfo, RiskStatusUpdateBySoar

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `GetAlarmSyncTask` | `mcs` | 密钥、安全策略、风险或告警证据 |
| `GetApiV1AlarmDetail` | `mcs` | 密钥、安全策略、风险或告警证据 |
| `GetApiV1OverviewAlarmStats` | `mcs` | 密钥、安全策略、风险或告警证据 |
| `GetApiV1OverviewSecurityScores` | `mcs` | 网络路径、入口、路由或安全策略证据 |
| `GetAssetSyncTask` | `mcs` | 资源存在性、状态、配置或诊断证据 |
| `GetOverviewCard` | `mcs` | 资源存在性、状态、配置或诊断证据 |
| `GetOverviewServiceModule` | `mcs` | 资源存在性、状态、配置或诊断证据 |
| `GetRisk` | `mcs` | 密钥、安全策略、风险或告警证据 |
| `GetRiskDetectionTask` | `mcs` | 密钥、安全策略、风险或告警证据 |
| `GetRiskStat` | `mcs` | 密钥、安全策略、风险或告警证据 |

### 密钥管理系统
- 官方文档识别 Action 数：53
- 纳入只读/诊断 Action：15
- 排除自动执行的写/变更 Action：25
- 其它需按场景人工判断 Action：ArchiveKey, AsymmetricDecrypt, AsymmetricEncrypt, AsymmetricSign, AsymmetricVerify, BackupSecret, ConnectCustomKeyStore, Decrypt, DisconnectCustomKeyStore, Encrypt, GenerateDataKey, GenerateMac, ReEncrypt, ReplicateKey, RestoreSecret, RotateSecret, ScheduleKeyDeletion, ScheduleSecretDeletion

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `BatchGetSecretValue` | `kms` | 密钥、安全策略、风险或告警证据 |
| `DescribeCustomKeyStores` | `kms` | 密钥、安全策略、风险或告警证据 |
| `DescribeKey` | `kms` | 密钥、安全策略、风险或告警证据 |
| `DescribeKeyrings` | `kms` | 密钥、安全策略、风险或告警证据 |
| `DescribeKeys` | `kms` | 密钥、安全策略、风险或告警证据 |
| `DescribeRegions` | `kms` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSecret` | `kms` | 密钥、安全策略、风险或告警证据 |
| `DescribeSecretVersions` | `kms` | 密钥、安全策略、风险或告警证据 |
| `DescribeSecrets` | `kms` | 密钥、安全策略、风险或告警证据 |
| `GetParametersForImport` | `kms` | 资源存在性、状态、配置或诊断证据 |
| `GetPublicKey` | `kms` | 密钥、安全策略、风险或告警证据 |
| `GetSecretValue` | `kms` | 密钥、安全策略、风险或告警证据 |
| `ListTagsForResources` | `kms` | 资源存在性、状态、配置或诊断证据 |
| `QueryKeyring` | `kms` | 密钥、安全策略、风险或告警证据 |
| `VerifyMac` | `kms` | 资源存在性、状态、配置或诊断证据 |

### 攻击面管理
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 高级网络威胁检测系统
- 官方文档识别 Action 数：2
- 纳入只读/诊断 Action：1
- 排除自动执行的写/变更 Action：1

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `GetFileDetection` | `nta` | 资源存在性、状态、配置或诊断证据 |

## 使用建议
- 优先使用章节 reference 中已经编排好的命令包；当用户问题落在未细化章节时，再从本矩阵选择最小只读 Action 补充证据。
- 如果某个只读 Action 需要分页、跨产品联动或深层字段归一，再考虑新增 `scripts/` 只读脚本，并同步更新脚本说明。
- 如果只读证据指向写操作修复，必须先输出影响面、资源 ID、回滚/恢复建议，并等待用户确认。
