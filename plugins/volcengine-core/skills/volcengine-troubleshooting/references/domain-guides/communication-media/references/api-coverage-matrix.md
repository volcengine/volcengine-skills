# API 覆盖审查矩阵
本文件由 2026-05-22 审查生成，用于证明本 skill 已对 `cli-meta/` 中对应分类的 OpenAPI / CLI / Python SDK 能力做过覆盖盘点。它不是执行顺序清单；Agent 仍应先按主 `SKILL.md` 和章节 reference 选择最小必要证据。
## 审查口径
- 纳入排障优先级：`Describe/List/Get/Query/Check/Search/BatchGet/Verify/Validate/Test/Diagnose/Preview/Estimate` 等只读或诊断型 Action。
- 默认排除自动执行：`Create/Modify/Delete/Update/Attach/Detach/Start/Stop/Run/Invoke/Pay/Renew/Set` 等会改变资源、资金、权限或任务状态的 Action；只能作为解释错误码或 Human-in-the-Loop 建议背景。
- 命令形态：执行时统一写作 `ve <service> <Action> [--Param value...]`；参数不确定时先查 `ve <service> <Action> --help` 或对应 `cli-meta`。
- 凭证边界：只从临时环境读取 `VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、`VOLCENGINE_REGION`，不得写入配置、文档或日志。
## 总览
- 覆盖产品数：10
- 官方文档识别 OpenAPI Action 数合计：849
- 纳入排障候选的只读/诊断 Action 数：414
- 默认不自动执行的写/变更 Action 数：366
- 需人工判断语义的其它 Action 数：111

## 产品级覆盖
### WebRTC 传输网络
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：3
- 排除自动执行的写/变更 Action：0

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `ListApps` | `wtn` | 资源存在性、状态、配置或诊断证据 |
| `ListAppsV3` | `wtn` | 资源存在性、状态、配置或诊断证据 |
| `ListRealTimePublicStreamInfo` | `wtn` | 域名、证书、CDN、直播或入口链路证据 |

### veImageX
- 官方文档识别 Action 数：1
- 纳入只读/诊断 Action：112
- 排除自动执行的写/变更 Action：37
- 其它需按场景人工判断 Action：ApplyUpload, ApplyVideoAnalysisTaskToken, AsyncUpload, ChunkUpload, CommitUpload, CommitVideoAnalysisTask, DeviceContinuousMove, DoUpload, EdgeCall, GenerateMergeBody, ImagexGet, ImagexPost, ImagexRequest, InitUploadPart

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeImagexBaseOpUsage` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexBucketUsage` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `DescribeImagexCdnDurationAll` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeImagexCdnDurationDetailByTime` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeImagexCdnErrorCodeAll` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeImagexCdnErrorCodeByTime` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeImagexCdnProtocolRateByTime` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeImagexCdnReuseRateAll` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `DescribeImagexCdnReuseRateByTime` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `DescribeImagexCdnSuccessRateAll` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeImagexCdnSuccessRateByTime` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeImagexCdntopRequestData` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeImagexClientCountByTime` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexClientDecodeDurationByTime` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexClientDecodeSuccessRateByTime` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexClientDemotionRateByTime` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexClientErrorCodeAll` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexClientErrorCodeByTime` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexClientFailureRate` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexClientFileSize` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexClientLoadDuration` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexClientLoadDurationAll` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexClientQualityRateByTime` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexClientQueueDurationByTime` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexClientScoreByTime` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexClientSdkVerByTime` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexClientTopDemotionUrl` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexClientTopFileSize` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexClientTopQualityUrl` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexCompressUsage` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexDomainBandwidthData` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |
| `DescribeImagexDomainTrafficData` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeImagexEdgeRequest` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexEdgeRequestBandwidth` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |
| `DescribeImagexEdgeRequestRegions` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexEdgeRequestTraffic` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexHitRateRequestData` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexHitRateTrafficData` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexMirrorRequestBandwidth` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |
| `DescribeImagexMirrorRequestHttpCodeByTime` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexMirrorRequestHttpCodeOverview` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexMirrorRequestTraffic` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexRequestCntUsage` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexSensibleCacheHitRateByTime` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexSensibleCountByTime` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexSensibleTopRamUrl` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexSensibleTopResolutionUrl` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexSensibleTopSizeUrl` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexSensibleTopUnknownUrl` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexServiceQuality` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexSummary` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexUploadCountByTime` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexUploadDuration` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexUploadErrorCodeAll` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexUploadErrorCodeByTime` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexUploadFileSize` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexUploadSegmentSpeedByTime` | `Python SDK-only/未匹配 CLI` | 存储、备份或数据库控制面证据 |
| `DescribeImagexUploadSpeed` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeImagexUploadSuccessRateByTime` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `Describeimagevolccdnaccesslog` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `FetchImageUrl` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetApiInfo` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetImageBgFillResult` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetImageComicResult` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetImageContentBlockList` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetImageContentTaskDetail` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetImageDuplicateDetection` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetImageDuplicateTaskStatus` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetImageEnhanceResult` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetImageEnhanceResultWithData` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetImageEraseModels` | `Python SDK-only/未匹配 CLI` | 模型、端点、Agent 或工作空间状态证据 |
| `GetImageEraseResult` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetImageInfo` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetImageOcrV2` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetImageQuality` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetImageSegment` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetImageStyleResult` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetImageSuperResolutionResult` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetImagexQueryApps` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetImagexQueryDims` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetImagexQueryRegions` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetImagexQueryVals` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetLastDevicePropertyValue` | `veiapi` | 资源存在性、状态、配置或诊断证据 |
| `GetLicensePlateDetection` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetLogRule` | `veiapi` | 资源存在性、状态、配置或诊断证据 |
| `GetMediapipeEvent` | `veiapi` | 资源存在性、状态、配置或诊断证据 |
| `GetNodeGroup` | `veiapi` | 资源状态、实例/节点/集群运行态证据 |
| `GetServiceInfo` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetUploadAuth` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `GetUploadAuthToken` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `GetUrlFetchTask` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
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

