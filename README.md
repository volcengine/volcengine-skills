# volcengine-skills

---
[![Volcengine SKILL & CLI Survey](img.png)](https://www.volcengine.com/survey/q/v2/7662656599489085475/q36U8r81/5ffc/channel=doc)

为提高您对火山引擎 skill 的使用体验，2026/7/27-2026/8/21 邀您参加[有奖调研](https://www.volcengine.com/survey/q/v2/7662656599489085475/q36U8r81/5ffc/channel=doc)。

---

[English](./README_en.md) | **简体中文**

火山引擎团队维护的 skill marketplace，面向 Claude Code / Codex / OpenCode / Cursor / Gemini CLI
等 AI coding agent。仓库默认只安装核心插件；其他技能按火山引擎产品域拆分为可选插件，由
`volcengine-find-skills` 统一发现和安装。

**[快速安装 →](#快速安装)**

## Plugins

| Plugin | 产品分类 | Skills | 默认安装 |
| --- | --- | --- | --- |
| `volcengine-core` | 核心 | `volcengine-cli`、`volcengine-troubleshooting`、`volcengine-knowledge-search`、`volcengine-find-skills` | 是 |
| `volcengine-elastic-compute` | 弹性计算 | `volcengine-prepare`、`volcengine-deploy`、`volcengine-iac` | 否 |
| `volcengine-storage` | 存储 | `volcengine-tosutil` | 否 |
| `volcengine-database` | 数据库 | `volcengine-db-supabase` | 否 |
| `volcengine-containers-middleware` | 容器与中间件 | `volcengine-vefaas` | 否 |
| `volcengine-security` | 安全 | `volcengine-compliance` | 否 |
| `volcengine-identity-access-control` | 身份与访问控制 | `volcengine-landing-zone` | 否 |
| `volcengine-service-support` | 服务支持 | `volcengine-api`、`volcengine-sdk-generator` | 否 |

核心插件的 marketplace 策略为 `INSTALLED_BY_DEFAULT`，其他插件均为 `AVAILABLE`。
`skills/` 下只保留 `core/` 分类，其中严格包含四个核心 skill。其他 skill 由各自的可选 plugin 直接拥有，不在 `skills/` 下保留副本。

## Skills

| Skill | Plugin | 场景 |
| --- | --- | --- |
| [`volcengine-cli`](./skills/core/volcengine-cli/SKILL.md) | `volcengine-core` | 用 `ve` CLI 创建、查询和管理云资源 |
| [`volcengine-troubleshooting`](./skills/core/volcengine-troubleshooting/SKILL.md) | `volcengine-core` | 火山引擎故障排查与诊断 |
| [`volcengine-knowledge-search`](./skills/core/volcengine-knowledge-search/SKILL.md) | `volcengine-core` | 检索火山引擎官方文档并获取全文 |
| [`volcengine-find-skills`](./skills/core/volcengine-find-skills/SKILL.md) | `volcengine-core` | 按任务或产品域查找、安装其他 skill |
| [`volcengine-prepare`](./plugins/volcengine-elastic-compute/skills/volcengine-prepare/SKILL.md) | `volcengine-elastic-compute` | 分析仓库并推荐 ECS / VKE / veFaaS 部署形态 |
| [`volcengine-deploy`](./plugins/volcengine-elastic-compute/skills/volcengine-deploy/SKILL.md) | `volcengine-elastic-compute` | 将本地目录或 Git 仓库部署到火山引擎 |
| [`volcengine-iac`](./plugins/volcengine-elastic-compute/skills/volcengine-iac/SKILL.md) | `volcengine-elastic-compute` | 使用 Terraform 编排火山引擎基础设施 |
| [`volcengine-tosutil`](./plugins/volcengine-storage/skills/volcengine-tosutil/SKILL.md) | `volcengine-storage` | 管理 TOS 对象存储资源 |
| [`volcengine-db-supabase`](./plugins/volcengine-database/skills/volcengine-db-supabase/SKILL.md) | `volcengine-database` | 管理 AI 原生 BaaS 平台 Supabase 版（AIDAP） |
| [`volcengine-vefaas`](./plugins/volcengine-containers-middleware/skills/volcengine-vefaas/SKILL.md) | `volcengine-containers-middleware` | 部署和管理 veFaaS Serverless 应用 |
| [`volcengine-compliance`](./plugins/volcengine-security/skills/volcengine-compliance/SKILL.md) | `volcengine-security` | 推荐合规基线、汇总态势并编写自定义规则 |
| [`volcengine-landing-zone`](./plugins/volcengine-identity-access-control/skills/volcengine-landing-zone/SKILL.md) | `volcengine-identity-access-control` | Landing Zone、账号工厂与治理基线 |
| [`volcengine-api`](./plugins/volcengine-service-support/skills/volcengine-api/SKILL.md) | `volcengine-service-support` | 查询 API 参数、错误码和返回结构 |
| [`volcengine-sdk-generator`](./plugins/volcengine-service-support/skills/volcengine-sdk-generator/SKILL.md) | `volcengine-service-support` | 生成可运行的多语言 SDK 示例 |

## 默认安装

### Finder 设计

`volcengine-find-skills` 内置唯一 catalog，覆盖四个 core skill 和所有可选 plugin skill：

1. `search` 只做无副作用检索，按名称、产品域、摘要和中英文关键词加权排序。
2. 安装前必须解析为精确的 skill 或 plugin 名称；模糊结果不会直接触发安装。
3. Codex 安装目标 skill 所属的 plugin；通用 skills CLI 安装精确 skill 集合。
4. 安装命令成功后再次读取宿主安装清单，只有目标全部可见才返回 `verified: true`。
5. plugin 安装后需新开对话，避免把“已安装”误判为“当前对话已加载”。

### Codex

添加 marketplace 后只安装核心插件：

```bash
codex plugin marketplace add volcengine/volcengine-skills
codex plugin add volcengine-core@volcengine-skills
```

在新对话中直接描述需求，例如“查找对象存储相关 skill”或“安装 `volcengine-tosutil`”。finder 会先给出
匹配结果，再安装所属插件。Codex 安装新插件后需要新开对话，当前对话不会动态加载新增 skill。

在源码仓库内也可以直接验证发现结果：

```bash
python3 plugins/volcengine-core/skills/volcengine-find-skills/scripts/find_skills.py search "对象存储"
python3 plugins/volcengine-core/skills/volcengine-find-skills/scripts/find_skills.py status
```

### 通用 skills CLI

下面的命令只安装四个核心 skill，不会默认安装可选产品域 skill：

```bash
npx skills add volcengine/volcengine-skills \
  --global --yes --copy --full-depth \
  --skill volcengine-cli volcengine-troubleshooting volcengine-knowledge-search volcengine-find-skills
```

后续可由 finder 调用 `npx skills add` 安装单个 skill，也可以交互式选择：

```bash
npx skills add volcengine/volcengine-skills --full-depth
```

### Claude Code

```text
/plugin marketplace add volcengine/volcengine-skills
/plugin install volcengine-core@volcengine-skills
/reload-plugins
```

### Gemini CLI

```bash
gemini extensions install https://github.com/volcengine/volcengine-skills
```

### OpenCode

按 [OpenCode 安装说明](./.opencode/INSTALL.md) 挂载核心插件的 `skills/` 目录。

### Cursor

```text
/add-plugin volcengine-core@https://github.com/volcengine/volcengine-skills
```

## 目录结构

```text
volcengine-skills/
├── skills/
│   └── core/                         # 仅四个核心 skill
├── plugins/
│   ├── volcengine-core/              # 默认核心 plugin，复制 skills/core
│   └── volcengine-<domain>/          # 可选 plugin，也是其 skill 的唯一源码
└── .agents/plugins/marketplace.json
```

`skills/core/` 是四个核心 skill 的规范源码；可选 skill 直接在所属 plugin 中维护。同步脚本只复制 core、生成 manifest 和 marketplace。修改或新增 skill 后运行：

```bash
python3 scripts/sync_plugins.py
python3 scripts/validate_codex_plugin_layout.py
python3 -m unittest discover -s tests -v
```

## License

MIT，见 [LICENSE](./LICENSE)。
