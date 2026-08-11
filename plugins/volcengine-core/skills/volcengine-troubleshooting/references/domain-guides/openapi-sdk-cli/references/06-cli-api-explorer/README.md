# CLI / API Explorer 问题

用于排查 `ve` / `tosutil` CLI 与 API Explorer 的调用差异、参数形态、代理和网络环境问题。

## 前置输入

- CLI 版本、命令文本、错误输出。
- 手写 HTTP 请求的 Method、URL、Header key、Body 类型；不要收完整 Authorization。
- API Explorer 成功/失败截图或脱敏请求信息。
- 代理、TLS、容器/CI 环境、Region。

## 命令包

```text
ve version
ve <service> --help
ve <service> <Action> --help
```

使用方式：

- 先用 `--help` 判断参数形态，不猜 `--body` 还是展开参数。
- CLI help 输出用户目录配置文件读取告警时，只要命令 help 正常显示，不影响元数据判断。
- API Explorer 成功但本地失败时，逐项比对 Method、Host、Path、Query、Header、Body、Region、Service。

## 结果解读

| 证据 | 常见结论/下一步 |
|---|---|
| CLI 不支持 service/action | CLI 版本落后，或产品使用独立 CLI |
| 手写 HTTP 401/403 但 CLI 成功 | 签名、Authorization、Token 或 Header 错误 |
| API Explorer 成功但 CLI 失败 | CLI 参数形态、Region、Endpoint 或环境变量问题 |
| 代理 407 | 本地代理认证失败，不是火山引擎服务端拒绝 |
| TLS/证书链错误 | 本地 CA、代理中间人或运行时证书配置问题 |

## 禁止默认执行

- `ve configure`、`ve login`、`ve logout`、`ve sso`。
- 任何会把 AK/SK 写入本地配置或 shell history 的命令。
- 未经确认的手写 HTTP 写操作。
