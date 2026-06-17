# volcengine-skills

本仓库是 Volcengine Team 维护的 skill 仓库，为 AI coding agent（Claude Code / Codex / OpenCode / Cursor / Gemini CLI）提供面向**火山引擎（Volcengine）**场景的开箱即用能力。

## 仓库提供什么

- `skills/` — 按场景封装的、可被 agent 自动触发的 skill（每个 skill 一个 `volcengine-<xxx>/` 子目录）
- `hooks/` — 跨 skill 复用的 hook（session-start 注入、tool-pre 校验等），暂无
- `commands/` — slash commands，暂无
- `agents/` — subagent 配置，暂无
- `scripts/` — 仓库级辅助脚本，暂无
- `docs/` — 规范文档，暂无

> **当前状态**：已经提供 skills，会随后续陆续补充其他能力。如你在 `skills/` 下没看到想要的能力，优先检查是否已有相关 MR 在评审中。

## 什么时候用本仓库

以下场景优先在本仓库里找 skill：

- 操作火山引擎云资源：ECS / VPC / VKE / CLB / RDS / Redis / TOS / DNS / CDN 等
- 使用 `ve` 命令（Volcengine CLI）
- 读取 `VOLCENGINE_ACCESS_KEY` / `VOLCENGINE_SECRET_KEY` / `VOLCENGINE_REGION` 等鉴权变量
- 火山引擎相关的部署、监控、运维场景
- 用户消息里出现「火山」「volcengine」等关键词

## 给 Agent 的简短约束

修改或新增 skill 前：

- 所有 skill **必须**以 `volcengine-` 为前缀，读 env / 调 bin 必须在 `metadata.openclaw.requires` 声明
- 用户补充某个 API 的精确 payload、Action、Version 或服务名时，封装脚本、skill 正文、reference 和 TESTING 中的示例必须同步使用该精确值，不要保留旧的空 payload 或猜测参数。
- 跨 skill 的经验应放在“决策发生的 skill”里；工具型 skill 只保留工具自身能力、参数约束和安全边界，不承载上层部署/排障策略。
- 不要把一次验证里的具体地域、规格、镜像、镜像源候选、资源清理顺序或临时栈形状写成默认流程；除非它是 API/资源依赖的强约束，否则写成判断原则、约束和示例。
- 排障 skill 不要把可并行验证的证据项写成固定顺序 checklist；只有存在真实依赖关系时才写顺序，否则按症状、证据类型和判断分支组织。
- 提交的内容不得包含如：账号信息、AK，SK 凭证信息、本地目录、资源ID、TRN 等信息
- 有固定前缀的资源 ID 脱敏时保留真实前缀并抽象随机段，例如 `vpc-<id>`、`clb-<id>`、`task-<id>`；无固定前缀的账号或数字 ID 使用语义占位符，例如 `<account-id>`。

## 新增一个 skill 要改哪些文件

新增 `skills/volcengine-<name>/` 后，下面这些**硬编码了 skill 清单**的文件都要同步加一行，否则不同 agent 看到的清单会漂移：

- `skills/volcengine-<name>/SKILL.md` — skill 本体（frontmatter 里的 `name` / `description`）
- `README.md` — 「Skills」表格
- `README_en.md` — 「Skills」表格（英文，描述与中文对应）
- `.cursor/rules/volcengine-skills.mdc` — Available skills 列表
- `GEMINI.md` — Available skills 列表

**不需要改**：`.claude-plugin/plugin.json`、`.claude-plugin/marketplace.json`、`.codex-plugin/plugin.json`、`.opencode/opencode.json`、`gemini-extension.json` —— 这些都用 `./skills/` 整目录引用，新增 skill 会被自动发现。

> 改完后核对一遍：上面 4 个清单文件里的 skill 名称必须完全一致（含 `volcengine-` 前缀），不要出现漏项或简写。

## 当前已提供的 skill

见 [README 的 Skills 表](./README.md#skills)

## 当前已提供的 hook

> 暂无。
