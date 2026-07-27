# 云通信与媒体查询入口索引

本文件只做入口索引，不承载完整接口清单。通信与媒体产品的 CLI 覆盖并不均匀，先判断“能否被公共 CLI 稳定查询”，再决定下一步。

| 问题域 | 必读 reference | 主要工具 / 服务 | 典型查询 |
|---|---|---|---|
| 总入口 | `01-overview-routing/README.md` | 多产品 | 先判断链路阶段 |
| 短信服务 | `02-sms-service/README.md` | 旧版 Python SDK `volcengine.sms` | `get_sms_send_details`、`get_signature_and_order_list`、`get_sms_template_and_order_list` |
| RTC / WebRTC | `03-rtc-webrtc/README.md` | `wtn`，官方文档 | `ListApps`、`ListAppsV3`、`ListRealTimePublicStreamInfo` |
| VOD / 点播 | `04-vod-playback-media/README.md` | `vod20250101`、官方 VOD 文档 | `GetExecution`、`ListAITranslationProject`；传统 `GetPlayInfo` 需按官方文档/SDK 处理 |
| Live / 直播 | `05-live-streaming/README.md` | 旧版 Python SDK `volcengine.live` | `describe_live_stream_state`、`describe_domain`、`describe_callback` |
| 企业直播 | `05-live-streaming/README.md` | `livesaas`、`livesaas20230801` | `ListActivityAPI`、`ListLiveChannelConfig` |
| CV / OCR / 媒体处理 | `06-cv-ocr-media-processing/README.md` | `veiapi`、旧版 SDK `imagex` / `imp` / `visual` | `GetVideoAnalysisTask`、`ListVideoAnalysisTask`、`retrieve_job`、OCR 查询 |
| 高频 Playbook | `07-playbooks/README.md` | 视 case 而定 | 按错误码映射 |

公共约定：

- 能用 `ve` 的只用只读 Action。
- `cli-meta` 未明确匹配 CLI 的产品，不把“公共 CLI 存在”误写成“产品 CLI 可直接用”。
- `vod20250101 ListAITranslationProject` 至少需要 `--SpaceName <space-name>`，不要把无参失败误判成服务不可用。
- 需要签名、Action/Version、SDK 机制解释时，转 OpenAPI / SDK / CLI skill。

## 来源

- `cli-meta/火山引擎云通信与音视频媒体服务排查手册/*/接口清单.md`
- `产品官方文档/火山引擎云通信与音视频媒体服务排查手册/`
