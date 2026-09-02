#!/usr/bin/env python3
# Copyright (c) 2026 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: MIT
"""
Report which extension-API recipes have become plain CLI actions.

references/extend-apis.md lists Actions that need `ve ... --force` (section 1)
or scripts/call_extend_api.py (section 2) because the installed `ve` does not
know them. Every ve release adds metadata, so the list goes stale. This tool
asks the installed `ve` which of those Actions it now lists and prints them,
so the reference can be trimmed. Read-only: it never calls an API.

    python3 scripts/audit_extend_apis.py          # human-readable report
    python3 scripts/audit_extend_apis.py --json   # machine-readable
Exit 0 when nothing is stale, 1 when at least one recipe is now in the CLI,
2 on a usage/IO problem.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
REFERENCE = os.path.join(HERE, "..", "references", "extend-apis.md")
HELPER = os.path.join(HERE, "call_extend_api.py")

ACTION_RE = re.compile(r"`([A-Z][A-Za-z0-9]+)`")
ROW_RE = re.compile(r"^\|\s*`([A-Za-z0-9_]+)`(?:\s*\([^)]*\))?\s*\|")


def parse_force_recipes(markdown: str) -> dict[str, set[str]]:
    """Return {service: {Action, ...}} from the section-1 recipe table."""
    recipes: dict[str, set[str]] = {}
    in_section = False
    for line in markdown.splitlines():
        if line.startswith("## "):
            in_section = line.startswith("## 1.")
            continue
        if not in_section:
            continue
        row = ROW_RE.match(line)
        if not row:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 6:
            continue
        service = row.group(1)
        actions_cell = cells[5]
        for action in ACTION_RE.findall(actions_cell):
            recipes.setdefault(service, set()).add(action)
    return recipes


def load_helper_registry() -> dict[str, set[str]]:
    spec = importlib.util.spec_from_file_location("call_extend_api", HELPER)
    if spec is None or spec.loader is None:
        return {}
    module = importlib.util.module_from_spec(spec)
    sys.modules["call_extend_api"] = module
    spec.loader.exec_module(module)
    registry: dict[str, set[str]] = {}
    for entry in module.API_REGISTRY:
        registry.setdefault(entry["service"], set()).add(entry["name"])
    return registry


def parse_cli_actions(text: str) -> set[str] | None:
    """Parse the `Available Actions:` block of `ve <service>`; None means the service is unknown.

    A known service prints that block. An unknown one prints only a generic
    `ve <service> <action> ...` usage line and still exits 0, so the block's
    absence is the signal, not the exit code.
    """
    lines = text.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.strip().lower().startswith("available actions"))
    except StopIteration:
        return None
    actions: set[str] = set()
    for line in lines[start + 1:]:
        if not line.strip():
            continue
        # Action rows are indented; the next section header ("Flags:",
        # "Reserved double-dash controls (...):") and the trailing
        # `Use "ve <svc> [action] --help"` hint start at column 0.
        if not line[0].isspace() or line.strip().startswith('Use "ve '):
            break
        token = line.split()[0]
        if token == "Action":
            continue  # the "Action  Description" column header
        if token[0].isupper() and re.fullmatch(r"[A-Za-z0-9]+", token):
            actions.add(token)
    return actions


def cli_actions(service: str, runner=subprocess.run) -> set[str] | None:
    """Actions the installed ve lists for a service; None when the service is unknown."""
    # Signing service codes can be case-sensitive (`CDN`) while CLI commands
    # are lowercase (`ve cdn`); try the exact spelling first, then lowercase.
    for cli_service in dict.fromkeys((service, service.lower())):
        try:
            completed = runner(["ve", cli_service], capture_output=True, text=True, timeout=30, check=False)
        except FileNotFoundError:
            raise SystemExit("`ve` is not installed; nothing to audit against.")
        except subprocess.TimeoutExpired:
            raise SystemExit(f"`ve {cli_service}` timed out.")
        actions = parse_cli_actions((completed.stdout or "") + "\n" + (completed.stderr or ""))
        if actions is not None:
            return actions
    return None


def audit(recipes: dict[str, set[str]], helper: dict[str, set[str]], runner=subprocess.run) -> dict[str, Any]:
    report: dict[str, Any] = {"now_in_cli": [], "unknown_service": [], "still_extension": []}
    services = sorted(set(recipes) | set(helper))
    for service in services:
        listed = cli_actions(service, runner)
        wanted = {("force", a) for a in recipes.get(service, set())} | {("helper", a) for a in helper.get(service, set())}
        if listed is None:
            report["unknown_service"].append(service)
            report["still_extension"].extend({"service": service, "action": a, "via": via} for via, a in sorted(wanted))
            continue
        for via, action in sorted(wanted):
            target = report["now_in_cli"] if action in listed else report["still_extension"]
            target.append({"service": service, "action": action, "via": via})
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Find extension-API recipes that the installed ve now supports natively.")
    parser.add_argument("--json", action="store_true", help="Print the report as JSON")
    parser.add_argument("--reference", default=REFERENCE, help=argparse.SUPPRESS)
    args = parser.parse_args()

    try:
        with open(args.reference, "r", encoding="utf-8") as f:
            markdown = f.read()
    except OSError as exc:
        print(f"cannot read {args.reference}: {exc}", file=sys.stderr)
        return 2

    recipes = parse_force_recipes(markdown)
    if not recipes:
        print("no recipe rows found in the reference; is section 1 intact?", file=sys.stderr)
        return 2
    report = audit(recipes, load_helper_registry())

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        stale = report["now_in_cli"]
        if stale:
            print("Now in the CLI metadata — remove from extend-apis.md / the helper registry and use plain `ve <service> <Action>`:")
            for item in stale:
                print(f"  {item['service']:16} {item['action']:40} ({item['via']})")
        else:
            print("No stale recipes: every listed Action is still absent from the installed ve.")
        if report["unknown_service"]:
            print("Services the installed ve does not know at all (recipes still needed): " + ", ".join(report["unknown_service"]))
        print(f"{len(report['still_extension'])} recipe(s) still require --force or the helper.")
    return 1 if report["now_in_cli"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