### 企业直播
- 官方文档识别 Action 数：332
- 纳入只读/诊断 Action：198
- 排除自动执行的写/变更 Action：172
- 其它需按场景人工判断 Action：AnalysisUserBehaviorPeople, AnalysisUserBehaviorPeopleV2, BatchSendActivityRobotComment, ConfirmReviewChatAPI, ConfirmReviewChatApi, DelActivityAntidirtAPI, DelActivityAntidirtApi, DrawActivityRedPacket, EditInteractionScriptComment, EmptyChatAPI, EmptyChatApi, ExplainProduct, ExplainProductAPI, ExplainProductApi, ForbidLiveChannel, GenerateActivityStreamSlice, HideProductPrice, InsertPhoneList, InsertWhiteList, LikeChatAPI ...

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `GetAccountAggregatedStatistics` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetAccountRealTimeOnlineNumber` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetAccountTemplateAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetAccountTemplateApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetAccountUserTrackData` | `livesaas20230801` | 身份、权限、密钥或授权证据 |
| `GetActivityAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityAllCouponsPickData` | `livesaas20230801` | 计费、订单、成本、配额或资源包证据 |
| `GetActivityAntidirtAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityAntidirtApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityBanIps` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityBanUsers` | `livesaas20230801` | 身份、权限、密钥或授权证据 |
| `GetActivityBands` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityBasicConfigAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityBasicConfigApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityBonusTask` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityCommentConfig` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityCouponPickData` | `livesaas20230801` | 计费、订单、成本、配额或资源包证据 |
| `GetActivityCustomEmojiSetDetail` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityEmbeddedUrls` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityExportFile` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityLinks` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityLoginSecret` | `livesaas20230801` | 密钥、安全策略、风险或告警证据 |
| `GetActivityMenuAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityMenuApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityMenus` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityMessageConfig` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityPartnerRebroadcast` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityPoster` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityProducts` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityRedPacket` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityReplayPlayerConfig` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityReservationAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityReservationAPIV2` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityReservationApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityReservationApiv2` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityRobotCommentConfig` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetActivityThumbUpNumber` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetAdvertisementDataAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetAdvertisementDataAPIV2` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetAdvertisementDataApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetAdvertisementDataApiv2` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetAdvertisementDataDetailAPI` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetAdvertisementDataDetailApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetAllStreamPullInfoAPI` | `livesaas` | 域名、证书、CDN、直播或入口链路证据 |
| `GetAllStreamPullInfoApi` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `GetApiInfo` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetAttentionDetectionConfig` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetAudienceGroupConfig` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetAwardConfigListAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetAwardConfigListApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetAwardItemList` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetAwardRecordStatisticsAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetAwardRecordStatisticsApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetBusinessAccountInfo` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetBusinessAccountInfoAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetBusinessAccountInfoApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetCheckInListAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetCheckInListApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetCheckInRecordStatisticsAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetCheckInRecordStatisticsApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetCoupon` | `livesaas20230801` | 计费、订单、成本、配额或资源包证据 |
| `GetCustomActMsgAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetCustomActMsgApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetCustomViewingRestrictionInfoAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetCustomViewingRestrictionInfoApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetDownloadLiveClient` | `livesaas20230801` | 域名、证书、CDN、直播或入口链路证据 |
| `GetDownloadLiveClientAPI` | `livesaas` | 域名、证书、CDN、直播或入口链路证据 |
| `GetDownloadLiveClientApi` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `GetHotChatAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetHotChatApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetInPageAdvertisement` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetInteractionScriptRecordConfig` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetInviterToken` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetLarkSubAccountInfo` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetLinkUserAmount` | `livesaas20230801` | 身份、权限、密钥或授权证据 |
| `GetLiveLinkDurationData` | `livesaas20230801` | 域名、证书、CDN、直播或入口链路证据 |
| `GetLiveTrafficPostPayData` | `livesaas20230801` | 域名、证书、CDN、直播或入口链路证据 |
| `GetLoginLivesaasSts` | `livesaas20230801` | 域名、证书、CDN、直播或入口链路证据 |
| `GetPageWatchDataAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetPageWatchDataAPIV2` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetPageWatchDataApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetPageWatchDataApiv2` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetPhoneList` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetPopularitySettingsAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetPopularitySettingsApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetQuizDataAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetQuizDataApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetRealTimeOnlineNumberAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetRealTimeOnlineNumberApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetSDKTokenAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetSdkTokenApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetSecurityControlConfig` | `livesaas20230801` | 网络路径、入口、路由或安全策略证据 |
| `GetServiceInfo` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetSilenceUserListAPI` | `livesaas` | 身份、权限、密钥或授权证据 |
| `GetSilenceUserListApi` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `GetStreamsAPI` | `livesaas` | 域名、证书、CDN、直播或入口链路证据 |
| `GetStreamsApi` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `GetSubAccount` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetTaskAwardItemListAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetTaskAwardItemListApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetTaskAwardRecordStatisticsAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetTaskAwardRecordStatisticsApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetTeachAssistantConfig` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetTemporaryLoginTokenAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetTemporaryLoginTokenApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetTopChatAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetTopChatApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetUserTaskAwardResultAPI` | `livesaas` | 身份、权限、密钥或授权证据 |
| `GetUserTaskAwardResultApi` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `GetVideoLibraryFolderTree` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetViewerLevelConfig` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetViewingRestrictionInfo` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetVipOrBlackListUserInfo` | `livesaas20230801` | 身份、权限、密钥或授权证据 |
| `GetVodPlayerConfig` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetVodPlayerToken` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `GetVoteListAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetVoteListApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetVoteStatisticsAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `GetVoteStatisticsApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetWebPushLiveClientAPI` | `livesaas` | 域名、证书、CDN、直播或入口链路证据 |
| `GetWebPushLiveClientApi` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `GetWhiteList` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListAccountActivityData` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListAccountUserData` | `livesaas20230801` | 身份、权限、密钥或授权证据 |
| `ListAccountViewerLevelGroup` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListActivityAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `ListActivityApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListActivityBonusTaskWinners` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListActivityBonusTasks` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListActivityByCacheAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `ListActivityByCacheApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListActivityCoupons` | `livesaas20230801` | 计费、订单、成本、配额或资源包证据 |
| `ListActivityCustomEmojiSets` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListActivityMediaAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `ListActivityMediaApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListActivityQuizConfigs` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListActivityRedPacket` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListActivityRobotCommentRepository` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListActivityUsers` | `livesaas20230801` | 身份、权限、密钥或授权证据 |
| `ListAnActivityStartAndEndTimeAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `ListAnActivityStartAndEndTimeApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListAudienceGroupUser` | `livesaas20230801` | 身份、权限、密钥或授权证据 |
| `ListAwardConfigs` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListAwardRecordStatistics` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListCallbackConfigs` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListCallbackEvents` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListChannelAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `ListChannelApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListCoupons` | `livesaas20230801` | 计费、订单、成本、配额或资源包证据 |
| `ListHostAccountAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `ListHostAccountApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListHostAccounts` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListInteractionScriptComments` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListLiveChannelConfig` | `livesaas20230801` | 域名、证书、CDN、直播或入口链路证据 |
| `ListLivePromotionsAPI` | `livesaas` | 域名、证书、CDN、直播或入口链路证据 |
| `ListLivePromotionsApi` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `ListLoopVideos` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListMediasAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `ListMediasApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListPosterInviteAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `ListPosterInviteApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListPrograms` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListQuestionnaireAnswerDataAPIV2` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `ListQuestionnaireAnswerDataApiv2` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListQuestionnaireDataAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `ListQuestionnaireDataAPIV2` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `ListQuestionnaireDataApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListQuestionnaireDataApiv2` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListQuizRecordAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `ListQuizRecordApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListQuizStatisticsAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `ListQuizStatisticsApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListRedPacketDataAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `ListRedPacketDataApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListRedPacketRecordAPI` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `ListRedPacketRecordApi` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListRobotComments` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListRobotNickNames` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListSiteTagAPIV2` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `ListSiteTagApiv2` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListSubAccountOrganizations` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListSubAccountRoles` | `livesaas20230801` | 身份、权限、密钥或授权证据 |
| `ListSubAccounts` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListTeachAssistantAccounts` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListUserBehaviorDataAPI` | `livesaas` | 身份、权限、密钥或授权证据 |
| `ListUserBehaviorDataAPIV2` | `livesaas` | 身份、权限、密钥或授权证据 |
| `ListUserBehaviorDataApi` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `ListUserBehaviorDataApiv2` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `ListUserSubmitEnterReviewAPI` | `livesaas` | 身份、权限、密钥或授权证据 |
| `ListUserSubmitEnterReviewApi` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `ListVodPlayerConfig` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListWaitLinkAudience` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |
| `ListWebSDKDomainConfigs` | `livesaas20230801` | 域名、证书、CDN、直播或入口链路证据 |
| `ListWebSdkDomainConfigs` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `QueryUploadMediaByURL` | `livesaas` | 资源存在性、状态、配置或诊断证据 |
| `QueryUploadMediaByUrl` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `SearchVideoLibraryFolderTree` | `livesaas20230801` | 资源存在性、状态、配置或诊断证据 |

### 实时音视频
- 官方文档识别 Action 数：1
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 智能处理
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：1
- 其它需按场景人工判断 Action：KillJob, RetrieveJob

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 智能视联
- 官方文档识别 Action 数：64
- 纳入只读/诊断 Action：23
- 排除自动执行的写/变更 Action：31
- 其它需按场景人工判断 Action：CloudControl, ControlPlayback, FreshDevice, GenSipId, PlayCloudRecord, StatStream, StreamStartRecord, StreamStopRecord

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `GetDataProjectWithBindWidthAndFlow` | `aiotvideo` | 资源存在性、状态、配置或诊断证据 |
| `GetDevice` | `aiotvideo` | 资源存在性、状态、配置或诊断证据 |
| `GetDeviceChannelsV2` | `aiotvideo` | 资源存在性、状态、配置或诊断证据 |
| `GetLocalDownload` | `aiotvideo` | 资源存在性、状态、配置或诊断证据 |
| `GetPushStreamCnt` | `aiotvideo` | 域名、证书、CDN、直播或入口链路证据 |
| `GetRecordList` | `aiotvideo20231001` | 资源存在性、状态、配置或诊断证据 |
| `GetRecordPlan` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetScreenshotTemplate` | `aiotvideo` | 资源存在性、状态、配置或诊断证据 |
| `GetSpace` | `aiotvideo` | 资源存在性、状态、配置或诊断证据 |
| `GetSpaceTemplate` | `aiotvideo` | 资源存在性、状态、配置或诊断证据 |
| `GetStream` | `aiotvideo` | 域名、证书、CDN、直播或入口链路证据 |
| `GetStreamData` | `aiotvideo` | 域名、证书、CDN、直播或入口链路证据 |
| `GetStreamRecord` | `aiotvideo` | 域名、证书、CDN、直播或入口链路证据 |
| `GetTotalData` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListDeviceScreenshotsV2` | `aiotvideo` | 资源存在性、状态、配置或诊断证据 |
| `ListDevices` | `aiotvideo` | 资源存在性、状态、配置或诊断证据 |
| `ListRecordPlanChannels` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListRecordPlans` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListScreenshotTemplates` | `aiotvideo` | 资源存在性、状态、配置或诊断证据 |
| `ListSpaces` | `aiotvideo` | 资源存在性、状态、配置或诊断证据 |
| `ListStreamRecords` | `aiotvideo20231001` | 域名、证书、CDN、直播或入口链路证据 |
| `ListStreamScreenshots` | `aiotvideo20231001` | 域名、证书、CDN、直播或入口链路证据 |
| `ListStreams` | `aiotvideo` | 域名、证书、CDN、直播或入口链路证据 |

### 短信服务
- 官方文档识别 Action 数：23
- 纳入只读/诊断 Action：9
- 排除自动执行的写/变更 Action：7
- 其它需按场景人工判断 Action：ApplySignatureIdent, ApplySmsSignature, ApplySmsSignatureV2, ApplySmsTemplate, ApplyVmsTemplate, BatchBindSignatureIdent, Conversion, InsertSmsSubAccount

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `CheckSmsVerifyCode` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetServiceInfo` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetSignatureAndOrderList` | `Python SDK-only/未匹配 CLI` | 计费、订单、成本、配额或资源包证据 |
| `GetSignatureIdentList` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |
| `GetSmsSendDetails` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetSmsTemplateAndOrderList` | `Python SDK-only/未匹配 CLI` | 计费、订单、成本、配额或资源包证据 |
| `GetSubAccountDetail` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetSubAccountList` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetVmsTemplateStatus` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |

