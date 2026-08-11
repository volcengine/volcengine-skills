# 火山引擎密钥安全与加密服务排障技能

这是面向火山引擎 KMS、云加密机、WAF、DDoS、云防火墙、云安全中心、云堡垒机、云工作负载保护、多云安全、攻击面管理、业务风险识别、云信任中心和可信隐私计算问题的产品/场景 skill。它回答的是“密钥、加密材料或安全防护链路为什么不可用或误拦截”，不是替代账号权限、计费、OpenAPI/Python SDK/CLI 或网络连通横向 skill。

## 上层信息

- 手册定位：覆盖 KMS 服务开通、密钥状态、密钥权限、加密/解密参数、密钥生命周期、安全风控、WAF/DDoS/云防火墙/云安全中心等高风险排障。
- 横向分工：IAM/AK/STS 权限转账号权限 skill；账单、欠费、配额转计费 skill；CLI 参数、签名、SDK 安装转 OpenAPI / SDK / CLI skill；业务链路网络不通转计算容器网络 skill；证书和域名入口转域名 CDN 入口 skill。
- 工具优先级：默认 CLI-first，只使用 `ve` 中 `Describe/List/Get/Query/Check/Desc` 类只读命令；KMS 加解密、密钥启停、策略变更、防护规则变更都必须 Human-in-the-Loop。
- 数据来源：手册、`cli-meta/火山引擎密钥安全与加密服务排查手册/`、`产品官方文档/火山引擎密钥安全与加密服务排查手册/`、`cli/volcengine-cli`、`python-sdk/volcengine-python-sdk`。
- 安全边界：默认只读；不读取或输出密文原文、明文、SecretValue、证书私钥、完整攻击日志载荷、完整业务请求体。

## 先读这些

- `references/query-cli-catalog.md`：按问题域定位查询入口。
- `references/api-coverage-matrix.md`：本分类 `cli-meta/` API 覆盖审查矩阵，列出已纳入排障候选的只读/诊断 Action 与默认排除的写操作边界。
- `references/python-sdk-script-patterns.md`：什么时候才需要脚本。
- `references/01-overview-routing/README.md`：总入口和横向跳转。

同时可查：

- 产品手册：`火山引擎问题排查手册/火山引擎密钥安全与加密服务排查手册/README.md`
- 接口元数据：`cli-meta/火山引擎密钥安全与加密服务排查手册/<产品>/接口清单.md`
- 官方文档：`产品官方文档/火山引擎密钥安全与加密服务排查手册/<产品>/...`

## 使用边界

Use this skill when the user describes:

- `KMS service not open yet`、KMS 服务不可用、地域不支持、密钥列表/密钥环查询。
- `KMSEncryptFailed`、`InvalidParameter Plaintext`、`InvalidEncryptedContent`、加密上下文不一致、密文无法解密。
- 密钥无权限、密钥被禁用、待删除、轮转后调用失败、Secret/凭据查询异常。
- 云加密机、专属密钥库、自带密钥材料、密钥导入参数或 HSM 状态问题。
- WAF 误拦截、攻击事件查询、Bot/CC/ACL/黑白名单、防护域名/TLS 配置问题。
- DDoS 清洗、黑洞、攻击流量、Web 攻击统计、回源 IP 放行问题。
- 云防火墙访问控制策略、NAT/VPC 防火墙、策略命中、放行/拦截判断。
- 云安全中心告警、Agent 安装状态、基线/漏洞/恶意进程告警。
- 多云安全、攻击面管理、云工作负载保护、可信隐私计算或业务风险识别的只读状态查询。

Do not use this as the primary skill for:

- 纯 IAM 授权、AK/SK/STS 失效：转账号权限 skill。
- CLI 命令不存在、签名构造、SDK 安装和参数序列化：转 OpenAPI / SDK / CLI skill。
- 欠费、余额、服务配额或库存：转计费 skill。
- 纯网络路径不通、安全组/路由/NAT：转计算容器网络 skill。
- 域名解析、证书链、CDN/CLB 入口转发：转域名 CDN 入口 skill，保留 WAF/DDoS/云防火墙上下文。

