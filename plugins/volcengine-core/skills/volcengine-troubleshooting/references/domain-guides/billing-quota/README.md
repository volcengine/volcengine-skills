# 火山引擎计费排障技能

这是面向火山引擎全平台计费、余额、欠费、订阅、资源包、订单、用量、配额和账单问题的 Agent skill。它对应上层手册 `火山引擎计费问题排查手册`，职责是判断“商业状态为什么导致服务不可用或用户无法继续使用”，而不是解释单个产品的运行时故障。

## 上层信息

本技能继承的上层设计信息如下：

- 手册定位：处理余额不足、欠费、预扣费失败、套餐/订阅过期、资源包不抵扣、quota/调用次数耗尽、购买/开通失败、账单/成本明细查询等问题。
- 横向分工：账号/IAM 负责“有没有权限查账单或购买”；OpenAPI/Python SDK/CLI 负责“签名、参数、客户端调用机制”；产品 skill 负责“具体云服务运行态”。本 skill 保留产品上下文并判断计费机制。
- 工具优先级：优先使用 `ve` 查询 CLI；复杂账单分页、成本聚合、资源包抵扣分析可后续补 Python SDK 只读脚本。
- 数据来源：产品手册、`火山引擎问题排查手册/README.md` 的产品/Python SDK/CLI 总表、`cli-meta/` 接口元数据、`产品官方文档/` 官方原始文档、`cli/` 和 `python-sdk/` 本地源码。
- 安全边界：默认只做查询；支付、续费、退订、购买、取消订单、预算/财务关系变更、配额申请等动作必须先进行 Human-in-the-Loop 确认。

## 先读这些

处理本领域问题前，先阅读当前目录下的参考文档：

- `references/query-cli-catalog.md`：查询型 CLI 入口索引，按问题域路由到细分 reference。
- `references/api-coverage-matrix.md`：本分类 `cli-meta/` API 覆盖审查矩阵，列出已纳入排障候选的只读/诊断 Action 与默认排除的写操作边界。
- `references/provider-code-aliases.md`：配额中心 `ProviderCode` 速查；处理 quota 时优先读，避免参数名或产品编码试错。
- `references/python-sdk-script-patterns.md`：什么时候从 CLI 切换到 Python SDK 脚本，以及只读脚本的安全边界。
- `references/01-overview-routing/README.md`：排查总入口，按用户现象收集证据，以及计费手册和其他横向/产品手册如何分工。
- `scripts/README.md`：当前脚本状态和未来脚本入口规范。**任何 `RunSkillScript` 调用前都必须先读它或对应 reference 中的完整脚本签名，不能凭脚本名猜参数。**

同时可查阅：

- 产品手册：`火山引擎问题排查手册/火山引擎计费问题排查手册/README.md`
- 产品/Python SDK/CLI 总表：`火山引擎问题排查手册/README.md`
- 接口元数据：`cli-meta/火山引擎计费问题排查手册/<产品>/接口清单.md`
- 官方原始文档：`产品官方文档/火山引擎计费问题排查手册/<产品>/...`

## 使用边界

Use this skill when the user describes:

- `AccountOverdueError`、`BalanceNotEnough`、余额不足、欠费停服、预扣费失败、代金券不可用。
- Coding Plan、套餐、订阅、资源包、节省计划、权益、到期、续费、抵扣不生效。
- quota、调用次数耗尽、推理次数上限、安全用量上限、配额不足、资源冻结。
- 购买、开通、订单、支付、CreatePreorder、CreateOrder、商品不可购、无购买权限。
- 账单、成本分析、消费明细、账单总览、分账账单、费用突增、预算、发票。

Do not use this as the primary skill for pure IAM 策略配置、AK/SK 签名、SDK 安装、模型参数错误、ECS/TOS/CDN/VKE 等产品运行态故障。遇到这些机制问题时，保留计费上下文并转向对应横向技能或产品技能。

## 强约束

- 默认只执行查询命令。当前阶段只设计 `Describe/List/Get/Query/Check/Search` 类读接口，不设计购买、支付、退订、续费、取消订单、创建预算、创建配额申请等写操作。
- 查询优先使用 `ve <service> <Action> [--Param value...]`。`cli-meta` 里可能显示历史形态 `volcengine <service> <Action>`，在执行设计中统一写成 `ve`。
- 不执行 `ve configure`、登录、SSO、凭证写入或任何密钥管理命令。凭证只能来自运行环境，不能在 skill 中硬编码 AK/SK。
- 计费结果通常涉及敏感金额、账号、合同、发票、资源 ID。输出时只保留排障必要字段，避免泄露完整账单明细。
- 如果用户请求修复性动作，先给出将要执行的资源、Action、金额/订单影响、不可逆风险和替代方案，获得用户明确确认后再转入写操作设计。

## 交互式确认与 Human-in-the-Loop

### 概述

本 skill 默认只执行查询动作。账单、余额、订单、资源包、配额、资源归属等查询可以作为证据采集自动执行；任何可能改变资金、订单、订阅、配额申请、预算或财务关系的动作必须先获得用户明确确认。

