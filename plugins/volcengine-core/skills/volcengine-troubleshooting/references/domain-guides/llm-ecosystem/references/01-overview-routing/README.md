# 1. 排查总入口与全局框架

用于用户只说“大模型调用失败”“方舟报错”“Agent 不工作”“语音合成失败”时，把问题路由到 8 个子类之一。

## 前置输入

- 产品或入口：方舟、AgentKit、扣子、ArkClaw、VikingDB、豆包语音、Trae、机器学习平台、LLM 安全。
- 资源：model id、Endpoint ID、API Key 类型、Workspace ID、Instance ID、Collection/Index、任务 ID。
- 错误：Code、Message、HTTP status、RequestId、发生时间、Region、ProjectName。
- 调用方式：控制台、受支持 Python SDK、OpenAI 兼容请求、ve CLI、WebSocket、Trae。

## 先判断方向

| 用户现象 | 优先路径 |
|---|---|
| 模型不存在、未开通、无访问权 | 先读 `08-playbooks`，再读 `03-l2-ark-maas` |
| 参数、模态、token、上下文不支持 | `02-l1-model-capability` |
| Endpoint/API Key/OpenAI 兼容调用失败 | `03-l2-ark-maas` |
| Agent、工具、知识库、ArkClaw、Coding Plan | `04-l3-agent-development` |
| 推理服务、资源组、超时、高并发 | `05-l4-ai-native-infra` |
| 语音、多模态、RAG、AI IDE、行业 Agent | `06-l5-vertical-scenarios` |
| 鉴权、权限、计费、限流、网络、服务端错误 | `07-cross-cutting` |
| 错误文本命中固定卡片 | `08-playbooks` |

## 证据分层

1. 产品层事实：资源是否存在、状态是否正常、绑定模型是否正确。
2. 模型层事实：模型是否支持当前能力、参数、模态和 token 长度。
3. 横向机制事实：身份、权限、开通、计费、限流、网络和 Python SDK/CLI 调用机制。
4. 用户输入事实：Prompt、文件、音色、图片、知识库内容是否超限或不兼容。

## 输出要求

- 不要只说“请检查权限”。必须先说明这是哪一层的问题。
- 如果跳转横向 skill，要带上大模型产品上下文，例如 Endpoint、model id、RequestId。
- 如果缺信息，按最少必要信息提问，优先要脱敏错误响应和 RequestId。
