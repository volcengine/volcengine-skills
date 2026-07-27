# Live / 直播

用于直播推流、拉流、转码、录制、回调和流状态问题。

## 前置输入

- domain、vhost、app、stream、推流/拉流 URL、发生时间。
- 是否有鉴权、是否经 CDN、回调 URL、录制 preset。

## 先判断方向

| 现象 | 优先检查 |
|---|---|
| 推不上流 | 推流 URL、鉴权、流状态 |
| 能推不能播 | 播放域名、流状态、CDN/证书 |
| 回调失败 | 回调地址、公网可达性、签名 |
| 录制/转码异常 | preset 和任务结果 |

## 查询能力

当前公共 CLI 未明确匹配直播服务；不要编造 `ve live ...`。

若需要只读事实，按旧版官方 SDK `volcengine.live` 的查询能力组织：

- `describe_domain`
- `describe_live_stream_state`
- `describe_live_stream_info_by_page`
- `describe_push_stream_metrics`
- `describe_callback`
- `list_vhost_record_preset`
- `list_vhost_transcode_preset`

## 相邻产品：企业直播

企业直播不是视频直播本体，但同属本手册覆盖面。公共 CLI 已确认存在：

```text
ve livesaas ListActivityAPI --body '{"PageNo":1,"PageItemCount":1}'
ve livesaas20230801 ListLiveChannelConfig --ActivityId <activity-id>
```

当前验证账号调用 `ListActivityAPI` 已进入服务层，但返回“暂无此权限”；这说明命令映射存在，是否能取数仍取决于账号授权。

## 结果解读

- 源流未进入时，先查推流与鉴权，不先查播放器。
- 源流存在但播放失败时，优先转域名 CDN 与流量入口 skill。
- 回调失败如果是公网不可达，不属于直播控制面单独问题。