### 需要确认的动作

| 动作类型 | 示例 | 确认要求 |
|---|---|---|
| 订单与支付 | `PayOrder`、`CommonBuy`、购买资源包、开通服务 | 说明商品、金额、账号、订单 ID、扣费方式和失败回滚边界 |
| 续费与退订 | `RenewInstance`、`UnsubscribeInstance`、`SetRenewalType` | 说明实例、周期、费用、到期时间和退订影响 |
| 预算与财务关系 | `CreateBudget`、`UpdateBudget`、财务托管/解除 | 说明影响账户、预算阈值、通知对象和组织范围 |
| 配额申请与告警变更 | `CreateQuotaApplication`、`CreateAlarmRule`、`UpdateAlarmRule` | 说明产品、地域、额度、业务必要性和审批预期 |
| 资源归属/组织变更 | 账号移动、财务关系调整、组织关系变更 | 本 skill 不直接执行；转账号/IAM 或组织管理流程并要求确认 |

## 快速路由

| 用户现象 | 优先证据 | 先查产品/工具 |
|---|---|---|
| 不确定是余额、订阅、配额、订单还是账单权限 | 错误码、RequestId、产品、账号、时间、资源 ID | [`01-overview-routing/README.md`](references/01-overview-routing/README.md) |
| 余额不足、欠费、预扣费失败 | 账户余额、代金券、预留金额、欠费状态、错误码 | [`02-balance-arrears-precharge/README.md`](references/02-balance-arrears-precharge/README.md) |
| Coding Plan、套餐、订阅、资源包不生效 | 订阅有效期、资源包范围、抵扣明细、产品/地域/规格 | [`03-subscription-package/README.md`](references/03-subscription-package/README.md) |
| quota、调用次数耗尽、推理上限 | 产品配额、配额维度、申请记录、当期用量、错误码 | [`04-usage-quota-limit/README.md`](references/04-usage-quota-limit/README.md) |
| 购买、开通、订单、支付失败 | 订单状态、商品、购买资格、余额、账号认证、购买 Action | [`05-order-purchase-activation/README.md`](references/05-order-purchase-activation/README.md) |
| 查询账单、成本、余额、费用突增 | 账期、产品、实例、用量、成本口径、分账/摊销 | [`06-bill-cost-detail/README.md`](references/06-bill-cost-detail/README.md) |
| 高频错误码或已知 case | 错误文本、产品、账号、发生时间 | [`07-playbooks/README.md`](references/07-playbooks/README.md) |

## 高频固定流程

### MaaS 月度配额 / quota

用户提到 `MaaS`、火山方舟、方舟、大模型、模型 Endpoint、API Key 或 `You have exceeded the monthly usage quota` 时，按这个顺序执行：

1. 读取 `references/provider-code-aliases.md`。
2. 直接执行：

```text
ve quota ListProductQuotas --ProviderCode MaaS
```

3. 再用 `scripts/collect_billing_context.py --region cn-beijing --include-packages` 查资源包和余额。

禁止先执行无 `ProviderCode` 的 `ve quota ListProductQuotas`，禁止执行 `--ProviderCode ark`。

### 费用突增 / 完整分页

用户提到费用突增、完整归因、全量、分页、尽量完整时，按这个模板执行：

```text
python3 scripts/collect_billing_context.py --region cn-beijing --bill-period <yyyy-MM> --include-bill-detail --include-packages --all-pages --max-pages 3 --max-results 20
```

禁止只传 `--max-results 100` 来冒充分页；没有 `--all-pages` 就不是分页查询。

## 章节目录

| 上层章节 | 本 skill reference |
|---|---|
| 1. 排查总入口 | [`01-overview-routing/README.md`](references/01-overview-routing/README.md) |
| 2. 余额、欠费与预扣费 | [`02-balance-arrears-precharge/README.md`](references/02-balance-arrears-precharge/README.md) |
| 3. 套餐、订阅与资源包 | [`03-subscription-package/README.md`](references/03-subscription-package/README.md) |
| 4. 用量、配额与调用次数 | [`04-usage-quota-limit/README.md`](references/04-usage-quota-limit/README.md) |
| 5. 购买、开通与订单失败 | [`05-order-purchase-activation/README.md`](references/05-order-purchase-activation/README.md) |
| 6. 账单、成本与消费明细 | [`06-bill-cost-detail/README.md`](references/06-bill-cost-detail/README.md) |
| 7. 计费问题 Playbook | [`07-playbooks/README.md`](references/07-playbooks/README.md) |

## 已验证易错参数

这些约束来自真实沙箱 benchmark，优先级高于通用接口命名直觉：

