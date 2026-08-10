# 存储与数据库查询 CLI 入口索引

| 问题域 | 必读 reference | 主要工具 / 服务 | 典型查询 |
|---|---|---|---|
| 总入口 | `01-overview-routing/README.md` | 多产品 | 先定位产品与资源 |
| TOS / 对象访问 | `02-tos-object-access/README.md` | `tosutil` | `ls -e tos-<region>.volces.com -re <region>`、`stat` |
| TOS 签名 / S3 | `03-tos-signature-s3/README.md` | 文档 + OpenAPI skill | 先核对 host/region/service |
| 文件存储 | `04-file-storage/README.md` | `efs`、`cfs` | `DescribeFileSystems`、`DescribeMountPoints`、`DescribePermissionGroups` |
| 块存储 / 云盘 / EBS | `05-block-storage-volume/README.md` | `storageebs` | `DescribeVolumes`、`DescribeSnapshots`、`DescribeSnapshotGroups` |
| 云备份 / Vault / 恢复点 | `06-backup-restore/README.md` | `cbr` | `DescribeVaults`、`DescribeBackupPlans`、`DescribeRecoveryPoints`、`DescribeRestoreJobs` |
| 数据库连接 | `07-database-connectivity-permission/README.md` | `rdsmysqlv2`、`redis` | `DescribeDBInstances`、`DescribeDBInstanceEndpoints`、`DescribeAllowLists` |
| 数据库性能 | `08-database-performance-availability/README.md` | `rdsmysqlv2`、`redis` | `DescribeReadOnlyNodeDelay`、`DescribeSlowLogs`、`DescribeHotKeys` |
| Playbook | `09-playbooks/README.md` | 视 case 而定 | 按错误码映射 |

公共约定：

- 只默认执行查询 Action。
- TOS 数据面事实优先使用官方 `tosutil` 只读 CLI；当前不需要默认脚本。
- 数据库网络问题先保留数据库上下文，再按需转计算网络 skill。
