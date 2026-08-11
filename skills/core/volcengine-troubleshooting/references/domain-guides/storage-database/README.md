# 火山引擎存储与数据库排障技能

这是面向火山引擎 TOS、文件存储、块存储、云备份和数据库问题的产品 skill。它回答的是“数据为什么不能被正确存取、挂载、恢复或连接”，不是替代账号权限、OpenAPI、网络连通和计费横向 skill。

## 上层信息

- 手册定位：覆盖对象存储、TOS 签名/S3 兼容、文件存储、块存储、备份恢复、数据库连接、权限、性能和可用性。
- 横向分工：权限问题转账号权限 skill；签名/SDK 参数机制转 OpenAPI skill；数据库网络不通转计算网络 skill；欠费/配额转计费 skill。
- 工具优先级：控制面优先 `ve` 查询 CLI；TOS 数据面优先使用官方 `tosutil` 只读命令确认 bucket/object 存在性。
- 数据来源：手册、`cli-meta/`、`产品官方文档/`、`cli/`、`python-sdk/`。
- 安全边界：默认只读；上传/删除对象、创建 bucket、挂载/卸载卷、恢复、切换、重启等动作都必须 Human-in-the-Loop。

## 先读这些

- `references/query-cli-catalog.md`：按问题域定位查询入口。
- `references/api-coverage-matrix.md`：本分类 `cli-meta/` API 覆盖审查矩阵，列出已纳入排障候选的只读/诊断 Action 与默认排除的写操作边界。
- `references/python-sdk-script-patterns.md`：什么时候才需要脚本。
- `references/01-overview-routing/README.md`：总入口和横向跳转。

同时可查：

- 产品手册：`火山引擎问题排查手册/火山引擎存储与数据库问题排查手册/README.md`
- 接口元数据：`cli-meta/火山引擎存储与数据库问题排查手册/<产品>/接口清单.md`
- 官方文档：`产品官方文档/火山引擎存储与数据库问题排查手册/<产品>/...`

## 使用边界

Use this skill when the user describes:

- TOS 上传/下载失败、403/404、`BucketAlreadyExists`、`SignatureDoesNotMatch`、S3 兼容访问失败。
- NFS/SMB 文件系统挂载失败、读写异常、权限组或吞吐问题。
- 云盘未挂载、扩容后容量未生效、快照/卷状态异常。
- 备份任务失败、恢复点、恢复任务、跨地域复制。
- MySQL/Redis/PostgreSQL 等数据库连接超时、白名单、账号权限、SSL、慢 SQL、复制延迟。

Do not use this as the primary skill for:

- 纯 IAM 授权：转账号权限 skill。
- 纯 AK/SK 签名构造、SDK 安装和 CLI 参数：转 OpenAPI / SDK / CLI skill。
- ECS 到数据库网络不通、安全组/VPC 路由：转计算容器网络 skill。
- 欠费、余额、配额：转计费 skill。

## 强约束

- 默认只执行 `Describe/List/Get/Check/Head` 类查询。
- 公共控制面命令统一写成 `ve <service> <Action> [--Param value...]`；TOS 数据面只使用 `tosutil stat/ls/du/probe/ping/connect/traceroute/hash/help/version` 等已登记的只读命令。
- 不执行上传、删除、挂载、卸载、扩容、恢复、重启、切换等变更动作。
- 不执行数据库内 SQL 写操作；控制面排障和业务 SQL 问题要分层说明。
- 不输出完整 AK、对象内容、数据库密码或完整备份下载链接。

## 交互式确认与 Human-in-the-Loop

| 动作类型 | 示例 | 确认要求 |
|---|---|---|
| TOS 写操作 | `PutObject`、`DeleteObject`、`CreateBucket` | 说明 bucket/object、数据覆盖或删除风险 |
| 存储变更 | `AttachVolume`、`DetachVolume`、`ExtendVolume`、权限组更新 | 说明实例/卷/文件系统、影响窗口和回滚 |
| 备份恢复 | `CreateRestoreJob`、`RollbackVolume`、跨地域恢复 | 说明恢复点、目标资源、数据覆盖风险 |
| 数据库运维 | 重启、切换、参数修改、账号授权 | 说明实例、业务影响和高可用风险 |

## 快速路由

