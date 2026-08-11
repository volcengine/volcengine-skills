# OpenAPI 基础调用模型

用于排查 Action、Version、Service、Region、Endpoint、RequestId 不清楚或不匹配的问题。

## 前置输入

- `Action`、`Version`、`Service`、`Region`。
- Endpoint / Host，例如 `open.volcengineapi.com` 或产品专属域名。
- RequestId、ResponseMetadata、错误码。

## 命令包

```text
ve <service> --help
ve <service> <Action> --help
```

使用方式：

- 如果 `ve <service> <Action> --help` 报 unsupported action，先判断 CLI 版本是否落后，或 Action/Service 是否写错。
- 如果 help 存在，记录参数形态：展开参数还是 `--body` JSON。
- 如果用户走 Python SDK 或手写 HTTP 请求，仍可用 CLI help 作为本地接口元数据对照。

## 结果解读

| 证据 | 常见结论/下一步 |
|---|---|
| Service 不存在 | ServiceName 写错，或该产品使用独立 CLI/SDK |
| Action 不存在 | Action/Version 不匹配，或 CLI 元数据未覆盖最新 API |
| Action 存在但 Endpoint 不同 | 核对产品 API 文档中的 Endpoint/Region |
| Region 与资源地域不一致 | 修正 Region 后重试 |
| ResponseMetadata 中 Action/Version 与请求不一致 | 检查 SDK 默认版本或 CLI 服务映射 |

## 常见提醒

- 火山引擎 OpenAPI 排障先抽取四元组：Action、Version、Service、Region。
- `Service` 用于签名和路由，不能只看产品中文名。
- `Region` 同时影响签名和资源定位。
- `RequestId` 必须和发生时间、Region、Service 一起保留。
