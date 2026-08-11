# TOS / 对象存储访问

用于 TOS 上传下载失败、403/404、`BucketAlreadyExists`、对象路径错误。

## 前置输入

- Region、bucket、object key、访问方式。
- RequestId、错误码、是否经 CDN / S3 endpoint。

## 命令包

TOS 数据面优先使用官方 `tosutil` 只读 CLI。

查询当前账号可见 bucket：

```text
tosutil ls -e tos-<region>.volces.com -re <region>
```

确认 bucket / object 是否存在：

```text
tosutil stat tos://<bucket> -e tos-<region>.volces.com -re <region>
tosutil stat tos://<bucket>/<object-key> -e tos-<region>.volces.com -re <region>
```

若怀疑 object key 写错，补查同前缀样本：

```text
tosutil ls tos://<bucket>/<prefix> -limit=10 -e tos-<region>.volces.com -re <region>
```

## 关注字段

- bucket `Region`、`StorageClass`，确认 bucket 是否存在且当前身份可读。
- object `LastModified`、`Size`、`ETag`、`VersionID`，确认对象是否存在。
- 同前缀对象列表，帮助识别大小写或路径错误。

## 结果解读

| 证据 | 常见结论 |
|---|---|
| bucket 不可访问 | 先区分不存在、权限不足、region 错 |
| object 不存在但同前缀有近似 key | 多半是路径/大小写错误 |
| object 存在但访问仍 403 | 转账号权限或签名章节 |
| `BucketAlreadyExists` | bucket 名全局冲突，不代表当前账号可访问 |

## 变更边界

- 只允许 `stat`、`ls` 等已登记只读命令。
- TOS 数据面存在性查询只走 `tosutil`；不要回退到未登记的 `ve tos` 命令。
- `tosutil ls` 必须显式携带 `-e tos-<region>.volces.com -re <region>`。
- 不要使用 `cp`、`rm`、`presign` 等可能写入、上传或生成外发授权的命令。
