# API 覆盖审查矩阵
本文件由 2026-05-22 审查生成，用于证明本 skill 已对 `cli-meta/` 中对应分类的 OpenAPI / CLI / Python SDK 能力做过覆盖盘点。它不是执行顺序清单；Agent 仍应先按主 `SKILL.md` 和章节 reference 选择最小必要证据。
## 审查口径
- 纳入排障优先级：`Describe/List/Get/Query/Check/Search/BatchGet/Verify/Validate/Test/Diagnose/Preview/Estimate` 等只读或诊断型 Action。
- 默认排除自动执行：`Create/Modify/Delete/Update/Attach/Detach/Start/Stop/Run/Invoke/Pay/Renew/Set` 等会改变资源、资金、权限或任务状态的 Action；只能作为解释错误码或 Human-in-the-Loop 建议背景。
- 命令形态：执行时统一写作 `ve <service> <Action> [--Param value...]`；参数不确定时先查 `ve <service> <Action> --help` 或对应 `cli-meta`。
- 凭证边界：只从临时环境读取 `VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、`VOLCENGINE_REGION`，不得写入配置、文档或日志。
## 总览
- 覆盖产品数：30
- 官方文档识别 OpenAPI Action 数合计：1204
- 纳入排障候选的只读/诊断 Action 数：567
- 默认不自动执行的写/变更 Action 数：1074
- 需人工判断语义的其它 Action 数：125

## 产品级覆盖
### GPU云服务器
- 官方文档识别 Action 数：3
- 纳入只读/诊断 Action：44
- 排除自动执行的写/变更 Action：73
- 其它需按场景人工判断 Action：DetectImage, RedeployDedicatedHost, RepairImage, ReportInstancesStatus, UpgradeCloudAssistants

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAutoInstallPackages` | `ecs` | 计费、订单、成本、配额或资源包证据 |
| `DescribeAvailableResource` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeCloudAssistantStatus` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeCommands` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDedicatedHostClusters` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDedicatedHostTypes` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDedicatedHosts` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDeploymentSetSupportedInstanceTypeFamily` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDeploymentSets` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeEventTypes` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeHpcClusters` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeHpcInstancePosition` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeImageSharePermission` | `ecs` | 身份、权限、密钥或授权证据 |
| `DescribeImages` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeInstanceECSTerminalUrl` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstanceEcsTerminalUrl` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstanceTypeFamilies` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstanceTypes` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstanceVncUrl` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstances` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstancesIamRoles` | `ecs` | 身份、权限、密钥或授权证据 |
| `DescribeInvocationInstances` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInvocationResults` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeInvocations` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeKeyPairs` | `ecs` | 密钥、安全策略、风险或告警证据 |
| `DescribeLaunchTemplateVersions` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeLaunchTemplates` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRegions` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeReservedInstances` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeScheduledInstanceStock` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeScheduledInstances` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeSpotAdvice` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSpotPriceHistory` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSubscriptions` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSystemEventDefaultAction` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSystemEvents` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTags` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTasks` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeUserData` | `ecs` | 身份、权限、密钥或授权证据 |
| `DescribeZones` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `GetConsoleOutput` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `GetConsoleScreenshot` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `GetScheduledInstanceLatestReleaseAt` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `ListTagsForResources` | `ecs` | 资源存在性、状态、配置或诊断证据 |

### IPv6网关
- 官方文档识别 Action 数：16
- 纳入只读/诊断 Action：33
- 排除自动执行的写/变更 Action：90
- 其它需按场景人工判断 Action：ActiveFlowLog, AssignIpv6Addresses, AssignPrivateIpAddresses, AuthorizeSecurityGroupEgress, AuthorizeSecurityGroupIngress, ConvertEipAddressBillingType, DeactiveFlowLog, TemporaryUpgradeEipAddress, UnassignIpv6Addresses, UnassignPrivateIpAddresses

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeBandwidthPackages` | `vpc` | 计费、订单、成本、配额或资源包证据 |
| `DescribeEipAddressAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeEipAddresses` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeFlowLogs` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeHaVips` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeInstanceGroups` | `vpc` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeIpAddressPoolAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpAddressPoolCidrBlocks` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpAddressPools` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpv6AddressBandwidthAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpv6AddressBandwidths` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpv6EgressOnlyRules` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpv6GatewayAttribute` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpv6Gateways` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNetworkAclAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNetworkAcls` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNetworkInterfaceAttributes` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeNetworkInterfaces` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribePrefixListAssociations` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribePrefixListEntries` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribePrefixLists` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRouteEntryList` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeRouteTableList` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeSecurityGroupAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeSecurityGroups` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeSubnetAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeSubnets` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTrafficMirrorFilters` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTrafficMirrorSessions` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTrafficMirrorTargets` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeVpcAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeVpcs` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `ListTagsForResources` | `vpc` | 资源存在性、状态、配置或诊断证据 |

### NAT网关
- 官方文档识别 Action 数：36
- 纳入只读/诊断 Action：11
- 排除自动执行的写/变更 Action：17

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeDnatEntries` | `natgateway` | 网络路径、入口、路由或安全策略证据 |
| `DescribeDnatEntryAttributes` | `natgateway` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNatGatewayAttributes` | `natgateway` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNatGateways` | `natgateway` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNatIpAttributes` | `natgateway` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNatIpLimitRules` | `natgateway` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNatIps` | `natgateway` | 网络路径、入口、路由或安全策略证据 |
| `DescribeSnatEntries` | `natgateway` | 网络路径、入口、路由或安全策略证据 |
| `DescribeSnatEntryAttributes` | `natgateway` | 网络路径、入口、路由或安全策略证据 |
| `ListNatGatewayAvailableZones` | `natgateway` | 网络路径、入口、路由或安全策略证据 |
| `ListTagsForResources` | `natgateway` | 资源存在性、状态、配置或诊断证据 |

