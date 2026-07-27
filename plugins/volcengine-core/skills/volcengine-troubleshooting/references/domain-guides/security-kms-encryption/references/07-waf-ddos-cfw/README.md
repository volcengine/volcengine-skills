# WAF / DDoS / 云防火墙

用于 WAF 误拦截、DDoS 清洗/黑洞、Web 攻击统计、云防火墙策略命中、访问被阻断。

## 前置输入

- 域名、Host、源 IP、目标 IP、端口、协议。
- 时间范围：StartTime / EndTime，建议 Unix 秒。
- WAF EventType、RuleId、防护域名。
- 云防火墙 Direction、RuleId、Source、Destination。
- DDoS 实例 IP、攻击时间。

## WAF 命令包

### 1. 查询防护域名

```text
ve waf ListDomain --body '{"Page":1,"PageSize":10,"Region":"<region>"}'
```

### 2. 查询 WAF 服务状态

```text
ve waf GetInstanceCtl --body '{"Region":"<region>"}'
```

### 3. 查询攻击/拦截事件

```text
ve waf QueryAttackSecurityEvent --body '{"StartTime":<start-unix>,"EndTime":<end-unix>,"Page":1,"PageSize":10,"Host":"<host>"}'
```

### 4. 查询规则和组

```text
ve waf ListAllowRule --body '{"Page":1,"PageSize":10}'
ve waf ListBlockRule --body '{"Page":1,"PageSize":10}'
ve waf ListAclRule --body '{"Page":1,"PageSize":10}'
ve waf ListCCRule --body '{"Page":1,"PageSize":10}'
ve waf GetTLSConfig --body '{"Host":"<host>"}'
```

## DDoS 命令包

```text
ve advdefence20230308 DescribeAttackFlow --body '{"BeginTime":<start-unix>,"EndTime":<end-unix>,"InstanceIps":["<ip>"],"Tab":"attack"}'
ve advdefence GetHostDefStatus --body '{"Host":"<host>"}'
ve advdefence DescWebAtkOverview --body '{"StartTime":<start-unix>,"EndTime":<end-unix>,"Hosts":["<host>"]}'
ve advdefence DescWebQpsFlow --body '{"StartTime":<start-unix>,"EndTime":<end-unix>,"Hosts":["<host>"]}'
```

## 云防火墙命令包

`DescribeControlPolicy` 必须指定 `Direction`，不要空参查询。排查“是否被策略拦截”时通常分别查询入站和出站：

```text
ve fwcenter DescribeControlPolicy --body '{"PageNumber":1,"PageSize":10,"Direction":"in"}'
ve fwcenter DescribeControlPolicy --body '{"PageNumber":1,"PageSize":10,"Direction":"out"}'
ve fwcenter DescribeControlPolicyByRuleId --body '{"RuleId":"<rule-id>"}'
ve fwcenter DescribeNatFirewallList --body '{"PageNumber":1,"PageSize":10}'
ve fwcenter DescribeVpcFirewallList --body '{"PageNumber":1,"PageSize":10}'
ve fwcenter GetPolicyCheckResult --body '{"RuleId":"<rule-id>"}'
```

## 结果解读

| 证据 | 常见结论 |
|---|---|
| WAF 有攻击事件且命中规则 | WAF 正常拦截或规则误伤 |
| WAF 无事件但用户 403 | 可能是 CDN/CLB/源站/应用层，转域名入口或计算网络 |
| DDoS 有攻击流量或清洗 | 清洗/黑洞链路，确认回源 IP 放行 |
| 云防火墙策略命中 deny | 云防火墙拦截，变更策略需确认 |
| 云防火墙无命中 | 继续查安全组、路由、NAT 或源站 |

## 变更边界

不要自动创建白名单、关闭防护、删除规则、切换防护模式。需要变更时必须说明域名/IP/规则影响面并等待确认。
