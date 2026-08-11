# 火山引擎域名证书 CDN 与流量入口排障技能

这是面向火山引擎 DNS、域名、备案、证书中心、CDN、全站加速、全球加速、CLB/ALB 和公网入口链路的产品/场景 skill。它回答的是“用户访问入口为什么解析不对、证书不对、CDN/回源不对、负载均衡不健康或公网访问异常”，不是替代后端 ECS/VPC/安全组/WAF 的横向排障。

## 上层信息

- 手册定位：覆盖 DNS 与域名解析、SSL/HTTPS 证书、CDN/全站加速、负载均衡与流量入口、公网访问与源站连通。
- 横向分工：AK/IAM 权限转账号权限 skill；账单/配额/欠费转计费 skill；CLI/SDK 参数、签名转 OpenAPI / SDK / CLI skill；ECS/VPC/安全组/路由/NAT/源站端口转计算容器网络 skill；WAF/DDoS/云防火墙拦截转密钥安全与加密服务 skill。
- 工具优先级：默认 CLI-first，只使用 `ve` 中 `Describe/List/Get/Query/Check` 类只读命令；刷新预热、证书绑定、域名启停、负载均衡配置变更都必须 Human-in-the-Loop。
- 数据来源：手册、`cli-meta/火山引擎域名证书 CDN 与流量入口排查手册/`、负载均衡接口元数据、官方文档、`cli/volcengine-cli`、`python-sdk/volcengine-python-sdk`。
- 安全边界：默认只读；不输出证书私钥、完整访问日志、Cookie、Authorization header、完整业务 URL 参数或用户敏感请求体。

## 先读这些

- `references/query-cli-catalog.md`：按问题域定位查询入口。
- `references/api-coverage-matrix.md`：本分类 `cli-meta/` API 覆盖审查矩阵，列出已纳入排障候选的只读/诊断 Action 与默认排除的写操作边界。
- `references/python-sdk-script-patterns.md`：什么时候才需要脚本。
- `references/01-overview-routing/README.md`：总入口和横向跳转。

同时可查：

- 产品手册：`火山引擎问题排查手册/火山引擎域名证书CDN与流量入口排查手册/README.md`
- 接口元数据：`cli-meta/火山引擎域名证书 CDN 与流量入口排查手册/<产品>/接口清单.md`
- 负载均衡元数据：`cli-meta/火山引擎云服务器、容器与网络连通问题排查手册/负载均衡/接口清单.md`
- 官方文档：`产品官方文档/火山引擎域名证书CDN与流量入口排查手册/<产品>/...`

## 使用边界

Use this skill when the user describes:

- DNS 解析失败、解析到错误 IP、CNAME 未生效、TTL 缓存、解析线路异常、TrafficRoute / HTTPDNS 问题。
- 域名备案、域名状态、域名无法访问或公网入口合规限制。
- HTTPS 证书过期、域名不匹配、证书链不完整、CDN/CLB/ALB 证书绑定异常。
- CDN/DCDN 访问 403/404/5xx、回源失败、缓存未刷新、刷新预热任务异常、命中率低、边缘节点访问慢。
- 全球加速、多云 CDN、边缘计算节点或边缘智能入口查询。
- CLB/ALB 监听器、转发规则、后端服务器、健康检查、会话保持、WebSocket/长连接入口异常。

Do not use this as the primary skill for:

- 后端 ECS 服务未监听、端口未开、安全组/路由/NAT/VPC 不通：转计算容器网络 skill。
- WAF 误拦截、DDoS 清洗、云防火墙 deny：转密钥安全与加密服务 skill。
- 权限不足、`AccessDenied`、AK/SK/STS 失效：转账号权限 skill。
- 刷新预热配额、欠费停服、资源冻结：转计费 skill。
- CLI 命令不存在、SDK 序列化和签名错误：转 OpenAPI / SDK / CLI skill。

## 强约束

- 默认只执行 `Describe/List/Get/Query/Check` 类查询。
- 公共 CLI 命令统一写成 `ve <service> <Action> [--body '<json>' | --Param value]`；如果 `cli-meta` 中写的是 `volcengine`，在本 skill 中统一转成 `ve`。
- CDN/DNS/证书/DCDN/GA 多数 API 使用 `--body`；CLB/ALB 多数 API 使用展开参数。执行前必须读对应 reference 或 `ve <service> <Action> --help`，不要猜字段名。
- 不执行刷新、预热、封禁、解封、证书上传/替换/绑定、域名新增/删除/启停、DNS 记录修改、负载均衡监听/后端/规则变更等写操作，除非用户明确确认。
- 不通过命令或脚本收集 AK/SK，不运行 `ve configure`、`ve sso` 等凭证配置命令。
- 不输出完整访问日志、证书私钥、Cookie、Authorization header、完整 URL query 或用户业务敏感字段。

## 交互式确认与 Human-in-the-Loop

| 动作类型 | 示例 | 确认要求 |
|---|---|---|
| CDN/DCDN 刷新预热/封禁 | `SubmitRefreshTask`、`SubmitPreloadTask`、`CreatePurgePrefetchTask`、`SubmitBlockTask` | 说明 URL/目录范围、配额消耗、可能影响缓存命中和源站压力 |
| 域名/解析变更 | `CreateRecord`、`UpdateRecord`、`DeleteRecord`、`UpdateRecordStatus` | 说明域名、主机记录、线路、TTL、回滚记录 |
| 证书变更 | `ImportCertificate`、`BatchDeployCert`、`ReplaceCertificate`、证书绑定/解绑 | 说明证书 ID、域名、监听器/CDN 域名、私钥不会输出 |
| 负载均衡变更 | 修改监听、规则、后端服务器、健康检查、权重、ACL | 说明 LB/Listener/ServerGroup/Backend、影响流量和回滚方式 |
| 全球加速/边缘入口变更 | 加速器、监听、终端节点组更新 | 说明加速区域、监听协议端口、终端节点影响面 |

