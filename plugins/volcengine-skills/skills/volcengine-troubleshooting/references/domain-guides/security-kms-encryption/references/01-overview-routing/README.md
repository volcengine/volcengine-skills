# 排查总入口

用于用户只说“加密失败”“密钥不可用”“被安全产品拦截”“有安全告警”，但还没明确产品和证据时。

## 前置输入

- 产品名或控制台入口：KMS、云加密机、WAF、DDoS、云防火墙、云安全中心、云堡垒机等。
- Region、错误码、RequestId、发生时间。
- 资源 ID：KeyID、Keyring、SecretName、Domain、Host、IP、RuleId、AlarmId、AgentId。
- 调用主体：主账号、子用户、角色、STS。
- 影响对象：API 调用、域名访问、源站回源、主机、容器、数据库、模型接口。

## 先判断方向

| 现象 | 优先路径 |
|---|---|
| KMS 服务未开通、密钥列表为空 | `02-kms-service-key-state` |
| 密钥无权限、AccessDenied | `03-key-permission-access-control`，必要时转账号权限 skill |
| Plaintext / CiphertextBlob / InvalidEncryptedContent | `04-crypto-params-secret` |
| 密钥禁用、待删除、轮转 | `05-key-lifecycle-hsm` |
| 风控、合规、业务风险识别 | `06-security-risk-compliance` |
| WAF/DDoS/云防火墙误拦截 | `07-waf-ddos-cfw` |
| 云安全中心告警、Agent 状态 | `08-security-center-bastion-workload` |

## 最小证据

先让用户补齐：

- `Region`
- `RequestId` 或日志时间
- 具体错误文本
- 资源标识
- 调用主体

没有资源 ID 时，可以先用章节里的列表类只读命令确认账号下是否存在资源。

## 横向跳转

| 判断结果 | 跳转 |
|---|---|
| 明确是 IAM Action 或资源级授权缺失 | 账号权限 skill |
| 服务欠费、冻结、配额不足 | 计费 skill |
| CLI 参数不识别、签名错误、SDK 序列化问题 | OpenAPI / SDK / CLI skill |
| 安全产品正常放行但网络仍不通 | 计算容器网络 skill |
| WAF/DDoS 前置于域名/CDN/CLB | 域名 CDN 入口 skill |