### VPN连接
- 官方文档识别 Action 数：41
- 纳入只读/诊断 Action：12
- 排除自动执行的写/变更 Action：24

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeCustomerGatewayAttributes` | `vpn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeCustomerGateways` | `vpn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSslVpnClientCertAttributes` | `vpn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeSslVpnClientCerts` | `vpn` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeSslVpnServers` | `vpn` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeVpnConnectionAttributes` | `vpn` | 网络路径、入口、路由或安全策略证据 |
| `DescribeVpnConnections` | `vpn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeVpnGatewayAttributes` | `vpn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeVpnGatewayRouteAttributes` | `vpn` | 网络路径、入口、路由或安全策略证据 |
| `DescribeVpnGatewayRoutes` | `vpn` | 网络路径、入口、路由或安全策略证据 |
| `DescribeVpnGateways` | `vpn` | 资源存在性、状态、配置或诊断证据 |
| `DescribeVpnGatewaysBilling` | `vpn` | 计费、订单、成本、配额或资源包证据 |

### veStack全栈版
- 官方文档识别 Action 数：2
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 专线连接
- 官方文档识别 Action 数：75
- 纳入只读/诊断 Action：16
- 排除自动执行的写/变更 Action：28
- 其它需按场景人工判断 Action：ApplyDirectConnectConnectionLoa, ConfirmDirectConnectVirtualInterface

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeBgpPeerAttributes` | `directconnect` | 资源存在性、状态、配置或诊断证据 |
| `DescribeBgpPeers` | `directconnect` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDirectConnectAccessPoints` | `directconnect` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDirectConnectConnectionAttributes` | `directconnect` | 网络路径、入口、路由或安全策略证据 |
| `DescribeDirectConnectConnectionLoaAttributes` | `directconnect` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDirectConnectConnections` | `directconnect` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDirectConnectGatewayAttributes` | `directconnect` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDirectConnectGatewayRouteAttributes` | `directconnect` | 网络路径、入口、路由或安全策略证据 |
| `DescribeDirectConnectGatewayRoutes` | `directconnect` | 网络路径、入口、路由或安全策略证据 |
| `DescribeDirectConnectGateways` | `directconnect` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDirectConnectTrafficQosPolicies` | `directconnect` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDirectConnectTrafficQosQueues` | `directconnect` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDirectConnectTrafficQosRules` | `directconnect` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDirectConnectVirtualInterfaceAttributes` | `directconnect` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDirectConnectVirtualInterfaces` | `directconnect` | 资源存在性、状态、配置或诊断证据 |
| `ListTagsForResources` | `directconnect` | 资源存在性、状态、配置或诊断证据 |

### 中转路由器
- 官方文档识别 Action 数：123
- 纳入只读/诊断 Action：26
- 排除自动执行的写/变更 Action：75
- 其它需按场景人工判断 Action：DissociateTransitRouterAttachmentFromRouteTable, DissociateTransitRouterForwardPolicyTableFromAttachment, DissociateTransitRouterMulticastDomain, DissociateTransitRouterRoutePolicyFromRouteTable, DissociateTransitRouterTrafficQosMarkingPolicyFromAttachment, DissociateTransitRouterTrafficQosQueuePolicyFromAttachment

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeTransitRouterAttachments` | `transitrouter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTransitRouterBandwidthPackages` | `transitrouter` | 计费、订单、成本、配额或资源包证据 |
| `DescribeTransitRouterBandwidthPackagesBilling` | `transitrouter` | 计费、订单、成本、配额或资源包证据 |
| `DescribeTransitRouterDirectConnectGatewayAttachments` | `transitrouter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTransitRouterFlowLogs` | `transitrouter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTransitRouterForwardPolicyEntries` | `transitrouter` | 身份、权限、密钥或授权证据 |
| `DescribeTransitRouterForwardPolicyTables` | `transitrouter` | 身份、权限、密钥或授权证据 |
| `DescribeTransitRouterMulticastDomainAssociations` | `transitrouter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTransitRouterMulticastDomains` | `transitrouter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTransitRouterMulticastGroups` | `transitrouter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTransitRouterPeerAttachments` | `transitrouter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTransitRouterRegions` | `transitrouter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTransitRouterRouteEntries` | `transitrouter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTransitRouterRoutePolicyEntries` | `transitrouter` | 身份、权限、密钥或授权证据 |
| `DescribeTransitRouterRoutePolicyTables` | `transitrouter` | 身份、权限、密钥或授权证据 |
| `DescribeTransitRouterRouteTableAssociations` | `transitrouter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTransitRouterRouteTablePropagations` | `transitrouter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTransitRouterRouteTables` | `transitrouter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTransitRouterTrafficQosMarkingEntries` | `transitrouter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTransitRouterTrafficQosMarkingPolicies` | `transitrouter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTransitRouterTrafficQosQueueEntries` | `transitrouter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTransitRouterTrafficQosQueuePolicies` | `transitrouter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTransitRouterVpcAttachments` | `transitrouter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTransitRouterVpnAttachments` | `transitrouter` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTransitRouters` | `transitrouter` | 网络路径、入口、路由或安全策略证据 |
| `ListTagsForResources` | `transitrouter` | 资源存在性、状态、配置或诊断证据 |

