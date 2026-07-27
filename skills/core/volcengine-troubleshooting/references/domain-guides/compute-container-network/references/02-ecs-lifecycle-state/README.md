# ECS 实例生命周期与状态查询

用于 ECS/GPU ECS 创建、启动、停止、重启、实例状态异常、系统事件、控制台输出、弹性伸缩实例异常等问题。

## 前置输入

尽量先拿到：

- `Region`、实例 ID、可用区、项目/标签。
- 用户操作：创建、启动、停止、重启、释放、升配、系统盘更换、弹性伸缩拉起。
- 错误码、RequestId、发生时间。

## 命令包

### 1. 实例与库存状态

```text
ve ecs DescribeInstances --Region "<region>" --InstanceIds.1 "<instance-id>"
ve ecs DescribeInstanceTypes --Region "<region>"
ve ecs DescribeAvailableResource --Region "<region>" --ZoneId "<zone-id>"
ve ecs DescribeZones --Region "<region>"
```

关注字段：

- 实例 `Status`、`StoppedMode`、`ChargeStatus`、`ExpiredTime`、`ZoneId`、`InstanceTypeId`。
- `VpcId`、`SubnetId`、`NetworkInterfaces`、`SecurityGroupIds`，后续用于网络链路展开。
- 库存/规格是否支持当前地域和可用区。

### 2. 系统事件、任务与控制台输出

```text
ve ecs DescribeSystemEvents --Region "<region>" --InstanceId "<instance-id>"
ve ecs DescribeTasks --Region "<region>" --ResourceId "<instance-id>"
ve ecs GetConsoleOutput --Region "<region>" --InstanceId "<instance-id>"
ve ecs GetConsoleScreenshot --Region "<region>" --InstanceId "<instance-id>"
```

关注字段：

- 是否有宿主机维护、实例异常、系统盘异常、启动失败事件。
- 控制台输出中是否出现 kernel panic、文件系统只读、磁盘满、cloud-init 卡住、sshd 缺失。
- 任务是否处于执行中、失败或被前置状态阻塞。

### 3. 镜像、密钥、云助手和标签

```text
ve ecs DescribeImages --Region "<region>" --ImageIds.1 "<image-id>"
ve ecs DescribeKeyPairs --Region "<region>"
ve ecs DescribeCloudAssistantStatus --Region "<region>" --InstanceIds.1 "<instance-id>"
ve ecs ListTagsForResources --Region "<region>" --ResourceIds.1 "<instance-id>"
```

用于判断：

- 自定义镜像是否可用、是否跨地域复制失败、是否缺少驱动。
- 密钥是否存在但不匹配当前实例。
- 云助手是否在线，能否作为后续只读诊断通道。

### 4. 弹性伸缩相关

```text
ve autoscaling DescribeScalingGroups --Region "<region>"
ve autoscaling DescribeScalingInstances --Region "<region>" --InstanceIds.1 "<instance-id>"
ve autoscaling DescribeScalingActivities --Region "<region>" --ScalingGroupId "<scaling-group-id>"
ve autoscaling DescribeScalingConfigurations --Region "<region>" --ScalingConfigurationId "<config-id>"
ve autoscaling DescribeScalingPolicies --Region "<region>" --ScalingGroupId "<scaling-group-id>"
```

关注字段：

- 伸缩活动失败原因、实例是否被伸缩组托管。
- 伸缩配置中的镜像、规格、子网、安全组是否仍有效。
- 失败是否实际属于配额/库存/计费问题，需要转横向手册。

## 诊断判断

| 证据 | 常见结论 |
|---|---|
| 实例不存在或地域不匹配 | 用户资源 ID/地域错，先修正定位 |
| 状态为欠费冻结/过期 | 转计费手册 |
| `AccessDenied` / `NoPermission` | 转平台账号与权限手册 |
| 控制台输出显示系统错误 | 进入登录/OS 或镜像初始化排查 |
| 伸缩活动失败原因为库存/配额 | 转计费/配额手册，保留伸缩组上下文 |
