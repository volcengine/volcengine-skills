# 密钥安全与加密服务查询 CLI 入口索引

| 问题域 | 必读 reference | 主要工具 / 服务 | 典型查询 |
|---|---|---|---|
| 总入口 | `01-overview-routing/README.md` | 多产品 | 先定位安全层和资源 |
| KMS 服务与密钥状态 | `02-kms-service-key-state/README.md` | `kms` | `DescribeRegions`、`DescribeKeyrings`、`DescribeKeys`、`DescribeKey` |
| 密钥权限与访问控制 | `03-key-permission-access-control/README.md` | `kms` + 账号权限 skill | `DescribeKey`、`ListTagsForResources`，权限策略转横向 skill |
| 加密/解密参数与 Secret | `04-crypto-params-secret/README.md` | `kms`、`metakms` | `DescribeSecret`、`DescribeSecretVersions`、`DescribeSecrets`、`GetPublicKey` |
| 密钥生命周期与云加密机 | `05-key-lifecycle-hsm/README.md` | `kms`、`metakms` | `DescribeKey`、`DescribeCustomKeyStores`、`DescribeSecrets` |
| 风控与合规 | `06-security-risk-compliance/README.md` | `risk`、`tis`、`pca`、`mcs` | 先识别产品；多产品当前以官方文档和只读接口为主 |
| WAF / DDoS / 云防火墙 | `07-waf-ddos-cfw/README.md` | `waf`、`advdefence`、`advdefence20230308`、`fwcenter` | `ListDomain`、`QueryAttackSecurityEvent`、`DescribeAttackFlow`、`DescribeControlPolicy` |
| 云安全中心 / 堡垒机 / 工作负载 | `08-security-center-bastion-workload/README.md` | `seccenter20240508`、`secagent` | `CheckInstallAgentClient`、`GetAlarmDetail`、`DescribeAlarmStatOverviewV2` |
| Playbook | `09-playbooks/README.md` | 视 case 而定 | 按错误码映射 |

公共约定：

- 只默认执行查询 Action。
- `cli-meta` 中的 `volcengine <service> <Action>` 在 skill 中统一写成 `ve <service> <Action>`。
- 安全产品很多命令需要 `--body '<json>'`；章节 reference 中给出可执行最小 body。
- KMS `GetSecretValue`、`Encrypt`、`Decrypt`、`GenerateDataKey` 等虽然存在于 CLI/SDK，但会触达敏感材料，不作为默认自动查询命令。