### 云企业网
- 官方文档识别 Action 数：45
- 纳入只读/诊断 Action：15
- 排除自动执行的写/变更 Action：25
- 其它需按场景人工判断 Action：PublishCenRouteEntry, WithdrawCenRouteEntry

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeCenAttachedInstanceAttributes` | `cen` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeCenAttachedInstances` | `cen` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeCenAttributes` | `cen` | 网络路径、入口、路由或安全策略证据 |
| `DescribeCenBandwidthPackageAttributes` | `cen` | 计费、订单、成本、配额或资源包证据 |
| `DescribeCenBandwidthPackages` | `cen` | 计费、订单、成本、配额或资源包证据 |
| `DescribeCenBandwidthPackagesBilling` | `cen` | 计费、订单、成本、配额或资源包证据 |
| `DescribeCenInterRegionBandwidthAttributes` | `cen` | 网络路径、入口、路由或安全策略证据 |
| `DescribeCenInterRegionBandwidths` | `cen` | 网络路径、入口、路由或安全策略证据 |
| `DescribeCenRouteEntries` | `cen` | 网络路径、入口、路由或安全策略证据 |
| `DescribeCenServiceRouteEntries` | `cen` | 网络路径、入口、路由或安全策略证据 |
| `DescribeCenSummaryRouteEntries` | `cen` | 网络路径、入口、路由或安全策略证据 |
| `DescribeCens` | `cen` | 资源存在性、状态、配置或诊断证据 |
| `DescribeGrantRulesToCen` | `cen` | 资源存在性、状态、配置或诊断证据 |
| `DescribeInstanceGrantedRules` | `cen` | 资源状态、实例/节点/集群运行态证据 |
| `ListTagsForResources` | `cen` | 资源存在性、状态、配置或诊断证据 |

### 云原生消息引擎
- 官方文档识别 Action 数：47
- 纳入只读/诊断 Action：25
- 排除自动执行的写/变更 Action：17
- 其它需按场景人工判断 Action：GroupExist, RefreshDeviceCredential, RegisterDeviceCredential, ScaleDownInstance, ScaleUpTopic, TopicExist, UnRegisterDeviceCredential

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAvailableZones` | `bmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDeviceCredential` | `bmq20240901` | 资源存在性、状态、配置或诊断证据 |
| `DescribeGroup` | `bmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeGroupsInTopic` | `bmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeInstance` | `bmq` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstanceResourceStat` | `bmq` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeMQTTClients` | `bmq20240901` | 资源存在性、状态、配置或诊断证据 |
| `DescribeMqttClients` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribePartitionsInTopic` | `bmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSubscription` | `bmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTopic` | `bmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTopicTimeRange` | `bmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTopicsInGroup` | `bmq` | 资源存在性、状态、配置或诊断证据 |
| `ListAvailableSecurityGroupsForBMQ` | `bmq` | 网络路径、入口、路由或安全策略证据 |
| `ListAvailableSecurityGroupsForBmq` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |
| `ListAvailableSubnetsForBMQ` | `bmq` | 网络路径、入口、路由或安全策略证据 |
| `ListAvailableSubnetsForBmq` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |
| `ListAvailableVPCForBMQ` | `bmq` | 网络路径、入口、路由或安全策略证据 |
| `ListAvailableVpcForBmq` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |
| `ListInstanceResourceStats` | `bmq` | 资源状态、实例/节点/集群运行态证据 |
| `ListSpecifications` | `bmq` | 资源存在性、状态、配置或诊断证据 |
| `PreviewTopicData` | `bmq` | 资源存在性、状态、配置或诊断证据 |
| `SearchGroups` | `bmq` | 资源存在性、状态、配置或诊断证据 |
| `SearchInstances` | `bmq` | 资源状态、实例/节点/集群运行态证据 |
| `SearchTopics` | `bmq` | 资源存在性、状态、配置或诊断证据 |

### 云手机
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：32
- 排除自动执行的写/变更 Action：57
- 其它需按场景人工判断 Action：AutoInstallApp, BackupData, BackupPod, BanUser, BatchScreenShot, BuildAOSPImage, BuildAospImage, DetailApp, DetailDNSRule, DetailDisplayLayoutMini, DetailDnsRule, DetailHost, DetailPod, DetailPortMappingRule, LaunchApp, LaunchApps, MigratePod, PodAdb, PodDataDelete, PodMute ...

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `GetAppCrashLog` | `acep` | 资源存在性、状态、配置或诊断证据 |
| `GetDcBandwidthDailyPeak` | `acep` | 网络路径、入口、路由或安全策略证据 |
| `GetImagePreheating` | `acep` | 资源存在性、状态、配置或诊断证据 |
| `GetPhoneTemplate` | `acep` | 资源存在性、状态、配置或诊断证据 |
| `GetPodAppList` | `acep` | 资源状态、实例/节点/集群运行态证据 |
| `GetPodMetric` | `acep` | 资源状态、实例/节点/集群运行态证据 |
| `GetPodProperty` | `acep` | 资源状态、实例/节点/集群运行态证据 |
| `GetPreSignedEdgeURL` | `acep` | 资源存在性、状态、配置或诊断证据 |
| `GetPreSignedEdgeUrl` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetProductResource` | `acep` | 资源存在性、状态、配置或诊断证据 |
| `GetProxy` | `acep` | 资源存在性、状态、配置或诊断证据 |
| `GetTaskInfo` | `acep` | 资源存在性、状态、配置或诊断证据 |
| `ListAOSPImage` | `acep` | 资源存在性、状态、配置或诊断证据 |
| `ListAospImage` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListApp` | `acep` | 资源存在性、状态、配置或诊断证据 |
| `ListAppVersionDeploy` | `acep` | 资源存在性、状态、配置或诊断证据 |
| `ListBackupData` | `acep` | 存储、备份或数据库控制面证据 |
| `ListConfiguration` | `acep` | 资源存在性、状态、配置或诊断证据 |
| `ListCustomRoute` | `acep` | 网络路径、入口、路由或安全策略证据 |
| `ListDNSRule` | `acep` | 域名、证书、CDN、直播或入口链路证据 |
| `ListDc` | `acep` | 资源存在性、状态、配置或诊断证据 |
| `ListDisplayLayoutMini` | `acep` | 资源存在性、状态、配置或诊断证据 |
| `ListDnsRule` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `ListHost` | `acep` | 资源存在性、状态、配置或诊断证据 |
| `ListImageResource` | `acep` | 资源存在性、状态、配置或诊断证据 |
| `ListPhoneTemplate` | `acep` | 资源存在性、状态、配置或诊断证据 |
| `ListPod` | `acep` | 资源状态、实例/节点/集群运行态证据 |
| `ListPodResource` | `acep` | 资源状态、实例/节点/集群运行态证据 |
| `ListPodResourceSet` | `acep` | 资源状态、实例/节点/集群运行态证据 |
| `ListPortMappingRule` | `acep` | 资源存在性、状态、配置或诊断证据 |
| `ListTag` | `acep` | 资源存在性、状态、配置或诊断证据 |
| `ListTask` | `acep` | 资源存在性、状态、配置或诊断证据 |

### 云服务器
- 官方文档识别 Action 数：187
- 纳入只读/诊断 Action：44
- 排除自动执行的写/变更 Action：73
- 其它需按场景人工判断 Action：DetectImage, RedeployDedicatedHost, RepairImage, ReportInstancesStatus, UpgradeCloudAssistants

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAutoInstallPackages` | `ecs` | 计费、订单、成本、配额或资源包证据 |
| `DescribeAvailableResource` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeCloudAssistantStatus` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeCommands` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDedicatedHostClusters` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDedicatedHostTypes` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDedicatedHosts` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeDeploymentSetSupportedInstanceTypeFamily` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDeploymentSets` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeEventTypes` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeHpcClusters` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeHpcInstancePosition` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeImageSharePermission` | `ecs` | 身份、权限、密钥或授权证据 |
| `DescribeImages` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeInstanceECSTerminalUrl` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstanceEcsTerminalUrl` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstanceTypeFamilies` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstanceTypes` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstanceVncUrl` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstances` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstancesIamRoles` | `ecs` | 身份、权限、密钥或授权证据 |
| `DescribeInvocationInstances` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInvocationResults` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeInvocations` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeKeyPairs` | `ecs` | 密钥、安全策略、风险或告警证据 |
| `DescribeLaunchTemplateVersions` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeLaunchTemplates` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRegions` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeReservedInstances` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeScheduledInstanceStock` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeScheduledInstances` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeSpotAdvice` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSpotPriceHistory` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSubscriptions` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSystemEventDefaultAction` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSystemEvents` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTags` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTasks` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `DescribeUserData` | `ecs` | 身份、权限、密钥或授权证据 |
| `DescribeZones` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `GetConsoleOutput` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `GetConsoleScreenshot` | `ecs` | 资源存在性、状态、配置或诊断证据 |
| `GetScheduledInstanceLatestReleaseAt` | `ecs` | 资源状态、实例/节点/集群运行态证据 |
| `ListTagsForResources` | `ecs` | 资源存在性、状态、配置或诊断证据 |

### 云连接器
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 公网IP
- 官方文档识别 Action 数：23
- 纳入只读/诊断 Action：33
- 排除自动执行的写/变更 Action：90
- 其它需按场景人工判断 Action：ActiveFlowLog, AssignIpv6Addresses, AssignPrivateIpAddresses, AuthorizeSecurityGroupEgress, AuthorizeSecurityGroupIngress, ConvertEipAddressBillingType, DeactiveFlowLog, TemporaryUpgradeEipAddress, UnassignIpv6Addresses, UnassignPrivateIpAddresses

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeBandwidthPackages` | `vpc` | 计费、订单、成本、配额或资源包证据 |
| `DescribeEipAddressAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeEipAddresses` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeFlowLogs` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeHaVips` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeInstanceGroups` | `vpc` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeIpAddressPoolAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpAddressPoolCidrBlocks` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpAddressPools` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpv6AddressBandwidthAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpv6AddressBandwidths` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpv6EgressOnlyRules` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpv6GatewayAttribute` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpv6Gateways` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNetworkAclAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNetworkAcls` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNetworkInterfaceAttributes` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeNetworkInterfaces` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribePrefixListAssociations` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribePrefixListEntries` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribePrefixLists` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRouteEntryList` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeRouteTableList` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeSecurityGroupAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeSecurityGroups` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeSubnetAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeSubnets` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTrafficMirrorFilters` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTrafficMirrorSessions` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTrafficMirrorTargets` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeVpcAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeVpcs` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `ListTagsForResources` | `vpc` | 资源存在性、状态、配置或诊断证据 |

### 共享带宽包
- 官方文档识别 Action 数：12
- 纳入只读/诊断 Action：33
- 排除自动执行的写/变更 Action：90
- 其它需按场景人工判断 Action：ActiveFlowLog, AssignIpv6Addresses, AssignPrivateIpAddresses, AuthorizeSecurityGroupEgress, AuthorizeSecurityGroupIngress, ConvertEipAddressBillingType, DeactiveFlowLog, TemporaryUpgradeEipAddress, UnassignIpv6Addresses, UnassignPrivateIpAddresses

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeBandwidthPackages` | `vpc` | 计费、订单、成本、配额或资源包证据 |
| `DescribeEipAddressAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeEipAddresses` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeFlowLogs` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeHaVips` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeInstanceGroups` | `vpc` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeIpAddressPoolAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpAddressPoolCidrBlocks` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpAddressPools` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpv6AddressBandwidthAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpv6AddressBandwidths` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpv6EgressOnlyRules` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpv6GatewayAttribute` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpv6Gateways` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNetworkAclAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNetworkAcls` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNetworkInterfaceAttributes` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeNetworkInterfaces` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribePrefixListAssociations` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribePrefixListEntries` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribePrefixLists` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRouteEntryList` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeRouteTableList` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeSecurityGroupAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeSecurityGroups` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeSubnetAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeSubnets` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTrafficMirrorFilters` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTrafficMirrorSessions` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTrafficMirrorTargets` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeVpcAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeVpcs` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `ListTagsForResources` | `vpc` | 资源存在性、状态、配置或诊断证据 |

### 共享流量包
- 官方文档识别 Action 数：0
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 函数服务
- 官方文档识别 Action 数：7
- 纳入只读/诊断 Action：32
- 排除自动执行的写/变更 Action：26
- 其它需按场景人工判断 Action：AbortRelease, GenWebshellEndpoint, KillSandbox, PauseSandbox, PrecacheSandboxImages, TransitionSandbox, UpsertSecretToken, WriteFiles

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeSandbox` | `vefaas, vefaasdev` | 存储、备份或数据库控制面证据 |
| `GetAvailabilityZones` | `vefaas, vefaasdev` | 资源存在性、状态、配置或诊断证据 |
| `GetCodeUploadAddress` | `vefaas` | 资源存在性、状态、配置或诊断证据 |
| `GetDependencyInstallTaskLogDownloadURI` | `vefaas` | 资源存在性、状态、配置或诊断证据 |
| `GetDependencyInstallTaskLogDownloadUri` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetDependencyInstallTaskStatus` | `vefaas` | 资源存在性、状态、配置或诊断证据 |
| `GetFunction` | `vefaas, vefaasdev` | 资源存在性、状态、配置或诊断证据 |
| `GetFunctionInstanceLogs` | `vefaas, vefaasdev` | 资源状态、实例/节点/集群运行态证据 |
| `GetFunctionResource` | `vefaas` | 资源存在性、状态、配置或诊断证据 |
| `GetImageSyncStatus` | `vefaas` | 资源存在性、状态、配置或诊断证据 |
| `GetKafkaTrigger` | `vefaas` | 资源存在性、状态、配置或诊断证据 |
| `GetPublicSandboxImageGroups` | `vefaas` | 存储、备份或数据库控制面证据 |
| `GetReleaseStatus` | `vefaas, vefaasdev` | 资源存在性、状态、配置或诊断证据 |
| `GetRevision` | `vefaas, vefaasdev` | 资源存在性、状态、配置或诊断证据 |
| `GetRocketMQTrigger` | `vefaas` | 资源存在性、状态、配置或诊断证据 |
| `GetRocketMqTrigger` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `GetSandboxImagePrecacheTicket` | `vefaas` | 存储、备份或数据库控制面证据 |
| `GetTimer` | `vefaas` | 资源存在性、状态、配置或诊断证据 |
| `ListAsyncTasks` | `vefaas` | 资源存在性、状态、配置或诊断证据 |
| `ListE2BAPIKeys` | `vefaas` | 身份、权限、密钥或授权证据 |
| `ListE2BapiKeys` | `Python SDK-only/未匹配 CLI` | 身份、权限、密钥或授权证据 |
| `ListFunctionElasticScaleStrategy` | `vefaas` | 资源存在性、状态、配置或诊断证据 |
| `ListFunctionInstances` | `vefaas, vefaasdev` | 资源状态、实例/节点/集群运行态证据 |
| `ListFunctions` | `vefaas, vefaasdev` | 资源存在性、状态、配置或诊断证据 |
| `ListReleaseRecords` | `vefaas, vefaasdev` | 资源存在性、状态、配置或诊断证据 |
| `ListRevisions` | `vefaas, vefaasdev` | 资源存在性、状态、配置或诊断证据 |
| `ListSandboxImagePrecacheTickets` | `vefaas` | 存储、备份或数据库控制面证据 |
| `ListSandboxImages` | `vefaas` | 存储、备份或数据库控制面证据 |
| `ListSandboxes` | `vefaas, vefaasdev` | 存储、备份或数据库控制面证据 |
| `ListTriggers` | `vefaas` | 资源存在性、状态、配置或诊断证据 |
| `QueryUserCrVpcTunnel` | `vefaas` | 身份、权限、密钥或授权证据 |
| `ReadFiles` | `vefaasdev` | 资源存在性、状态、配置或诊断证据 |

### 容器服务
- 官方文档识别 Action 数：62
- 纳入只读/诊断 Action：19
- 排除自动执行的写/变更 Action：27
- 其它需按场景人工判断 Action：ExecContainerImageCommitment, ForwardKubernetesApi

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeContainerImageCommitments` | `vke` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSnapshots` | `vke` | 资源存在性、状态、配置或诊断证据 |
| `GetGlobalDefaultDeleteOption` | `vke` | 资源存在性、状态、配置或诊断证据 |
| `ListAddons` | `vke` | 资源存在性、状态、配置或诊断证据 |
| `ListClusters` | `vke` | 资源状态、实例/节点/集群运行态证据 |
| `ListInstanceTypeLabels` | `vke` | 资源状态、实例/节点/集群运行态证据 |
| `ListKubeconfigs` | `vke` | 资源存在性、状态、配置或诊断证据 |
| `ListNodePools` | `vke` | 资源状态、实例/节点/集群运行态证据 |
| `ListNodes` | `vke` | 资源状态、实例/节点/集群运行态证据 |
| `ListPermissions` | `vke` | 身份、权限、密钥或授权证据 |
| `ListRemedyConfigs` | `vke` | 资源存在性、状态、配置或诊断证据 |
| `ListScalingEvents` | `vke` | 资源存在性、状态、配置或诊断证据 |
| `ListScalingPolicies` | `vke` | 资源存在性、状态、配置或诊断证据 |
| `ListSupportedAddInstanceTypes` | `vke` | 资源状态、实例/节点/集群运行态证据 |
| `ListSupportedAddons` | `vke` | 资源存在性、状态、配置或诊断证据 |
| `ListSupportedGpuDriverVersions` | `vke` | 资源存在性、状态、配置或诊断证据 |
| `ListSupportedImages` | `vke` | 资源存在性、状态、配置或诊断证据 |
| `ListSupportedResourceTypes` | `vke` | 资源存在性、状态、配置或诊断证据 |
| `ListTagsForResources` | `vke` | 资源存在性、状态、配置或诊断证据 |

### 弹性伸缩
- 官方文档识别 Action 数：45
- 纳入只读/诊断 Action：9
- 排除自动执行的写/变更 Action：29
- 其它需按场景人工判断 Action：CompleteLifecycleActivity, EnterStandby, ExitStandby, SuspendProcesses

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeLifecycleActivities` | `autoscaling` | 资源存在性、状态、配置或诊断证据 |
| `DescribeLifecycleHooks` | `autoscaling` | 资源存在性、状态、配置或诊断证据 |
| `DescribeNotificationConfigurations` | `autoscaling` | 资源存在性、状态、配置或诊断证据 |
| `DescribeScalingActivities` | `autoscaling` | 资源存在性、状态、配置或诊断证据 |
| `DescribeScalingConfigurations` | `autoscaling` | 资源存在性、状态、配置或诊断证据 |
| `DescribeScalingGroups` | `autoscaling` | 资源存在性、状态、配置或诊断证据 |
| `DescribeScalingInstances` | `autoscaling` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeScalingPolicies` | `autoscaling` | 资源存在性、状态、配置或诊断证据 |
| `ListTagResources` | `autoscaling` | 资源存在性、状态、配置或诊断证据 |

### 微服务引擎
- 官方文档识别 Action 数：11
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 持续交付
- 官方文档识别 Action 数：3
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 服务器迁移中心
- 官方文档识别 Action 数：14
- 纳入只读/诊断 Action：4
- 排除自动执行的写/变更 Action：8
- 其它需按场景人工判断 Action：TriggerLastIncrementalSync

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeMigrationJobs` | `smc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeMigrationLogs` | `smc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeMigrationSources` | `smc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeMigrationSystemSupportTypes` | `smc` | 资源存在性、状态、配置或诊断证据 |

