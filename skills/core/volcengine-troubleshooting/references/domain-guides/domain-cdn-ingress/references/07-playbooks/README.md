# 高频 Playbook

## DNS 解析未生效

1. 查 Zone：

```text
ve dns ListZones --body '{"PageNumber":1,"PageSize":10,"Key":"<domain>"}'
```

2. 查记录：

```text
ve dns ListRecords --body '{"PageNumber":1,"PageSize":20,"ZID":<zone-id>,"Host":"<host>"}'
```

3. 如果配置正确但公网未生效，提示检查 TTL、递归 DNS 缓存、本地 hosts/缓存。

## HTTPS 证书不匹配

```text
ve certificateservice CertificateGetInstanceList --body '{"PageNumber":1,"PageSize":10,"Domain":"<domain>"}'
ve cdn DescribeCertConfig --body '{"Domain":"<cdn-domain>"}'
ve clb DescribeListenerAttributes --ListenerId <listener-id>
ve alb DescribeListenerAttributes --ListenerId <listener-id>
```

确认 CommonName/SAN、过期时间和入口绑定是否一致。

## CDN 回源失败 / 403 / 404

```text
ve cdn ListCdnDomains --body '{"PageNum":1,"PageSize":10,"Domain":"<domain>"}'
ve cdn DescribeCdnConfig --body '{"Domain":"<domain>"}'
ve cdn DescribeOriginSummary --body '{"Domain":"<domain>","StartTime":<start-unix>,"EndTime":<end-unix>}'
ve cdn DescribeOriginStatusCodeRanking --body '{"Domain":"<domain>","StartTime":<start-unix>,"EndTime":<end-unix>}'
```

有源站 5xx/404 转源站；边缘独有错误优先查 CDN 配置和访问控制。

## CDN 刷新预热失败

```text
ve cdn DescribeContentTasks --body '{"PageNum":1,"PageSize":10,"DomainName":"<domain>","TaskID":"<task-id>"}'
ve cdn DescribeContentQuota --body '{}'
```

只查询任务和配额。`SubmitRefreshTask` / `SubmitPreloadTask` 必须确认。

## CLB/ALB 健康检查失败

```text
ve clb DescribeListenerHealth --ListenerId <listener-id> --OnlyUnHealthy true --PageNumber 1 --PageSize 20
ve alb DescribeListenerHealth --ListenerIds.N <listener-id> --OnlyUnHealthy true
```

再查 listener、server group、backend；后端端口和安全组转计算网络 skill。
