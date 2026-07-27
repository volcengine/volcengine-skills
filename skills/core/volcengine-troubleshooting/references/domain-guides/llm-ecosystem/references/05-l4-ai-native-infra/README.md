# 5. L4 AI 云原生基础设施排查

用于推理服务、高并发、AI 网关、网络连接、WebSocket、超时、观测日志和资源组问题。

## 前置输入

- 服务或资源组：Service ID/Name、ResourceGroup、Deployment、Region、ProjectName。
- 性能现象：QPS、TPM、延迟、超时、429、5xx、WebSocket 断连。
- 时间窗口和 RequestId。

## 命令包

### 机器学习平台服务和资源组

```text
ve mlplatform20240701 ListServices --body '{"PageNumber":1,"PageSize":10}'
ve mlplatform20240701 ListResourceGroups --body '{"PageNumber":1,"PageSize":10}'
```

关注字段：

- 服务状态、资源组状态、资源规格、项目和更新时间。
- 是否存在服务不可用、资源组异常或项目不匹配。

### AgentKit Compute

```text
ve aidap DescribeComputes --body '{"WorkspaceId":"<workspace-id>"}'
```

关注字段：

- Compute 状态和服务类型。
- 工作区和 Compute 是否匹配。

## 结果解读

| 证据 | 下一步 |
|---|---|
| 服务/资源组状态异常 | 说明只读证据，变更或启停必须用户确认 |
| 429 但服务资源正常 | 转 `07-cross-cutting` 判断限流、配额、订阅 |
| WebSocket/网络错误 | 区分 SDK 连接、代理、DNS、TLS，必要时转网络或 OpenAPI skill |
| 无资源或权限不足 | 保留 ProjectName/Region，转账号权限或计费 skill |