## 强约束

- 默认只执行 `Describe/List/Get/Query/Check/Desc` 类查询。
- 公共 CLI 命令统一写成 `ve <service> <Action> [--body '<json>']`；如果 `cli-meta` 中写的是 `volcengine`，在本 skill 中统一转成 `ve`。
- 多数安全产品 API 使用 `--body` 传参；执行前必须先读对应 reference 或 `ve <service> <Action> --help`，不要猜字段名。
- 不执行 KMS 加密/解密/签名/验签/生成数据密钥等会处理敏感材料的命令，除非用户明确要求且完成风险确认。
- 不执行创建、删除、启用、禁用、轮转、导入、归档、恢复、策略修改、WAF 放行/封禁、DDoS 开关、云防火墙策略变更等写操作。
- 不输出完整明文、密文、SecretValue、证书私钥、攻击请求体、Cookie、Authorization header 或用户业务敏感字段。

## 交互式确认与 Human-in-the-Loop

| 动作类型 | 示例 | 确认要求 |
|---|---|---|
| KMS 数据面敏感操作 | `Encrypt`、`Decrypt`、`GenerateDataKey`、`AsymmetricSign` | 说明将处理的敏感材料类型、脱敏方式、不会回显明文/密文原文 |
| 密钥生命周期变更 | `EnableKey`、`DisableKey`、`ScheduleKeyDeletion`、`CancelKeyDeletion`、`EnableKeyRotation` | 说明 KeyID、影响服务、恢复窗口和业务风险 |
| Secret/凭据操作 | `GetSecretValue`、`SetSecretValue`、`ScheduleSecretDeletion` | 查询 SecretValue 也需确认，输出必须脱敏 |
| WAF/DDoS/云防火墙变更 | 创建/更新/删除规则、放行、封禁、切换防护模式 | 说明规则 ID、命中范围、可能影响的域名/IP/业务 |
| 云安全处置 | 隔离、封禁 IP、白名单、基线配置修改 | 说明资产、告警 ID、处置影响和回滚方式 |

## 快速路由

| 用户现象 | 优先证据 | 必读 reference |
|---|---|---|
| 不确定是 KMS、加密参数、防护误拦还是安全告警 | 产品名、错误码、RequestId、Region、资源 ID、发生时间 | [`01-overview-routing/README.md`](references/01-overview-routing/README.md) |
| `KMS service not open yet`、服务/地域/密钥列表问题 | Region、Keyring、KeyID、服务状态 | [`02-kms-service-key-state/README.md`](references/02-kms-service-key-state/README.md) |
| 密钥无权限、AccessDenied、资源级授权 | 调用主体、Action、KeyID/Keyring、策略 | [`03-key-permission-access-control/README.md`](references/03-key-permission-access-control/README.md) |
| `KMSEncryptFailed`、`InvalidEncryptedContent`、Secret 查询异常 | Plaintext/CiphertextBlob 类型、KeyID、上下文、Secret 名称 | [`04-crypto-params-secret/README.md`](references/04-crypto-params-secret/README.md) |
| 密钥禁用、轮转、待删除、云加密机/专属密钥库 | KeyState、Rotation、Deletion、CustomKeyStore | [`05-key-lifecycle-hsm/README.md`](references/05-key-lifecycle-hsm/README.md) |
| 账号风控、业务风险识别、可信隐私计算 | 风控错误码、设备/风险 ID、合规状态 | [`06-security-risk-compliance/README.md`](references/06-security-risk-compliance/README.md) |
| WAF 误拦截、DDoS 清洗、云防火墙策略命中 | 域名/IP、时间范围、事件 ID、规则 ID | [`07-waf-ddos-cfw/README.md`](references/07-waf-ddos-cfw/README.md) |
| 云安全中心、云工作负载、堡垒机 | 资产 ID、Agent ID、告警 ID、会话/主机 | [`08-security-center-bastion-workload/README.md`](references/08-security-center-bastion-workload/README.md) |
| 高频错误码 | 原始错误文本 | [`09-playbooks/README.md`](references/09-playbooks/README.md) |

