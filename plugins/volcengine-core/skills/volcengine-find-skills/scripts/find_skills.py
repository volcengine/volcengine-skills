#!/usr/bin/env python3
"""List the Volcengine skills catalog and install owning plugins or exact skills."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = SKILL_ROOT / "references" / "catalog.json"


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


def run_json(command: list[str]) -> tuple[subprocess.CompletedProcess[str], Any | None]:
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        return completed, None
    try:
        return completed, json.loads(completed.stdout)
    except json.JSONDecodeError:
        return completed, None


def codex_state(marketplace: str) -> tuple[set[str], set[str]]:
    completed, payload = run_json(
        [
            "codex",
            "plugin",
            "list",
            "--marketplace",
            marketplace,
            "--available",
            "--json",
        ]
    )
    if completed.returncode != 0 or payload is None:
        detail = (
            completed.stderr.strip()
            or completed.stdout.strip()
            or "invalid JSON output"
        )
        fail(f"unable to list Codex plugins: {detail}", completed.returncode or 2)
    installed = {item["name"] for item in payload.get("installed", [])}
    available = {item["name"] for item in payload.get("available", [])}
    return installed, available


def ensure_codex_marketplace(marketplace: str, repository: str) -> None:
    completed, payload = run_json(["codex", "plugin", "marketplace", "list", "--json"])
    if completed.returncode != 0 or payload is None:
        detail = (
            completed.stderr.strip()
            or completed.stdout.strip()
            or "invalid JSON output"
        )
        fail(f"unable to list Codex marketplaces: {detail}", completed.returncode or 2)
    names = {item.get("name") for item in payload.get("marketplaces", [])}
    if marketplace not in names:
        fail(
            f"Codex marketplace {marketplace!r} is not configured. Run: "
            f"codex plugin marketplace add {repository}"
        )


def install_codex(
    catalog: dict[str, Any], plugin: dict[str, Any], dry_run: bool, as_json: bool
) -> None:
    marketplace = catalog["marketplace"]
    selector = f"{plugin['name']}@{marketplace}"
    command = ["codex", "plugin", "add", selector, "--json"]
    if dry_run:
        payload = {"method": "codex", "plugin": plugin["name"], "command": command}
        print(
            json.dumps(payload, ensure_ascii=False, indent=2)
            if as_json
            else " ".join(command)
        )
        return
    if shutil.which("codex") is None:
        fail("codex executable not found; use --method skills for a non-Codex host")
    ensure_codex_marketplace(marketplace, catalog["repository"])
    installed, available = codex_state(marketplace)
    if plugin["name"] in installed:
        result = {
            "status": "already_installed",
            "plugin": plugin["name"],
            "marketplace": marketplace,
        }
        print(
            json.dumps(result, ensure_ascii=False, indent=2)
            if as_json
            else f"{plugin['name']} is already installed."
        )
        return
    if plugin["name"] not in available:
        fail(
            f"plugin {plugin['name']!r} is not available from marketplace {marketplace!r}"
        )
    completed, payload = run_json(command)
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        fail(f"Codex plugin install failed: {detail}", completed.returncode)
    installed, _ = codex_state(marketplace)
    if plugin["name"] not in installed:
        fail(f"Codex reported success but {plugin['name']!r} is not installed")
    result = {
        "status": "installed",
        "plugin": plugin["name"],
        "marketplace": marketplace,
        "restart_required": True,
        "install_result": payload,
    }
    print(
        json.dumps(result, ensure_ascii=False, indent=2)
        if as_json
        else f"Installed {plugin['name']}. Start a new thread before using its skills."
    )


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
        fail(
            "npx executable not found; install Node.js or use the host's plugin marketplace"
        )
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        fail(f"skills CLI install failed: {detail}", completed.returncode)

    verify_command = ["npx", "--yes", "skills", "list"]
    if scope == "global":
        verify_command.append("--global")
    if agent:
        verify_command.extend(["--agent", agent])
    verify_command.append("--json")
    verified, payload = run_json(verify_command)
    if verified.returncode != 0 or not isinstance(payload, list):
        detail = (
            verified.stderr.strip() or verified.stdout.strip() or "invalid JSON output"
        )
        fail(f"unable to verify skills CLI install: {detail}", verified.returncode or 2)
    installed_names = {
        item.get("name")
        for item in payload
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    }
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


def show_status(catalog: dict[str, Any], as_json: bool) -> None:
    if shutil.which("codex") is None:
        fail("codex executable not found")
    marketplace = catalog["marketplace"]
    ensure_codex_marketplace(marketplace, catalog["repository"])
    installed, available = codex_state(marketplace)
    rows = []
    for plugin in catalog["plugins"]:
        state = (
            "installed"
            if plugin["name"] in installed
            else "available"
            if plugin["name"] in available
            else "missing"
        )
        rows.append(
            {
                "plugin": plugin["name"],
                "domain": plugin["domain"],
                "state": state,
                "skills": [skill["name"] for skill in plugin["skills"]],
            }
        )
    if as_json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        for row in rows:
            print(f"{row['plugin']}: {row['state']} ({', '.join(row['skills'])})")


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
        "install", help="Install an owning plugin or direct skill"
    )
    install_parser.add_argument("target")
    install_parser.add_argument(
        "--method", choices=("codex", "skills"), default="codex"
    )
    install_parser.add_argument("--agent", help="Target agent name for --method skills")
    install_parser.add_argument(
        "--scope",
        choices=("global", "project"),
        default="global",
        help="Scope for --method skills",
    )
    install_parser.add_argument(
        "--source", help="Repository or reviewed local checkout for --method skills"
    )
    install_parser.add_argument("--dry-run", action="store_true")
    install_parser.add_argument("--json", action="store_true")

    status_parser = subparsers.add_parser(
        "status", help="Show Codex plugin installation status"
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
        plugin, records = resolve_target(catalog, args.target)
        if args.method == "codex":
            install_codex(catalog, plugin, args.dry_run, args.json)
        else:
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
        show_status(catalog, args.json)


if __name__ == "__main__":
    main()
