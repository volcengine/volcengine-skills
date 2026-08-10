# VOD / 点播

用于点播上传、播放、媒资状态、转码产物和 `GetPlayInfo` 相关问题。

## 前置输入

- Vid / FileId、空间、播放方式、期望格式/清晰度、RequestId。
- 是上传、处理、发布还是播放阶段失败。

## 先判断方向

| 现象 | 优先检查 |
|---|---|
| `GetPlayInfo` 失败 | Vid、发布状态、请求参数、转码产物 |
| 能拿到播放地址但播放失败 | 域名、加密、CDN、播放器 |
| 转码/截图未完成 | 任务状态与产物 |

## CLI 与文档边界

当前公共 CLI 匹配到的是 `vod20250101` 的 AI 翻译类新接口，不覆盖传统高频 `GetPlayInfo`。

可直接用的查询示例：

```text
ve vod20250101 GetExecution --Region <region>
ve vod20250101 ListAITranslationProject --Region <region> --SpaceName <space-name> --PageSize 1
```

但 `GetPlayInfo`、媒资状态和传统播放链路，首版应优先依赖官方 VOD 文档 / 官方服务端 SDK，不要把 `vod20250101` 当成完整 VOD 控制面。

已验证易错点：

- `ListAITranslationProject` 缺少 `SpaceName` 会返回 `InvalidParameter.SpaceMissing`。

## 结果解读

| 证据 | 常见结论 |
|---|---|
| 未发布 | `GetPlayInfo` 拿不到正式播放地址 |
| 请求清晰度没有对应产物 | 可能降级或失败 |
| 播放地址已返回但播放异常 | 更像域名、鉴权、播放器或 CDN 问题 |