## 快速路由

| 用户现象 | 优先证据 | 必读 reference |
|---|---|---|
| 不确定是 DNS、证书、CDN、LB 还是源站 | 域名、URL、状态码、时间、Region、入口产品 | [`01-overview-routing/README.md`](references/01-overview-routing/README.md) |
| 解析不到、CNAME 未生效、线路问题 | Zone、Host、Record、Type、Line、TTL | [`02-dns-domain-resolution/README.md`](references/02-dns-domain-resolution/README.md) |
| HTTPS 不安全、证书过期/不匹配 | 域名、证书 ID、CommonName/SAN、监听器/CDN 域名 | [`03-ssl-https-certificate/README.md`](references/03-ssl-https-certificate/README.md) |
| CDN/DCDN 403/404/5xx、回源失败、缓存问题 | 加速域名、URL、回源 Host、任务 ID、时间范围 | [`04-cdn-dcdn-cache-origin/README.md`](references/04-cdn-dcdn-cache-origin/README.md) |
| CLB/ALB 健康检查失败、转发异常 | LB ID、Listener ID、ServerGroup ID、Backend IP/Port | [`05-load-balancer-ingress/README.md`](references/05-load-balancer-ingress/README.md) |
| 公网访问源站不可达、备案/合规限制 | 源站 IP/域名、端口、备案状态、直连结果 | [`06-public-origin-connectivity/README.md`](references/06-public-origin-connectivity/README.md) |
| 高频问题 | 原始错误文本或用户现象 | [`07-playbooks/README.md`](references/07-playbooks/README.md) |

## 高频固定流程

### CDN 403/404/回源失败

1. 先查 `cdn ListCdnDomains` 定位域名和状态。
2. 再查 `cdn DescribeCdnConfig` 看源站、回源 Host、HTTPS、缓存、访问控制。
3. 必要时查 `cdn DescribeEdgeSummary` / `DescribeOriginSummary` / `DescribeOriginStatusCodeRanking` 区分边缘返回还是源站返回。
4. 如果疑似 WAF/DDoS/源站安全策略，保留 CDN 证据后跳转对应 skill。

### DNS / CNAME 未生效

1. 先查 `dns ListZones` 定位 Zone。
2. 再用 `dns ListRecords` 或 `dns QueryRecord` 查询 Host/Type/Line/Value。
3. 对 TrafficRoute / HTTPDNS，查 `gtm ListGtms/ListPools/ListRules` 或 `httpdns ListDomainRecords`。
4. 如果控制台配置正确但公网未生效，提示检查 TTL、递归 DNS 缓存和本地缓存。

### HTTPS 证书异常

1. 先查证书中心 `CertificateGetInstanceList` 或 CDN `ListCdnCertInfo`。
2. CDN 场景查 `cdn DescribeCertConfig`；CLB/ALB 场景查 `DescribeCertificates` 和 listener attributes。
3. 证书替换、部署、上传都必须确认，且不输出私钥。

### CLB/ALB 健康检查失败

1. 查 LB 列表和属性。
2. 查 Listener 和 ListenerHealth。
3. 查 ServerGroup / BackendServers。
4. 后端端口、安全组、路由、ECS 服务状态转计算容器网络 skill。

## 章节目录

| 上层章节 | 本 skill reference |
|---|---|
| 1. 排查总入口 | [`01-overview-routing/README.md`](references/01-overview-routing/README.md) |
| 2. DNS 与域名解析 | [`02-dns-domain-resolution/README.md`](references/02-dns-domain-resolution/README.md) |
| 3. SSL / HTTPS 证书 | [`03-ssl-https-certificate/README.md`](references/03-ssl-https-certificate/README.md) |
| 4. CDN / 全站加速 | [`04-cdn-dcdn-cache-origin/README.md`](references/04-cdn-dcdn-cache-origin/README.md) |
| 5. 负载均衡与流量入口 | [`05-load-balancer-ingress/README.md`](references/05-load-balancer-ingress/README.md) |
| 6. 公网访问与源站连通 | [`06-public-origin-connectivity/README.md`](references/06-public-origin-connectivity/README.md) |
| 7. 高频 Playbook | [`07-playbooks/README.md`](references/07-playbooks/README.md) |

## 工作流

1. 收集域名、URL、状态码、发生时间、客户端地域/运营商、入口产品、Region、资源 ID、RequestId。
2. 画访问链路：DNS -> CDN/DCDN/GA -> HTTPS/TLS -> CLB/ALB -> 源站/后端。
3. 打开 `query-cli-catalog` 后只读取当前问题需要的章节 reference。
4. 用最小只读命令确认入口资源、配置、状态、证书、回源、健康检查或任务状态。
5. 输出时区分：
   - 已确认事实
   - 最可能根因
   - 仍缺证据
   - 下一步安全动作
   - 横向跳转

## 输出格式

- `现象归类`
- `链路判断`
- `已查证据`
- `结论`
- `建议动作`
- `横向跳转`
