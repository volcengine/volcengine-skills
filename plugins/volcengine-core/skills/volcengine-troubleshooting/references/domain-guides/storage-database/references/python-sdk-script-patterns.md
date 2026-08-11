# Python SDK 脚本模式

CLI 优先。只有这些场景再切脚本：

- 一个数据库实例需要批量聚合 endpoint、allow list、备份、只读节点状态。
- 返回 JSON 层级深、分页多，Agent 手串命令容易漏字段。

当前首版不保留 TOS 专用脚本：`tosutil stat` 已能判断 bucket/object 是否可见，`tosutil ls` 已能返回前缀样本，满足 TOS 403/404 首轮排查。
后续只有在需要分页聚合、批量摘要或跨服务相关性判断时，再重新引入 Python SDK 脚本。
