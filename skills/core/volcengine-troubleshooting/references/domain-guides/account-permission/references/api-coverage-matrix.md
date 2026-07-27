# API 覆盖审查矩阵
本文件由 2026-05-22 审查生成，用于证明本 skill 已对 `cli-meta/` 中对应分类的 OpenAPI / CLI / Python SDK 能力做过覆盖盘点。它不是执行顺序清单；Agent 仍应先按主 `SKILL.md` 和章节 reference 选择最小必要证据。
## 审查口径
- 纳入排障优先级：`Describe/List/Get/Query/Check/Search/BatchGet/Verify/Validate/Test/Diagnose/Preview/Estimate` 等只读或诊断型 Action。
- 默认排除自动执行：`Create/Modify/Delete/Update/Attach/Detach/Start/Stop/Run/Invoke/Pay/Renew/Set` 等会改变资源、资金、权限或任务状态的 Action；只能作为解释错误码或 Human-in-the-Loop 建议背景。
- 命令形态：执行时统一写作 `ve <service> <Action> [--Param value...]`；参数不确定时先查 `ve <service> <Action> --help` 或对应 `cli-meta`。
- 凭证边界：只从临时环境读取 `VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、`VOLCENGINE_REGION`，不得写入配置、文档或日志。
## 总览
- 覆盖产品数：10
- 官方文档识别 OpenAPI Action 数合计：388
- 纳入排障候选的只读/诊断 Action 数：356
- 默认不自动执行的写/变更 Action 数：457
- 需人工判断语义的其它 Action 数：47

## 产品级覆盖
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

### 云身份中心
- 官方文档识别 Action 数：56
- 纳入只读/诊断 Action：24
- 排除自动执行的写/变更 Action：34
- 其它需按场景人工判断 Action：DeprovisionPermissionSet, ProvisionPermissionSet, RetryUserProvisioningEvent

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `GetExternalSAMLIdentityProvider` | `cloudidentity` | 身份、权限、密钥或授权证据 |
| `GetExternalSamlIdentityProvider` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `GetGroup` | `cloudidentity` | 资源存在性、状态、配置或诊断证据 |
| `GetPermissionSet` | `cloudidentity` | 身份、权限、密钥或授权证据 |
| `GetPortalLoginConfig` | `cloudidentity` | 资源存在性、状态、配置或诊断证据 |
| `GetSAMLServiceProvider` | `cloudidentity` | 资源存在性、状态、配置或诊断证据 |
| `GetSamlServiceProvider` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetServiceStatus` | `cloudidentity` | 资源存在性、状态、配置或诊断证据 |
| `GetTaskStatus` | `cloudidentity` | 资源存在性、状态、配置或诊断证据 |
| `GetUser` | `cloudidentity` | 身份、权限、密钥或授权证据 |
| `GetUserProvisioning` | `cloudidentity` | 身份、权限、密钥或授权证据 |
| `ListAccountAssignments` | `cloudidentity` | 资源存在性、状态、配置或诊断证据 |
| `ListGroupMembers` | `cloudidentity` | 资源存在性、状态、配置或诊断证据 |
| `ListGroups` | `cloudidentity` | 资源存在性、状态、配置或诊断证据 |
| `ListPermissionPoliciesInPermissionSet` | `cloudidentity` | 身份、权限、密钥或授权证据 |
| `ListPermissionSetProvisionings` | `cloudidentity` | 身份、权限、密钥或授权证据 |
| `ListPermissionSets` | `cloudidentity` | 身份、权限、密钥或授权证据 |
| `ListPortalLoginSettings` | `cloudidentity` | 资源存在性、状态、配置或诊断证据 |
| `ListSCIMServerCredentials` | `cloudidentity` | 资源状态、实例/节点/集群运行态证据 |
| `ListScimServerCredentials` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `ListTasks` | `cloudidentity` | 资源存在性、状态、配置或诊断证据 |
| `ListUserProvisioningEvents` | `cloudidentity` | 身份、权限、密钥或授权证据 |
| `ListUserProvisionings` | `cloudidentity` | 身份、权限、密钥或授权证据 |
| `ListUsers` | `cloudidentity` | 身份、权限、密钥或授权证据 |

