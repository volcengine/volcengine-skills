# SDK 问题

用于排查 SDK 安装、导入、初始化、依赖版本、异常封装、序列化、超时和重试问题。

## 前置输入

- SDK 名称、版本、语言和运行时版本。
- 初始化代码中的 Region、Endpoint、Service、AK/SK/STS 注入方式。
- 异常对象文本、ResponseMetadata、RequestId、HTTP status、Code、Message。

## 来源提醒

- 新版公共 Python SDK：`python-sdk/volcengine-python-sdk`，包名通常为 `volcenginesdk<service>`。
- 旧版 Python SDK：`python-sdk/volc-sdk-python`，包名通常为 `volcengine.<service>`。
- 部分产品有独立 Python SDK/CLI，先查 `火山引擎问题排查手册/README.md` 的产品行。

## 排查步骤

1. 先确认 SDK 来源和版本，避免新版/旧版包混用。
2. 用 `ve sts GetCallerIdentity` 确认当前环境凭证可用于基础 OpenAPI 调用。
3. 对照 `ve <service> <Action> --help` 判断 SDK 方法对应的 Action 是否存在。
4. 区分 SDK 本地异常和服务端返回错误：
   - 本地异常：导入失败、类型错误、证书链、代理、超时。
   - 服务端错误：有 Code、Message、RequestId、ResponseMetadata。
5. 如果 SDK 失败但 CLI 成功，重点查 Region/Endpoint、序列化字段、Content-Type、STS token。

## 结果解读

| 证据 | 常见结论/下一步 |
|---|---|
| `ModuleNotFoundError` | SDK 未安装或包名不匹配 |
| `AttributeError` | SDK 版本或响应对象结构和示例不一致 |
| TLS / X.509 错误 | 证书链、代理或运行时 CA 配置问题 |
| HTTP 200 但业务 code 失败 | 服务端业务错误，不要误判为 SDK 成功 |
| SDK 超时但 CLI 正常 | 查 SDK timeout、代理、连接池、endpoint |

## 脚本边界

首版不默认生成 SDK 脚本。只有需要解析复杂异常对象、分页聚合或 API Gateway/云控制 API 多接口联动时，才按 `python-sdk-script-patterns.md` 新增脚本。