### 消息队列 Kafka版
- 官方文档识别 Action 数：56
- 纳入只读/诊断 Action：19
- 排除自动执行的写/变更 Action：33
- 其它需按场景人工判断 Action：PublishPrivateDomainToPublic

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAcls` | `kafka` | 网络路径、入口、路由或安全策略证据 |
| `DescribeAllowListDetail` | `kafka` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAllowLists` | `kafka` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAvailabilityZones` | `kafka` | 资源存在性、状态、配置或诊断证据 |
| `DescribeConsumedPartitions` | `kafka` | 资源存在性、状态、配置或诊断证据 |
| `DescribeConsumedTopics` | `kafka` | 资源存在性、状态、配置或诊断证据 |
| `DescribeGroups` | `kafka` | 资源存在性、状态、配置或诊断证据 |
| `DescribeInstanceDetail` | `kafka` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstances` | `kafka` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeRegions` | `kafka` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTagsByResource` | `kafka` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTopicAccessPolicies` | `kafka` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTopicParameters` | `kafka` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTopicPartitions` | `kafka` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTopics` | `kafka` | 资源存在性、状态、配置或诊断证据 |
| `DescribeUsers` | `kafka` | 身份、权限、密钥或授权证据 |
| `QueryMessageByOffsets` | `kafka` | 资源存在性、状态、配置或诊断证据 |
| `QueryMessageByTimestamp` | `kafka` | 资源存在性、状态、配置或诊断证据 |
| `VerifyMigrateSubTasks` | `kafka` | 资源存在性、状态、配置或诊断证据 |

