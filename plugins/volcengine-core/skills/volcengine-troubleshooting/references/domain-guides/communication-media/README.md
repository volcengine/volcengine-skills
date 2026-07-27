# 火山引擎云通信与音视频媒体服务排障技能

这是面向短信、RTC、点播、直播、CV/OCR 和媒体处理问题的产品 skill。它优先回答“消息或媒体链路卡在哪一段”，再决定是继续查本产品，还是把权限、计费、OpenAPI、CDN/域名问题交给横向或邻接 skill。

## 上层信息

- 手册定位：覆盖短信服务、RTC、VOD、Live、CV/OCR、媒体智能处理，并补充 WebRTC、veImageX、语音服务等邻近产品的查询入口。
- 横向分工：权限问题转账号权限 skill；签名/Action/Version/SDK 调用机制转 OpenAPI skill；欠费/套餐/额度转计费 skill；直播域名、证书、CNAME、CDN 回源转域名 CDN 与流量入口 skill。
- 工具优先级：能用 `ve` 查询的控制面事实先用 CLI；公共 CLI 无稳定映射的短信、RTC、Live、IMP、OCR 等问题，先依赖官方文档和官方 SDK 映射，不伪造 CLI。
- 数据来源：手册、`cli-meta/`、`产品官方文档/`、`cli/`、`python-sdk/`。
- 安全边界：默认只读；发送短信、发起呼叫、生成推流地址、创建/更新模板、启动/停止任务、删除媒资等动作都必须 Human-in-the-Loop。

## 先读这些

- `references/query-cli-catalog.md`：按问题域定位查询入口。
- `references/api-coverage-matrix.md`：本分类 `cli-meta/` API 覆盖审查矩阵，列出已纳入排障候选的只读/诊断 Action 与默认排除的写操作边界。
- `references/python-sdk-script-patterns.md`：什么时候需要脚本。
- `references/01-overview-routing/README.md`：总入口和横向跳转。
- `scripts/README.md`：脚本边界和后续扩展约定。

同时可查：

- 产品手册：`火山引擎问题排查手册/火山引擎云通信与音视频媒体服务排查手册/README.md`
- 接口元数据：`cli-meta/火山引擎云通信与音视频媒体服务排查手册/<产品>/接口清单.md`
- 官方文档：`产品官方文档/火山引擎云通信与音视频媒体服务排查手册/<产品>/...`

## 使用边界

Use this skill when the user describes:

- 短信发送失败、回执失败、签名/模板/号码资质审核、`SY:0500`、`RE:0500`。
- RTC / WebRTC Token、房间、StartVoiceChat、客户端接入、实时流质量。
- 点播上传、播放、转码、截图、媒资状态、`GetPlayInfo`。
- 直播推流、拉流、转码、录制、回调、流状态。
- CV/OCR、图像处理、异步任务提交、结果查询、veImageX。

Do not use this as the primary skill for:

- 纯 IAM / AccessDenied：转账号权限 skill。
- 纯签名、SDK 安装、Action/Version、CLI 语法：转 OpenAPI / SDK / CLI skill。
- 直播域名、HTTPS、CDN 回源、证书：转域名 CDN 与流量入口 skill。
- 欠费、余额、套餐、配额：转计费 skill。

## 强约束

- 默认只执行 `Describe/List/Get/Query/Check/Search` 类查询。
- 能确认的 CLI 统一写成 `ve <service> <Action> [--Param value...]`。
- 对 `cli-meta` 明确显示“未在已克隆 CLI 元数据中明确匹配”的产品，不要编造 `ve` 命令。
- 不执行短信发送、语音呼叫、创建模板、生成生产推流地址、启动/停止任务、更新回调、删除媒资等变更动作。
- 不输出完整手机号、完整 Token、完整回调密钥、完整播放密钥或完整业务内容。

## 交互式确认与 Human-in-the-Loop

| 动作类型 | 示例 | 确认要求 |
|---|---|---|
| 通信发送 | `SendSms`、`SendBatchSms`、语音呼叫 | 说明号码范围、发送内容、计费与触达风险 |
| 配置变更 | 更新签名/模板、直播鉴权、回调、证书 | 说明业务影响、传播时间和回滚方式 |
| 媒体任务 | 提交转码/处理任务、启动流分析 | 说明输入资源、输出位置、费用和覆盖风险 |
| 生命周期 | 停止任务、禁流、删除媒资 | 说明资源 ID、影响窗口和不可逆后果 |

