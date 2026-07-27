# 查询 CLI Catalog

按问题域定位最小只读命令集合。命令统一使用 `ve`，来源为 `cli-meta`、`cli/volcengine-cli` 和本地 `ve <service> <Action> --help` 验证。

| 问题域 | 必读 reference | 服务/工具 | 推荐只读动作 |
|---|---|---|---|
| 调用主体和凭证可用性 | `01-overview-routing/README.md`、`03-auth-signature/README.md` | `sts`、`iam` | `GetCallerIdentity`、`GetAccountSummary`、`GetAccessKeyLastUsed` |
| Action/Version/Endpoint/Region | `02-openapi-call-model/README.md` | `ve` CLI 元数据 | `ve <service> <Action> --help`、`ve <service> --help` |
| 参数和接口版本 | `04-parameters-version/README.md` | `ve` CLI 元数据 | `--help` 查看参数位置、类型、`--body` 结构 |
| SDK 运行时 | `05-sdk-runtime/README.md` | `python3`、SDK 源码 | 只做版本/导入/异常结构检查，不默认调用写接口 |
| CLI/API Explorer | `06-cli-api-explorer/README.md` | `ve`、`tosutil` | `ve version`、`ve <service> <Action> --help`、`tosutil help` |
| API 网关 | `08-api-gateway-cloudcontrol-iac/README.md` | `apig`、`apig20221112` | `ListGateways`、`GetGateway`、`ListGatewayServices`、`ListUpstreams`、`ListCustomDomains`、`ListRoutes` |
| 云控制 API | `08-api-gateway-cloudcontrol-iac/README.md` | `cp` | `ListWorkspaces`、`ListResources`、`ListDeployResources`、`ListServiceConnections` |

## 高频入口命令

这些命令可以从 catalog 直接执行；需要更完整排查时再打开对应 reference。

```text
ve sts GetCallerIdentity
ve iam GetAccountSummary
ve apig ListGateways --body '{"PageNumber":1,"PageSize":10}'
ve cp ListWorkspaces --body '{"PageNumber":1,"PageSize":10}'
```

如果用户提供 API Gateway 资源线索：

```text
ve apig ListGateways --body '{"PageNumber":1,"PageSize":10,"Filter":{"Name":"<gateway-name>"}}'
ve apig GetGateway --body '{"Id":"<gateway-id>"}'
ve apig ListGatewayServices --body '{"PageNumber":1,"PageSize":10,"GatewayId":"<gateway-id>"}'
ve apig ListUpstreams --body '{"PageNumber":1,"PageSize":10,"GatewayId":"<gateway-id>"}'
ve apig ListCustomDomains --body '{"PageNumber":1,"PageSize":10,"GatewayId":"<gateway-id>"}'
ve apig20221112 ListRoutes --body '{"PageNumber":1,"PageSize":10,"GatewayId":"<gateway-id>"}'
```

如果用户提供云控制 API 工作空间：

```text
ve cp ListResources --body '{"PageNumber":1,"PageSize":10,"WorkspaceId":"<workspace-id>"}'
ve cp ListDeployResources --body '{"PageNumber":1,"PageSize":10,"WorkspaceId":"<workspace-id>"}'
ve cp ListServiceConnections --body '{"PageNumber":1,"PageSize":10,"WorkspaceId":"<workspace-id>"}'
```

## 禁止默认执行

- 凭证配置和登录：`ve configure`、`ve login`、`ve logout`、`ve sso`。
- STS 角色扮演：`sts AssumeRole`，除非用户明确要求验证角色链并确认不会输出临时凭证。
- API Gateway 变更：`Create*`、`Update*`、`Delete*`、`Attach*`、`Detach*`。
- 云控制 API 变更：`Create*`、`Update*`、`Delete*`、`RunPipeline`、`Trigger*`、`Cancel*`。
