# 领域排障手册

本目录按火山引擎常见故障域组织排障手册。每个领域目录都包含：

- `README.md`：该领域的触发场景、边界、路由、固定流程和输出格式。
- `references/`：查询命令索引、章节手册、API 覆盖矩阵、SDK 脚本模式等。
- `scripts/`：该领域可复用的只读辅助脚本和脚本说明。

使用时先从上层 `SKILL.md` 完成通用工具和身份检查，再进入最匹配的领域目录。不要一次性展开所有领域；只读取当前问题需要的入口、章节和脚本说明。

| 场景 | 入口 |
|---|---|
| 账号、IAM、AccessKey、STS、角色、权限 | `account-permission/README.md` |
| 余额、欠费、账单、订单、资源包、配额 | `billing-quota/README.md` |
| 短信、RTC、VOD、Live、CV/OCR、媒体处理 | `communication-media/README.md` |
| ECS、VKE、VPC、CLB/ALB、NAT、EIP、路由、登录和网络 | `compute-container-network/README.md` |
| DNS、域名、证书、CDN/DCDN、全球加速、入口链路 | `domain-cdn-ingress/README.md` |
| Ark、豆包、VikingDB、AgentKit、ArkClaw、AI 应用 | `llm-ecosystem/README.md` |
| OpenAPI、Python SDK、`ve`/`tosutil` CLI、API Gateway | `openapi-sdk-cli/README.md` |
| KMS、Secret、WAF、DDoS、云防火墙、安全中心 | `security-kms-encryption/README.md` |
| TOS、EBS、文件存储、云备份、RDS、Redis、数据库连接 | `storage-database/README.md` |

所有领域默认只读。写操作、敏感读取、凭证配置、支付/续费、推理/生成、刷新预热、授权变更、KMS 解密等动作必须先向用户解释影响并等待明确确认。
