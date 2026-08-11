# API 网关 / 云控制 API

用于排查 API Gateway 鉴权/转发和云控制 API 资源查询问题。

## 前置输入

- API Gateway：Gateway ID/名称、Service、Upstream、Route、CustomDomain、Consumer、Credential、PluginBinding、时间和错误码。
- 云控制 API：Workspace ID、Resource ID、Resource Type、Pipeline/Task、ServiceConnection。

## API Gateway 命令包

```text
ve apig ListGateways --body '{"PageNumber":1,"PageSize":10}'
ve apig GetGateway --body '{"Id":"<gateway-id>"}'
ve apig ListGatewayServices --body '{"PageNumber":1,"PageSize":10,"GatewayId":"<gateway-id>"}'
ve apig ListUpstreams --body '{"PageNumber":1,"PageSize":10,"GatewayId":"<gateway-id>"}'
ve apig ListCustomDomains --body '{"PageNumber":1,"PageSize":10,"GatewayId":"<gateway-id>"}'
ve apig ListPluginBindings --body '{"PageNumber":1,"PageSize":10,"GatewayId":"<gateway-id>"}'
ve apig20221112 ListRoutes --body '{"PageNumber":1,"PageSize":10,"GatewayId":"<gateway-id>"}'
```

关注字段：

- Gateway 状态、类型、VPC、绑定的 LB。
- Service / Upstream 的目标、协议、端口和版本。
- CustomDomain、Route 的 Host/Path/Method 匹配。
- PluginBinding 是否有鉴权、限流、Header 改写等插件。

## 云控制 API 命令包

```text
ve cp ListWorkspaces --body '{"PageNumber":1,"PageSize":10}'
ve cp ListResources --body '{"PageNumber":1,"PageSize":10,"WorkspaceId":"<workspace-id>"}'
ve cp ListDeployResources --body '{"PageNumber":1,"PageSize":10,"WorkspaceId":"<workspace-id>"}'
ve cp ListServiceConnections --body '{"PageNumber":1,"PageSize":10,"WorkspaceId":"<workspace-id>"}'
ve cp ListPipelineRuns --body '{"PageNumber":1,"PageSize":10}'
ve cp ListTaskRuns --body '{"PageNumber":1,"PageSize":10}'
```

关注字段：

- Workspace 是否存在、资源类型是否匹配、资源状态是否异常。
- ServiceConnection 是否缺失或状态异常。
- Pipeline/Task 是否失败；日志读取仍只读，但不要输出敏感环境变量。

如果需要验证当前调用身份，不要调用脚本，直接执行：

```text
ve sts GetCallerIdentity
```

结果解读：

| 证据 | 常见结论/下一步 |
|---|---|
## 横向跳转

- 后端网络、CLB、域名证书、WAF 命中：转对应产品 skill。
- `AccessDenied`：转账号权限 skill。
- 频控、余额、配额：转计费 skill。