### 消息队列 RabbitMQ版
- 官方文档识别 Action 数：27
- 纳入只读/诊断 Action：9
- 排除自动执行的写/变更 Action：16
- 其它需按场景人工判断 Action：RestartInstance

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAllowListDetail` | `rabbitmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAllowLists` | `rabbitmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAvailabilityZones` | `rabbitmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeInstanceConfigs` | `rabbitmq` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstanceDetail` | `rabbitmq` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstances` | `rabbitmq` | 资源状态、实例/节点/集群运行态证据 |
| `DescribePlugins` | `rabbitmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRegions` | `rabbitmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTagsByResource` | `rabbitmq` | 资源存在性、状态、配置或诊断证据 |

### 消息队列 RocketMQ版
- 官方文档识别 Action 数：68
- 纳入只读/诊断 Action：33
- 排除自动执行的写/变更 Action：39
- 其它需按场景人工判断 Action：ManualProcessResult, ManualTriggerInspect, MessageSend, ResendDLQMessageById, ResendDlqMessageById

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAccessKeyDetail` | `rocketmq` | 身份、权限、密钥或授权证据 |
| `DescribeAccessKeys` | `rocketmq` | 身份、权限、密钥或授权证据 |
| `DescribeAllowListDetail` | `rocketmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAllowLists` | `rocketmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeAvailabilityZones` | `rocketmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeConsumedClients` | `rocketmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeConsumedTopicDetail` | `rocketmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeConsumedTopics` | `rocketmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeGroups` | `rocketmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeGroupsDetail` | `rocketmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeInstanceDetail` | `rocketmq` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeInstances` | `rocketmq` | 资源状态、实例/节点/集群运行态证据 |
| `DescribePLWhitelist` | `rocketmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribePlWhitelist` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRegions` | `rocketmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeSecretKey` | `rocketmq` | 密钥、安全策略、风险或告警证据 |
| `DescribeTagsByResource` | `rocketmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTopicAccessPolicies` | `rocketmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTopicDetail` | `rocketmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTopicGroups` | `rocketmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTopicQueue` | `rocketmq` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTopics` | `rocketmq` | 资源存在性、状态、配置或诊断证据 |
| `GetInspectConfig` | `rocketmq` | 资源存在性、状态、配置或诊断证据 |
| `GetInstanceInspectResult` | `rocketmq` | 资源状态、实例/节点/集群运行态证据 |
| `QueryDLQMessageByGroupId` | `rocketmq` | 资源存在性、状态、配置或诊断证据 |
| `QueryDLQMessageById` | `rocketmq` | 资源存在性、状态、配置或诊断证据 |
| `QueryDlqMessageByGroupId` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `QueryDlqMessageById` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `QueryMessageByMsgId` | `rocketmq` | 资源存在性、状态、配置或诊断证据 |
| `QueryMessageByMsgKey` | `rocketmq` | 密钥、安全策略、风险或告警证据 |
| `QueryMessageByOffset` | `rocketmq` | 资源存在性、状态、配置或诊断证据 |
| `QueryMessageByTimestamp` | `rocketmq` | 资源存在性、状态、配置或诊断证据 |
| `QueryMessageTraceByMessageId` | `rocketmq` | 资源存在性、状态、配置或诊断证据 |

### 私有网络
- 官方文档识别 Action 数：107
- 纳入只读/诊断 Action：33
- 排除自动执行的写/变更 Action：90
- 其它需按场景人工判断 Action：ActiveFlowLog, AssignIpv6Addresses, AssignPrivateIpAddresses, AuthorizeSecurityGroupEgress, AuthorizeSecurityGroupIngress, ConvertEipAddressBillingType, DeactiveFlowLog, TemporaryUpgradeEipAddress, UnassignIpv6Addresses, UnassignPrivateIpAddresses

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeBandwidthPackages` | `vpc` | 计费、订单、成本、配额或资源包证据 |
| `DescribeEipAddressAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeEipAddresses` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeFlowLogs` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeHaVips` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeInstanceGroups` | `vpc` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeIpAddressPoolAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpAddressPoolCidrBlocks` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpAddressPools` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpv6AddressBandwidthAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpv6AddressBandwidths` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpv6EgressOnlyRules` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpv6GatewayAttribute` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeIpv6Gateways` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNetworkAclAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNetworkAcls` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNetworkInterfaceAttributes` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeNetworkInterfaces` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribePrefixListAssociations` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribePrefixListEntries` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribePrefixLists` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRouteEntryList` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeRouteTableList` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeSecurityGroupAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeSecurityGroups` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeSubnetAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeSubnets` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeTrafficMirrorFilters` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTrafficMirrorSessions` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeTrafficMirrorTargets` | `vpc` | 资源存在性、状态、配置或诊断证据 |
| `DescribeVpcAttributes` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `DescribeVpcs` | `vpc` | 网络路径、入口、路由或安全策略证据 |
| `ListTagsForResources` | `vpc` | 资源存在性、状态、配置或诊断证据 |

