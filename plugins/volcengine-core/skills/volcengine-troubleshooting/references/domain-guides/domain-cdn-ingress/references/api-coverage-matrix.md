# API 覆盖审查矩阵
本文件由 2026-05-22 审查生成，用于证明本 skill 已对 `cli-meta/` 中对应分类的 OpenAPI / CLI / Python SDK 能力做过覆盖盘点。它不是执行顺序清单；Agent 仍应先按主 `SKILL.md` 和章节 reference 选择最小必要证据。
## 审查口径
- 纳入排障优先级：`Describe/List/Get/Query/Check/Search/BatchGet/Verify/Validate/Test/Diagnose/Preview/Estimate` 等只读或诊断型 Action。
- 默认排除自动执行：`Create/Modify/Delete/Update/Attach/Detach/Start/Stop/Run/Invoke/Pay/Renew/Set` 等会改变资源、资金、权限或任务状态的 Action；只能作为解释错误码或 Human-in-the-Loop 建议背景。
- 命令形态：执行时统一写作 `ve <service> <Action> [--Param value...]`；参数不确定时先查 `ve <service> <Action> --help` 或对应 `cli-meta`。
- 凭证边界：只从临时环境读取 `VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、`VOLCENGINE_REGION`，不得写入配置、文档或日志。
## 总览
- 覆盖产品数：11
- 官方文档识别 OpenAPI Action 数合计：304
- 纳入排障候选的只读/诊断 Action 数：222
- 默认不自动执行的写/变更 Action 数：271
- 需人工判断语义的其它 Action 数：42

## 产品级覆盖
### TrafficRoute DNS 套件
- 官方文档识别 Action 数：121
- 纳入只读/诊断 Action：11
- 排除自动执行的写/变更 Action：19

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `GetGtm` | `gtm` | 资源存在性、状态、配置或诊断证据 |
| `GetPolicy` | `gtm` | 身份、权限、密钥或授权证据 |
| `GetPool` | `gtm` | 资源存在性、状态、配置或诊断证据 |
| `GetProbe` | `gtm` | 资源存在性、状态、配置或诊断证据 |
| `GetRule` | `gtm` | 资源存在性、状态、配置或诊断证据 |
| `ListDomainOverview` | `httpdns` | 域名、证书、CDN、直播或入口链路证据 |
| `ListDomainRecords` | `httpdns` | 域名、证书、CDN、直播或入口链路证据 |
| `ListGtms` | `gtm` | 资源存在性、状态、配置或诊断证据 |
| `ListLines` | `httpdns` | 资源存在性、状态、配置或诊断证据 |
| `ListPools` | `gtm` | 资源存在性、状态、配置或诊断证据 |
| `ListRules` | `gtm` | 资源存在性、状态、配置或诊断证据 |

### 全球加速
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：25
- 排除自动执行的写/变更 Action：48
- 其它需按场景人工判断 Action：AcceleratorReplacePublicBandwidthPackage, BasicAcceleratorReplacePublicBandwidthPackage, PublicBandwidthPackageBindAccelerator, PublicBandwidthPackageBindBasicAccelerator, PublicBandwidthPackageUnbindAccelerator, PublicBandwidthPackageUnbindBasicAccelerator

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAccelerator` | `ga` | 资源存在性、状态、配置或诊断证据 |
| `DescribeBasicAccelerator` | `ga` | 资源存在性、状态、配置或诊断证据 |
| `DescribeBasicEndpointGroup` | `ga` | 模型、端点、Agent 或工作空间状态证据 |
| `DescribeBasicIPSet` | `ga` | 资源存在性、状态、配置或诊断证据 |
| `DescribeBasicIpSet` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeEndpointGroup` | `ga` | 模型、端点、Agent 或工作空间状态证据 |
| `DescribeIPSet` | `ga` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpSet` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |
| `DescribeListener` | `ga` | 网络路径、入口、路由或安全策略证据 |
| `DescribePublicBandwidthPackage` | `ga` | 计费、订单、成本、配额或资源包证据 |
| `DescribeStatistics` | `ga` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTopStatistics` | `ga` | 资源存在性、状态、配置或诊断证据 |
| `ListAccelerators` | `ga` | 资源存在性、状态、配置或诊断证据 |
| `ListBasicAccelerateIPs` | `ga` | 网络路径、入口、路由或安全策略证据 |
| `ListBasicAccelerateIps` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |
| `ListBasicAccelerators` | `ga` | 资源存在性、状态、配置或诊断证据 |
| `ListBasicEndpointGroups` | `ga` | 模型、端点、Agent 或工作空间状态证据 |
| `ListBasicEndpoints` | `ga` | 模型、端点、Agent 或工作空间状态证据 |
| `ListBasicIPSets` | `ga` | 资源存在性、状态、配置或诊断证据 |
| `ListBasicIpSets` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListEndpointGroups` | `ga` | 模型、端点、Agent 或工作空间状态证据 |
| `ListIPSets` | `ga` | 资源存在性、状态、配置或诊断证据 |
| `ListIpSets` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListListeners` | `ga` | 网络路径、入口、路由或安全策略证据 |
| `ListPublicBandwidthPackages` | `ga` | 计费、订单、成本、配额或资源包证据 |

### 全站加速
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：45
- 排除自动执行的写/变更 Action：15
- 其它需按场景人工判断 Action：BatchBlockIP, BatchBlockIp, RetryPurgePrefetchTask

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `CheckPurgePrefetchTask` | `dcdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeBlockIP` | `dcdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeBlockIp` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDcdnEdgeIp` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |
| `DescribeDcdnOriginIp` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeDcdnRegionAndIsp` | `dcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeDomainConfig` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeDomainDetail` | `dcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeDomainIspData` | `dcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeDomainLogs` | `dcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeDomainOverview` | `dcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeDomainPVData` | `dcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeDomainProbeSetting` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeDomainProbeSettings` | `dcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeDomainPvData` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeDomainRegionData` | `dcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeDomainUVData` | `dcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeDomainUvData` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeGaOriginPolicy` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `DescribeL2Ips` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeOriginRealTimeData` | `dcdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeOriginRealtimeData` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeOriginStatistics` | `dcdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeOriginStatisticsDetail` | `dcdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRealTimeData` | `dcdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRealtimeData` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeStatistics` | `dcdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeStatisticsDetail` | `dcdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTopDomains` | `dcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeTopIP` | `dcdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTopIps` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTopReferer` | `dcdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTopReferers` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTopURL` | `dcdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTopUrls` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeUserDomains` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `DescribeVerifyContent` | `dcdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeWsStatistics` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetApiInfo` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetPurgePrefetchTaskQuota` | `dcdn` | 计费、订单、成本、配额或资源包证据 |
| `GetServiceInfo` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListCert` | `dcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `ListCertBind` | `dcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `ListDomainConfig` | `dcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `VerifyDomainOwnership` | `dcdn` | 域名、证书、CDN、直播或入口链路证据 |

### 内容分发网络
- 官方文档识别 Action 数：101
- 纳入只读/诊断 Action：33
- 排除自动执行的写/变更 Action：19
- 其它需按场景人工判断 Action：BatchDeployCert, BatchUpdateCdnConfig

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeBillingDetail` | `cdn` | 计费、订单、成本、配额或资源包证据 |
| `DescribeCdnAccessLog` | `cdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeCdnConfig` | `cdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeCdnEdgeIp` | `cdn` | 网络路径、入口、路由或安全策略证据 |
| `DescribeCdnIP` | `cdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeCdnIp` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeCdnRegionAndIsp` | `cdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeCdnService` | `cdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeCdnUpperIp` | `cdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeCertConfig` | `cdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeContentBlockTasks` | `cdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeContentQuota` | `cdn` | 计费、订单、成本、配额或资源包证据 |
| `DescribeContentTasks` | `cdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDistrictData` | `cdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDistrictRanking` | `cdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDistrictSummary` | `cdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeEdgeData` | `cdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeEdgeRanking` | `cdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeEdgeStatusCodeRanking` | `cdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeEdgeSummary` | `cdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeOriginData` | `cdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeOriginRanking` | `cdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeOriginStatusCodeRanking` | `cdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeOriginSummary` | `cdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSharedConfig` | `cdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeStatisticalRanking` | `cdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeUserData` | `cdn` | 身份、权限、密钥或授权证据 |
| `ListCdnCertInfo` | `cdn` | 域名、证书、CDN、直播或入口链路证据 |
| `ListCdnDomains` | `cdn` | 域名、证书、CDN、直播或入口链路证据 |
| `ListCertInfo` | `cdn` | 域名、证书、CDN、直播或入口链路证据 |
| `ListResourceTags` | `cdn` | 资源存在性、状态、配置或诊断证据 |
| `ListSharedConfig` | `cdn` | 资源存在性、状态、配置或诊断证据 |
| `ListUsageReports` | `cdn` | 资源存在性、状态、配置或诊断证据 |

### 域名服务
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：14
- 排除自动执行的写/变更 Action：13
- 其它需按场景人工判断 Action：BatchDeleteCustomLine, RestoreUserZoneBackup, RetrieveZone

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `CheckRetrieveZone` | `dns` | 资源存在性、状态、配置或诊断证据 |
| `CheckZone` | `dns` | 资源存在性、状态、配置或诊断证据 |
| `ListCustomLines` | `dns` | 资源存在性、状态、配置或诊断证据 |
| `ListDomainStatistics` | `dns` | 域名、证书、CDN、直播或入口链路证据 |
| `ListLines` | `dns` | 资源存在性、状态、配置或诊断证据 |
| `ListRecordDigestByLine` | `dns` | 资源存在性、状态、配置或诊断证据 |
| `ListRecordSets` | `dns` | 资源存在性、状态、配置或诊断证据 |
| `ListRecords` | `dns` | 资源存在性、状态、配置或诊断证据 |
| `ListUserZoneBackups` | `dns` | 身份、权限、密钥或授权证据 |
| `ListZoneStatistics` | `dns` | 资源存在性、状态、配置或诊断证据 |
| `ListZones` | `dns` | 资源存在性、状态、配置或诊断证据 |
| `QueryBackupSchedule` | `dns` | 存储、备份或数据库控制面证据 |
| `QueryRecord` | `dns` | 资源存在性、状态、配置或诊断证据 |
| `QueryZone` | `dns` | 资源存在性、状态、配置或诊断证据 |

### 备案
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 多云CDN
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：20
- 排除自动执行的写/变更 Action：8

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAlertStrategy` | `mcdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeCdnAccessLog` | `mcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeCdnDataOffline` | `mcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeCdnOriginDataOffline` | `mcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeCdnRegionAndIsp` | `mcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeCdnTopIp` | `mcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeCdnTopUrl` | `mcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeContentQuota` | `mcdn` | 计费、订单、成本、配额或资源包证据 |
| `DescribeContentTaskByTaskId` | `mcdn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDnsSchedule` | `mcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeDnsScheduleActiveWeights` | `mcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeDnsScheduleStaticWeights` | `mcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `ListAlertMetaMetrics` | `mcdn` | 资源存在性、状态、配置或诊断证据 |
| `ListAlertStrategies` | `mcdn` | 资源存在性、状态、配置或诊断证据 |
| `ListCdnDomains` | `mcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `ListCloudAccounts` | `mcdn` | 资源存在性、状态、配置或诊断证据 |
| `ListContentTasks` | `mcdn` | 资源存在性、状态、配置或诊断证据 |
| `ListDnsSchedules` | `mcdn` | 域名、证书、CDN、直播或入口链路证据 |
| `ListVendorContentTask` | `mcdn` | 资源存在性、状态、配置或诊断证据 |
| `ListViews` | `mcdn` | 资源存在性、状态、配置或诊断证据 |

