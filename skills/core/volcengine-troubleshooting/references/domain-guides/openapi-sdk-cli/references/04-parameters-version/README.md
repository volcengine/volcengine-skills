# 参数与接口版本

用于排查 `InvalidParameter`、`MissingParameter`、`InvalidAction`、`InvalidActionOrVersion`、SDK 序列化和 CLI 参数形态问题。

## 前置输入

- Action、Version、Service、Region。
- 完整错误码和 Message。
- 参数名、参数值类型、是否在 Query、Header 或 Body。
- SDK 模型字段或 CLI help 输出。

## 命令包

```text
ve <service> <Action> --help
```

使用方式：

- help 中显示 `--body '{...}'` 时，复杂对象和数组必须用 JSON body。
- help 中显示展开参数时，按参数名逐个传入。
- `InvalidAction` 先回到 `02-openapi-call-model` 判断 Action/Version/Service。

## 结果解读

| 证据 | 常见结论/下一步 |
|---|---|
| 参数名大小写和 help 不一致 | 按 CLI/OpenAPI 字段修正 |
| 数组/对象被当成字符串 | 改用 `--body` JSON 或 SDK 模型对象 |
| SDK 字段存在但服务端说缺参 | 检查 SDK 版本、字段序列化名、是否传 `None`/空值 |
| API Explorer 成功、本地失败 | 对比实际请求体、Content-Type、URL 编码、shell 转义 |
| 参数合法但产品状态不允许 | 转产品 skill，例如资源状态、库存、实例规格等 |

## CLI 参数提醒

- `apig ListGateways` 使用：

```text
ve apig ListGateways --body '{"PageNumber":1,"PageSize":10}'
```

- `cp ListResources` 使用：

```text
ve cp ListResources --body '{"PageNumber":1,"PageSize":10,"WorkspaceId":"<workspace-id>"}'
```

不要把复杂 JSON 拆成未验证的展开参数。
