# 镜像、初始化与云助手查询

用于自定义镜像启动异常、cloud-init 失败、用户数据未执行、云助手不可用、初始化脚本失败等问题。

## 前置输入

- 实例 ID、镜像 ID、Region、发生时间。
- 是否使用自定义镜像、启动脚本、用户数据、云助手命令。
- 控制台输出中的关键报错。

## 命令包

### 1. 镜像和实例初始化

```text
ve ecs DescribeInstances --Region "<region>" --InstanceIds.1 "<instance-id>"
ve ecs DescribeImages --Region "<region>" --ImageIds.1 "<image-id>"
ve ecs DescribeUserData --Region "<region>" --InstanceId "<instance-id>"
ve ecs GetConsoleOutput --Region "<region>" --InstanceId "<instance-id>"
ve ecs GetConsoleScreenshot --Region "<region>" --InstanceId "<instance-id>"
```

关注字段：

- 镜像状态、平台、架构、是否支持当前实例规格。
- 用户数据是否存在、是否被正确下发。
- 控制台输出里 cloud-init、网络初始化、磁盘挂载、驱动加载是否失败。

### 2. 云助手状态与历史

```text
ve ecs DescribeCloudAssistantStatus --Region "<region>" --InstanceIds.1 "<instance-id>"
ve ecs DescribeCommands --Region "<region>"
ve ecs DescribeInvocations --Region "<region>" --InstanceId "<instance-id>"
ve ecs DescribeInvocationResults --Region "<region>" --InvocationId "<invocation-id>"
```

关注字段：

- 云助手是否在线。
- 历史命令是否失败，失败输出是什么。
- 命令执行用户、超时时间、退出码。

## 结果解读

| 证据 | 常见根因 |
|---|---|
| 自定义镜像状态异常 | 镜像复制/导入/修复问题，回查镜像文档 |
| cloud-init 卡住 | 用户数据、网络初始化、包源、磁盘挂载问题 |
| 云助手离线 | 实例内 Agent 异常、网络不通、系统未正常启动 |
| 控制台显示驱动缺失 | 镜像不适配当前规格或 GPU/网卡驱动问题 |
