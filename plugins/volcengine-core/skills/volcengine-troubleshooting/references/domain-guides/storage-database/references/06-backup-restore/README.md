# 备份与恢复

用于云备份、Vault、备份计划、恢复点和恢复任务相关问题。

## 前置输入

- Region、vault、plan、policy、resource、recovery point、restore job。

## 命令包

```text
ve cbr DescribeBackupPlans --Region <region>
ve cbr DescribeBackupPolicies --Region <region>
ve cbr DescribeBackupResources --Region <region>
ve cbr DescribeRecoveryPoints --Region <region>
ve cbr DescribeRestoreJobs --Region <region>
ve cbr DescribeVaults --Region <region>
```

## 关注字段

- 备份计划是否启用。
- 资源是否已纳管。
- 是否存在可用恢复点。
- 恢复任务状态与失败原因。