| 用户现象 | 优先证据 | 必读 reference |
|---|---|---|
| 不确定是 TOS、文件、块、备份还是数据库 | 产品、资源 ID、错误码、RequestId、网络路径 | [`01-overview-routing/README.md`](references/01-overview-routing/README.md) |
| TOS 403/404、bucket/object 访问失败 | bucket、object key、访问方式、policy/ACL | [`02-tos-object-access/README.md`](references/02-tos-object-access/README.md) |
| `SignatureDoesNotMatch`、S3 endpoint 混用 | host、region、service、endpoint、签名版本 | [`03-tos-signature-s3/README.md`](references/03-tos-signature-s3/README.md) |
| NFS/SMB 挂载失败、权限组问题 | 文件系统、挂载点、权限组、规则 | [`04-file-storage/README.md`](references/04-file-storage/README.md) |
| 云盘挂载、扩容、快照、I/O | volume、instance、snapshot、AZ | [`05-block-storage-volume/README.md`](references/05-block-storage-volume/README.md) |
| 备份、恢复、恢复点、Vault | plan、policy、resource、recovery point、restore job | [`06-backup-restore/README.md`](references/06-backup-restore/README.md) |
| 数据库连不上、白名单、权限、SSL | endpoint、instance、allow list、account | [`07-database-connectivity-permission/README.md`](references/07-database-connectivity-permission/README.md) |
| 慢 SQL、复制延迟、只读节点、热 key | 指标、慢日志、节点、复制状态 | [`08-database-performance-availability/README.md`](references/08-database-performance-availability/README.md) |
| 高频错误码 | 原始错误文本 | [`09-playbooks/README.md`](references/09-playbooks/README.md) |

## 高频固定流程

### TOS 403 / 404

1. 先确认 bucket 与 object 是否存在，不要把所有 403 都直接归因权限。
2. 读 `02-tos-object-access`；若需要数据面事实，优先使用 `tosutil stat` 与 `tosutil ls`。
3. 如果错误更像签名构造问题，再转 `03-tos-signature-s3`。

### 数据库连接超时

1. 先确认实例与 endpoint 存在。
2. 再查 allow list / 白名单。
3. 若控制面正常但客户端仍超时，转计算网络 skill 继续查 VPC、安全组、路由。

### 云盘 / 弹性块存储

用户说“云盘”“弹性块存储”“EBS”“卷”“快照”时，优先保留在本 skill，不要转到 ECS 通用查询 skill：

```text
ve storageebs DescribeVolumes --Region <region>
ve storageebs DescribeSnapshots --Region <region>
```

### 云备份 / Vault

用户说“云备份”“Vault”“恢复点”“恢复任务”时，优先命中本 skill：

```text
ve cbr DescribeVaults --Region <region>
ve cbr DescribeRecoveryPoints --Region <region>
ve cbr DescribeRestoreJobs --Region <region>
```

## 章节目录

| 上层章节 | 本 skill reference |
|---|---|
| 1. 排查总入口 | [`01-overview-routing/README.md`](references/01-overview-routing/README.md) |
| 2. TOS / 对象存储访问 | [`02-tos-object-access/README.md`](references/02-tos-object-access/README.md) |
| 3. TOS 签名与 S3 兼容 | [`03-tos-signature-s3/README.md`](references/03-tos-signature-s3/README.md) |
| 4. 文件存储 | [`04-file-storage/README.md`](references/04-file-storage/README.md) |
| 5. 块存储与云盘 | [`05-block-storage-volume/README.md`](references/05-block-storage-volume/README.md) |
| 6. 备份与恢复 | [`06-backup-restore/README.md`](references/06-backup-restore/README.md) |
| 7. 数据库连接与权限 | [`07-database-connectivity-permission/README.md`](references/07-database-connectivity-permission/README.md) |
| 8. 数据库性能与可用性 | [`08-database-performance-availability/README.md`](references/08-database-performance-availability/README.md) |
| 9. 高频 Playbook | [`09-playbooks/README.md`](references/09-playbooks/README.md) |

## TOS CLI 调用协议

TOS 数据面查询只使用已登记的 `tosutil` 只读命令，不要回退到未登记的 `ve tos` 命令。TOS 403/404 首选以下只读命令，不再默认进入 Python 脚本：

```text
tosutil ls -e tos-<region>.volces.com -re <region>
tosutil stat tos://<bucket> -e tos-<region>.volces.com -re <region>
tosutil stat tos://<bucket>/<object-key> -e tos-<region>.volces.com -re <region>
tosutil ls tos://<bucket>/<prefix> -limit=10 -e tos-<region>.volces.com -re <region>
```

`tosutil ls` 查询账号下 bucket 时也必须显式携带 `-e tos-<region>.volces.com -re <region>`，避免工具尝试读取本地配置文件后返回配置提示。`tosutil` 由沙箱 wrapper 从 `VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、`VOLCENGINE_SESSION_TOKEN` 自动补齐凭证参数；Agent 不要显式拼接 `-i/-k/-t`。如果后续出现“需要分页聚合、结构化归一、跨服务判断”的场景，再重新引入脚本。

## 工作流

1. 收集产品、region、resource ID、endpoint、bucket/object 或 instance、错误码、RequestId、发生时间。
2. 判断是数据面访问、控制面状态、恢复链路、数据库连接还是性能问题。
3. 打开 `query-cli-catalog` 后只读取当前问题需要的章节 reference。
4. 用最小查询命令确认资源存在、状态、关联配置；跨产品机制问题保留上下文后跳转横向 skill。
5. 输出时区分：
   - 已确认事实
   - 最可能根因
   - 仍缺证据
   - 下一步安全动作
   - 横向跳转

## 输出格式

- `现象归类`
- `已查证据`
- `结论`
- `建议动作`
- `横向跳转`