### 证书中心
- 官方文档识别 Action 数：53
- 纳入只读/诊断 Action：1
- 排除自动执行的写/变更 Action：4
- 其它需按场景人工判断 Action：CertificateAddOrganization, CertificateDeleteInstance, CertificateDeleteOrganization, CertificateGetInstance, CertificateGetInstanceList, CertificateGetOrganization, CertificateGetOrganizationList, CertificateUpdateInstance, CertificateUpdateOrganization, QuickApplyCertificate

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `ListTagsForResources` | `certificateservice` | 资源存在性、状态、配置或诊断证据 |

### 跨域带宽包
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 边缘智能
- 官方文档识别 Action 数：28
- 纳入只读/诊断 Action：25
- 排除自动执行的写/变更 Action：29
- 其它需按场景人工判断 Action：ApplyVideoAnalysisTaskToken, CommitVideoAnalysisTask, DeviceContinuousMove, EdgeCall

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `GetLastDevicePropertyValue` | `veiapi` | 资源存在性、状态、配置或诊断证据 |
| `GetLogRule` | `veiapi` | 资源存在性、状态、配置或诊断证据 |
| `GetMediapipeEvent` | `veiapi` | 资源存在性、状态、配置或诊断证据 |
| `GetNodeGroup` | `veiapi` | 资源状态、实例/节点/集群运行态证据 |
| `GetVideoAnalysisStatistics` | `veiapi` | 资源存在性、状态、配置或诊断证据 |
| `GetVideoAnalysisTask` | `veiapi` | 资源存在性、状态、配置或诊断证据 |
| `GetVideoAnalysisTaskData` | `veiapi` | 资源存在性、状态、配置或诊断证据 |
| `GetVideoAnalysisTaskMediaMeta` | `veiapi` | 资源存在性、状态、配置或诊断证据 |
| `GetVideoFirstFrame` | `veiapi` | 资源存在性、状态、配置或诊断证据 |
| `ListDeployment` | `veiapi` | 资源存在性、状态、配置或诊断证据 |
| `ListDevice` | `veiapi` | 资源存在性、状态、配置或诊断证据 |
| `ListHCINew` | `veiapi` | 资源存在性、状态、配置或诊断证据 |
| `ListHciNew` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListIotModels` | `veiapi` | 模型、端点、Agent 或工作空间状态证据 |
| `ListLLModelsV2` | `veiapi` | 模型、端点、Agent 或工作空间状态证据 |
| `ListLlModelsV2` | `Python SDK-only/未匹配 CLI` | 模型、端点、Agent 或工作空间状态证据 |
| `ListMediapipeEvent` | `veiapi` | 资源存在性、状态、配置或诊断证据 |
| `ListMediapipeInstance` | `veiapi` | 资源状态、实例/节点/集群运行态证据 |
| `ListModel` | `veiapi` | 模型、端点、Agent 或工作空间状态证据 |
| `ListModelService` | `veiapi` | 模型、端点、Agent 或工作空间状态证据 |
| `ListNodeGroup` | `veiapi` | 资源状态、实例/节点/集群运行态证据 |
| `ListProject` | `veiapi` | 资源存在性、状态、配置或诊断证据 |
| `ListVideoAnalysisTask` | `veiapi` | 资源存在性、状态、配置或诊断证据 |
| `ListVideoAnalysisTaskData` | `veiapi` | 资源存在性、状态、配置或诊断证据 |
| `ListVideoAnalysisTaskObjectClasses` | `veiapi` | 存储、备份或数据库控制面证据 |

### 边缘计算节点
- 官方文档识别 Action 数：1
- 纳入只读/诊断 Action：48
- 排除自动执行的写/变更 Action：116
- 其它需按场景人工判断 Action：AckSecondaryInternalIpStatus, BatchBindEipToInternalIpsRandomly, BatchCreateEIPInstances, BatchDeleteInternalIps, BatchResetSystem, BatchUnbindEipFromInternalIP, BuildImageByVM, GenerateSSHKey, JoinSecurityGroup, LeaveSecurityGroup, OfflineInstances, ScaleEbsInstanceCapacity, UnassociateRouteTableWithSubnets, UpgradeStandardSpec

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeSecurityGroup` | `veenedge` | 网络路径、入口、路由或安全策略证据 |
| `DescribeSecurityGroupAssociationInstances` | `veenedge` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeSecurityGroupRules` | `veenedge` | 网络路径、入口、路由或安全策略证据 |
| `DescribeSecurityGroups` | `veenedge` | 网络路径、入口、路由或安全策略证据 |
| `GetCloudServer` | `veenedge` | 资源状态、实例/节点/集群运行态证据 |
| `GetEIPInstance` | `veenedge` | 资源状态、实例/节点/集群运行态证据 |
| `GetENIInstance` | `veenedge` | 资源状态、实例/节点/集群运行态证据 |
| `GetEbsInstance` | `veenedge` | 资源状态、实例/节点/集群运行态证据 |
| `GetImage` | `veenedge` | 资源存在性、状态、配置或诊断证据 |
| `GetInstance` | `veenedge` | 资源状态、实例/节点/集群运行态证据 |
| `GetInstanceCloudDiskInfo` | `veenedge` | 资源状态、实例/节点/集群运行态证据 |
| `GetInstancesIPv6UpgradeStatus` | `veenedge` | 资源状态、实例/节点/集群运行态证据 |
| `GetLNIInstance` | `veenedge` | 资源状态、实例/节点/集群运行态证据 |
| `GetRouteTable` | `veenedge` | 网络路径、入口、路由或安全策略证据 |
| `GetSecurityGroupQuota` | `veenedge` | 计费、订单、成本、配额或资源包证据 |
| `GetVNCUrl` | `veenedge` | 资源存在性、状态、配置或诊断证据 |
| `ListAvailableClassicNetworkClusters` | `veenedge` | 资源状态、实例/节点/集群运行态证据 |
| `ListAvailableResourceInfo` | `veenedge` | 资源存在性、状态、配置或诊断证据 |
| `ListClassicNetworkSubnets` | `veenedge` | 网络路径、入口、路由或安全策略证据 |
| `ListClassicNetworks` | `veenedge` | 资源存在性、状态、配置或诊断证据 |
| `ListCloudServers` | `veenedge` | 资源状态、实例/节点/集群运行态证据 |
| `ListEIPDisplayClusters` | `veenedge` | 资源状态、实例/节点/集群运行态证据 |
| `ListEIPInstances` | `veenedge` | 资源状态、实例/节点/集群运行态证据 |
| `ListEIPLbBindableInfo` | `veenedge` | 网络路径、入口、路由或安全策略证据 |
| `ListEIPVeenBindableInfo` | `veenedge` | 网络路径、入口、路由或安全策略证据 |
| `ListENIExternalIps` | `veenedge` | 资源存在性、状态、配置或诊断证据 |
| `ListENIInstances` | `veenedge` | 资源状态、实例/节点/集群运行态证据 |
| `ListENIInternalIps` | `veenedge` | 资源存在性、状态、配置或诊断证据 |
| `ListENIIpv6Ips` | `veenedge` | 资源存在性、状态、配置或诊断证据 |
| `ListEbsInstances` | `veenedge` | 资源状态、实例/节点/集群运行态证据 |
| `ListEipsOfNatGateway` | `veenedge` | 网络路径、入口、路由或安全策略证据 |
| `ListImages` | `veenedge` | 资源存在性、状态、配置或诊断证据 |
| `ListInstanceInternalIps` | `veenedge` | 资源状态、实例/节点/集群运行态证据 |
| `ListInstanceTypes` | `veenedge` | 资源状态、实例/节点/集群运行态证据 |
| `ListInstances` | `veenedge` | 资源状态、实例/节点/集群运行态证据 |
| `ListIpCidrBlocks` | `veenedge` | 资源存在性、状态、配置或诊断证据 |
| `ListIpPools` | `veenedge` | 资源存在性、状态、配置或诊断证据 |
| `ListLNIInstances` | `veenedge` | 资源状态、实例/节点/集群运行态证据 |
| `ListLNIIps` | `veenedge` | 资源存在性、状态、配置或诊断证据 |
| `ListResourceEvents` | `veenedge` | 资源存在性、状态、配置或诊断证据 |
| `ListRouteEntries` | `veenedge` | 网络路径、入口、路由或安全策略证据 |
| `ListRouteTableAssociatedSubnets` | `veenedge` | 网络路径、入口、路由或安全策略证据 |
| `ListRouteTables` | `veenedge` | 网络路径、入口、路由或安全策略证据 |
| `ListSSHKey` | `veenedge` | 密钥、安全策略、风险或告警证据 |
| `ListSecurityGroupBindInstances` | `veenedge` | 资源状态、实例/节点/集群运行态证据 |
| `ListSecurityGroupTree` | `veenedge` | 网络路径、入口、路由或安全策略证据 |
| `ListSubnetInstances` | `veenedge` | 资源状态、实例/节点/集群运行态证据 |
| `ListVPCInstances` | `veenedge` | 资源状态、实例/节点/集群运行态证据 |

## 使用建议
- 优先使用章节 reference 中已经编排好的命令包；当用户问题落在未细化章节时，再从本矩阵选择最小只读 Action 补充证据。
- 如果某个只读 Action 需要分页、跨产品联动或深层字段归一，再考虑新增 `scripts/` 只读脚本，并同步更新脚本说明。
- 如果只读证据指向写操作修复，必须先输出影响面、资源 ID、回滚/恢复建议，并等待用户确认。
