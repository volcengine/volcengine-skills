# volcengine-skills

**English** | [简体中文](./README.md)

A skills repository maintained by the Volcengine team, targeting Volcengine use cases and providing out-of-the-box skills for agents such as Claude Code / Codex / OpenCode / Cursor / Gemini CLI.

**[Quick Install →](#quick-install)**

## What's Included

### Skills

| Skill | Use case |
| --- | --- |
| `volcengine-cli` | Create/query/manage cloud resources via the `ve` CLI (ECS/VPC/CLB/RDS/Redis/TOS, etc.) |
| `volcengine-prepare` | Analyze a local directory or GitHub repo and recommend a deployment shape (ECS/VKE/veFaaS) |
| `volcengine-deploy` | Deploy a local directory or GitHub repo to Volcengine |
| `volcengine-iac` | Terraform-based infrastructure orchestration for Volcengine |
| `volcengine-api` | Query Volcengine API specs (parameters, error codes, response structures, etc.) |
| `volcengine-sdk-generator` | Generate runnable Volcengine SDK examples and answer SDK config questions on demand |
| `volcengine-tosutil` | Manage Volcengine TOS object storage resources |
| `volcengine-vefaas` | Deploy and manage Volcengine veFaaS serverless applications |
| `volcengine-db-supabase` | Manage Volcengine AI-native BaaS (Supabase edition / AIDAP): workspaces, branches, SQL, Auth, Realtime, Edge Functions, Storage, frontend hosting, type generation; also the deployment database provider |
| `volcengine-troubleshooting` | Troubleshoot and diagnose Volcengine issues |
| `volcengine-knowledge-search` | Search Volcengine official docs and fetch full text (product concepts/usage/billing/deploy/best practices/terms) |
| `volcengine-landing-zone` | Consult, set up, and manage a Volcengine Landing Zone, including initial setup, account factory, and baselines |
| `volcengine-compliance` | Volcengine compliance best-practice assistant: recommends which official built-in compliance baselines to enable based on the user's needs (flagging already-enabled ones), and summarizes the account's current compliance posture into an overview report grouped by category and severity; when built-in baselines don't cover a case, guides authoring a Rego policy as a custom compliance rule and registering it for evaluation; can deploy a recommended template as a conformance pack after confirmation (write ops require explicit confirmation) |

## Quick Install

### Prerequisites

#### Install ve and vefaas

```bash
npm i -g @volcengine/cli
npm i -g https://vefaas-cli.tos-cn-beijing.volces.com/volcengine-vefaas-latest.tgz
```

#### Install tosutil

See [installation commands](./skills/volcengine-tosutil/SKILL.md#安装命令).

### Generic Install

```bash
# Choose one of the following three

# 1) Recommended: install globally, skip all confirmation prompts
npx skills add volcengine/volcengine-skills --global --yes

# 2) Interactive: manually choose scope (global/project), target agents, and specific skills
npx skills add volcengine/volcengine-skills

# 3) Install to specific agents only, copying files instead of symlinking (eg. Claude Code)
npx skills add volcengine/volcengine-skills --global --yes --agent claude-code --copy

# Or copy manually
# Copy the skills/ directory to ~/.claude/skills/ (for Claude Code)
# Copy the skills/ directory to ~/.agents/skills/ (for Codex, etc.)
```

### Claude Code

**Add the marketplace** (first time only):

```bash
/plugin marketplace add volcengine/volcengine-skills
```

**Install and reload the plugin**:

```bash
/plugin install volcengine@volcengine-skills
/reload-plugins
```

**Update**:

```bash
/plugin marketplace update volcengine-skills
```

### Codex

```bash
codex plugin marketplace add volcengine/volcengine-skills
```

```text
Then open Codex, run /plugins, and select volcengine-skills to install.
```

### Gemini CLI

```bash
gemini extensions install https://github.com/volcengine/volcengine-skills
```

### OpenCode

Type the following directly in OpenCode:

```text
Fetch and follow instructions from https://github.com/volcengine/volcengine-skills/blob/main/.opencode/INSTALL.md
```

### Cursor

Type the following in the Cursor Agent chat:

```text
/add-plugin volcengine-skills@https://github.com/volcengine/volcengine-skills
```

## Directory Structure

```
volcengine-skills/
├── skills/                 # All skills
├── .claude-plugin/         # Claude Code plugin / marketplace manifest
├── .codex-plugin/          # Codex plugin / marketplace manifest
├── .opencode/              # OpenCode configuration
├── .cursor/                # Cursor rules
└── gemini-extension.json   # Gemini CLI extension manifest
```

## License

MIT — see [LICENSE](./LICENSE)
