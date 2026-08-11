# 火山引擎平台账号与权限排障技能

这是面向火山引擎全平台账号、身份、IAM、角色、STS、AccessKey 和产品资源权限问题的横向 skill。它回答的是“谁在以什么身份，对哪个 Action/Resource 被拒绝”，不是替代产品 skill 解释 ECS、TOS、CDN、大模型等产品自身运行态。

## 上层信息

- 手册定位：处理账号状态、实名认证/风控、IAM 子用户策略、角色扮演、临时凭证、AccessKey、项目/资源级授权和产品侧 `AccessDenied`。
- 横向分工：产品 skill 负责保留用户场景与资源语义；本 skill 负责身份、策略、角色链和授权范围判断；计费 skill 负责欠费/商业状态；OpenAPI skill 负责签名、SDK、CLI 机制。
- 工具优先级：优先 `ve` 查询 CLI；复杂“主体 -> 组 -> 策略 -> 项目”联动后续可用 Python SDK 脚本聚合。
- 数据来源：产品手册、`火山引擎问题排查手册/README.md`、`cli-meta/`、`产品官方文档/`、`cli/`、`python-sdk/`。
- 安全边界：默认只读；创建用户、创建密钥、附加策略、修改角色、变更组织关系等都必须 Human-in-the-Loop。

## 先读这些

- `references/query-cli-catalog.md`：按问题域路由查询 CLI。
- `references/api-coverage-matrix.md`：本分类 `cli-meta/` API 覆盖审查矩阵，列出已纳入排障候选的只读/诊断 Action 与默认排除的写操作边界。
- `references/python-sdk-script-patterns.md`：什么时候从 CLI 切到脚本。
- `references/01-overview-routing/README.md`：总入口和横向分工。
- `scripts/README.md`：当前脚本状态与脚本入口规范。

同时可查：

- 产品手册：`火山引擎问题排查手册/火山引擎平台账号与权限问题排查手册/README.md`
- 接口元数据：`cli-meta/火山引擎平台账号与权限问题排查手册/<产品>/接口清单.md`
- 官方文档：`产品官方文档/火山引擎平台账号与权限问题排查手册/<产品>/...`

## 使用边界

Use this skill when the user describes:

- `AccessDenied`、`NoPermission`、`IAM无权限诊断`、子用户没有权限、策略不生效。
- `AssumeRole`、`RoleNotExist`、服务角色不存在、STS 临时凭证过期或权限不足。
- 查询当前身份、AccessKey、账号下用户/角色/策略、项目授权。
- 实名认证异常、风控拦截、账号状态异常。
- 产品操作报权限错误，需要判断是 IAM、项目、角色还是产品资源权限。

Do not use this as the primary skill for:

- 纯签名错误、SDK 安装、CLI 参数错误：转 OpenAPI / SDK / CLI skill。
- 余额不足、欠费、套餐到期：转计费 skill。
- 产品自身故障、资源状态异常：产品 skill 主导，本 skill 只补权限机制。

## 强约束

- 默认只执行查询动作：`Get/List/Describe/Search`。
- 命令统一写成 `ve <service> <Action> [--Param value...]`。
- 不执行 `ve configure`、登录、SSO、凭证写入。
- 不创建/删除用户、密钥、角色、策略，不附加/解绑策略，不修改组织关系。
- 输出最小必要身份和权限证据，不泄露完整策略文档、完整 AK 或敏感联系人信息。
- `ListAccessKeys`、`GetAccessKeyLastUsed` 等密钥相关查询的原始 JSON 不能整段贴给用户；`AccessKeyId` 必须脱敏，只保留前 4 位和后 4 位或仅保留末 4 位，`SecretAccessKey`/`SecretKey` 一律不得输出。

## 交互式确认与 Human-in-the-Loop

| 动作类型 | 示例 | 确认要求 |
|---|---|---|
| 用户/组/角色管理 | `CreateUser`、`DeleteUser`、`CreateRole`、`UpdateRole` | 说明目标主体、影响范围、回滚边界 |
| 策略授权 | `AttachUserPolicy`、`AttachRolePolicy`、`AttachPolicyInProject` | 说明主体、策略、资源范围、最小授权理由 |
| AccessKey 管理 | `CreateAccessKey`、`DeleteAccessKey`、`UpdateAccessKey` | 说明密钥归属、轮转风险和不可回显原则 |
| 组织/控制台权限 | `EnableConsoleLogin`、`MoveAccount`、SCP 变更 | 说明组织影响面，默认不在本 skill 直接执行 |

