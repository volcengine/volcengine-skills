# EIP / NAT / 路由 / 网关查询

用于 EIP 不通、出公网 IP 不符合预期、NAT 异常、路由表缺失、IPv6、VPN/CEN/TR/专线、私网连接等问题。

## 前置输入

- 访问方向：入公网、出公网、私网跨 VPC、跨地域、混合云。
- VPC/Subnet/RouteTable、EIP、NAT、VPN、CEN、TR、专线、PrivateLink 相关 ID。
- 源/目的 CIDR、协议、端口。

## 命令包

### 1. EIP 与带宽

```text
ve vpc DescribeEipAddresses --Region "<region>"
ve vpc DescribeEipAddressAttributes --Region "<region>" --AllocationId "<eip-id>"
ve vpc DescribeBandwidthPackages --Region "<region>"
```

关注字段：

- EIP 是否绑定正确资源。
- ISP、带宽包、计费状态、限速相关字段。
- 绑定资源类型是否与用户预期一致。

### 2. NAT 与 SNAT/DNAT

```text
ve natgateway DescribeNatGateways --Region "<region>"
ve natgateway DescribeNatGatewayAttributes --Region "<region>" --NatGatewayId "<nat-gateway-id>"
ve natgateway DescribeSnatEntries --Region "<region>" --NatGatewayId "<nat-gateway-id>"
ve natgateway DescribeDnatEntries --Region "<region>" --NatGatewayId "<nat-gateway-id>"
ve natgateway DescribeNatIps --Region "<region>" --NatGatewayId "<nat-gateway-id>"
```

关注字段：

- SNAT 是否覆盖源子网/源 CIDR。
- DNAT 是否映射到正确私网 IP 和端口。
- NAT 网关状态、NAT IP、绑定 EIP 是否正常。

### 3. 路由、IPv6、PrivateLink

```text
ve vpc DescribeRouteTableList --Region "<region>" --VpcId "<vpc-id>"
ve vpc DescribeRouteEntryList --Region "<region>" --RouteTableId "<route-table-id>"
ve vpc DescribeIpv6Gateways --Region "<region>"
ve vpc DescribeIpv6GatewayAttribute --Region "<region>" --Ipv6GatewayId "<ipv6-gateway-id>"
ve privatelink DescribeVpcEndpointServices --Region "<region>"
ve privatelink DescribeVpcEndpointAttributes --Region "<region>" --EndpointId "<endpoint-id>"
ve privatelink DescribeVpcEndpointConnections --Region "<region>" --EndpointServiceId "<service-id>"
```

关注字段：

- 子网关联的路由表是否包含目的 CIDR。
- 下一跳是否正确指向 NAT、TR、VPN、CEN、专线或 IPv6 网关。
- PrivateLink 服务和 endpoint 连接是否已接受、可用区是否匹配。

### 4. VPN / CEN / TR / 专线

```text
ve vpn DescribeVpnGateways --Region "<region>"
ve vpn DescribeVpnConnections --Region "<region>"
ve vpn DescribeVpnGatewayRoutes --Region "<region>" --VpnGatewayId "<vpn-gateway-id>"
ve cen DescribeCens --Region "<region>"
ve cen DescribeCenAttachedInstances --Region "<region>" --CenId "<cen-id>"
ve cen DescribeCenRouteEntries --Region "<region>" --CenId "<cen-id>"
ve transitrouter DescribeTransitRouters --Region "<region>"
ve transitrouter DescribeTransitRouterAttachments --Region "<region>"
ve transitrouter DescribeTransitRouterRouteTables --Region "<region>"
ve directconnect DescribeDirectConnectConnections --Region "<region>"
ve directconnect DescribeDirectConnectVirtualInterfaces --Region "<region>"
```

关注字段：

- 附件/连接状态是否可用。
- 路由是否双向传播或学习。
- 带宽包、跨地域带宽、BGP peer、虚拟接口是否异常。

## 结果解读

| 证据 | 常见根因 |
|---|---|
| EIP 绑定错资源 | 用户访问到了错误入口 |
| SNAT 未覆盖源子网 | 出公网失败或出口 IP 不符合预期 |
| 路由缺少目的 CIDR | 私网或跨域链路不可达 |
| CEN/TR/VPN 单向路由 | 请求能出去但回包失败 |
| 专线 BGP/虚拟接口异常 | 混合云链路中断或路由未学习 |
