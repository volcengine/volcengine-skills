#!/usr/bin/env python3
"""List the Volcengine skills catalog and install exact skills."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = SKILL_ROOT / "references" / "catalog.json"
ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def fail(message: str, code: int = 2) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def load_catalog() -> dict[str, Any]:
    try:
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"catalog not found: {CATALOG_PATH}")
    except json.JSONDecodeError as exc:
        fail(f"invalid catalog JSON: {exc}")
    if catalog.get("schema_version") != 1 or not isinstance(
        catalog.get("plugins"), list
    ):
        fail("unsupported or malformed catalog")
    return catalog


def iter_records(catalog: dict[str, Any]):
    for plugin in catalog["plugins"]:
        for skill in plugin["skills"]:
            yield {
                **skill,
                "plugin": plugin["name"],
                "plugin_display_name": plugin["display_name"],
                "domain": plugin["domain"],
                "domain_en": plugin["domain_en"],
                "default_plugin": bool(plugin.get("default")),
            }


def plugin_by_name(catalog: dict[str, Any], name: str) -> dict[str, Any] | None:
    return next(
        (plugin for plugin in catalog["plugins"] if plugin["name"] == name), None
    )


def resolve_target(
    catalog: dict[str, Any], target: str
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    plugin = plugin_by_name(catalog, target)
    if plugin:
        records = [
            record for record in iter_records(catalog) if record["plugin"] == target
        ]
        return plugin, records
    exact = [record for record in iter_records(catalog) if record["name"] == target]
    if exact:
        owner = plugin_by_name(catalog, exact[0]["plugin"])
        assert owner is not None
        return owner, exact
    skill_names = ", ".join(record["name"] for record in iter_records(catalog))
    plugin_names = ", ".join(plugin["name"] for plugin in catalog["plugins"])
    fail(
        f"target must be an exact skill or plugin name: {target!r}\n"
        f"Valid skills: {skill_names}\n"
        f"Valid plugins: {plugin_names}"
    )


def resolve_skills(
    catalog: dict[str, Any], targets: list[str]
) -> list[dict[str, Any]]:
    records_by_name = {record["name"]: record for record in iter_records(catalog)}
    invalid = [target for target in targets if target not in records_by_name]
    if invalid:
        valid_names = ", ".join(records_by_name)
        fail(
            "install targets must be exact skill names; plugins are not install targets: "
            f"{', '.join(invalid)}\nValid skills: {valid_names}"
        )
    return [records_by_name[name] for name in dict.fromkeys(targets)]


def output_records(records: list[dict[str, Any]], as_json: bool) -> None:
    if as_json:
        print(json.dumps(records, ensure_ascii=False, indent=2))
        return
    if not records:
        print("No Volcengine skills are catalogued.")
        return
    for record in records:
        print(
            f"{record['name']}\n"
            f"  domain: {record['domain']} / {record['domain_en']}\n"
            f"  plugin: {record['plugin']}\n"
            f"  {record['summary_zh']}"
        )


def run_json(
    command: list[str], attempts: int = 3
) -> tuple[subprocess.CompletedProcess[str], Any | None]:
    completed: subprocess.CompletedProcess[str] | None = None
    for _ in range(attempts):
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
        if completed.returncode != 0:
            return completed, None
        try:
            return completed, json.loads(completed.stdout)
        except json.JSONDecodeError:
            continue
    assert completed is not None
    return completed, None


def installed_skill_names(
    catalog: dict[str, Any], agent: str | None, scope: str
) -> set[str]:
    command = ["npx", "--yes", "skills", "list"]
    if scope == "global":
        command.append("--global")
    if agent:
        command.extend(["--agent", agent])

    completed, payload = run_json([*command, "--json"])
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        fail(f"unable to list installed skills: {detail}", completed.returncode)
    if isinstance(payload, list):
        return {
            item.get("name")
            for item in payload
            if isinstance(item, dict) and isinstance(item.get("name"), str)
        }

    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        fail(f"unable to list installed skills: {detail}", completed.returncode)
    catalog_names = {record["name"] for record in iter_records(catalog)}
    installed: set[str] = set()
    for raw_line in completed.stdout.splitlines():
        fields = ANSI_ESCAPE_RE.sub("", raw_line).split()
        if fields and fields[0] in catalog_names:
            installed.add(fields[0])
    return installed


def install_skills_cli(
    catalog: dict[str, Any],
    records: list[dict[str, Any]],
    agent: str | None,
    scope: str,
    source: str | None,
    dry_run: bool,
    as_json: bool,
) -> None:
    skill_names = [record["name"] for record in records]
    package_source = source or catalog["repository"]
    command = [
        "npx",
        "--yes",
        "skills",
        "add",
        package_source,
    ]
    if scope == "global":
        command.append("--global")
    command.extend(
        [
            "--yes",
            "--copy",
            "--full-depth",
            "--skill",
            *skill_names,
        ]
    )
    if agent:
        command.extend(["--agent", agent])
    if dry_run:
        payload = {
            "method": "skills",
            "skills": skill_names,
            "scope": scope,
            "source": package_source,
            "command": command,
        }
        print(
            json.dumps(payload, ensure_ascii=False, indent=2)
            if as_json
            else " ".join(command)
        )
        return
    if shutil.which("npx") is None:
        fail("npx executable not found; install Node.js to install skills")
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        fail(f"skills CLI install failed: {detail}", completed.returncode)

    installed_names = installed_skill_names(catalog, agent, scope)
    missing = sorted(set(skill_names) - installed_names)
    if missing:
        fail(
            f"skills CLI reported success but did not list installed skills: {', '.join(missing)}"
        )
    result = {
        "status": "installed",
        "method": "skills",
        "skills": skill_names,
        "agent": agent,
        "scope": scope,
        "source": package_source,
        "verified": True,
    }
    print(
        json.dumps(result, ensure_ascii=False, indent=2)
        if as_json
        else f"Installed: {', '.join(skill_names)}"
    )


def show_status(
    catalog: dict[str, Any], agent: str | None, scope: str, as_json: bool
) -> None:
    if shutil.which("npx") is None:
        fail("npx executable not found; install Node.js to inspect installed skills")
    installed_names = installed_skill_names(catalog, agent, scope)
    rows = [
        {
            "skill": record["name"],
            "plugin": record["plugin"],
            "domain": record["domain"],
            "state": (
                "installed"
                if record["name"] in installed_names
                else "not_installed"
            ),
        }
        for record in iter_records(catalog)
    ]
    if as_json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        for row in rows:
            print(f"{row['skill']}: {row['state']} ({row['plugin']})")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser(
        "list", help="List all catalogued skills for agent selection"
    )
    list_parser.add_argument("--json", action="store_true")

    info_parser = subparsers.add_parser("info", help="Show one exact skill or plugin")
    info_parser.add_argument("target")
    info_parser.add_argument("--json", action="store_true")

    install_parser = subparsers.add_parser(
        "install", help="Install one or more exact skills"
    )
    install_parser.add_argument("targets", nargs="+")
    install_parser.add_argument("--agent", help="Target agent name for skills CLI")
    install_parser.add_argument(
        "--scope",
        choices=("global", "project"),
        default="global",
        help="Installation scope for skills CLI",
    )
    install_parser.add_argument(
        "--source", help="Repository or reviewed local checkout for skills CLI"
    )
    install_parser.add_argument("--dry-run", action="store_true")
    install_parser.add_argument("--json", action="store_true")

    status_parser = subparsers.add_parser(
        "status", help="Show catalogued skill installation status"
    )
    status_parser.add_argument("--agent", help="Target agent name for skills CLI")
    status_parser.add_argument(
        "--scope", choices=("global", "project"), default="global"
    )
    status_parser.add_argument("--json", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    catalog = load_catalog()
    if args.command == "list":
        output_records(list(iter_records(catalog)), args.json)
    elif args.command == "info":
        _, records = resolve_target(catalog, args.target)
        output_records(records, args.json)
    elif args.command == "install":
        records = resolve_skills(catalog, args.targets)
        install_skills_cli(
            catalog,
            records,
            args.agent,
            args.scope,
            args.source,
            args.dry_run,
            args.json,
        )
    elif args.command == "status":
        show_status(catalog, args.agent, args.scope, args.json)


if __name__ == "__main__":
    main()
