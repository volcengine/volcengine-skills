# Python SDK 脚本使用边界

本 skill 默认 CLI-first。只有 CLI 不能稳定完成证据聚合时，才考虑在 `scripts/` 下新增 Python 脚本。

## 适合脚本的场景

| 场景 | 为什么 CLI 不够 | 脚本应做什么 |
|---|---|---|
| 同一个 RequestId 需要串多个只读查询 | Agent 手工复制字段容易漏上下文 | 聚合调用主体、产品元数据、错误码、API Gateway 资源状态 |
| API Gateway 链路需要 Gateway -> Service -> Upstream -> Route -> Plugin 多层展开 | 单条 CLI 只能看到局部 | 接收 `--gateway-id`，分页查询并输出结构化摘要 |
| 云控制 API 需要 Workspace -> Resource -> DeployResource -> ServiceConnection | 多接口联动且字段嵌套 | 接收 `--workspace-id`，输出资源类型、状态、连接关系 |
| SDK 异常对象字段不统一 | 不同 SDK 包装 ResponseMetadata 的方式不同 | 从异常 JSON/对象文本中提取 Code、Message、RequestId、Action、Version |

## 不适合脚本的场景

- 单条 `ve sts GetCallerIdentity`、`ve apig ListGateways`、`ve <service> <Action> --help` 能回答的问题。
- 签名复现需要用户完整 AK/SK 或输出 Authorization 的场景。
- IaC 写操作或资源变更。
- 产品业务语义已经明确，应该转具体产品 skill。

## 脚本规范

- 只调用查询接口。
- 不硬编码 AK/SK/Token。
- 凭证优先读取 `VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、`VOLCENGINE_SESSION_TOKEN`。
- 输出 JSON，包含 `summary`、`findings`、`raw` 三段。
- 默认分页限制小范围，超过范围先询问用户。
- 不输出完整 Authorization、签名值、JWT、临时凭证、Secret、业务敏感请求体。

## 当前首版脚本结论

首版暂不新增脚本。原因：

- 核心身份验证可以由 `ve sts GetCallerIdentity` 完成。
- API Gateway 和云控制 API 的首层查询可以由 `ve apig ... --body`、`ve cp ... --body` 完成。
- 签名、参数、SDK、CLI 问题更依赖机制解释和最小复现，而不是多接口联动。

后续如果 benchmark 显示 Agent 在 API Gateway 或云控制 API 场景中多次漏查关联资源，再补 `collect_apig_context.py` 或 `collect_cloudcontrol_context.py`。

执行约束：

- 当前 skill 没有 `scripts/` 目录和可执行脚本。
- 不要调用 `RunSkillScript`。
- 不要臆造 `sts_get_caller_identity.py`、`signature_check.py`、`collect_openapi_context.py` 等脚本名。
- 身份验证固定使用 `ve sts GetCallerIdentity`。
