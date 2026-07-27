# 文件存储

用于 NFS/SMB 挂载失败、权限组异常、目录权限、吞吐问题。

## 前置输入

- Region、file system ID、mount point、客户端 VPC/subnet、协议版本。

## 命令包

```text
ve efs DescribeFileSystems --Region <region>
ve efs DescribeMountPoints --Region <region> --body '{"FileSystemId":"<file-system-id>"}'
ve efs DescribePermissionGroups --Region <region>
ve efs DescribePermissionRules --Region <region> --body '{"PermissionGroupId":"<permission-group-id>"}'
```

## 关注字段

- 文件系统状态。
- 挂载点状态、VPC/Subnet。
- 权限组和客户端 CIDR 是否匹配。

## 结果解读

| 证据 | 常见结论 |
|---|---|
| 挂载点不存在或状态异常 | 控制面未就绪 |
| 权限规则不含客户端网段 | 客户端被拒绝 |
| 控制面正常但挂载超时 | 转计算网络 skill |
