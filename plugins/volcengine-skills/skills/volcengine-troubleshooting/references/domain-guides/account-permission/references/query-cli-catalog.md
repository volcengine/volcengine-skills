# 账号与权限查询 CLI 入口索引

| 问题域 | 必读 reference | 主要服务 | 典型查询 Action |
|---|---|---|---|
| 总入口 | `01-overview-routing/README.md` | `sts`、`iam` | `GetCallerIdentity`、`GetAccountSummary` |
| 账号状态 / 风控 | `02-account-verification-risk/README.md` | 官方文档为主 | 账号相关无明确公共 CLI |
| IAM 用户与策略 | `03-iam-user-policy/README.md` | `iam`、`iam20210801` | `GetUser`、`ListAttachedUserPolicies`、`ListGroupsForUser`、`ListProjectIdentities` |
| Role / STS | `04-role-sts/README.md` | `iam`、`sts` | `ListRoles`、`GetRole`、`ListAttachedRolePolicies`、`GetCallerIdentity` |
| 产品资源权限 | `05-product-resource-access/README.md` | `iam20210801` + 产品服务 | `GetProject`、`ListProjectResources` |
| AccessKey | `06-access-key/README.md` | `iam` | `ListAccessKeys`、`GetAccessKeyLastUsed` |
| Playbook | `07-playbooks/README.md` | 视 case 而定 | 按错误码映射 |

公共约定：

- 只默认使用查询 Action。
- 产品问题先保留产品上下文，再回到本 skill 判定权限机制。
- 账号风控/实名认证类问题往往没有足够公共 CLI，先按错误文本和官方流程分流，不要伪造查询能力。
