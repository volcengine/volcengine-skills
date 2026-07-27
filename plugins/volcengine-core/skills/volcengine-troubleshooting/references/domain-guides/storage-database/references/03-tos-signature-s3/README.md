# TOS 签名与 S3 兼容

用于 `SignatureDoesNotMatch`、S3 兼容 endpoint 混用、签名 region/host/service 不一致。

## 前置输入

- 请求 URL、Host、Region、Service、签名版本。
- 使用的是 TOS 原生 SDK、S3 兼容 SDK 还是手写签名。

## 先判断方向

| 现象 | 优先检查 |
|---|---|
| `SignatureDoesNotMatch` | host、region、service、canonical request |
| S3 SDK 访问失败 | 是否用了 S3 endpoint |
| 同一份 AK/SK 在别的请求可用 | 多半不是密钥本身，而是签名上下文 |

## 结果解读

- 这类问题的最终机制解释应转 OpenAPI / SDK / CLI skill。
- 本 skill 负责保留 TOS 场景上下文：bucket、endpoint、region、访问方式。
