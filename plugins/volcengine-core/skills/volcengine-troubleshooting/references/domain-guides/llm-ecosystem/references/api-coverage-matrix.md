# API 覆盖审查矩阵
本文件由 2026-05-22 审查生成，用于证明本 skill 已对 `cli-meta/` 中对应分类的 OpenAPI / CLI / Python SDK 能力做过覆盖盘点。它不是执行顺序清单；Agent 仍应先按主 `SKILL.md` 和章节 reference 选择最小必要证据。
## 审查口径
- 纳入排障优先级：`Describe/List/Get/Query/Check/Search/BatchGet/Verify/Validate/Test/Diagnose/Preview/Estimate` 等只读或诊断型 Action。
- 默认排除自动执行：`Create/Modify/Delete/Update/Attach/Detach/Start/Stop/Run/Invoke/Pay/Renew/Set` 等会改变资源、资金、权限或任务状态的 Action；只能作为解释错误码或 Human-in-the-Loop 建议背景。
- 命令形态：执行时统一写作 `ve <service> <Action> [--Param value...]`；参数不确定时先查 `ve <service> <Action> --help` 或对应 `cli-meta`。
- 凭证边界：只从临时环境读取 `VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、`VOLCENGINE_REGION`，不得写入配置、文档或日志。
## 总览
- 覆盖产品数：25
- 官方文档识别 OpenAPI Action 数合计：523
- 纳入排障候选的只读/诊断 Action 数：221
- 默认不自动执行的写/变更 Action 数：269
- 需人工判断语义的其它 Action 数：76

## 产品级覆盖
### AgentKit
- 官方文档识别 Action 数：111
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

### ArkClaw
- 官方文档识别 Action 数：72
- 纳入只读/诊断 Action：2
- 排除自动执行的写/变更 Action：4
- 其它需按场景人工判断 Action：ExecuteClawOmniInstanceCommand, PauseClawOmniInstance

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `GetClawOmniInstance` | `arkclaw` | 资源状态、实例/节点/集群运行态证据 |
| `ListClawOmniInstances` | `arkclaw` | 资源状态、实例/节点/集群运行态证据 |

### TRAE CN
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### Viking AI 搜索
- 官方文档识别 Action 数：16
- 纳入只读/诊断 Action：6
- 排除自动执行的写/变更 Action：12
- 其它需按场景人工判断 Action：MemoryCollectionDelete, MemoryCollectionInfo, MemoryCollectionList, MemoryCollectionUpdate

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `GetVikingdbCollection` | `vikingdb` | 存储、备份或数据库控制面证据 |
| `GetVikingdbIndex` | `vikingdb` | 存储、备份或数据库控制面证据 |
| `GetVikingdbTask` | `vikingdb` | 存储、备份或数据库控制面证据 |
| `ListVikingdbCollection` | `vikingdb` | 存储、备份或数据库控制面证据 |
| `ListVikingdbIndex` | `vikingdb` | 存储、备份或数据库控制面证据 |
| `ListVikingdbTask` | `vikingdb` | 存储、备份或数据库控制面证据 |

### 创作Agent
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 即梦AI
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 向量数据库VikingDB
- 官方文档识别 Action 数：2
- 纳入只读/诊断 Action：6
- 排除自动执行的写/变更 Action：12
- 其它需按场景人工判断 Action：MemoryCollectionDelete, MemoryCollectionInfo, MemoryCollectionList, MemoryCollectionUpdate

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `GetVikingdbCollection` | `vikingdb` | 存储、备份或数据库控制面证据 |
| `GetVikingdbIndex` | `vikingdb` | 存储、备份或数据库控制面证据 |
| `GetVikingdbTask` | `vikingdb` | 存储、备份或数据库控制面证据 |
| `ListVikingdbCollection` | `vikingdb` | 存储、备份或数据库控制面证据 |
| `ListVikingdbIndex` | `vikingdb` | 存储、备份或数据库控制面证据 |
| `ListVikingdbTask` | `vikingdb` | 存储、备份或数据库控制面证据 |

### 图像生成大模型
- 官方文档识别 Action 数：1
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0
- 其它需按场景人工判断 Action：AIGCStylizeImage, AIGCStylizeImageUsage, AIgcStylizeImage, AIgcStylizeImageUsage, EmotionPortrait, EntitySegment, FaceFusionMovieGetResult, FaceFusionMovieSubmitTask, FaceSwap, FaceSwapAI, FaceSwapAi, HairStyle, HighAesAnimeV13, HighAesGeneralV13, HighAesGeneralV14, HighAesGeneralV14IPKeep, HighAesGeneralV14IpKeep, HighAesGeneralV20, HighAesGeneralV20L, HighAesIPV20 ...

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 大模型安全测评
- 官方文档识别 Action 数：36
- 纳入只读/诊断 Action：18
- 排除自动执行的写/变更 Action：9
- 其它需按场景人工判断 Action：ConnectAgent, ConnectModel, EditEvalTask, OperateTask

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `GetAgentDetail` | `llmscan` | 模型、端点、Agent 或工作空间状态证据 |
| `GetConnectAgentResult` | `llmscan` | 模型、端点、Agent 或工作空间状态证据 |
| `GetDimensionTreeByTask` | `llmscan` | 资源存在性、状态、配置或诊断证据 |
| `GetLLMEvalTaskReport` | `llmscan` | 资源存在性、状态、配置或诊断证据 |
| `GetLlmEvalTaskReport` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetModelDetail` | `llmscan` | 模型、端点、Agent 或工作空间状态证据 |
| `GetRiskSummary` | `llmscan` | 密钥、安全策略、风险或告警证据 |
| `GetTaskDetail` | `llmscan` | 资源存在性、状态、配置或诊断证据 |
| `GetTaskProgress` | `llmscan` | 资源存在性、状态、配置或诊断证据 |
| `ListAgent` | `llmscan` | 模型、端点、Agent 或工作空间状态证据 |
| `ListAttackSuccessExample` | `llmscan` | 资源存在性、状态、配置或诊断证据 |
| `ListAttackSummary` | `llmscan` | 资源存在性、状态、配置或诊断证据 |
| `ListAttackTypeSummary` | `llmscan` | 资源存在性、状态、配置或诊断证据 |
| `ListLLMEvalTasks` | `llmscan` | 资源存在性、状态、配置或诊断证据 |
| `ListLlmEvalTasks` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListModelApplication` | `llmscan` | 模型、端点、Agent 或工作空间状态证据 |
| `ListRiskSeverity` | `llmscan` | 密钥、安全策略、风险或告警证据 |
| `ListTaskDetails` | `llmscan` | 资源存在性、状态、配置或诊断证据 |

### 大模型应用防火墙
- 官方文档识别 Action 数：3
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 客服Agent
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 扣子
- 官方文档识别 Action 数：1
- 纳入只读/诊断 Action：1
- 排除自动执行的写/变更 Action：1
- 其它需按场景人工判断 Action：AuthorizeCozeToUser, AuthorizeVolcToUser

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `ListCozeUser` | `coze20250601` | 身份、权限、密钥或授权证据 |

### 智能体身份和权限管理平台
- 官方文档识别 Action 数：133
- 纳入只读/诊断 Action：102
- 排除自动执行的写/变更 Action：120
- 其它需按场景人工判断 Action：BatchCreateRoutes, BatchListDepartmentsForUsers, BatchSyncDepartmentMembers, BatchUpsertDepartments, CommitDepartmentSyncSession, CompleteResourceTokenAuth, LinkIdentityProviderToUser, Oauth2Callback, PublishRoute, PublishService, RegisterService

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `BatchGetApiKeyCredentialProviders` | `id` | 身份、权限、密钥或授权证据 |
| `BatchGetDepartments` | `id` | 资源存在性、状态、配置或诊断证据 |
| `BatchGetInboundAuthConfig` | `id` | 身份、权限、密钥或授权证据 |
| `BatchGetOauth2CredentialProviders` | `id` | 身份、权限、密钥或授权证据 |
| `CheckApiKey` | `id` | 身份、权限、密钥或授权证据 |
| `CheckPermission` | `id` | 身份、权限、密钥或授权证据 |
| `CheckServiceName` | `id` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRouteTemplateOptions` | `id` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTagOptions` | `id` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTemplateOptions` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetApiKeyCredentialProvider` | `id` | 身份、权限、密钥或授权证据 |
| `GetDepartment` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetDepartmentPath` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetDepartmentSyncJob` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetDepartmentSyncSession` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetDepartmentTree` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetDocumentStatus` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetFaasService` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetGroup` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetIamRoleAttachment` | `id` | 身份、权限、密钥或授权证据 |
| `GetIdentityProviderFeishuScopes` | `id` | 身份、权限、密钥或授权证据 |
| `GetIdentityProviderLDAPADAgent` | `id` | 身份、权限、密钥或授权证据 |
| `GetIdentityProviderLdapadAgent` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `GetIdentityProviderOAuth` | `id` | 身份、权限、密钥或授权证据 |
| `GetIdentityProviderOIDC` | `id` | 身份、权限、密钥或授权证据 |
| `GetIdentityProviderOidc` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `GetIdentityProviderSAML` | `id` | 身份、权限、密钥或授权证据 |
| `GetIdentityProviderSaml` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `GetIdentityProviderWeCom` | `id` | 身份、权限、密钥或授权证据 |
| `GetInboundAuthConfig` | `id` | 身份、权限、密钥或授权证据 |
| `GetNamespace` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetOauth2CredentialProvider` | `id` | 身份、权限、密钥或授权证据 |
| `GetPermissionPoint` | `id` | 身份、权限、密钥或授权证据 |
| `GetPolicy` | `id` | 身份、权限、密钥或授权证据 |
| `GetResourceApiKey` | `id` | 身份、权限、密钥或授权证据 |
| `GetResourceOauth2Token` | `id` | 身份、权限、密钥或授权证据 |
| `GetRoleCredentialProvider` | `id` | 身份、权限、密钥或授权证据 |
| `GetRoleCredentials` | `id` | 身份、权限、密钥或授权证据 |
| `GetRoute` | `id` | 网络路径、入口、路由或安全策略证据 |
| `GetSCIMProvisioningDefaults` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetScimProvisioningDefaults` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetService` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetSmsService` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetTask` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetTaskStateUserSync` | `id` | 身份、权限、密钥或授权证据 |
| `GetTenantServiceStatus` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetTrustAnchor` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetUser` | `id` | 身份、权限、密钥或授权证据 |
| `GetUserCSVTemplate` | `id` | 身份、权限、密钥或授权证据 |
| `GetUserCredential` | `id` | 身份、权限、密钥或授权证据 |
| `GetUserCsvTemplate` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `GetUserPool` | `id` | 身份、权限、密钥或授权证据 |
| `GetUserPoolClient` | `id` | 身份、权限、密钥或授权证据 |
| `GetUserPoolIamCredentialsServiceConfig` | `id` | 身份、权限、密钥或授权证据 |
| `GetUserPoolMaus` | `id` | 身份、权限、密钥或授权证据 |
| `GetWorkloadAccessToken` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetWorkloadAccessTokenForJWT` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetWorkloadAccessTokenForJwt` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetWorkloadAccessTokenForUserId` | `id` | 身份、权限、密钥或授权证据 |
| `GetWorkloadIdentity` | `id` | 身份、权限、密钥或授权证据 |
| `GetWorkloadPool` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListApiKeyCredentialProviders` | `id` | 身份、权限、密钥或授权证据 |
| `ListCredentialProviders` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListDepartmentMembers` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListDepartmentSyncJobs` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListDepartments` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListDepartmentsForUser` | `id` | 身份、权限、密钥或授权证据 |
| `ListFaasServices` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListGroups` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListGroupsForUser` | `id` | 身份、权限、密钥或授权证据 |
| `ListGroupsForUsers` | `id` | 身份、权限、密钥或授权证据 |
| `ListIdentityProviderLDAPADAgent` | `id` | 身份、权限、密钥或授权证据 |
| `ListIdentityProviderLdapadAgent` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `ListIdentityProviders` | `id` | 身份、权限、密钥或授权证据 |
| `ListIdentityProvidersOAuth` | `id` | 身份、权限、密钥或授权证据 |
| `ListIdentityProvidersOIDC` | `id` | 身份、权限、密钥或授权证据 |
| `ListIdentityProvidersOidc` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `ListIdentityProvidersSAML` | `id` | 身份、权限、密钥或授权证据 |
| `ListIdentityProvidersSaml` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `ListIdentityProvidersWeCom` | `id` | 身份、权限、密钥或授权证据 |
| `ListInboundAuthConfigs` | `id` | 身份、权限、密钥或授权证据 |
| `ListMergeUserSyncResultUsers` | `id` | 身份、权限、密钥或授权证据 |
| `ListNamespaces` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListOauth2CredentialProviders` | `id` | 身份、权限、密钥或授权证据 |
| `ListPermissionPoints` | `id` | 身份、权限、密钥或授权证据 |
| `ListPolicies` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListRoleCredentialProviders` | `id` | 身份、权限、密钥或授权证据 |
| `ListRoutes` | `id` | 网络路径、入口、路由或安全策略证据 |
| `ListSCIMTokens` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListScimTokens` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListServices` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListTagsForResources` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListTasks` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListTrustAnchors` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListUserPoolClients` | `id` | 身份、权限、密钥或授权证据 |
| `ListUserPools` | `id` | 身份、权限、密钥或授权证据 |
| `ListUsers` | `id` | 身份、权限、密钥或授权证据 |
| `ListUsersInDepartment` | `id` | 身份、权限、密钥或授权证据 |
| `ListUsersInGroup` | `id` | 身份、权限、密钥或授权证据 |
| `ListWorkloadIdentities` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListWorkloadPools` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ValidateDepartmentSyncSession` | `id` | 资源存在性、状态、配置或诊断证据 |

### 智能美化特效
- 官方文档识别 Action 数：1
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 智能视频分析
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 智能视频创作SDK
- 官方文档识别 Action 数：1
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 机器学习平台
- 官方文档识别 Action 数：60
- 纳入只读/诊断 Action：24
- 排除自动执行的写/变更 Action：35
- 其它需按场景人工判断 Action：PauseResourceQueue, RebuildDevInstance, SignJwtToken

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `GetDeployment` | `mlplatform20240701` | 资源存在性、状态、配置或诊断证据 |
| `GetDevInstance` | `mlplatform20240701` | 资源状态、实例/节点/集群运行态证据 |
| `GetInstanceType` | `mlplatform20240701` | 资源状态、实例/节点/集群运行态证据 |
| `GetJob` | `mlplatform20240701` | 资源存在性、状态、配置或诊断证据 |
| `GetResourceGroup` | `mlplatform20240701` | 资源存在性、状态、配置或诊断证据 |
| `GetResourceQueue` | `mlplatform20240701` | 资源存在性、状态、配置或诊断证据 |
| `GetResourceReservationPlan` | `mlplatform20240701` | 资源存在性、状态、配置或诊断证据 |
| `GetService` | `mlplatform20240701` | 资源存在性、状态、配置或诊断证据 |
| `ListAvailabilityZones` | `mlplatform20240701` | 资源存在性、状态、配置或诊断证据 |
| `ListDeployments` | `mlplatform20240701` | 资源存在性、状态、配置或诊断证据 |
| `ListDevInstances` | `mlplatform20240701` | 资源状态、实例/节点/集群运行态证据 |
| `ListInstanceTypes` | `mlplatform20240701` | 资源状态、实例/节点/集群运行态证据 |
| `ListJobInstances` | `mlplatform20240701` | 资源状态、实例/节点/集群运行态证据 |
| `ListJobs` | `mlplatform20240701` | 资源存在性、状态、配置或诊断证据 |
| `ListPublicImageRepos` | `mlplatform20240701` | 资源存在性、状态、配置或诊断证据 |
| `ListPublicImageTags` | `mlplatform20240701` | 资源存在性、状态、配置或诊断证据 |
| `ListResourceClaimOptions` | `mlplatform20240701` | 资源存在性、状态、配置或诊断证据 |
| `ListResourceGroups` | `mlplatform20240701` | 资源存在性、状态、配置或诊断证据 |
| `ListResourceQueues` | `mlplatform20240701` | 资源存在性、状态、配置或诊断证据 |
| `ListResourceReservationPlanAvailableResources` | `mlplatform20240701` | 资源存在性、状态、配置或诊断证据 |
| `ListResourceReservationPlans` | `mlplatform20240701` | 资源存在性、状态、配置或诊断证据 |
| `ListResourceReservationRecords` | `mlplatform20240701` | 资源存在性、状态、配置或诊断证据 |
| `ListServices` | `mlplatform20240701` | 资源存在性、状态、配置或诊断证据 |
| `ListVolumeTypes` | `mlplatform20240701` | 存储、备份或数据库控制面证据 |

### 火山方舟
- 官方文档识别 Action 数：60
- 纳入只读/诊断 Action：9
- 排除自动执行的写/变更 Action：8

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `GetApiKey` | `ark` | 身份、权限、密钥或授权证据 |
| `GetEndpoint` | `ark` | 模型、端点、Agent 或工作空间状态证据 |
| `GetEndpointCertificate` | `ark` | 域名、证书、CDN、直播或入口链路证据 |
| `GetModelCustomizationJob` | `ark` | 模型、端点、Agent 或工作空间状态证据 |
| `GetModelCustomizationJobMetricData` | `ark` | 模型、端点、Agent 或工作空间状态证据 |
| `GetModelCustomizationJobMetrics` | `ark` | 模型、端点、Agent 或工作空间状态证据 |
| `ListBatchInferenceJobs` | `ark` | 资源存在性、状态、配置或诊断证据 |
| `ListEndpoints` | `ark` | 模型、端点、Agent 或工作空间状态证据 |
| `ListModelCustomizationJobs` | `ark` | 模型、端点、Agent 或工作空间状态证据 |

### 联网搜索
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：9
- 排除自动执行的写/变更 Action：8

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `GetApiKey` | `ark` | 身份、权限、密钥或授权证据 |
| `GetEndpoint` | `ark` | 模型、端点、Agent 或工作空间状态证据 |
| `GetEndpointCertificate` | `ark` | 域名、证书、CDN、直播或入口链路证据 |
| `GetModelCustomizationJob` | `ark` | 模型、端点、Agent 或工作空间状态证据 |
| `GetModelCustomizationJobMetricData` | `ark` | 模型、端点、Agent 或工作空间状态证据 |
| `GetModelCustomizationJobMetrics` | `ark` | 模型、端点、Agent 或工作空间状态证据 |
| `ListBatchInferenceJobs` | `ark` | 资源存在性、状态、配置或诊断证据 |
| `ListEndpoints` | `ark` | 模型、端点、Agent 或工作空间状态证据 |
| `ListModelCustomizationJobs` | `ark` | 模型、端点、Agent 或工作空间状态证据 |

### 联网问答Agent
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 虚拟数字人
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 视频高光提取
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 豆包语音
- 官方文档识别 Action 数：25
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 音视频理解与处理
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 音频技术
- 官方文档识别 Action 数：1
- 纳入只读/诊断 Action：20
- 排除自动执行的写/变更 Action：20
- 其它需按场景人工判断 Action：ExistResourcePool, existResourcePool

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeApplication` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeApplicationInstance` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeProject` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeResourcePool` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListAppInstance` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `ListApplication` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListApplicationHistory` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListProject` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListResourcePool` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListZone` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `describeApplication` | `spark` | 资源存在性、状态、配置或诊断证据 |
| `describeApplicationInstance` | `spark` | 资源状态、实例/节点/集群运行态证据 |
| `describeProject` | `spark` | 资源存在性、状态、配置或诊断证据 |
| `describeResourcePool` | `spark` | 资源存在性、状态、配置或诊断证据 |
| `listAppInstance` | `spark` | 资源状态、实例/节点/集群运行态证据 |
| `listApplication` | `spark` | 资源存在性、状态、配置或诊断证据 |
| `listApplicationHistory` | `spark` | 资源存在性、状态、配置或诊断证据 |
| `listProject` | `spark` | 资源存在性、状态、配置或诊断证据 |
| `listResourcePool` | `spark` | 资源存在性、状态、配置或诊断证据 |
| `listZone` | `spark` | 资源存在性、状态、配置或诊断证据 |

## 使用建议
- 优先使用章节 reference 中已经编排好的命令包；当用户问题落在未细化章节时，再从本矩阵选择最小只读 Action 补充证据。
- 如果某个只读 Action 需要分页、跨产品联动或深层字段归一，再考虑新增 `scripts/` 只读脚本，并同步更新脚本说明。
- 如果只读证据指向写操作修复，必须先输出影响面、资源 ID、回滚/恢复建议，并等待用户确认。
