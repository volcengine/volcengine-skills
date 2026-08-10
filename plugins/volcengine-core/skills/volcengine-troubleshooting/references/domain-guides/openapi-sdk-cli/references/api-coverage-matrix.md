# API 覆盖审查矩阵
本文件由 2026-05-22 审查生成，用于证明本 skill 已对 `cli-meta/` 中对应分类的 OpenAPI / CLI / Python SDK 能力做过覆盖盘点。它不是执行顺序清单；Agent 仍应先按主 `SKILL.md` 和章节 reference 选择最小必要证据。
## 审查口径
- 纳入排障优先级：`Describe/List/Get/Query/Check/Search/BatchGet/Verify/Validate/Test/Diagnose/Preview/Estimate` 等只读或诊断型 Action。
- 默认排除自动执行：`Create/Modify/Delete/Update/Attach/Detach/Start/Stop/Run/Invoke/Pay/Renew/Set` 等会改变资源、资金、权限或任务状态的 Action；只能作为解释错误码或 Human-in-the-Loop 建议背景。
- 命令形态：执行时统一写作 `ve <service> <Action> [--Param value...]`；参数不确定时先查 `ve <service> <Action> --help` 或对应 `cli-meta`。
- 凭证边界：只从临时环境读取 `VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、`VOLCENGINE_REGION`，不得写入配置、文档或日志。
## 总览
- 覆盖产品数：7
- 官方文档识别 OpenAPI Action 数合计：11
- 纳入排障候选的只读/诊断 Action 数：236
- 默认不自动执行的写/变更 Action 数：309
- 需人工判断语义的其它 Action 数：49

## 产品级覆盖
### API 网关
- 官方文档识别 Action 数：1
- 纳入只读/诊断 Action：29
- 排除自动执行的写/变更 Action：37

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `CheckConsumerCredentialExist` | `apig` | 资源存在性、状态、配置或诊断证据 |
| `CheckConsumerExist` | `apig` | 资源存在性、状态、配置或诊断证据 |
| `CheckConsumerUsed` | `apig` | 资源存在性、状态、配置或诊断证据 |
| `CheckCustomDomainExist` | `apig` | 域名、证书、CDN、直播或入口链路证据 |
| `CheckGatewayExist` | `apig` | 资源存在性、状态、配置或诊断证据 |
| `CheckGatewayServiceExist` | `apig` | 资源存在性、状态、配置或诊断证据 |
| `CheckRouteExist` | `apig20221112` | 网络路径、入口、路由或安全策略证据 |
| `CheckUpstreamExist` | `apig` | 域名、证书、CDN、直播或入口链路证据 |
| `CheckUpstreamVersionExist` | `apig` | 域名、证书、CDN、直播或入口链路证据 |
| `GetConsumer` | `apig` | 资源存在性、状态、配置或诊断证据 |
| `GetCustomDomain` | `apig` | 域名、证书、CDN、直播或入口链路证据 |
| `GetGateway` | `apig` | 资源存在性、状态、配置或诊断证据 |
| `GetGatewayService` | `apig` | 资源存在性、状态、配置或诊断证据 |
| `GetJwtToken` | `apig` | 资源存在性、状态、配置或诊断证据 |
| `GetPluginBinding` | `apig` | 资源存在性、状态、配置或诊断证据 |
| `GetRoute` | `apig20221112` | 网络路径、入口、路由或安全策略证据 |
| `GetUpstream` | `apig` | 域名、证书、CDN、直播或入口链路证据 |
| `GetUpstreamSource` | `apig` | 域名、证书、CDN、直播或入口链路证据 |
| `ListConsumerCredentials` | `apig` | 资源存在性、状态、配置或诊断证据 |
| `ListConsumers` | `apig` | 资源存在性、状态、配置或诊断证据 |
| `ListCustomDomains` | `apig` | 域名、证书、CDN、直播或入口链路证据 |
| `ListGatewayLBs` | `apig` | 资源存在性、状态、配置或诊断证据 |
| `ListGatewayLbs` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListGatewayServices` | `apig` | 资源存在性、状态、配置或诊断证据 |
| `ListGateways` | `apig` | 资源存在性、状态、配置或诊断证据 |
| `ListPluginBindings` | `apig` | 资源存在性、状态、配置或诊断证据 |
| `ListRoutes` | `apig20221112` | 网络路径、入口、路由或安全策略证据 |
| `ListUpstreamSources` | `apig` | 域名、证书、CDN、直播或入口链路证据 |
| `ListUpstreams` | `apig` | 域名、证书、CDN、直播或入口链路证据 |

