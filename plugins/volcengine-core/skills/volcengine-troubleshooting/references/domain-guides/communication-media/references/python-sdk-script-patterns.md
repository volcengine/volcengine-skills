# Python SDK 脚本模式

CLI 优先，但这个领域里 CLI 覆盖不完整。只有这些情况再补脚本：

- 一个问题要同时查签名/模板/发送明细/回执，Agent 手工串 SDK 过于容易漏字段。
- 直播问题需要把域名、鉴权、流状态、回调、录制 preset 聚合到一个摘要。
- 媒体任务返回深层 JSON 或分页很多，需要统一抽取 `status`、`reason`、`task_id`、`output`。
- OCR/CV 异步任务需要把 submit / query 的参数和结果做成稳定回归样本。

首版暂不落脚本，原因：

- 短信、RTC、Live、IMP 的 CLI / SDK 来源差异很大，先通过真实验证确认稳定接口和安装条件。
- 当前高频问题更需要先把链路分流和横向跳转讲清楚。

后续若新增脚本，必须：

- 只读。
- 优先读取 `VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、`VOLCENGINE_SESSION_TOKEN`。
- 在文件头声明 SDK 来源、调用接口、输入参数和不会执行的写操作。
