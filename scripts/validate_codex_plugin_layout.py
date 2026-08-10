#!/usr/bin/env python3
"""Validate authoritative skills, plugin packages, and the discovery/install contract."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = (
    REPO_ROOT
    / "skills"
    / "core"
    / "volcengine-find-skills"
    / "references"
    / "catalog.json"
)
FINDER_SCRIPT = CATALOG_PATH.parents[1] / "scripts" / "find_skills.py"
CORE_PLUGIN = "volcengine-core"
CORE_SKILLS = {
    "volcengine-cli",
    "volcengine-find-skills",
    "volcengine-troubleshooting",
    "volcengine-knowledge-search",
}
LIST_FILES = (
    REPO_ROOT / "README.md",
    REPO_ROOT / "README_en.md",
    REPO_ROOT / ".cursor" / "rules" / "volcengine-skills.mdc",
    REPO_ROOT / "GEMINI.md",
)
NAME_RE = re.compile(r"^volcengine-[a-z0-9]+(?:-[a-z0-9]+)*$")
errors: list[str] = []


def error(message: str) -> None:
    errors.append(message)
    print(f"ERROR: {message}", file=sys.stderr)


def relative(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def load_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        error(f"missing {relative(path)}")
        return None
    except json.JSONDecodeError as exc:
        error(f"invalid JSON in {relative(path)}: {exc}")
        return None
    if not isinstance(value, dict):
        error(f"expected an object in {relative(path)}")
        return None
    return value


def frontmatter_name(skill_md: Path) -> str | None:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        error(f"missing YAML frontmatter in {relative(skill_md)}")
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        error(f"unterminated YAML frontmatter in {relative(skill_md)}")
        return None
    match = re.search(r"^name:\s*([^\s]+)\s*$", text[4:end], re.MULTILINE)
    if not match:
        error(f"missing frontmatter name in {relative(skill_md)}")
        return None
    return match.group(1).strip("\"'")


def validate_catalog(
    catalog: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    if catalog.get("schema_version") != 1:
        error("catalog schema_version must be 1")
    if catalog.get("marketplace") != "volcengine-skills":
        error("catalog marketplace must be 'volcengine-skills'")
    plugins = catalog.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        error("catalog plugins must be a non-empty list")
        return {}, {}

    plugin_map: dict[str, dict[str, Any]] = {}
    skill_map: dict[str, dict[str, Any]] = {}
    default_plugins = []
    catalog_paths: set[str] = set()
    for plugin in plugins:
        if not isinstance(plugin, dict):
            error("every catalog plugin must be an object")
            continue
        name = plugin.get("name")
        if not isinstance(name, str) or not NAME_RE.fullmatch(name):
            error(f"invalid plugin name: {name!r}")
            continue
        if name in plugin_map:
            error(f"duplicate plugin name: {name}")
            continue
        plugin_map[name] = plugin
        if plugin.get("default"):
            default_plugins.append(name)
        for required in (
            "display_name",
            "domain",
            "domain_en",
            "description",
            "short_description",
        ):
            if (
                not isinstance(plugin.get(required), str)
                or not plugin[required].strip()
            ):
                error(f"plugin {name} has invalid {required}")
        skills = plugin.get("skills")
        if not isinstance(skills, list) or not skills:
            error(f"plugin {name} must contain at least one skill")
            continue
        for skill in skills:
            if not isinstance(skill, dict):
                error(f"plugin {name} has a non-object skill")
                continue
            skill_name = skill.get("name")
            source_path = skill.get("path")
            if not isinstance(skill_name, str) or not NAME_RE.fullmatch(skill_name):
                error(f"invalid skill name in {name}: {skill_name!r}")
                continue
            if skill_name in skill_map:
                error(f"skill is assigned more than once: {skill_name}")
                continue
            if (
                not isinstance(source_path, str)
                or Path(source_path).is_absolute()
                or ".." in Path(source_path).parts
            ):
                error(f"invalid source path for {skill_name}: {source_path!r}")
                continue
            expected_path = (
                Path("skills", "core", skill_name)
                if plugin.get("default")
                else Path("plugins", name, "skills", skill_name)
            )
            if Path(source_path).parts != expected_path.parts:
                error(
                    f"skill {skill_name} must be owned by {expected_path.as_posix()}, "
                    f"got {source_path!r}"
                )
                continue
            source = REPO_ROOT / source_path
            if not (source / "SKILL.md").is_file():
                error(f"catalog source is missing SKILL.md: {source_path}")
            elif frontmatter_name(source / "SKILL.md") != skill_name:
                error(f"frontmatter name does not match catalog for {source_path}")
            if source.name != skill_name:
                error(f"source directory does not match skill name: {source_path}")
            if source_path in catalog_paths:
                error(f"duplicate catalog source path: {source_path}")
            catalog_paths.add(source_path)
            skill_map[skill_name] = {**skill, "plugin": name}

    if default_plugins != [CORE_PLUGIN]:
        error(f"expected only {CORE_PLUGIN} to be default, got {default_plugins}")

    skills_root = REPO_ROOT / "skills"
    unexpected_skill_entries = sorted(
        path.name for path in skills_root.iterdir() if path.name != "core"
    )
    if unexpected_skill_entries:
        error(f"skills/ may contain only core/, got {unexpected_skill_entries}")
    authoritative_paths = {
        relative(skill_md.parent)
        for skill_md in (skills_root / "core").rglob("SKILL.md")
    }
    for plugin_name, plugin in plugin_map.items():
        if plugin.get("default"):
            continue
        authoritative_paths.update(
            relative(skill_md.parent)
            for skill_md in (REPO_ROOT / "plugins" / plugin_name / "skills").rglob(
                "SKILL.md"
            )
        )
    if authoritative_paths != catalog_paths:
        missing = sorted(authoritative_paths - catalog_paths)
        extra = sorted(catalog_paths - authoritative_paths)
        error(f"catalog/authoritative skill mismatch; missing={missing}, extra={extra}")

    core_dir = REPO_ROOT / "skills" / "core"
    actual_core = {path.name for path in core_dir.iterdir() if path.is_dir()}
    if actual_core != CORE_SKILLS:
        error(
            f"skills/core must contain exactly {sorted(CORE_SKILLS)}, got {sorted(actual_core)}"
        )
    finder = skill_map.get("volcengine-find-skills")
    if not finder or finder.get("path") != "skills/core/volcengine-find-skills":
        error("volcengine-find-skills must live in skills/core and be catalogued")
    if finder and finder.get("plugin") != CORE_PLUGIN:
        error("volcengine-find-skills must be owned by volcengine-core")
    return plugin_map, skill_map


def validate_marketplaces(plugin_map: dict[str, dict[str, Any]]) -> None:
    expected_names = set(plugin_map)
    codex = load_json(REPO_ROOT / ".agents" / "plugins" / "marketplace.json")
    claude = load_json(REPO_ROOT / ".claude-plugin" / "marketplace.json")
    cursor = load_json(REPO_ROOT / ".cursor-plugin" / "marketplace.json")
    for label, marketplace in (
        ("Codex", codex),
        ("Claude", claude),
        ("Cursor", cursor),
    ):
        if marketplace is None:
            continue
        entries = marketplace.get("plugins")
        if not isinstance(entries, list):
            error(f"{label} marketplace plugins must be a list")
            continue
        names = {entry.get("name") for entry in entries if isinstance(entry, dict)}
        if names != expected_names:
            error(f"{label} marketplace names differ from catalog: {sorted(names)}")

    if codex:
        for entry in codex["plugins"]:
            name = entry["name"]
            expected_path = f"./plugins/{name}"
            if entry.get("source") != {"source": "local", "path": expected_path}:
                error(f"Codex marketplace source is invalid for {name}")
            expected_policy = (
                "INSTALLED_BY_DEFAULT" if name == CORE_PLUGIN else "AVAILABLE"
            )
            policy = entry.get("policy", {})
            if policy.get("installation") != expected_policy:
                error(f"Codex install policy for {name} must be {expected_policy}")
            if policy.get("authentication") != "ON_INSTALL":
                error(f"Codex auth policy for {name} must be ON_INSTALL")
            if entry.get("category") != "Cloud":
                error(f"Codex category for {name} must be Cloud")

    for label, marketplace in (("Claude", claude), ("Cursor", cursor)):
        if marketplace:
            for entry in marketplace["plugins"]:
                expected_path = f"./plugins/{entry['name']}"
                if entry.get("source") != expected_path:
                    error(f"{label} marketplace source is invalid for {entry['name']}")


def validate_plugin_manifests(
    plugin_map: dict[str, dict[str, Any]], version: str
) -> None:
    plugins_root = REPO_ROOT / "plugins"
    actual_plugins = {path.name for path in plugins_root.iterdir() if path.is_dir()}
    if actual_plugins != set(plugin_map):
        error(
            f"plugins directory differs from catalog; actual={sorted(actual_plugins)}, "
            f"expected={sorted(plugin_map)}"
        )
    for name, plugin in plugin_map.items():
        root = plugins_root / name
        expected_skills = {skill["name"] for skill in plugin["skills"]}
        skills_dir = root / "skills"
        actual_skills = (
            {path.name for path in skills_dir.iterdir() if path.is_dir()}
            if skills_dir.is_dir()
            else set()
        )
        if actual_skills != expected_skills:
            error(f"plugin {name} skills differ from catalog: {sorted(actual_skills)}")
        for path in root.rglob("*"):
            if path.is_symlink():
                error(f"plugin packages must not contain symlinks: {relative(path)}")

        manifests = {
            "Codex": (root / ".codex-plugin" / "plugin.json", "./skills/"),
            "Claude": (root / ".claude-plugin" / "plugin.json", ["./skills/"]),
            "Cursor": (root / ".cursor-plugin" / "plugin.json", "./skills/"),
        }
        for label, (path, skills_value) in manifests.items():
            manifest = load_json(path)
            if not manifest:
                continue
            if manifest.get("name") != name:
                error(f"{label} manifest name mismatch in {relative(path)}")
            if manifest.get("version") != version:
                error(f"{label} manifest version mismatch in {relative(path)}")
            if manifest.get("skills") != skills_value:
                error(f"{label} manifest skills path mismatch in {relative(path)}")
            if label == "Codex" and not isinstance(manifest.get("interface"), dict):
                error(f"Codex manifest interface missing in {relative(path)}")

    core_packaged = {
        path.name
        for path in (plugins_root / CORE_PLUGIN / "skills").iterdir()
        if path.is_dir()
    }
    if core_packaged != CORE_SKILLS:
        error(
            f"core plugin must package exactly the four core skills, got {sorted(core_packaged)}"
        )


def validate_root_hosts(version: str) -> None:
    for path in (
        REPO_ROOT / ".codex-plugin" / "plugin.json",
        REPO_ROOT / ".claude-plugin" / "plugin.json",
        REPO_ROOT / ".cursor-plugin" / "plugin.json",
    ):
        if path.exists():
            error(
                f"multi-plugin repository must not expose a root single-plugin manifest: {relative(path)}"
            )
    opencode = load_json(REPO_ROOT / ".opencode" / "opencode.json")
    if opencode and opencode.get("skills", {}).get("paths") != [
        "plugins/volcengine-core/skills"
    ]:
        error("OpenCode must expose only the core plugin skills path")
    openclaw = load_json(REPO_ROOT / "openclaw.plugin.json")
    if openclaw and openclaw.get("skills") != ["./plugins/volcengine-core/skills"]:
        error("OpenClaw must expose only the core plugin skills path")
    if openclaw and openclaw.get("version") != version:
        error("OpenClaw plugin version must match package.json")
    openclaw_entry_path = REPO_ROOT / "hooks" / "openclaw-telemetry.js"
    try:
        openclaw_entry = openclaw_entry_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        error(f"missing {relative(openclaw_entry_path)}")
    else:
        entry_id = re.search(
            r'definePluginEntry\s*\(\s*\{\s*id:\s*["\']([^"\']+)["\']',
            openclaw_entry,
        )
        if not entry_id:
            error("OpenClaw extension must declare its definePluginEntry id")
        elif openclaw and entry_id.group(1) != openclaw.get("id"):
            error("OpenClaw extension id must match openclaw.plugin.json")
    gemini = load_json(REPO_ROOT / "gemini-extension.json")
    if gemini and gemini.get("version") != version:
        error("Gemini extension version must match package.json")


def validate_core_hooks() -> None:
    payload = load_json(REPO_ROOT / "hooks" / "hooks.json")
    if not payload:
        return
    entries = payload.get("hooks", {}).get("PostToolUse", [])
    if not isinstance(entries, list):
        error("hooks/hooks.json PostToolUse must be a list")
        return
    by_matcher = {
        entry.get("matcher"): entry
        for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("matcher"), str)
    }

    def commands(entry: dict[str, Any] | None) -> list[str]:
        if not entry or not isinstance(entry.get("hooks"), list):
            return []
        return [
            hook.get("command", "")
            for hook in entry["hooks"]
            if isinstance(hook, dict) and isinstance(hook.get("command"), str)
        ]

    skill_commands = commands(by_matcher.get("Skill"))
    guarded_commands = commands(by_matcher.get("Read|Bash"))
    if not skill_commands or any(
        "--require-skill-md" in command for command in skill_commands
    ):
        error("Skill hook must dispatch without --require-skill-md")
    if not guarded_commands or any(
        "--require-skill-md" not in command for command in guarded_commands
    ):
        error("Read|Bash hooks must use --require-skill-md")


def validate_hardcoded_lists(skill_names: set[str], plugin_names: set[str]) -> None:
    allowed = skill_names | plugin_names | {"volcengine-skills"}
    token_re = re.compile(r"`(volcengine-[a-z0-9-]+)`")
    for path in LIST_FILES:
        try:
            text = path.read_text(encoding="utf-8")
        except FileNotFoundError:
            error(f"missing hard-coded skill list: {relative(path)}")
            continue
        for name in skill_names:
            if f"`{name}`" not in text:
                error(f"{relative(path)} is missing skill {name}")
        unknown = {match.group(1) for match in token_re.finditer(text)} - allowed
        if unknown:
            error(f"{relative(path)} contains uncatalogued names: {sorted(unknown)}")


def run_json(command: list[str]) -> Any | None:
    completed = subprocess.run(
        command, cwd=REPO_ROOT, capture_output=True, text=True, check=False
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        error(f"command failed ({' '.join(command)}): {detail}")
        return None
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        error(f"command did not return JSON ({' '.join(command)}): {exc}")
        return None


def validate_finder(skill_map: dict[str, dict[str, Any]]) -> None:
    payload = run_json([sys.executable, str(FINDER_SCRIPT), "list", "--json"])
    listed_skills = (
        {
            item.get("name"): item.get("plugin")
            for item in payload
            if isinstance(item, dict)
        }
        if isinstance(payload, list)
        else {}
    )
    expected_skills = {name: skill["plugin"] for name, skill in skill_map.items()}
    listed_count = len(payload) if isinstance(payload, list) else 0
    if listed_skills != expected_skills or listed_count != len(expected_skills):
        error(
            "finder list must return every catalogued skill exactly once with its owning plugin"
        )
    for name, skill in skill_map.items():
        payload = run_json(
            [
                sys.executable,
                str(FINDER_SCRIPT),
                "install",
                name,
                "--method",
                "codex",
                "--dry-run",
                "--json",
            ]
        )
        expected_selector = f"{skill['plugin']}@volcengine-skills"
        command = payload.get("command", []) if isinstance(payload, dict) else []
        if expected_selector not in command:
            error(f"finder maps {name} to the wrong Codex plugin: {command}")
        payload = run_json(
            [
                sys.executable,
                str(FINDER_SCRIPT),
                "install",
                name,
                "--method",
                "skills",
                "--dry-run",
                "--json",
            ]
        )
        command = payload.get("command", []) if isinstance(payload, dict) else []
        selected_skills = (
            payload.get("skills", []) if isinstance(payload, dict) else []
        )
        if (
            "--full-depth" not in command
            or "--global" not in command
            or selected_skills != [name]
        ):
            error(
                f"finder generic install must select the exact skill {name}: {command}"
            )
    payload = run_json(
        [
            sys.executable,
            str(FINDER_SCRIPT),
            "install",
            "volcengine-tosutil",
            "--method",
            "skills",
            "--scope",
            "project",
            "--source",
            ".",
            "--dry-run",
            "--json",
        ]
    )
    command = payload.get("command", []) if isinstance(payload, dict) else []
    if "--global" in command or "." not in command:
        error(
            "finder project install must preserve the reviewed source without using global scope"
        )

    finder_text = (CATALOG_PATH.parents[1] / "SKILL.md").read_text(encoding="utf-8")

    def requires_list(key: str) -> set[str]:
        match = re.search(
            rf"^      {re.escape(key)}:\n((?:        - [^\n]+\n?)+)",
            finder_text,
            re.MULTILINE,
        )
        return (
            set(re.findall(r"^        -\s+([^\s]+)\s*$", match.group(1), re.MULTILINE))
            if match
            else set()
        )

    bins = requires_list("bins")
    any_bins = requires_list("anyBins")
    if bins != {"python3"} or any_bins != {"codex", "npx"}:
        error(
            f"finder runtime requirements are invalid: bins={sorted(bins)}, anyBins={sorted(any_bins)}"
        )
    eligible = lambda present: bins <= present and bool(any_bins & present)
    if not eligible({"python3", "npx"}) or not eligible({"python3", "codex"}):
        error(
            "finder OpenClaw eligibility must allow either Codex or skills CLI installation"
        )

    cross_plugin_path = re.compile(r"\.\./(?:\.\./)+(?:volcengine-[a-z0-9-]+)")
    for root in (REPO_ROOT / "skills", REPO_ROOT / "plugins"):
        for path in root.rglob("*.md"):
            if cross_plugin_path.search(path.read_text(encoding="utf-8")):
                error(
                    f"cross-plugin relative path is not install-safe: {relative(path)}"
                )


def validate_generated_sync() -> None:
    completed = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "sync_plugins.py"), "--check"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        error(f"generated plugin packages are stale: {detail}")


def main() -> None:
    catalog = load_json(CATALOG_PATH)
    package = load_json(REPO_ROOT / "package.json")
    if not catalog or not package:
        raise SystemExit(1)
    version = package.get("version")
    if not isinstance(version, str):
        error("package.json version must be a string")
        version = ""

    plugin_map, skill_map = validate_catalog(catalog)
    validate_marketplaces(plugin_map)
    validate_plugin_manifests(plugin_map, version)
    validate_root_hosts(version)
    validate_core_hooks()
    validate_hardcoded_lists(set(skill_map), set(plugin_map))
    validate_finder(skill_map)
    validate_generated_sync()

    if errors:
        print(f"\nValidation failed with {len(errors)} error(s).", file=sys.stderr)
        raise SystemExit(1)
    print(
        f"Validated {len(skill_map)} authoritative skills across {len(plugin_map)} installable plugins; "
        "core-only discovery and install mappings are consistent."
    )


if __name__ == "__main__":
    main()
