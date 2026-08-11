# 4. L3 智能体开发体系排查

用于 AgentKit、扣子、HiAgent、ArkClaw、Coding Plan、Trae、工具调用、知识库和工作流问题。

## 前置输入

- 产品：AgentKit、扣子、ArkClaw、Trae、HiAgent。
- 工作区/实例/用户：WorkspaceId、InstanceId、Coze user、ProjectName。
- 关联资源：模型/Endpoint、知识库、工具、数据库、分支、Compute。
- 订阅或错误：Coding Plan 订阅、Unknown model、工具超时、知识库召回失败。

## 命令包

兼容性先读：`aidap`、`arkclaw` 在本地 CLI 元数据中存在，但当前远程沙箱镜像可能未安装这些 service。用户要求在沙箱里验证时，可以尝试一次只读查询；若返回 `unknown command`，应直接说明沙箱依赖不足并转为日志、订阅、模型名映射、控制台或工单证据，不要继续猜其他 service 名。

### AgentKit 工作区

这是可选命令，当前沙箱可能不可用：

```text
ve aidap DescribeWorkspaces --body '{"Limit":10,"Offset":0}'
ve aidap DescribeComputes --body '{"WorkspaceId":"<workspace-id>"}'
```

关注字段：

- Workspace 是否存在、状态是否异常。
- Compute 是否可用，是否与分支/服务类型匹配。

### ArkClaw

这是可选命令，当前沙箱可能不可用：

```text
ve arkclaw ListClawOmniInstances --PageNumber 1 --PageSize 10
ve arkclaw GetClawOmniInstance --Id <instance-id>
```

关注字段：

- 实例状态、ProjectName、关联 Space/订阅上下文。
- `Unknown model` 要同时检查本地模型配置和云端实例/订阅。

禁止默认执行：

```text
ve arkclaw ExecuteClawOmniInstanceCommand --InstanceId INSTANCE_ID --Command COMMAND_TEXT
ve arkclaw PauseClawOmniInstance --InstanceId INSTANCE_ID
ve arkclaw ResumeClawOmniInstance --InstanceId INSTANCE_ID
ve arkclaw ResetClawOmniInstance --InstanceId INSTANCE_ID
```

### 扣子

```text
ve coze20250601 ListCozeUser --body '{"PageNumber":1,"PageSize":10}'
```

关注字段：

- 用户映射是否存在。
- 授权和创建用户类接口是写操作，默认不执行。

## 结果解读

| 现象 | 下一步 |
|---|---|
| Coding Plan 过期 | 转计费 skill，保留产品和订阅上下文 |
| ArkClaw Unknown model | 先回方舟模型名/Endpoint 映射、ArkClaw 实例状态和 Coding Plan 订阅 |
| Agent 工具调用失败 | 区分工具 API、模型、知识库、网络和权限 |
| AgentKit 工作区不回复 | 若 `aidap` 可用，查 Workspace/Compute；若沙箱缺少 `aidap`，让用户提供 WorkspaceId、控制台状态和脱敏运行日志 |
| Trae 本地问题 | 需要用户提供本地版本、配置和脱敏日志，公共 CLI 通常无法直接查询 |