### API签名调用指南
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### API访问密钥（Access Key）
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：36
- 排除自动执行的写/变更 Action：60
- 其它需按场景人工判断 Action：AssumeRole

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `GetAccessKeyLastUsed` | `iam` | 身份、权限、密钥或授权证据 |
| `GetAccountSummary` | `iam` | 资源存在性、状态、配置或诊断证据 |
| `GetAllowedIPAddresses` | `iam` | 资源存在性、状态、配置或诊断证据 |
| `GetAllowedIpAddresses` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetCallerIdentity` | `sts` | 身份、权限、密钥或授权证据 |
| `GetGroup` | `iam` | 资源存在性、状态、配置或诊断证据 |
| `GetLoginProfile` | `iam` | 资源存在性、状态、配置或诊断证据 |
| `GetOAuthProvider` | `iam` | 身份、权限、密钥或授权证据 |
| `GetOIDCProvider` | `iam` | 资源存在性、状态、配置或诊断证据 |
| `GetOidcProvider` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetPolicy` | `iam` | 身份、权限、密钥或授权证据 |
| `GetRole` | `iam` | 身份、权限、密钥或授权证据 |
| `GetSAMLProvider` | `iam` | 资源存在性、状态、配置或诊断证据 |
| `GetSamlProvider` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetSecurityConfig` | `iam` | 网络路径、入口、路由或安全策略证据 |
| `GetServiceInfo` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetUser` | `iam` | 身份、权限、密钥或授权证据 |
| `ListAccessKeys` | `iam` | 身份、权限、密钥或授权证据 |
| `ListAttachedRolePolicies` | `iam` | 身份、权限、密钥或授权证据 |
| `ListAttachedUserGroupPolicies` | `iam` | 身份、权限、密钥或授权证据 |
| `ListAttachedUserPolicies` | `iam` | 身份、权限、密钥或授权证据 |
| `ListEntitiesForPolicy` | `iam` | 身份、权限、密钥或授权证据 |
| `ListGroups` | `iam` | 资源存在性、状态、配置或诊断证据 |
| `ListGroupsForUser` | `iam` | 身份、权限、密钥或授权证据 |
| `ListIdentityProviders` | `iam` | 身份、权限、密钥或授权证据 |
| `ListOIDCProviders` | `iam` | 资源存在性、状态、配置或诊断证据 |
| `ListOidcProviders` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListPolicies` | `iam` | 资源存在性、状态、配置或诊断证据 |
| `ListRoles` | `iam` | 身份、权限、密钥或授权证据 |
| `ListSAMLProviderCertificates` | `iam` | 域名、证书、CDN、直播或入口链路证据 |
| `ListSAMLProviders` | `iam` | 资源存在性、状态、配置或诊断证据 |
| `ListSamlProviderCertificates` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `ListSamlProviders` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListTagsForResources` | `iam` | 资源存在性、状态、配置或诊断证据 |
| `ListUsers` | `iam` | 身份、权限、密钥或授权证据 |
| `ListUsersForGroup` | `iam` | 身份、权限、密钥或授权证据 |