### 视频点播
- 官方文档识别 Action 数：170
- 纳入只读/诊断 Action：11
- 排除自动执行的写/变更 Action：31
- 其它需按场景人工判断 Action：ContinueAITranslationWorkflow, ContinueAiTranslationWorkflow, GenerateAITranslationUtteranceAudio, GenerateAiTranslationUtteranceAudio, RefreshAITranslationProject, RefreshAiTranslationProject

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `GetAITermbase` | `vod20250101` | 资源存在性、状态、配置或诊断证据 |
| `GetAITranslationProject` | `vod20250101` | 资源存在性、状态、配置或诊断证据 |
| `GetAiTermbase` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetAiTranslationProject` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetExecution` | `vod20250101` | 资源存在性、状态、配置或诊断证据 |
| `ListAITermbase` | `vod20250101` | 资源存在性、状态、配置或诊断证据 |
| `ListAITranslationProject` | `vod20250101` | 资源存在性、状态、配置或诊断证据 |
| `ListAITranslationSpeech` | `vod20250101` | 资源存在性、状态、配置或诊断证据 |
| `ListAiTermbase` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListAiTranslationProject` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListAiTranslationSpeech` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |

### 视频直播
- 官方文档识别 Action 数：200
- 纳入只读/诊断 Action：41
- 排除自动执行的写/变更 Action：36
- 其它需按场景人工判断 Action：ForbidStream, GeneratePlayURL, GeneratePushURL, KillStream, ManagerPullPushDomainBind, RestartPullToPushTask

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAuth` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `DescribeCDNSnapshotHistory` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeCallback` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeClosedStreamInfoByPage` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeDenyConfig` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDomain` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeForbiddenStreamInfoByPage` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeLiveAuditData` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeLiveBandwidthData` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |
| `DescribeLiveBatchPushStreamMetrics` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeLiveBatchSourceStreamMetrics` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeLiveDomainLog` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeLiveMetricBandwidthData` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |
| `DescribeLiveMetricTrafficData` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeLiveP95peakBandwidthData` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |
| `DescribeLiveStreamInfoByPage` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeLiveStreamSessions` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeLiveStreamState` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeLiveTrafficData` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribePlayResponseStatusStat` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribePlayStreamList` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribePullToPushBandwidthData` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |
| `DescribePushStreamMetrics` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeRecordData` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRecordTaskFileHistory` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeReferer` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRelaySourceV2` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSnapshotData` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTranscodeData` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeVQScoreTask` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetApiInfo` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetServiceInfo` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListCert` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `ListCommonTransPresetDetail` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListDomainDetail` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `ListPullToPushTask` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListVQScoreTask` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListVhostRecordPreset` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListVhostSnapshotAuditPreset` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListVhostSnapshotPreset` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListVhostTranscodePreset` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |

### 语音服务
- 官方文档识别 Action 数：58
- 纳入只读/诊断 Action：17
- 排除自动执行的写/变更 Action：51
- 其它需按场景人工判断 Action：BatchAppend, BatchAppendTask, Click2Call, Click2CallLite, CommitResourceUpload, CommonHandler, DoJsonHandler, DoPostHandler, DoQueryHandler, NumberList, NumberPoolList, PauseTask, RegisterIndustrialId, RouteAAuth, SelectNumber, SelectNumberAndBindAXB, SelectNumberAndBindAXN, SelectNumberAndBindAxb, SelectNumberAndBindAxn, SingleBatchAppend ...

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `FetchResource` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetResourceUploadUrl` | `vms` | 资源存在性、状态、配置或诊断证据 |
| `GetServiceInfo` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `QueryAudioRecordFileUrl` | `vms` | 资源存在性、状态、配置或诊断证据 |
| `QueryAudioRecordToTextFileUrl` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `QueryAudioRecordToTextFileUrlV2` | `vms` | 资源存在性、状态、配置或诊断证据 |
| `QueryAuth` | `vms` | 身份、权限、密钥或授权证据 |
| `QueryCallCall` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `QueryCallRecordMsg` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `QueryCallRecordMsgV2` | `vms` | 资源存在性、状态、配置或诊断证据 |
| `QueryOpenGetResource` | `vms` | 资源存在性、状态、配置或诊断证据 |
| `QueryQualification` | `vms` | 资源存在性、状态、配置或诊断证据 |
| `QuerySingleInfo` | `vms` | 资源存在性、状态、配置或诊断证据 |
| `QuerySubscription` | `vms` | 资源存在性、状态、配置或诊断证据 |
| `QuerySubscriptionForList` | `vms` | 资源存在性、状态、配置或诊断证据 |
| `QueryUsableResource` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `QueryUsableResourceV2` | `vms` | 资源存在性、状态、配置或诊断证据 |

## 使用建议
- 优先使用章节 reference 中已经编排好的命令包；当用户问题落在未细化章节时，再从本矩阵选择最小只读 Action 补充证据。
- 如果某个只读 Action 需要分页、跨产品联动或深层字段归一，再考虑新增 `scripts/` 只读脚本，并同步更新脚本说明。
- 如果只读证据指向写操作修复，必须先输出影响面、资源 ID、回滚/恢复建议，并等待用户确认。