### 企业组织
- 官方文档识别 Action 数：51
- 纳入只读/诊断 Action：18
- 排除自动执行的写/变更 Action：22
- 其它需按场景人工判断 Action：AcceptInvitation, AcceptQuitApplication, InviteAccount, MoveAccount, QuitOrganization, ReInviteAccount, RejectInvitation, RejectQuitApplication, RetryChangeAccountSecureContactInfo

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAccount` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAccountInvitation` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `DescribeOrganization` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `DescribeOrganizationalUnit` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `DescribeQuitApplication` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `GetAccountSecureContactInfo` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `GetServiceControlPolicy` | `organization` | 身份、权限、密钥或授权证据 |
| `GetServiceControlPolicyEnablement` | `organization` | 身份、权限、密钥或授权证据 |
| `ListAccounts` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `ListInvitations` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `ListOrganizationalUnits` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `ListOrganizationalUnitsForParent` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `ListPoliciesForTarget` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `ListServiceControlPolicies` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `ListTagResources` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `ListTagsKeys` | `organization` | 密钥、安全策略、风险或告警证据 |
| `ListTagsValues` | `organization` | 资源存在性、状态、配置或诊断证据 |
| `ListTargetsForPolicy` | `organization` | 身份、权限、密钥或授权证据 |

### 操作审计
- 官方文档识别 Action 数：7
- 纳入只读/诊断 Action：2
- 排除自动执行的写/变更 Action：5

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeTrails` | `cloudtrail20180101` | 资源存在性、状态、配置或诊断证据 |
| `LookupEvents` | `cloudtrail` | 资源存在性、状态、配置或诊断证据 |

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

### 智能体身份网关
- 官方文档识别 Action 数：0
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

### 管理控制台
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 访问控制
- 官方文档识别 Action 数：83
- 纳入只读/诊断 Action：39
- 排除自动执行的写/变更 Action：65
- 其它需按场景人工判断 Action：MoveProjectResource

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `GetAccessKeyLastUsed` | `iam` | 身份、权限、密钥或授权证据 |
| `GetAccountSummary` | `iam` | 资源存在性、状态、配置或诊断证据 |
| `GetAllowedIPAddresses` | `iam` | 资源存在性、状态、配置或诊断证据 |
| `GetAllowedIpAddresses` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetGroup` | `iam` | 资源存在性、状态、配置或诊断证据 |
| `GetLoginProfile` | `iam` | 资源存在性、状态、配置或诊断证据 |
| `GetOAuthProvider` | `iam` | 身份、权限、密钥或授权证据 |
| `GetOIDCProvider` | `iam` | 资源存在性、状态、配置或诊断证据 |
| `GetOidcProvider` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetPolicy` | `iam` | 身份、权限、密钥或授权证据 |
| `GetProject` | `iam20210801` | 资源存在性、状态、配置或诊断证据 |
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
| `ListProjectIdentities` | `iam20210801` | 资源存在性、状态、配置或诊断证据 |
| `ListProjectResources` | `iam20210801` | 资源存在性、状态、配置或诊断证据 |
| `ListProjects` | `iam20210801` | 资源存在性、状态、配置或诊断证据 |
| `ListRoles` | `iam` | 身份、权限、密钥或授权证据 |
| `ListSAMLProviderCertificates` | `iam` | 域名、证书、CDN、直播或入口链路证据 |
| `ListSAMLProviders` | `iam` | 资源存在性、状态、配置或诊断证据 |
| `ListSamlProviderCertificates` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `ListSamlProviders` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListTagsForResources` | `iam` | 资源存在性、状态、配置或诊断证据 |
| `ListUsers` | `iam` | 身份、权限、密钥或授权证据 |
| `ListUsersForGroup` | `iam` | 身份、权限、密钥或授权证据 |

### 账号相关
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

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

## 使用建议
- 优先使用章节 reference 中已经编排好的命令包；当用户问题落在未细化章节时，再从本矩阵选择最小只读 Action 补充证据。
- 如果某个只读 Action 需要分页、跨产品联动或深层字段归一，再考虑新增 `scripts/` 只读脚本，并同步更新脚本说明。
- 如果只读证据指向写操作修复，必须先输出影响面、资源 ID、回滚/恢复建议，并等待用户确认。
