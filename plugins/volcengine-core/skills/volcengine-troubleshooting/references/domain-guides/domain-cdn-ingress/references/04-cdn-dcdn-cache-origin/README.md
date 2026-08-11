# CDN / 全站加速 / 缓存与回源

用于 CDN/DCDN 域名状态、回源失败、缓存未刷新、刷新预热任务、403/404/5xx、命中率低、边缘访问慢。

## 前置输入

- 加速域名、URL、状态码、时间范围。
- 回源地址、回源 Host、源站协议/端口。
- 刷新/预热任务 ID、URL 列表。

## CDN 命令包

### 1. 查询 CDN 域名

```text
ve cdn ListCdnDomains --body '{"PageNum":1,"PageSize":10,"Domain":"<domain>"}'
```

关注字段：Domain、Status、CNAME、ServiceType、ServiceRegion、HTTPS、OriginProtocol。

### 2. 查询 CDN 配置

```text
ve cdn DescribeCdnConfig --body '{"Domain":"<domain>"}'
```

关注字段：源站、回源 Host、回源协议、缓存规则、访问控制、HTTPS。

### 3. 查询刷新预热任务

```text
ve cdn DescribeContentTasks --body '{"PageNum":1,"PageSize":10,"DomainName":"<domain>","TaskID":"<task-id>"}'
```

没有 TaskID 时，用时间范围和 URL 缩小：

```text
ve cdn DescribeContentTasks --body '{"PageNum":1,"PageSize":10,"DomainName":"<domain>","StartTime":<start-unix>,"EndTime":<end-unix>,"Url":"<url>"}'
```

### 4. 区分边缘与源站

```text
ve cdn DescribeEdgeSummary --body '{"Domain":"<domain>","StartTime":<start-unix>,"EndTime":<end-unix>}'
ve cdn DescribeOriginSummary --body '{"Domain":"<domain>","StartTime":<start-unix>,"EndTime":<end-unix>}'
ve cdn DescribeOriginStatusCodeRanking --body '{"Domain":"<domain>","StartTime":<start-unix>,"EndTime":<end-unix>}'
```

## DCDN / 全站加速

```text
ve dcdn ListDomainConfig --body '{"PageNumber":1,"PageSize":10,"Keyword":"<domain>"}'
ve dcdn DescribeDomainDetail --body '{"Domain":"<domain>"}'
ve dcdn CheckPurgePrefetchTask --body '{"TaskID":"<task-id>"}'
```

## 全球加速

```text
ve ga ListAccelerators --body '{"PageNum":1,"PageSize":10}'
ve ga DescribeAccelerator --body '{"AcceleratorId":"<accelerator-id>"}'
ve ga ListListeners --body '{"AcceleratorId":"<accelerator-id>","PageNum":1,"PageSize":10}'
ve ga ListEndpointGroups --body '{"AcceleratorId":"<accelerator-id>","PageNum":1,"PageSize":10}'
```

## 结果解读

| 证据 | 常见结论 |
|---|---|
| 域名不存在或停用 | CDN 未接入或状态异常 |
| CNAME 未指向 CDN | DNS/CNAME 链路问题 |
| 边缘 403/404 高，源站无对应错误 | CDN 访问控制、缓存或边缘配置问题 |
| 源站 5xx/404 高 | 回源或源站应用问题 |
| 刷新任务失败 | URL 范围、配额、权限或任务参数问题 |

## 变更边界

刷新、预热、封禁、解封、域名启停和配置修改都必须确认；避免无范围刷新导致源站压力。
