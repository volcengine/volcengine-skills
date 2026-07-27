# 高频 Playbook

## TOS `SignatureDoesNotMatch`

1. 保留 bucket/region/host。
2. 先确认是不是 S3 endpoint 与原生 endpoint 混用。
3. 再转 OpenAPI skill 检查签名。

## TOS 403 / AccessDenied

1. 先确认对象是否存在。
2. 再区分权限不足和签名错误。

## 云盘扩容后容量未生效

1. 先查控制面容量。
2. 控制面已扩容而 OS 未变时，提示继续检查分区和文件系统扩容。

## Redis `NOPERM`

1. 先判断命令权限，而非网络。
2. 查账号与 ACL 相关配置。

## 数据库连接超时

1. endpoint。
2. allow list。
3. 网络链路。
