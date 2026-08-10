# 排查总入口

用于先判断问题属于对象、文件、块、备份还是数据库。

## 前置输入

- 产品名、Region、错误码、RequestId、时间。
- bucket/object、file system、volume、backup job、DB instance 等资源标识。
- 是控制面 API 失败、数据面访问失败，还是客户端连接/性能问题。

## 先判断方向

| 现象 | 优先路径 |
|---|---|
| 403/404、bucket/object | TOS 访问 |
| `SignatureDoesNotMatch` | TOS 签名/S3 |
| 挂载失败 | 文件存储或块存储 |
| 恢复点/恢复任务 | 备份恢复 |
| 云备份 / Vault | 备份恢复 |
| 云盘 / EBS / 卷 / 快照 | 块存储 |
| 连接超时、白名单、账号 | 数据库连接 |
| 慢 SQL、复制延迟 | 数据库性能 |

## 横向跳转

- IAM / ACL / policy：账号权限 skill。
- 签名构造、SDK 调用：OpenAPI skill。
- VPC / 安全组 / DNS：计算网络 skill。
- 欠费 / 配额：计费 skill。
