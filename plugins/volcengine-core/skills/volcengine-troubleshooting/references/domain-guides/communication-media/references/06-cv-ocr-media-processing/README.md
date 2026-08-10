# CV / OCR / 媒体智能处理

用于 CV/OCR、veImageX、智能处理、媒体分析异步任务。

## 前置输入

- Action / req_key、task_id、图片或媒体 URL、输入格式、RequestId。
- 是同步接口失败、异步提交失败，还是查询结果失败。

## CLI 查询包

veImageX 对应 `veiapi` 可查询媒体分析任务：

```text
ve veiapi ListVideoAnalysisTask
ve veiapi GetVideoAnalysisTask
ve veiapi GetVideoAnalysisTaskData
ve veiapi GetVideoAnalysisTaskMediaMeta
```

## SDK / 文档兜底

- 智能处理可按旧版 SDK `volcengine.imp.retrieve_job` 查询任务。
- OCR / CV 历史接口在旧版 SDK 的 `volcengine.visual`、`volcengine.imagex` 中更常见。
- 对 `CVSync2AsyncSubmitTask`、`CVSync2AsyncGetResult`、`CVProcess`，首版保留 Action 上下文，优先查官方文档 / OpenAPI skill，不臆造 `ve` 命令。

## 结果解读

| 证据 | 常见结论 |
|---|---|
| 提交即 `Bad request` | 多半是参数、URL、格式问题 |
| task 已创建但失败 | 看任务状态、失败原因、输入可访问性 |
| task 查询不到 | task_id、账号、region 或产品上下文不一致 |
