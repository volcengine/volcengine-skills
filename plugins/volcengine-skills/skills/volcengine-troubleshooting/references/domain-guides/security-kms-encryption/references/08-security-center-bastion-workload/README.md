# 云安全中心 / 堡垒机 / 工作负载保护

用于主机安全告警、Agent 安装状态、基线/漏洞/恶意进程、云工作负载保护告警、堡垒机会话或登录问题。

## 前置输入

- 资产 ID、实例 ID、主机 IP、AgentID。
- 告警 ID、告警类型、发生时间。
- 堡垒机实例、用户、主机、协议、会话 ID。

## 云安全中心命令包

```text
ve seccenter20240508 CheckInstallAgentClient --body '{"AgentIDs":["<agent-id>"]}'
ve seccenter20240508 GetSecurityOverview
ve seccenter20240508 GetAIAlarmJudgeConfig
ve seccenter20240508 GetAIFingerprintStatistics
```

如果用户提供告警或主机详情，先查 `cli-meta/火山引擎密钥安全与加密服务排查手册/云安全中心/接口清单.md`，选择具体 `Get/List/Describe` 类接口，不要猜写操作。

## 云工作负载保护命令包

```text
ve secagent DescribeAlarmStatOverviewV2
ve secagent GetAlarmDetail --body '{"AlarmId":"<alarm-id>"}'
ve secagent GetResourceAuthConfig
ve secagent ListSyslogConfig
```

## 堡垒机处理方式

当前 `cli-meta` 未明确匹配云堡垒机可用 `ve` 服务。优先用官方文档和用户提供的控制台错误定位：

- 登录方式：SSH / SFTP / RDP / 数据库运维。
- 堡垒机实例、用户、资产、授权关系。
- 会话审计、资产连通、账号托管、MFA。

如果是 ECS/数据库本身不可达，转计算网络或存储数据库 skill。

## 结果解读

| 证据 | 常见结论 |
|---|---|
| Agent 未安装或离线 | 云安全中心无法检测或告警延迟 |
| 告警存在且状态未处置 | 需要确认风险与处置动作 |
| 工作负载告警详情指向容器/镜像 | 转计算容器网络 skill 保留安全上下文 |
| 堡垒机授权缺失 | 转账号权限 skill 或堡垒机授权检查 |

## 变更边界

不要自动隔离主机、封禁 IP、加白、修改基线或堡垒机授权。
