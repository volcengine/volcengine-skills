# 数据库性能与可用性

用于慢 SQL、只读延迟、热 key、慢日志、计划事件和高可用问题。

## MySQL 命令包

```text
ve rdsmysqlv2 DescribeReadOnlyNodeDelay --Region <region> --body '{"InstanceId":"<instance-id>"}'
ve rdsmysqlv2 DescribeFailoverLogs --Region <region> --body '{"InstanceId":"<instance-id>"}'
ve rdsmysqlv2 DescribePlannedEvents --Region <region>
```

## Redis 命令包

```text
ve redis DescribeSlowLogs --Region <region> --body '{"InstanceId":"<instance-id>","QueryStartTime":"<start>","QueryEndTime":"<end>"}'
ve redis DescribeHotKeys --Region <region> --body '{"InstanceId":"<instance-id>"}'
ve redis DescribeBigKeys --Region <region> --body '{"InstanceId":"<instance-id>"}'
ve redis DescribePlannedEvents --Region <region>
```

## 结果解读

- 先区分实例侧问题、查询模式问题和只读/复制链路问题。
- 监控指标缺失本身不等于数据库异常，必要时转监控日志问题域。
