# 块存储与云盘

用于云盘、弹性块存储、EBS、卷挂载、卸载、扩容、快照和 I/O 状态排查。用户说“云盘列表”时，也优先留在本章节。

## 前置输入

- Region、volume ID、instance ID、snapshot ID、AZ。

## 命令包

```text
ve storageebs DescribeVolumes --Region <region>
ve storageebs DescribeSnapshots --Region <region>
ve storageebs DescribeSnapshotGroups --Region <region>
```

## 关注字段

- volume 状态、可用区、挂载实例。
- snapshot 状态和来源卷。
- 容量是否已经在控制面扩容完成。

## 结果解读

| 证据 | 常见结论 |
|---|---|
| 控制面容量已增、OS 内未变 | 还需要分区/文件系统扩容 |
| 卷已挂载到其他实例 | 不能再次挂载 |
| 卷与实例 AZ 不一致 | 挂载失败高概率来自可用区不匹配 |
