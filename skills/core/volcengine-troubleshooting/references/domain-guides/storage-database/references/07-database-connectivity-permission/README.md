# 数据库连接与权限

用于 MySQL、Redis 等连接超时、白名单、endpoint、账号权限问题。

## 前置输入

- 引擎、Region、instance ID、endpoint、端口、客户端来源。

## MySQL 命令包

```text
ve rdsmysqlv2 DescribeDBInstances --Region <region>
ve rdsmysqlv2 DescribeDBInstanceDetail --Region <region> --body '{"InstanceId":"<instance-id>"}'
ve rdsmysqlv2 DescribeDBInstanceEndpoints --Region <region> --body '{"InstanceId":"<instance-id>"}'
ve rdsmysqlv2 DescribeAllowLists --Region <region>
```

## Redis 命令包

```text
ve redis DescribeDBInstances --Region <region>
ve redis DescribeDBInstanceDetail --Region <region> --body '{"InstanceId":"<instance-id>"}'
ve redis DescribeAllowLists --Region <region> --body '{"RegionId":"<region>","InstanceId":"<instance-id>"}'
ve redis ListDBAccount --Region <region> --body '{"InstanceId":"<instance-id>"}'
```

## 结果解读

| 证据 | 常见结论 |
|---|---|
| endpoint 不存在或类型不对 | 地址使用错误 |
| allow list 不含客户端来源 | 白名单问题 |
| 控制面正常但 TCP 超时 | 转计算网络 skill |
| Redis 返回 `NOPERM` | 更像命令权限，不是网络问题 |

## 已验证易错参数

- `rdsmysqlv2 DescribeDBInstanceDetail` / `DescribeDBInstanceEndpoints` 使用 `--body` 传 `InstanceId`。
- `redis DescribeDBInstanceDetail` 使用 `--body` 传 `InstanceId`。
- `redis DescribeAllowLists` 的 `RegionId` 在 body 里，不能只写 `--Region`。
