# Python SDK Script Patterns

本 skill 默认 CLI-first。首版不提供脚本；只有 CLI 难以稳定串联或需要复杂聚合时才新增 Python SDK 脚本。

## 什么时候需要脚本

| 场景 | 为什么 CLI 不够 | 脚本应做什么 |
|---|---|---|
| 一个域名需要展开 DNS -> CDN -> 证书 -> CLB/ALB -> 后端 | Agent 手工串联容易漏字段 | 接收域名，输出链路摘要和缺口 |
| CDN 403/404/5xx 需要按时间聚合边缘与源站指标 | 多个统计接口参数复杂 | 归一边缘/源站状态码、命中率、回源失败趋势 |
| 大量 CDN 域名或证书批量过期检查 | 分页和筛选容易漏 | 自动翻页，输出即将过期证书和绑定域名 |
| CLB/ALB 健康检查跨 listener/server group/backend 聚合 | 多层资源关系复杂 | 输出不健康后端、健康检查配置和下一跳 |

## 脚本约束

- 只调用查询接口。
- 凭证只从 `VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、`VOLCENGINE_SESSION_TOKEN` 读取，兼容沙箱历史别名但不作为首选契约。
- 不输出完整日志、证书私钥、Cookie、Authorization header、完整 URL query。
- 请求范围大时先让用户确认分页和时间范围。

## 暂不需要脚本的场景

- 单个 CDN 域名配置查询。
- 单个 DNS Zone/Record 查询。
- 单个证书实例查询。
- 单个 CLB/ALB 的 listener health 查询。
