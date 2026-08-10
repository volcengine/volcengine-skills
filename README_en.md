# volcengine-skills

---
[![Volcengine SKILL & CLI Survey](img.png)](https://www.volcengine.com/survey/q/v2/7662656599489085475/q36U8r81/5ffc/channel=doc)

To improve your experience with Volcengine skill, we invite you to participate in our [Survey with Prizes](https://www.volcengine.com/survey/q/v2/7662656599489085475/q36U8r81/5ffc/channel=doc) from July 27 to August 21, 2026.

---

**English** | [简体中文](./README.md)

A skill marketplace maintained by the Volcengine team for AI coding agents including Claude Code,
Codex, OpenCode, Cursor, and Gemini CLI. Only the core plugin is installed by default. Optional
skills are grouped into Volcengine product-domain plugins and discovered through
`volcengine-find-skills`.

**[Quick Install →](#quick-install)**

## Plugins

| Plugin | Product domain | Skills | Default |
| --- | --- | --- | --- |
| `volcengine-core` | Core | `volcengine-cli`, `volcengine-troubleshooting`, `volcengine-knowledge-search`, `volcengine-find-skills` | Yes |
| `volcengine-storage` | Storage | `volcengine-tosutil` | No |
| `volcengine-database` | Database | `volcengine-db-supabase` | No |
| `volcengine-containers-middleware` | Containers and Middleware | `volcengine-vefaas` | No |
| `volcengine-security` | Security | `volcengine-compliance` | No |
| `volcengine-identity-access-control` | Identity and Access Control | `volcengine-landing-zone` | No |
| `volcengine-service-support` | Service Support | `volcengine-prepare`, `volcengine-deploy`, `volcengine-iac`, `volcengine-api`, `volcengine-sdk-generator` | No |

The core marketplace entry uses `INSTALLED_BY_DEFAULT`; all optional plugins use `AVAILABLE`.
`skills/` contains only the `core/` category, with exactly four core skills. Every optional skill
is owned directly by its product-domain plugin and has no duplicate under `skills/`.

## Skills

| Skill | Plugin | Use case |
| --- | --- | --- |
| [`volcengine-cli`](./skills/core/volcengine-cli/SKILL.md) | `volcengine-core` | Create, query, and manage cloud resources with the `ve` CLI |
| [`volcengine-troubleshooting`](./skills/core/volcengine-troubleshooting/SKILL.md) | `volcengine-core` | Diagnose Volcengine errors and resource issues |
| [`volcengine-knowledge-search`](./skills/core/volcengine-knowledge-search/SKILL.md) | `volcengine-core` | Search and retrieve full official Volcengine documentation |
| [`volcengine-find-skills`](./skills/core/volcengine-find-skills/SKILL.md) | `volcengine-core` | List every skill for the agent to select and install |
| [`volcengine-prepare`](./plugins/volcengine-service-support/skills/volcengine-prepare/SKILL.md) | `volcengine-service-support` | Analyze a repository and recommend ECS, VKE, or veFaaS |
| [`volcengine-deploy`](./plugins/volcengine-service-support/skills/volcengine-deploy/SKILL.md) | `volcengine-service-support` | Deploy a local directory or Git repository to Volcengine |
| [`volcengine-iac`](./plugins/volcengine-service-support/skills/volcengine-iac/SKILL.md) | `volcengine-service-support` | Manage Volcengine infrastructure with Terraform |
| [`volcengine-tosutil`](./plugins/volcengine-storage/skills/volcengine-tosutil/SKILL.md) | `volcengine-storage` | Manage TOS object storage resources |
| [`volcengine-db-supabase`](./plugins/volcengine-database/skills/volcengine-db-supabase/SKILL.md) | `volcengine-database` | Manage Volcengine AI-native BaaS, Supabase edition (AIDAP) |
| [`volcengine-vefaas`](./plugins/volcengine-containers-middleware/skills/volcengine-vefaas/SKILL.md) | `volcengine-containers-middleware` | Deploy and manage veFaaS serverless applications |
| [`volcengine-compliance`](./plugins/volcengine-security/skills/volcengine-compliance/SKILL.md) | `volcengine-security` | Recommend baselines, report posture, and author custom rules |
| [`volcengine-landing-zone`](./plugins/volcengine-identity-access-control/skills/volcengine-landing-zone/SKILL.md) | `volcengine-identity-access-control` | Set up landing zones, account factories, and governance baselines |
| [`volcengine-api`](./plugins/volcengine-service-support/skills/volcengine-api/SKILL.md) | `volcengine-service-support` | Query API parameters, errors, and response schemas |
| [`volcengine-sdk-generator`](./plugins/volcengine-service-support/skills/volcengine-sdk-generator/SKILL.md) | `volcengine-service-support` | Generate runnable SDK examples in supported languages |

## Default Installation

### Finder Design

`volcengine-find-skills` embeds the single catalog for all four core skills and every optional
plugin skill:

1. `list` returns the complete catalog so the agent can select the minimum skill set from names,
   product domains, summaries, and keywords.
2. Installation requires an exact skill or plugin name.
3. Codex installs the owning plugin, while the generic skills CLI installs the exact skill set.
4. After the installer exits successfully, the finder reads the host's installed list and returns
   `verified: true` only when every requested skill is visible.
5. Plugin-based hosts require a new thread so installed state is not confused with current-thread loading.

### Codex

Add the marketplace and install only the core plugin:

```bash
codex plugin marketplace add volcengine/volcengine-skills
codex plugin add volcengine-core@volcengine-skills
```

In a new thread, ask for a skill by task, such as "find the object storage skill" or "install
`volcengine-tosutil`". The finder reads the complete catalog, selects the appropriate skill, and
installs its owning plugin. Start another new thread after installation because a running Codex
thread does not dynamically load new skills.

From a source checkout, discovery and status can be tested directly:

```bash
python3 plugins/volcengine-core/skills/volcengine-find-skills/scripts/find_skills.py list
python3 plugins/volcengine-core/skills/volcengine-find-skills/scripts/find_skills.py status
```

### Generic skills CLI

This command installs only the four core skills:

```bash
npx skills add volcengine/volcengine-skills \
  --global --yes --copy --full-depth \
  --skill volcengine-cli volcengine-troubleshooting volcengine-knowledge-search volcengine-find-skills
```

The finder can later invoke `npx skills add` for one skill, or users can choose interactively:

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

Follow the [OpenCode instructions](./.opencode/INSTALL.md) to mount the core plugin's `skills/`
directory.

### Cursor

```text
/add-plugin volcengine-core@https://github.com/volcengine/volcengine-skills
```

## Directory Structure

```text
volcengine-skills/
├── skills/
│   └── core/                         # exactly four core skills
├── plugins/
│   ├── volcengine-core/              # default plugin, copied from skills/core
│   └── volcengine-<domain>/          # optional plugin and authoritative skill source
└── .agents/plugins/marketplace.json
```

`skills/core/` is authoritative for the four core skills. Optional skills are maintained directly
inside their owning plugins. The sync script copies core and generates manifests and marketplaces.
After changing or adding a skill, run:

```bash
python3 scripts/sync_plugins.py
python3 scripts/validate_codex_plugin_layout.py
python3 -m unittest discover -s tests -v
```

## License

MIT. See [LICENSE](./LICENSE).