- 配额中心查询产品配额时，`ve quota ListProductQuotas`、`ListProductQuotaDimensions`、`GetProductQuota` 使用 `--ProviderCode <provider-code>`，不要使用 `--ProductCode`。
- 不确定产品对应的 `ProviderCode` 时，先读 `references/provider-code-aliases.md`；仍不确定再执行 `ve quota ListProducts`，不要凭产品名猜参数。
- 禁止调用缺少 `--ProviderCode` 的 `ve quota ListProductQuotas` / `GetProductQuota` / `ListQuotaApplications`。
- MaaS/火山方舟的配额中心 `ProviderCode` 是 `MaaS`。`ark` 是控制台/地域路径里的概念，不是配额中心 `ProviderCode`；不要执行 `--ProviderCode ark`。
- MaaS/火山方舟相关配额的已验证查询形态：

```text
ve quota ListProductQuotas --ProviderCode MaaS
```

用户明确提到 MaaS、火山方舟、方舟、大模型、模型 Endpoint 或 API Key 时，直接使用 `--ProviderCode MaaS`；不要先用无参数 `ListProductQuotas` 试探。

- 如果用户说的是“月度调用次数、套餐次数、模型推理上限”，配额中心正常并不代表问题结束；继续查资源包/套餐和余额，必要时转大模型生态产品 skill 判断产品侧安全上限。

## 脚本调用协议

脚本是复杂场景的提效层，不是跳过 reference 的捷径。当前提供 1 个只读 Python SDK 脚本，用于账单/资源包/费用突增这类 CLI body 查询不稳定或返回字段复杂的场景。使用脚本时必须遵守：

1. 先读取 `scripts/README.md` 或当前问题 reference 中的脚本段落，确认用途、必填参数和可选参数。
2. 只有在已拿到脚本的最小必填参数时才调用；缺参数时先向用户补问或先用 CLI 定位资源，不能先试错。
3. 脚本必须只读，只能查询余额、账单、订单、资源包、配额、资源归属，不得执行支付、购买、续费、退订或配额申请。
4. 脚本返回后，先读 `summary` 和 `findings`，再按需展开 `raw`；不要把完整账单 JSON 原样倾倒给用户。

| 脚本 | 适用入口 | 最小必填参数 | 可选参数 |
|---|---|---|---|
| `scripts/collect_billing_context.py` | 余额/欠费、订单、账单、资源包、费用突增初筛 | 无；默认使用 `--region` 或 `VOLCENGINE_REGION` | `--region`、`--bill-period <yyyy-MM>`、`--max-results <n>`、`--include-orders`、`--include-packages`、`--include-bill-detail`、`--include-raw` |

费用突增、资源包耗尽和账单归因需要尽量覆盖更多分页时，使用：

```text
python3 scripts/collect_billing_context.py --region cn-beijing --bill-period <yyyy-MM> --include-bill-detail --include-packages --all-pages --max-pages 3 --max-results 20
```

脚本会返回 `*_pagination` 字段；只有 `is_complete=true` 时才能把结果表述为“已覆盖全量”，否则只能说“已采集前 N 页/TopN 样本”。
费用中心列表接口单页上限按 100 的安全值处理；不要传 `--max-results 1000`。脚本会自动限幅并启用分页，但 Agent 应优先使用 20-100 的页大小。

用户明确说“全量、完整、分页、尽量完整、费用突增归因”时，必须带 `--all-pages`；只传 `--max-results 100` 仍然是单页样本，不满足完整分页查询。

## 工作流

1. 明确产品、账号/主子账号关系、资源 ID、订单 ID、账期、地域、错误码、RequestId、发生时间。
2. 判断这是余额/欠费、订阅/资源包、quota/调用次数、订单/购买、账单/成本，还是权限/OpenAPI/产品运行态问题。
3. 打开 `references/query-cli-catalog.md`，路由到一个细分 reference；只读取当前问题必要的 reference。
4. 如果命令不在清单里，查看对应 `cli-meta/.../<产品>/接口清单.md` 和官方文档后再补充。
5. 对跨产品问题，保留产品上下文：例如“大模型调用报 AccountOverdue”由本 skill 查余额/欠费，同时提示大模型 skill 只负责 endpoint/model/限流细节。
6. 对账单类问题，先确认账期和口径：账单、成本账单、摊销账单、分账账单、资源包抵扣明细不是同一个口径。若需要同时查询账单、订单、资源包，优先使用 `scripts/collect_billing_context.py --bill-period <yyyy-MM>` 聚合证据。
7. 对权限类表现，先确认是“用户无权查/买”，还是“账户商业状态不可用”；前者转账号/IAM skill，后者留在本 skill。
8. 输出诊断结论时分层说明：已确认事实、最可能根因、还缺哪些证据、下一步安全动作。

## 输出格式

排障回复应优先给出可执行判断，而不是堆命令：

- `现象归类`：这是哪类计费/商业状态问题。
- `已查证据`：列出关键余额、订单、订阅、资源包、配额或账单字段。
- `结论`：最可能根因，必要时给置信度。
- `建议动作`：只读补查、用户侧验证、或需要确认的变更动作。
- `横向跳转`：如果根因是 IAM、OpenAPI/Python SDK/CLI 或产品运行态，明确转到哪个横向/产品手册。
