# 查询 CLI Catalog

按问题域定位最小只读命令集合。命令统一使用 `ve`，来源为 `cli-meta` 和 `cli/volcengine-cli`。

| 问题域 | 必读 reference | 服务 | 推荐只读 Action |
|---|---|---|---|
| DNS 与域名解析 | `02-dns-domain-resolution/README.md` | `dns`、`gtm`、`httpdns` | `ListZones`、`ListRecords`、`QueryRecord`、`ListGtms`、`GetGtm`、`ListDomainRecords` |
| SSL / HTTPS 证书 | `03-ssl-https-certificate/README.md` | `certificateservice`、`cdn`、`clb`、`alb` | `CertificateGetInstanceList`、`CertificateGetInstance`、`ListCdnCertInfo`、`DescribeCertConfig`、`DescribeCertificates` |
| CDN / 缓存 / 回源 | `04-cdn-dcdn-cache-origin/README.md` | `cdn`、`dcdn`、`mcdn` | `ListCdnDomains`、`DescribeCdnConfig`、`DescribeContentTasks`、`DescribeEdgeSummary`、`DescribeOriginSummary`、`ListDomainConfig` |
| 全站加速 / 全球加速 | `04-cdn-dcdn-cache-origin/README.md` | `dcdn`、`ga` | `ListDomainConfig`、`DescribeDomainDetail`、`ListAccelerators`、`DescribeAccelerator`、`ListListeners`、`ListEndpointGroups` |
| 负载均衡入口 | `05-load-balancer-ingress/README.md` | `clb`、`alb` | `DescribeLoadBalancers`、`DescribeListeners`、`DescribeListenerHealth`、`DescribeServerGroups`、`DescribeServerGroupBackendServers` |
| 公网源站与合规 | `06-public-origin-connectivity/README.md` | `cdn`、`dns`、`clb`、`alb` | 用入口资源配置确认源站地址、证书绑定、监听状态；后端网络转计算网络 skill |

## 高频入口命令

这些命令可以从 catalog 直接执行；需要更完整排查时再打开对应 reference。

```text
ve cdn ListCdnDomains --body '{"PageNum":1,"PageSize":10}'
ve dns ListZones --body '{"PageNumber":1,"PageSize":10}'
ve certificateservice CertificateGetInstanceList --body '{"PageNumber":1,"PageSize":10}'
ve clb DescribeLoadBalancers --PageNumber 1 --PageSize 10
ve alb DescribeLoadBalancers --PageNumber 1 --PageSize 10
```

如果用户提供了具体域名：

```text
ve cdn ListCdnDomains --body '{"PageNum":1,"PageSize":10,"Domain":"<domain>"}'
ve dns ListZones --body '{"PageNumber":1,"PageSize":10,"Key":"<domain>"}'
ve certificateservice CertificateGetInstanceList --body '{"PageNumber":1,"PageSize":10,"Domain":"<domain>"}'
```

## 禁止默认执行

- CDN/DCDN 刷新、预热、封禁、解封：`SubmitRefreshTask`、`SubmitPreloadTask`、`CreatePurgePrefetchTask`、`SubmitBlockTask`。
- DNS 记录变更：`CreateRecord`、`UpdateRecord`、`DeleteRecord`、`UpdateRecordStatus`。
- 证书上传、替换、部署、删除：`ImportCertificate`、`BatchDeployCert`、`ReplaceCertificate`、`DeleteCertificate`。
- 负载均衡配置变更：`Create*`、`Modify*`、`Delete*`、`Add*`、`Remove*`、`Enable*`、`Disable*`。