## 快速路由

| 用户现象 | 优先证据 | 必读 reference |
|---|---|---|
| 不确定是短信、RTC、点播、直播还是 CV/OCR | 产品名、错误码、RequestId、链路阶段 | [`01-overview-routing/README.md`](references/01-overview-routing/README.md) |
| 短信发送失败、签名/模板/资质、回执 | 短信子账号、签名、模板、发送明细、回执 | [`02-sms-service/README.md`](references/02-sms-service/README.md) |
| RTC Token、房间、StartVoiceChat、实时流 | AppID、room、uid、token、action/version | [`03-rtc-webrtc/README.md`](references/03-rtc-webrtc/README.md) |
| `GetPlayInfo`、播放失败、媒资状态 | Vid、发布状态、转码产物、播放域名 | [`04-vod-playback-media/README.md`](references/04-vod-playback-media/README.md) |
| 推流、拉流、直播回调、录制 | domain、vhost、app、stream、回调、流状态 | [`05-live-streaming/README.md`](references/05-live-streaming/README.md) |
| CV/OCR、图像处理、异步任务 | req_key、task_id、图片 URL、任务状态 | [`06-cv-ocr-media-processing/README.md`](references/06-cv-ocr-media-processing/README.md) |
| 高频错误码与固定套路 | 原始错误文本 | [`07-playbooks/README.md`](references/07-playbooks/README.md) |

## 高频固定流程

### 短信 `SY:0500` / `RE:0500`

1. 先区分接口受理失败还是运营商回执失败。
2. 读 `02-sms-service`，核对签名、模板、号码资质、回执与发送明细。
3. 如果已经是权限或余额问题，再横跳账号权限 / 计费 skill。

固定分流：

- `SY:0500`：先按平台受理阶段失败排，不要直接说成“接口成功后的最终回执失败”。
- `RE:0500`：先按最终回执/投递阶段失败排，不要和 `SY:0500` 混用。

### RTC `ERROR_CODE_INVALID_TOKEN`

1. 先保留 AppID、room、uid、token 生成时间与过期时间。
2. 读 `03-rtc-webrtc`，区分 Token 过期、签发参数不一致和 OpenAPI 调用问题。
3. 如果用户给的是 API Action/Version 报错，再转 OpenAPI skill。

### VOD `GetPlayInfo`

1. 先确认 Vid、媒资发布状态、目标清晰度/格式是否有产物。
2. 读 `04-vod-playback-media`。
3. 如果问题落在播放域名、HTTPS 或 CDN，再转域名 CDN 与流量入口 skill。

## 章节目录

| 上层章节 | 本 skill reference |
|---|---|
| 1. 排查总入口 | [`01-overview-routing/README.md`](references/01-overview-routing/README.md) |
| 2. 短信服务 | [`02-sms-service/README.md`](references/02-sms-service/README.md) |
| 3. RTC 实时音视频 | [`03-rtc-webrtc/README.md`](references/03-rtc-webrtc/README.md) |
| 4. VOD / 点播 | [`04-vod-playback-media/README.md`](references/04-vod-playback-media/README.md) |
| 5. Live / 直播 | [`05-live-streaming/README.md`](references/05-live-streaming/README.md) |
| 6. CV / OCR / 媒体智能处理 | [`06-cv-ocr-media-processing/README.md`](references/06-cv-ocr-media-processing/README.md) |
| 7. 高频 Playbook | [`07-playbooks/README.md`](references/07-playbooks/README.md) |

## 脚本调用协议

当前首版不默认提供脚本。通信与媒体领域先把 CLI 可证实面和 SDK/文档兜底边界说明清楚；只有在真实验证中确认某类问题需要多接口联动、分页聚合或复杂结果归一时，才把脚本补进 `scripts/`。

## 工作流

1. 收集产品、链路阶段、Region、资源 ID、错误码、RequestId、发生时间。
2. 先判断问题发生在提交、审核、处理、分发还是客户端接入阶段。
3. 打开 `query-cli-catalog` 后只读取当前问题需要的章节 reference。
4. CLI 可查时用最小查询包确认控制面事实；CLI 不可查时明确说明需依赖官方 SDK / 官方文档，不要猜命令。
5. 输出时区分：
   - 已确认事实
   - 最可能根因
   - 仍缺证据
   - 下一步安全动作
   - 横向跳转

## 输出格式

- `现象归类`
- `已查证据`
- `结论`
- `建议动作`
- `横向跳转`