### 私网连接
- 官方文档识别 Action 数：59
- 纳入只读/诊断 Action：23
- 排除自动执行的写/变更 Action：34
- 其它需按场景人工判断 Action：AssignPrivateIpAddressesToVpcLink, UnAssignPrivateIpAddressesFromVpcLink

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribePrivateLinkAvailableZones` | `privatelink` | 资源存在性、状态、配置或诊断证据 |
| `DescribePrivateLinkGatewayAttributes` | `privatelink` | 资源存在性、状态、配置或诊断证据 |
| `DescribePrivateLinkGatewayAvailableZones` | `privatelink` | 资源存在性、状态、配置或诊断证据 |
| `DescribePrivateLinkGatewaySecurityGroups` | `privatelink` | 网络路径、入口、路由或安全策略证据 |
| `DescribePrivateLinkGateways` | `privatelink` | 资源存在性、状态、配置或诊断证据 |
| `DescribeVpcEndpointAttributes` | `privatelink` | 网络路径、入口、路由或安全策略证据 |
| `DescribeVpcEndpointConnections` | `privatelink` | 网络路径、入口、路由或安全策略证据 |
| `DescribeVpcEndpointSecurityGroups` | `privatelink` | 网络路径、入口、路由或安全策略证据 |
| `DescribeVpcEndpointServiceAttributes` | `privatelink` | 网络路径、入口、路由或安全策略证据 |
| `DescribeVpcEndpointServicePermissions` | `privatelink` | 身份、权限、密钥或授权证据 |
| `DescribeVpcEndpointServiceResources` | `privatelink` | 网络路径、入口、路由或安全策略证据 |
| `DescribeVpcEndpointServices` | `privatelink` | 网络路径、入口、路由或安全策略证据 |
| `DescribeVpcEndpointServicesByEndUser` | `privatelink` | 身份、权限、密钥或授权证据 |
| `DescribeVpcEndpointZones` | `privatelink` | 网络路径、入口、路由或安全策略证据 |
| `DescribeVpcEndpoints` | `privatelink` | 网络路径、入口、路由或安全策略证据 |
| `DescribeVpcGatewayEndpointAttributes` | `privatelink` | 网络路径、入口、路由或安全策略证据 |
| `DescribeVpcGatewayEndpointServices` | `privatelink` | 网络路径、入口、路由或安全策略证据 |
| `DescribeVpcGatewayEndpoints` | `privatelink` | 网络路径、入口、路由或安全策略证据 |
| `DescribeVpcLinkAttributes` | `privatelink` | 网络路径、入口、路由或安全策略证据 |
| `DescribeVpcLinks` | `privatelink` | 网络路径、入口、路由或安全策略证据 |
| `ListTagsForResources` | `privatelink` | 资源存在性、状态、配置或诊断证据 |
| `VerifyVpcEndpointServicePrivateDNS` | `privatelink` | 网络路径、入口、路由或安全策略证据 |
| `VerifyVpcEndpointServicePrivateDns` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |

### 网络介绍
- 官方文档识别 Action 数：1
- 纳入只读/诊断 Action：0
- 排除自动执行的写/变更 Action：0

当前未在 CLI/SDK 元数据中识别到只读/诊断 Action；排障时依赖产品文档、专用工具或横向 skill。

### 网络智能中心
- 官方文档识别 Action 数：13
- 纳入只读/诊断 Action：6
- 排除自动执行的写/变更 Action：4
- 其它需按场景人工判断 Action：ReanalysisPath

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeDiagnosisInstanceDetail` | `na` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeDiagnosisInstances` | `na` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeHistoryDiagnosis` | `na` | 资源存在性、状态、配置或诊断证据 |
| `GetAnalysisPathReport` | `na` | 资源存在性、状态、配置或诊断证据 |
| `GetNetworkTrafficMetrics` | `na` | 资源存在性、状态、配置或诊断证据 |
| `GetNetworkTrafficTopN` | `na` | 资源存在性、状态、配置或诊断证据 |

