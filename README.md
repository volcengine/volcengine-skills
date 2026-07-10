# volcengine-skills

[English](./README_en.md) | **简体中文**

火山引擎团队维护的 skill 仓库，面向火山引擎（Volcengine）使用场景，为 Claude Code / Codex / OpenCode / Cursor / Gemini CLI 等 agent 提供开箱即用的 skills。

**[快速安装 →](#快速安装)**

## 仓库包含什么

### Skills

| Skill | 场景 |
| --- | --- |
| `volcengine-cli` | 用 `ve` CLI 创建/查询/管理云资源（ECS/VPC/CLB/RDS/Redis/TOS 等） |
| `volcengine-prepare` | 分析本地目录或 GitHub 仓库，推荐部署形态（ECS/VKE/veFaaS） |
| `volcengine-deploy` | 把本地目录或 GitHub 仓库部署到火山引擎 |
| `volcengine-iac` | 基于 Terraform 的火山引擎基础设施编排 |
| `volcengine-api` | 查询火山引擎 API 规格（参数、错误码、返回结构等） |
| `volcengine-sdk-generator` | 生成可运行的火山引擎 SDK 示例，并按需回答 SDK 配置问题 |
| `volcengine-tosutil` | 管理火山引擎 TOS 对象存储资源 |
| `volcengine-vefaas` | 部署与管理火山引擎 veFaaS serverless 应用 |
| `volcengine-supabase` | 管理火山引擎 AIDAP 数据库 workspace（Supabase / PostgreSQL），并作为部署数据库方案 |
| `volcengine-troubleshooting` | 火山引擎故障排查与诊断 |
| `volcengine-knowledge-search` | 检索火山引擎官方文档并获取全文（产品概念/用法/计费/部署/最佳实践/服务条款等） |
| `volcengine-landing-zone` | 火山引擎 Landing Zone 咨询、初始化搭建、账号工厂与基线配置 |

## 快速安装

### 前置依赖

#### 安装 ve 和 vefaas

```bash
npm i -g @volcengine/cli
npm i -g https://vefaas-cli.tos-cn-beijing.volces.com/volcengine-vefaas-latest.tgz
```

#### 安装 tosutil

见 [安装命令](./skills/volcengine-tosutil/SKILL.md#安装命令)

### 通用安装

```bash
# 以下三条任选其一

# 1) 推荐：全局安装、跳过所有确认提示
npx skills add volcengine/volcengine-skills --global --yes

# 2) 交互式：手动选择安装范围（global/project）、目标 agent 和具体 skill
npx skills add volcengine/volcengine-skills

# 3) 只装到指定 agent，并用复制代替软链（如安装到 Claude Code）
npx skills add volcengine/volcengine-skills --global --yes --agent claude-code --copy

# 或手动复制
# 将 skills/ 目录复制到 ~/.claude/skills/ (适用于 Claude Code)
# 将 skills/ 目录复制到 ~/.agents/skills/ (适用于 codex 等)
```

### Claude Code

**添加 marketplace**（仅首次）：

```bash
/plugin marketplace add volcengine/volcengine-skills
```

**安装并重新加载 plugin**：

```bash
/plugin install volcengine@volcengine-skills
/reload-plugins
```

**更新**：

```bash
/plugin marketplace update volcengine-skills
```

### Codex

```bash
codex plugin marketplace add volcengine/volcengine-skills
```

```text
然后进入 Codex，执行 /plugins，选择 volcengine-skills 安装即可
```

### Gemini CLI

```bash
gemini extensions install https://github.com/volcengine/volcengine-skills
```

### OpenCode

直接在 OpenCode 中输入：

```text
Fetch and follow instructions from https://github.com/volcengine/volcengine-skills/blob/main/.opencode/INSTALL.md
```

### Cursor

在 Cursor Agent 聊天中输入：

```text
/add-plugin volcengine-skills@https://github.com/volcengine/volcengine-skills
```

## 目录结构

```
volcengine-skills/
├── skills/                 # 所有的 skill
├── .claude-plugin/         # Claude Code plugin / marketplace manifest
├── .codex-plugin/          # Codex plugin / marketplace manifest
├── .opencode/              # OpenCode 配置
├── .cursor/                # Cursor 规则
└── gemini-extension.json   # Gemini CLI 扩展清单
```

## License

MIT — 见 [LICENSE](./LICENSE)
