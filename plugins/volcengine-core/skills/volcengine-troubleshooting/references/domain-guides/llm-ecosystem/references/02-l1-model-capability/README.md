# 2. L1 基础模型层排查

用于模型能力、模态、上下文、参数和输出约束问题。

## 前置输入

- model id 或 Endpoint 绑定模型。
- 输入模态：文本、图像、音频、视频、Embedding、Rerank。
- 请求参数：temperature、top_p、max_tokens、tool_choice、response_format、guidance_scale 等。
- token 或文件大小、图片数量、音视频格式。

## 典型现象

| 现象 | 判断方向 |
|---|---|
| `guidance_scale is not supported` | 参数不属于当前模型能力 |
| 图片和文本 token 超限 | 多模态上下文限制或图片过多 |
| Embedding/Rerank 不可用 | 模型未开通、Endpoint 绑定错误或能力不匹配 |
| 工具调用/结构化输出失败 | 模型能力、SDK 版本或参数格式不一致 |

## 可执行查询

L1 多数依赖官方模型能力文档。若用户通过方舟 Endpoint 调用，可先回到方舟查询 Endpoint 绑定关系：

```text
ve ark ListEndpoints --body '{"PageNumber":1,"PageSize":10}'
ve ark GetEndpoint --body '{"Id":"<endpoint-id>"}'
```

关注字段：

- Endpoint 绑定的模型名称和版本。
- Endpoint 状态和项目。
- 用户实际传入的 `model` 字段是否等于 Endpoint ID、模型 ID 或别名。

## 结果解读

| 证据 | 下一步 |
|---|---|
| Endpoint 绑定模型与用户传入模型不一致 | 转 `03-l2-ark-maas` 修正调用方式 |
| 资源存在但参数不支持 | 指出参数和模型能力不匹配，建议换模型或去掉参数 |
| 模型能力文档未覆盖当前模态 | 让用户确认模型版本或改用支持该模态的模型 |
| Embedding/Rerank 资源不存在 | 转 `08-playbooks` 的 Embedding/Rerank 卡片 |