### 负载均衡
- 官方文档识别 Action 数：115
- 纳入只读/诊断 Action：47
- 排除自动执行的写/变更 Action：95
- 其它需按场景人工判断 Action：CloneLoadBalancer, ConvertLoadBalancerBillingType, LoadBalancerJoinSecurityGroup, LoadBalancerLeaveSecurityGroup

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `DescribeAclAttributes` | `alb, clb` | 网络路径、入口、路由或安全策略证据 |
| `DescribeAcls` | `alb, clb` | 网络路径、入口、路由或安全策略证据 |
| `DescribeAllCertificates` | `alb` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeCACertificates` | `alb` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeCaCertificates` | `Python SDK-only/未匹配 CLI` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeCertificates` | `alb, clb` | 域名、证书、CDN、直播或入口链路证据 |
| `DescribeCustomizedCfgAttributes` | `alb` | 资源存在性、状态、配置或诊断证据 |
| `DescribeCustomizedCfgs` | `alb` | 资源存在性、状态、配置或诊断证据 |
| `DescribeHealthCheckLogProjectAttributes` | `clb` | 资源存在性、状态、配置或诊断证据 |
| `DescribeHealthCheckLogTopicAttributes` | `clb` | 资源存在性、状态、配置或诊断证据 |
| `DescribeHealthCheckTemplates` | `alb` | 资源存在性、状态、配置或诊断证据 |
| `DescribeListenerAttributes` | `alb, clb` | 网络路径、入口、路由或安全策略证据 |
| `DescribeListenerHealth` | `alb, clb` | 网络路径、入口、路由或安全策略证据 |
| `DescribeListeners` | `alb, clb` | 网络路径、入口、路由或安全策略证据 |
| `DescribeLoadBalancerAttributes` | `alb, clb` | 计费、订单、成本、配额或资源包证据 |
| `DescribeLoadBalancerSpecs` | `clb` | 计费、订单、成本、配额或资源包证据 |
| `DescribeLoadBalancerStatus` | `clb` | 计费、订单、成本、配额或资源包证据 |
| `DescribeLoadBalancers` | `alb, clb` | 计费、订单、成本、配额或资源包证据 |
| `DescribeLoadBalancersBilling` | `clb` | 计费、订单、成本、配额或资源包证据 |
| `DescribeNLBListenerAttributes` | `clb` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNLBListenerCertificates` | `clb` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNLBListenerHealth` | `clb` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNLBListeners` | `clb` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNLBSecurityPolicies` | `clb` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNLBServerGroupAttributes` | `clb` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeNLBServerGroups` | `clb` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeNLBSystemSecurityPolicies` | `clb` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNLBZones` | `clb` | 资源存在性、状态、配置或诊断证据 |
| `DescribeNetworkLoadBalancerAttributes` | `clb` | 计费、订单、成本、配额或资源包证据 |
| `DescribeNetworkLoadBalancers` | `clb` | 计费、订单、成本、配额或资源包证据 |
| `DescribeNlbListenerAttributes` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNlbListenerCertificates` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNlbListenerHealth` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNlbListeners` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNlbSecurityPolicies` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNlbServerGroupAttributes` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeNlbServerGroups` | `Python SDK-only/未匹配 CLI` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeNlbSystemSecurityPolicies` | `Python SDK-only/未匹配 CLI` | 网络路径、入口、路由或安全策略证据 |
| `DescribeNlbZones` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `DescribeRules` | `alb, clb` | 资源存在性、状态、配置或诊断证据 |
| `DescribeServerGroupAttributes` | `alb, clb` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeServerGroupBackendServers` | `alb` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeServerGroups` | `alb, clb` | 资源状态、实例/节点/集群运行态证据 |
| `DescribeZones` | `alb, clb` | 资源存在性、状态、配置或诊断证据 |
| `ListTagsForNLBResources` | `clb` | 资源存在性、状态、配置或诊断证据 |
| `ListTagsForNlbResources` | `Python SDK-only/未匹配 CLI` | 资源存在性、状态、配置或诊断证据 |
| `ListTagsForResources` | `alb, clb` | 资源存在性、状态、配置或诊断证据 |