## 高频固定流程

### KMS 服务未开通

1. 先查 `kms DescribeRegions` 判断服务 API 是否可达。
2. 再查 `kms DescribeKeyrings` 判断是否有密钥环。
3. 查询密钥列表时必须带上从上一步返回的 `KeyringName` 或 `KeyringID`，不要直接空参调用 `DescribeKeys`。
4. 如果返回服务未开通或无权限，保留 KMS 上下文后分别转计费/账号权限 skill。

### 密钥无权限

1. 先查 `DescribeKey` 或 `DescribeKeys`，确认密钥是否存在和状态是否可用。
2. 如果 key 存在但 Action AccessDenied，转账号权限 skill 判断 IAM/资源级授权。
3. 如果 key 不存在或不在当前地域，先按资源定位问题处理。

### 加密/解密参数错误

1. 不直接执行 `Encrypt/Decrypt`，先判断错误字段：Plaintext、CiphertextBlob、EncryptionContext、Algorithm。
2. 只读查询 key 状态和 public key/secret 元数据。
3. 涉及真实明文/密文时必须确认脱敏方式。

### WAF/DDoS/云防火墙误拦截

1. 先按时间、域名/IP、规则 ID 查安全事件或策略。
2. 云防火墙访问控制策略必须显式指定 `Direction`，通常分别查询 `in` 与 `out`。
3. 判断是安全产品命中，还是上游 CDN/CLB/源站/网络链路问题。
4. 放行、封禁、切换防护模式都必须确认。

## 章节目录

| 上层章节 | 本 skill reference |
|---|---|
| 1. 排查总入口 | [`01-overview-routing/README.md`](references/01-overview-routing/README.md) |
| 2. KMS 服务开通与状态 | [`02-kms-service-key-state/README.md`](references/02-kms-service-key-state/README.md) |
| 3. 密钥权限与访问控制 | [`03-key-permission-access-control/README.md`](references/03-key-permission-access-control/README.md) |
| 4. 加密/解密参数与 Secret | [`04-crypto-params-secret/README.md`](references/04-crypto-params-secret/README.md) |
| 5. 密钥生命周期与云加密机 | [`05-key-lifecycle-hsm/README.md`](references/05-key-lifecycle-hsm/README.md) |
| 6. 安全风控与合规限制 | [`06-security-risk-compliance/README.md`](references/06-security-risk-compliance/README.md) |
| 7. WAF / DDoS / 云防火墙 | [`07-waf-ddos-cfw/README.md`](references/07-waf-ddos-cfw/README.md) |
| 8. 云安全中心 / 堡垒机 / 工作负载保护 | [`08-security-center-bastion-workload/README.md`](references/08-security-center-bastion-workload/README.md) |
| 9. 高频 Playbook | [`09-playbooks/README.md`](references/09-playbooks/README.md) |

## 工作流

1. 收集产品、Region、资源 ID、错误码、RequestId、时间范围、调用主体、域名/IP、规则 ID 或告警 ID。
2. 判断是密钥状态、权限、加密参数、生命周期、风控合规、安全防护命中还是主机/工作负载告警。
3. 打开 `query-cli-catalog` 后只读取当前问题需要的章节 reference。
4. 用最小只读命令确认资源存在、状态、策略或事件；跨产品机制问题保留上下文后跳转横向 skill。
5. 输出时区分：
   - 已确认事实
   - 最可能根因
   - 仍缺证据
   - 下一步安全动作
   - 横向跳转

## 输出格式

- `现象归类`
- `已查证据`
- `结论`
- `建议动作`
- `横向跳转`
