# Python SDK 脚本模式

本 skill 首版不默认生成 Python 脚本。安全/KMS 场景的首轮排障优先使用只读 CLI：

- 单个 key、keyring、secret、WAF 域名、DDoS 流量、云防火墙策略、告警状态，用 `ve` 查询即可。
- 涉及明文、密文、SecretValue、证书私钥、攻击请求体时，脚本更容易造成敏感数据扩散，默认避免。

只有以下场景才考虑 SDK 脚本：

| 场景 | 为什么 CLI 不够 | 脚本要求 |
|---|---|---|
| 批量核对大量 KeyID / SecretName | 手工多次 CLI 易漏资源 | 只读分页、输出状态摘要，不输出 SecretValue |
| WAF / 云防火墙跨规则聚合 | 需要按域名/IP/时间聚合多个接口 | 输出命中规则、时间范围、摘要字段 |
| 云安全中心告警详情批量归一 | 告警详情字段多且嵌套 | 输出 `summary/findings/raw`，隐藏敏感命令行、路径和载荷 |
| KMS 诊断需要关联 keyring、key、tag、custom key store | 多接口联动 | 只查元数据，不调用 Encrypt/Decrypt/GetSecretValue |

脚本必须：

- 使用 `volcengine-python-sdk`，优先读取 `VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、`VOLCENGINE_SESSION_TOKEN`。
- 只调用 `Describe/List/Get/Query/Check/Desc` 类接口。
- 不接收命令行 AK/SK。
- 不输出完整明文、密文、SecretValue、证书私钥或完整攻击载荷。
- 请求量较大时先让用户确认范围。
