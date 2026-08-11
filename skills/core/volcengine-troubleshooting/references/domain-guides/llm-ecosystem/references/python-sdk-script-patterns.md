# Python SDK 脚本边界

本 skill 首版不提供可执行脚本。默认 CLI-first，只有 CLI 不能稳定完成排障时才新增 `scripts/`。

## 何时需要脚本

| 触发条件 | 为什么 CLI 不够 | 脚本应做什么 |
|---|---|---|
| 一个方舟 Endpoint 要关联模型、精调、批量任务和权限证据 | 多个 API 返回结构不同，手工串联容易漏字段 | 聚合 Endpoint、模型绑定、任务状态，输出 `summary/findings/raw` |
| RAG 链路要关联知识库、VikingDB Collection、Index、构建任务和模型调用 | 单条 CLI 只能看到局部 | 以知识库/Collection 为入口展开状态和失败任务 |
| AgentKit 工作区要关联 Compute、Branch、数据库、API Key 和操作记录 | 多接口联动且字段深 | 生成工作区上下文和异常摘要 |
| 返回 JSON 过长或需要分页筛选 | CLI 单页输出容易漏 | 自动翻页、脱敏、汇总异常字段 |
| 需要稳定回归测试 | CLI 文本输出不稳定 | 输出结构化 JSON 便于 benchmark 断言 |

## 何时不要写脚本

- 单条 `List/Get/Describe` 已能回答资源是否存在或状态是否正常。
- 用户只是问错误码解释、参数兼容性或该读哪份文档。
- 需要执行模型推理、生成、创建、删除、启停、授权或变更。
- SDK 来源、接口参数或权限边界不清楚。

## 脚本规范

- 脚本放在 `scripts/`。
- 只调用查询接口。
- 优先读取 `VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、`VOLCENGINE_SESSION_TOKEN`，兼容旧变量由沙箱平台负责。
- 不接受命令行 AK/SK，不写凭证文件。
- 输出必须包含 `summary`、`findings`、`raw` 三段。
- 对 API Key、Prompt、知识库原文、音视频内容、模型输出进行脱敏或不输出。

## SDK 来源

- 默认来源：`python-sdk/volcengine-python-sdk`。
- 旧版 SDK：`python-sdk/volc-sdk-python`，仅在新版 SDK 没有相应服务或既有产品文档明确依赖时使用。
- 仅使用 `volc-sdk-python` 或 `volcengine-python-sdk`。如果某产品只能通过其它 SDK 完成，不在本 skill 中编写或执行脚本，改为说明限制并收集用户提供的脱敏证据。