### CLI工具
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 云控制API
- 官方文档识别 Action 数：9
- 纳入只读/诊断 Action：171
- 排除自动执行的写/变更 Action：212
- 其它需按场景人工判断 Action：AcceptResourceShareInvitation, BatchAppendTask, BatchCreateRoutes, BatchListDepartmentsForUsers, BatchRerank, BatchSyncDepartmentMembers, BatchUpsertDepartments, Click2Call, Click2CallLite, CommitDepartmentSyncSession, CommitResourceUpload, CommonHandler, CompleteResourceTokenAuth, DoJsonHandler, DoPostHandler, DoQueryHandler, DropCollection, DropIndex, DropTask, Embedding ...

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `BatchGetApiKeyCredentialProviders` | `id` | 身份、权限、密钥或授权证据 |
| `BatchGetDepartments` | `id` | 资源存在性、状态、配置或诊断证据 |
| `BatchGetInboundAuthConfig` | `id` | 身份、权限、密钥或授权证据 |
| `BatchGetOauth2CredentialProviders` | `id` | 身份、权限、密钥或授权证据 |
| `CheckApiKey` | `id` | 身份、权限、密钥或授权证据 |
| `CheckPermission` | `id` | 身份、权限、密钥或授权证据 |
| `CheckServiceName` | `id` | 资源存在性、状态、配置或诊断证据 |
| `DescribeResourceShareInvitations` | `resourceshare` | 资源存在性、状态、配置或诊断证据 |
| `DescribeResourceShares` | `resourceshare` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRouteTemplateOptions` | `id` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTagOptions` | `id` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTemplateOptions` | `id` | 资源存在性、状态、配置或诊断证据 |
| `FetchResource` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetAddress` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetAgent` | `Python SDK-only/未匹配 CLI` | 模型、端点、Agent 或工作空间状态证据 |
| `GetAgentGroup` | `Python SDK-only/未匹配 CLI` | 模型、端点、Agent 或工作空间状态证据 |
| `GetAgentGroupStatus` | `Python SDK-only/未匹配 CLI` | 模型、端点、Agent 或工作空间状态证据 |
| `GetApiAccesskey` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `GetApiKeyCredentialProvider` | `id` | 身份、权限、密钥或授权证据 |
| `GetCollection` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
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
| `GetIndex` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetManagedAppPodLog` | `cp` | 资源状态、实例/节点/集群运行态证据 |
| `GetNamespace` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetNotebookEditInfo` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetNotebookServerExtraPackages` | `Python SDK-only/未匹配 CLI` | 计费、订单、成本、配额或资源包证据 |
| `GetNotebookServerSettings` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `GetNotebookServerStat` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `GetOauth2CredentialProvider` | `id` | 身份、权限、密钥或授权证据 |
| `GetPermission` | `resourceshare` | 身份、权限、密钥或授权证据 |
| `GetPermissionPoint` | `id` | 身份、权限、密钥或授权证据 |
| `GetPolicy` | `id` | 身份、权限、密钥或授权证据 |
| `GetRealTimeStatistics` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetResourceApiKey` | `id` | 身份、权限、密钥或授权证据 |
| `GetResourceOauth2Token` | `id` | 身份、权限、密钥或授权证据 |
| `GetResourceUploadUrl` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetRoleCredentialProvider` | `id` | 身份、权限、密钥或授权证据 |
| `GetRoleCredentials` | `id` | 身份、权限、密钥或授权证据 |
| `GetRoute` | `id` | 网络路径、入口、路由或安全策略证据 |
| `GetSCIMProvisioningDefaults` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetScimProvisioningDefaults` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetService` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetServiceConnection` | `cp` | 资源存在性、状态、配置或诊断证据 |
| `GetServiceInfo` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetSmsService` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetTask` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetTaskRunLog` | `cp` | 资源存在性、状态、配置或诊断证据 |
| `GetTaskRunLogDownloadURI` | `cp` | 资源存在性、状态、配置或诊断证据 |
| `GetTaskRunLogDownloadUri` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetTaskStateUserSync` | `id` | 身份、权限、密钥或授权证据 |
| `GetTenantServiceStatus` | `id` | 资源存在性、状态、配置或诊断证据 |
| `GetTrsWorkflowInfo` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
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
| `ListAddresses` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListAgentGroups` | `Python SDK-only/未匹配 CLI` | 模型、端点、Agent 或工作空间状态证据 |
| `ListAgents` | `Python SDK-only/未匹配 CLI` | 模型、端点、Agent 或工作空间状态证据 |
| `ListApiKeyCredentialProviders` | `id` | 身份、权限、密钥或授权证据 |
| `ListClusters` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `ListClustersOfWorkspace` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `ListCollections` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListComponentStep` | `cp` | 资源存在性、状态、配置或诊断证据 |
| `ListCredentialProviders` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListDataFiles` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListDataModelRows` | `Python SDK-only/未匹配 CLI` | 模型、端点、Agent 或工作空间状态证据 |
| `ListDataModels` | `Python SDK-only/未匹配 CLI` | 模型、端点、Agent 或工作空间状态证据 |
| `ListDataSets` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListDepartmentMembers` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListDepartmentSyncJobs` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListDepartments` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListDepartmentsForUser` | `id` | 身份、权限、密钥或授权证据 |
| `ListDeployResources` | `cp` | 资源存在性、状态、配置或诊断证据 |
| `ListEmbeddings` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
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
| `ListIndexes` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListManagedAppChangeRecords` | `cp` | 资源存在性、状态、配置或诊断证据 |
| `ListManagedAppChangeSteps` | `cp` | 资源存在性、状态、配置或诊断证据 |
| `ListManagedAppPods` | `cp` | 资源状态、实例/节点/集群运行态证据 |
| `ListMergeUserSyncResultUsers` | `id` | 身份、权限、密钥或授权证据 |
| `ListNamespaces` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListNotebookServerImages` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `ListNotebookServerResourceOpts` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `ListNotebookServers` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `ListOauth2CredentialProviders` | `id` | 身份、权限、密钥或授权证据 |
| `ListOverviewSubmissions` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListPermissionPoints` | `id` | 身份、权限、密钥或授权证据 |
| `ListPermissions` | `resourceshare` | 身份、权限、密钥或授权证据 |
| `ListPipelineRuns` | `cp` | 资源存在性、状态、配置或诊断证据 |
| `ListPipelines` | `cp` | 资源存在性、状态、配置或诊断证据 |
| `ListPolicies` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListPrincipals` | `resourceshare` | 资源存在性、状态、配置或诊断证据 |
| `ListResourceShareAssociations` | `resourceshare` | 资源存在性、状态、配置或诊断证据 |
| `ListResourceSharePermissions` | `resourceshare` | 身份、权限、密钥或授权证据 |
| `ListResourceTypes` | `resourceshare` | 资源存在性、状态、配置或诊断证据 |
| `ListResources` | `cp, resourceshare` | 资源存在性、状态、配置或诊断证据 |
| `ListRoleCredentialProviders` | `id` | 身份、权限、密钥或授权证据 |
| `ListRoutes` | `id` | 网络路径、入口、路由或安全策略证据 |
| `ListRuns` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListSCIMTokens` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListScimTokens` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListServiceConnections` | `cp` | 资源存在性、状态、配置或诊断证据 |
| `ListServices` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListSubmissions` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListTagsForResources` | `id, resourceshare` | 资源存在性、状态、配置或诊断证据 |
| `ListTaskRuns` | `cp` | 资源存在性、状态、配置或诊断证据 |
| `ListTasks` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListTriggers` | `cp` | 资源存在性、状态、配置或诊断证据 |
| `ListTrustAnchors` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListUserPoolClients` | `id` | 身份、权限、密钥或授权证据 |
| `ListUserPools` | `id` | 身份、权限、密钥或授权证据 |
| `ListUsers` | `id` | 身份、权限、密钥或授权证据 |
| `ListUsersInDepartment` | `id` | 身份、权限、密钥或授权证据 |
| `ListUsersInGroup` | `id` | 身份、权限、密钥或授权证据 |
| `ListWorkflows` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListWorkloadIdentities` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListWorkloadPools` | `id` | 资源存在性、状态、配置或诊断证据 |
| `ListWorkspaceLabels` | `Python SDK-only/未匹配 CLI` | 模型、端点、Agent 或工作空间状态证据 |
| `ListWorkspaces` | `cp` | 模型、端点、Agent 或工作空间状态证据 |
| `QueryAudioRecordFileUrl` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `QueryAudioRecordToTextFileUrl` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `QueryCallCall` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `QueryCallRecordMsg` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `QueryOpenGetResource` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `QuerySubscription` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `QuerySubscriptionForList` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `QueryUsableResource` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ValidateDepartmentSyncSession` | `id` | 资源存在性、状态、配置或诊断证据 |

## 使用建议
- 优先使用章节 reference 中已经编排好的命令包；当用户问题落在未细化章节时，再从本矩阵选择最小只读 Action 补充证据。
- 如果某个只读 Action 需要分页、跨产品联动或深层字段归一，再考虑新增 `scripts/` 只读脚本，并同步更新脚本说明。
- 如果只读证据指向写操作修复，必须先输出影响面、资源 ID、回滚/恢复建议，并等待用户确认。
