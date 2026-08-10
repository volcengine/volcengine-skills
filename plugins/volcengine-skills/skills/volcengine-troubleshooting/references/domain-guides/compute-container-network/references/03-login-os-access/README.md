# SSH / RDP / VNC 登录失败查询

用于“连不上云服务器”“SSH 超时/拒绝连接”“RDP 登录失败”“VNC 无法打开”“密钥或密码看似正确但进不去”等问题。

## 前置输入

- 实例 ID、Region、公网 IP/EIP 或私网 IP。
- 登录协议和端口：SSH 22、RDP 3389、自定义端口。
- 报错类型：timeout、connection refused、permission denied、host key、VNC 打不开。
- 最近是否改过安全组、路由、密码、密钥、镜像、系统防火墙。

## 先判断方向

| 现象 | 优先路径 |
|---|---|
| 连接超时 | 网络路径、安全组、ACL、路由、EIP |
| 拒绝连接 | 实例内服务未监听、系统防火墙、sshd/RDP 服务异常 |
| 密钥/密码失败 | 密钥对、登录用户、系统认证配置 |
| VNC/控制台也异常 | 系统启动、系统盘、镜像、控制台输出 |

## 命令包

### 1. 实例与控制台

```text
ve ecs DescribeInstances --Region "<region>" --InstanceIds.1 "<instance-id>"
ve ecs GetConsoleOutput --Region "<region>" --InstanceId "<instance-id>"
ve ecs GetConsoleScreenshot --Region "<region>" --InstanceId "<instance-id>"
ve ecs DescribeKeyPairs --Region "<region>"
```

`GetConsoleOutput` 返回的 `Output` 是 Base64 控制台日志。Agent 应解码后摘取异常片段、网卡地址、默认路由、cloud-init/启动失败信息，不要把完整原文输出给用户。

关注字段：

- 实例是否 `RUNNING`，公网/私网 IP 是否符合用户连接目标。
- 控制台输出是否显示系统启动失败、磁盘满、`sshd.service could not be found`、网络配置失败。
- 密钥对是否与实例关联。

### 2. EIP、网卡、安全组

```text
ve vpc DescribeEipAddresses --Region "<region>"
ve vpc DescribeNetworkInterfaces --Region "<region>" --InstanceId "<instance-id>"
ve vpc DescribeSecurityGroups --Region "<region>"
ve vpc DescribeSecurityGroupAttributes --Region "<region>" --SecurityGroupId "<sg-id>"
ve vpc DescribeNetworkAcls --Region "<region>"
ve vpc DescribeNetworkAclAttributes --Region "<region>" --NetworkAclId "<acl-id>"
```

关注字段：

- EIP 是否绑定到当前实例或网卡。
- 安全组入方向是否允许源 IP、协议、端口。
- 出方向是否被收紧，导致回包失败。
- 网络 ACL 是否额外拒绝入站或出站。

### 3. 子网路由

```text
ve vpc DescribeSubnets --Region "<region>" --SubnetIds.1 "<subnet-id>"
ve vpc DescribeRouteTableList --Region "<region>" --VpcId "<vpc-id>"
ve vpc DescribeRouteEntryList --Region "<region>" --RouteTableId "<route-table-id>"
```

多接口联动时优先使用 `scripts/collect_ecs_network_context.py` 聚合实例、网卡、安全组、子网和路由表，避免人工漏查。

关注字段：

- 子网是否关联预期路由表。
- 公网入站依赖的 EIP/CLB 是否路径正确。
- 私网登录是否需要 VPN/CEN/TR/专线双向路由。

## 结果解读

| 证据 | 下一步 |
|---|---|
| 安全组未放通端口 | 给出需放通的协议、端口、源 CIDR，变更前确认 |
| EIP 未绑定当前实例 | 说明资源绑定错，变更需确认 |
| 控制台输出显示 sshd 缺失 | 建议 VNC/救援模式/系统修复，不直接执行写操作 |
| `AccessDenied` 查询失败 | 转权限手册，保留实例和 Action |
