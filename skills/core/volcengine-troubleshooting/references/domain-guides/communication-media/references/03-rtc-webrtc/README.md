# RTC / WebRTC

用于 RTC Token、房间、`StartVoiceChat`、WebRTC 应用和实时流问题。

## 前置输入

- AppID、room ID、user ID、Token 过期时间、Action、Version。
- 是服务端接口失败，还是客户端入会/发布/订阅失败。

## 先判断方向

| 现象 | 优先检查 |
|---|---|
| `ERROR_CODE_INVALID_TOKEN` | AppID/room/uid 与 token payload 是否一致、是否过期 |
| `StartVoiceChat` 报错 | Action / Version / 签名 / 权限 |
| 房间内无流或公共流异常 | WebRTC / WTN 查询 |

## CLI 查询包

WebRTC 传输网络可使用已匹配 CLI：

```text
ve wtn ListApps
ve wtn ListAppsV3
ve wtn ListRealTimePublicStreamInfo
```

## 关注字段

- 应用是否存在。
- 公共流是否存在、状态是否符合预期。
- 若 CLI 查不到 RTC 本体，不要把“无匹配接口”误判成“应用不存在”。

## 结果解读

- Token 类问题多数先看签发上下文，不先查网络。
- `StartVoiceChat` 本身是 OpenAPI 调用问题时，转 OpenAPI skill。
- 客户端音视频质量问题，需要补客户端日志、SDK 版本、网络环境，不应只靠控制面接口下结论。
