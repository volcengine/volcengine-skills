---
name: volcengine-find-skills
description: >-
  List, select, and install Volcengine skills from the volcengine-skills marketplace. Use when a
  user asks which Volcengine skill or plugin handles a task, wants to browse every available skill,
  needs an optional skill that is not currently installed, or asks to install or check the
  installation status of a Volcengine skill. Also use to discover any of the four core skills,
  including this finder.
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

Use the bundled catalog to inspect every available skill, select the minimum skill set that covers
the request, and resolve each selected skill to its owning plugin.

## Decision flow

1. List the complete catalog without changing installation state.
2. Inspect every name, product domain, summary, and keyword, then select the minimum exact skill set
   that covers the user's request. Make the selection directly when the catalog provides enough
   information.
3. Map each selected skill to its owning plugin. Core skills map to `volcengine-core`; optional
   skills map to their product-domain plugin.
4. Install through the host-specific method and verify the resulting installed state. Never report
   success from process exit alone.
5. For plugin-based hosts, tell the user to start a new thread before using a newly installed skill.

## List and select skills

Run the script relative to this skill directory:

```bash
python3 scripts/find_skills.py list
python3 scripts/find_skills.py list --json
python3 scripts/find_skills.py info <skill-or-plugin>
```

Always read the complete `list` output before selecting a skill. Use `--json` when keywords or the
English summaries help distinguish related skills. Choose by responsibility rather than name alone;
install multiple skills only when the request crosses distinct responsibilities.

The catalog includes all four skills in `skills/core/` and every optional skill owned directly by a
product-domain plugin. If none of the listed responsibilities covers the request, report that the
repository does not currently provide a matching skill.

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