### 镜像仓库
- 官方文档识别 Action 数：6
- 纳入只读/诊断 Action：9
- 排除自动执行的写/变更 Action：14

| Action | CLI 服务 | 排障用途 |
|---|---|---|
| `GetAuthorizationToken` | `cr` | 身份、权限、密钥或授权证据 |
| `GetPublicEndpoint` | `cr` | 模型、端点、Agent 或工作空间状态证据 |
| `GetUser` | `cr` | 身份、权限、密钥或授权证据 |
| `GetVpcEndpoint` | `cr` | 网络路径、入口、路由或安全策略证据 |
| `ListDomains` | `cr` | 域名、证书、CDN、直播或入口链路证据 |
| `ListNamespaces` | `cr` | 资源存在性、状态、配置或诊断证据 |
| `ListRegistries` | `cr` | 资源存在性、状态、配置或诊断证据 |
| `ListRepositories` | `cr` | 资源存在性、状态、配置或诊断证据 |
| `ListTags` | `cr` | 资源存在性、状态、配置或诊断证据 |

## 使用建议
- 优先使用章节 reference 中已经编排好的命令包；当用户问题落在未细化章节时，再从本矩阵选择最小只读 Action 补充证据。
- 如果某个只读 Action 需要分页、跨产品联动或深层字段归一，再考虑新增 `scripts/` 只读脚本，并同步更新脚本说明。
- 如果只读证据指向写操作修复，必须先输出影响面、资源 ID、回滚/恢复建议，并等待用户确认。
