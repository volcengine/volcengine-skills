---
name: volcengine-find-skills
description: >-
  Find, compare, and install Volcengine skills from the volcengine-skills marketplace. Use when a
  user asks which Volcengine skill or plugin handles a task, wants to browse skills by official
  product domain, needs an optional skill that is not currently installed, or asks to install or
  check the installation status of a Volcengine skill. Also use to discover any of the four core
  skills, including this finder.
license: MIT
metadata:
  openclaw:
    requires:
      bins:
        - python3
      anyBins:
        - codex
        - npx
---

# Volcengine Skills Finder

Use the bundled catalog to resolve a request to an exact skill and owning plugin. Never guess a
plugin name from memory when the catalog can answer it.

## Decision flow

1. Search the catalog without changing installation state.
2. Rank matches from names, product domains, summaries, and Chinese/English keywords.
3. Require an exact skill or plugin name before installation. If multiple matches remain plausible,
   show them and ask the user to choose.
4. Map a skill to its owning plugin. Core skills map to `volcengine-core`; optional skills map to
   their product-domain plugin.
5. Install through the host-specific method and verify the resulting installed state. Never report
   success from process exit alone.
6. For plugin-based hosts, tell the user to start a new thread before using a newly installed skill.

## Find a skill

Run the script relative to this skill directory:

```bash
python3 scripts/find_skills.py search "<task or product>"
python3 scripts/find_skills.py list
python3 scripts/find_skills.py info <skill-or-plugin>
```

Search accepts Chinese or English product names, task descriptions, skill names, and plugin names.
Show the closest matches with their product domain and owning plugin. If more than one result is
plausible, ask the user to choose before installing anything.

The catalog includes all four skills in `skills/core/` and every optional skill owned directly by a
product-domain plugin. A zero-result search means the repository does not currently provide a
matching skill; do not invent one.

## Install for Codex

For Codex, install the owning plugin through the configured `volcengine-skills` marketplace:

```bash
python3 scripts/find_skills.py install <skill-or-plugin> --method codex
```

The script checks that the marketplace is configured, skips an already-installed plugin, runs
`codex plugin add`, and verifies the installed state. If the marketplace is missing, report the
exact setup command emitted by the script instead of claiming installation succeeded.

After a successful Codex install, tell the user to start a new thread. A running thread does not
dynamically acquire newly installed skills.

## Install for other agents

For Claude Code, Cursor, OpenCode, Gemini CLI, or another host supported by the `skills` CLI, install
the selected skill directly:

```bash
python3 scripts/find_skills.py install <skill-or-plugin> --method skills --agent <agent-name>
```

This method uses `npx skills add` with `--full-depth` because optional skills live inside plugin
directories. It verifies the selected names with `skills list` after installation. Omit `--agent`
only when host auto-detection is intended.

Use `--scope global` for user-level installation or `--scope project` for the current project. The
default is global. `--source` may point at a reviewed local checkout or another repository source;
otherwise the catalog's official repository is used.

Use `--dry-run` before either installation method when the user asks to inspect the command first.
Installation is local, but any later cloud-resource operation remains governed by the installed
skill's own confirmation and safety rules.

## Check status

For Codex, inspect all marketplace plugins and their installed state:

```bash
python3 scripts/find_skills.py status
```

Do not equate "plugin installed" with "skill loaded in this thread". Use the status only to verify
installation; use a new thread to exercise the newly installed skill.