## 快速路由

| 用户现象 | 优先证据 | 必读 reference |
|---|---|---|
| 不确定是谁在调用、当前凭证属于谁 | Caller identity、主体类型、账号 ID | [`01-overview-routing/README.md`](references/01-overview-routing/README.md) |
| 实名认证异常、风控拦截、账号状态不同步 | 错误文本、主体账号、产品开通状态 | [`02-account-verification-risk/README.md`](references/02-account-verification-risk/README.md) |
| 子用户无权限、策略不生效、IAM 无权限诊断 | 用户、组、已附加策略、Action/Resource/Project | [`03-iam-user-policy/README.md`](references/03-iam-user-policy/README.md) |
| `AssumeRole`、`RoleNotExist`、服务角色 | 角色存在性、信任关系、附加策略、临时凭证 | [`04-role-sts/README.md`](references/04-role-sts/README.md) |
| ECS/TOS/CDN/大模型等产品操作报权限错 | 产品 Action、资源 ID、项目、产品资源模型 | [`05-product-resource-access/README.md`](references/05-product-resource-access/README.md) |
| 创建/查看 AccessKey、AK 归属问题 | 当前主体、密钥列表、最近使用时间 | [`06-access-key/README.md`](references/06-access-key/README.md) |
| 高频错误码、标准卡片 | 原始错误文本 | [`07-playbooks/README.md`](references/07-playbooks/README.md) |

## 高频固定流程

### 权限报错总入口

先识别调用主体，不要一上来猜策略：

```text
ve sts GetCallerIdentity
```

然后抽取四元组：

1. `Principal`：主账号、IAM 用户、Role、STS。
2. `Action`：失败 API Action。
3. `Resource`：资源 ID / TRN / Project。
4. `Condition`：Region、Project、IP、组织或服务角色。

### IAM 子用户策略链

拿到 `UserName` 后，按最小链路查：

```text
ve iam GetUser --UserName <user-name>
ve iam ListAttachedUserPolicies --UserName <user-name>
ve iam ListGroupsForUser --UserName <user-name>
```

如果用户走组授权，再查组策略；不要只看直绑策略就下结论。

## 章节目录

| 上层章节 | 本 skill reference |
|---|---|
| 1. 排查总入口 | [`01-overview-routing/README.md`](references/01-overview-routing/README.md) |
| 2. 账号与实名认证状态 | [`02-account-verification-risk/README.md`](references/02-account-verification-risk/README.md) |
| 3. IAM 子账号与策略权限 | [`03-iam-user-policy/README.md`](references/03-iam-user-policy/README.md) |
| 4. 角色与 STS 授权 | [`04-role-sts/README.md`](references/04-role-sts/README.md) |
| 5. 产品资源访问权限 | [`05-product-resource-access/README.md`](references/05-product-resource-access/README.md) |
| 6. API Key / AccessKey 管理权限 | [`06-access-key/README.md`](references/06-access-key/README.md) |
| 7. 权限问题 Playbook | [`07-playbooks/README.md`](references/07-playbooks/README.md) |

## 脚本调用协议

当前首版以 CLI 为主。只有在需要把用户、组、策略、项目授权和角色链批量聚合时，才补 Python 脚本。脚本必须：

1. 先读 `scripts/README.md`。
2. 只做查询。
3. 优先读取 `VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、`VOLCENGINE_SESSION_TOKEN`。
4. 输出 `summary`、`findings`、`raw`，并避免完整策略文档原样回显。

## 工作流

1. 收集 RequestId、错误码、原始错误文本、Action、Service、Resource、Region、Project。
2. 用 `GetCallerIdentity` 确认当前凭证代表谁。
3. 判断属于账号状态、IAM 用户策略、角色/STS、产品资源权限还是 AccessKey 管理。
4. 路由到一个章节 reference，只执行当前问题需要的最小命令集合。
5. 如果是产品场景里的权限错，保留产品 skill 作为主入口，本 skill 只解释授权机制。
6. 输出时分开写：已确认事实、最可能缺口、仍缺哪些证据、最小授权建议、需要横向跳转的位置。

## 输出格式

- `现象归类`
- `调用主体`
- `已查证据`
- `结论`
- `最小授权建议`
- `横向跳转`
