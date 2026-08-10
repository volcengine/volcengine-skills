# DNS 与域名解析

用于解析错误、CNAME 未生效、TTL 缓存、线路问题、TrafficRoute / HTTPDNS 异常。

## 前置输入

- 根域名、Host、记录类型：A / AAAA / CNAME / TXT。
- 解析线路、期望值、实际解析值。
- Zone ID、Record ID、客户端地域/运营商。

## 命令包

### 1. 查询 Zone

```text
ve dns ListZones --body '{"PageNumber":1,"PageSize":10,"Key":"<domain>"}'
```

关注字段：Zone ID、域名状态、项目、是否托管在火山 DNS。

### 2. 查询记录

```text
ve dns ListRecords --body '{"PageNumber":1,"PageSize":20,"ZID":<zone-id>,"Host":"<host>"}'
ve dns QueryRecord --body '{"ZID":<zone-id>,"RecordID":<record-id>}'
```

关注字段：Host、Type、Value、Line、TTL、Enable/Status。

### 3. TrafficRoute / HTTPDNS

```text
ve gtm ListGtms --body '{"PageNumber":1,"PageSize":10}'
ve gtm GetGtm --body '{"GtmId":"<gtm-id>"}'
ve httpdns ListDomainOverview --body '{"PageNumber":1,"PageSize":10}'
ve httpdns ListDomainRecords --body '{"Domain":"<domain>"}'
```

## 结果解读

| 证据 | 常见结论 |
|---|---|
| Zone 不存在 | 域名未托管到火山 DNS，需查权威 DNS 所在平台 |
| 记录值不是 CDN/CLB 目标 | 解析配置错误或 CNAME 未指向入口 |
| 配置正确但公网解析旧值 | TTL 或递归 DNS 缓存 |
| 仅部分线路异常 | 线路配置或运营商递归缓存问题 |
| HTTPDNS 有记录但公网 DNS 无 | HTTPDNS 与权威 DNS 是不同链路 |

## 变更边界

本 ref 只做查询。新增、修改、删除、停用解析记录都必须确认。
