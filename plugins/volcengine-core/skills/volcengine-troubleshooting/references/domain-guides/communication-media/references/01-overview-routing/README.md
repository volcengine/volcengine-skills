# 排查总入口

用于先判断问题属于短信、RTC、点播、直播还是 CV/OCR。

## 前置输入

- 产品名、Region、错误码、RequestId、发生时间。
- app/room/user、vid、domain/vhost/app/stream、task_id、模板/签名/资质等关键标识。
- 问题发生在提交、审核、处理、回调、分发还是客户端接入阶段。

## 先判断方向

| 现象 | 优先路径 |
|---|---|
| `SY:0500`、`RE:0500`、短信回执、模板/签名/资质 | 短信服务 |
| `StartVoiceChat`、`INVALID_TOKEN`、房间、实时音视频 | RTC |
| `GetPlayInfo`、播放地址、媒资、转码产物 | VOD / 点播 |
| 推流、拉流、直播回调、录制、流状态 | Live / 直播 |
| `CVSync2Async*`、OCR、图片处理、任务状态 | CV / OCR |

## 横向跳转

- `AccessDenied`、产品开通权限：账号权限 skill。
- `Action` / `Version` / 签名 / SDK 机制：OpenAPI / SDK / CLI skill。
- 余额、套餐、额度、欠费：计费 skill。
- 直播域名、CNAME、HTTPS、CDN：域名 CDN 与流量入口 skill。

## 最小判别原则

- 短信先区分“接口受理失败”和“最终投递失败”。
- RTC 先区分“控制面 Action 报错”和“客户端入会/音视频链路问题”。
- VOD 先区分“媒资还没准备好”和“播放域名/播放器问题”。
- Live 先区分“源流没进来”和“边缘分发出不去”。
- CV/OCR 先区分“提交失败”和“异步任务执行失败”。
