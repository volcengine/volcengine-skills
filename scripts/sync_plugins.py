#!/usr/bin/env python3
"""Synchronize core packaging and plugin manifests from the authoritative skill catalog."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGINS_ROOT = REPO_ROOT / "plugins"
CATALOG_PATH = (
    REPO_ROOT
    / "skills"
    / "core"
    / "volcengine-find-skills"
    / "references"
    / "catalog.json"
)
AUTHOR = {
    "name": "Volcengine Team",
    "email": "volcengine@bytedance.com",
    "url": "https://www.volcengine.com",
}
HOMEPAGE = "https://github.com/volcengine/volcengine-skills"
PRIVACY_URL = "https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement"
TERMS_URL = (
    "https://docs.github.com/en/site-policy/github-terms/github-terms-of-service"
)
BRAND_COLOR = "#1664FF"
CORE_HOOK_FILES = (
    "hooks.json",
    "hooks-cursor.json",
    "run-apmplus-reporter.sh",
    "volcengine-apmplus-hook-reporter.mjs",
)
NAME_RE = re.compile(r"^volcengine-[a-z0-9]+(?:-[a-z0-9]+)*$")
CORE_PLUGIN = "volcengine-skills"
CORE_SKILLS = {
    "volcengine-cli",
    "volcengine-find-skills",
    "volcengine-knowledge-search",
    "volcengine-troubleshooting",
}


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_plugin_root(name: str) -> Path:
    if not NAME_RE.fullmatch(name):
        raise ValueError(f"unsafe plugin name: {name!r}")
    if (
        PLUGINS_ROOT.is_symlink()
        or PLUGINS_ROOT.resolve().parent != REPO_ROOT.resolve()
    ):
        raise ValueError(f"unsafe plugins root: {PLUGINS_ROOT}")
    candidate = PLUGINS_ROOT / name
    if candidate.is_symlink():
        raise ValueError(f"plugin root must not be a symlink: {candidate}")
    resolved = candidate.resolve()
    if resolved.parent != PLUGINS_ROOT.resolve() or resolved.name != name:
        raise ValueError(f"unsafe plugin path: {candidate}")
    return candidate


def ensure_safe_output(path: Path) -> None:
    if path.is_symlink():
        raise ValueError(f"output must not be a symlink: {path}")
    repo_root = REPO_ROOT.resolve()
    resolved_parent = path.parent.resolve()
    if resolved_parent != repo_root and repo_root not in resolved_parent.parents:
        raise ValueError(f"output escapes repository: {path}")


def validate_catalog(catalog: dict[str, Any]) -> None:
    errors: list[str] = []
    if catalog.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if catalog.get("marketplace") != "volcengine-skills":
        errors.append("marketplace must be 'volcengine-skills'")
    plugins = catalog.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        raise ValueError("invalid catalog:\n- plugins must be a non-empty list")

    plugin_names: set[str] = set()
    skill_names: set[str] = set()
    source_paths: set[str] = set()
    default_plugins: list[str] = []
    skills_root = REPO_ROOT / "skills"
    core_dir = skills_root / "core"
    for index, plugin in enumerate(plugins):
        if not isinstance(plugin, dict):
            errors.append(f"plugin[{index}] must be an object")
            continue
        name = plugin.get("name")
        if not isinstance(name, str) or not NAME_RE.fullmatch(name):
            errors.append(f"invalid plugin name: {name!r}")
            continue
        if name in plugin_names:
            errors.append(f"duplicate plugin name: {name}")
        plugin_names.add(name)
        try:
            safe_plugin_root(name)
        except ValueError as exc:
            errors.append(str(exc))
        if plugin.get("default"):
            default_plugins.append(name)
        for field in (
            "display_name",
            "domain",
            "domain_en",
            "description",
            "short_description",
        ):
            if not isinstance(plugin.get(field), str) or not plugin[field].strip():
                errors.append(f"plugin {name} has invalid {field}")
        prompts = plugin.get("default_prompts")
        if (
            not isinstance(prompts, list)
            or not prompts
            or not all(isinstance(prompt, str) and prompt.strip() for prompt in prompts)
        ):
            errors.append(f"plugin {name} has invalid default_prompts")
        skills = plugin.get("skills")
        if not isinstance(skills, list) or not skills:
            errors.append(f"plugin {name} must contain at least one skill")
            continue
        for skill in skills:
            if not isinstance(skill, dict):
                errors.append(f"plugin {name} contains a non-object skill")
                continue
            skill_name = skill.get("name")
            source_path = skill.get("path")
            if not isinstance(skill_name, str) or not NAME_RE.fullmatch(skill_name):
                errors.append(f"invalid skill name in {name}: {skill_name!r}")
                continue
            if skill_name in skill_names:
                errors.append(f"duplicate skill name: {skill_name}")
            skill_names.add(skill_name)
            if not isinstance(source_path, str):
                errors.append(f"invalid source path for {skill_name}: {source_path!r}")
                continue
            expected_path = (
                Path("skills", "core", skill_name)
                if plugin.get("default")
                else Path("plugins", name, "skills", skill_name)
            )
            if Path(source_path).parts != expected_path.parts:
                errors.append(
                    f"skill {skill_name} must be owned by {expected_path.as_posix()}, "
                    f"got {source_path!r}"
                )
                continue
            if source_path in source_paths:
                errors.append(f"duplicate source path: {source_path}")
            source_paths.add(source_path)
            source = REPO_ROOT / expected_path
            resolved_source = source.resolve()
            expected_parent = (
                core_dir.resolve()
                if plugin.get("default")
                else (safe_plugin_root(name) / "skills").resolve()
            )
            if (
                not source.is_dir()
                or resolved_source.parent != expected_parent
                or resolved_source.name != skill_name
                or not (source / "SKILL.md").is_file()
            ):
                errors.append(f"invalid authoritative skill directory: {source_path}")
                continue
            if (
                source.is_symlink()
                or source.parent.is_symlink()
                or any(child.is_symlink() for child in source.rglob("*"))
            ):
                errors.append(
                    f"authoritative skill must not contain symlinks: {source_path}"
                )

    if default_plugins != [CORE_PLUGIN]:
        errors.append(
            f"expected only {CORE_PLUGIN} to be default, got {default_plugins}"
        )
    unexpected_skill_entries = sorted(
        path.name for path in skills_root.iterdir() if path.name != "core"
    )
    if unexpected_skill_entries:
        errors.append(f"skills/ may contain only core/, got {unexpected_skill_entries}")
    authoritative_paths = {
        skill_md.parent.relative_to(REPO_ROOT).as_posix()
        for skill_md in core_dir.rglob("SKILL.md")
    }
    for plugin in plugins:
        if not isinstance(plugin, dict) or plugin.get("default"):
            continue
        plugin_name = plugin.get("name")
        if not isinstance(plugin_name, str) or not NAME_RE.fullmatch(plugin_name):
            continue
        authoritative_paths.update(
            skill_md.parent.relative_to(REPO_ROOT).as_posix()
            for skill_md in (safe_plugin_root(plugin_name) / "skills").rglob("SKILL.md")
        )
    if authoritative_paths != source_paths:
        errors.append(
            "catalog/authoritative skill mismatch: "
            f"missing={sorted(authoritative_paths - source_paths)}, "
            f"extra={sorted(source_paths - authoritative_paths)}"
        )
    actual_core = (
        {path.name for path in core_dir.iterdir() if path.is_dir()}
        if core_dir.is_dir()
        else set()
    )
    if actual_core != CORE_SKILLS:
        errors.append(
            f"skills/core must contain exactly {sorted(CORE_SKILLS)}, got {sorted(actual_core)}"
        )
    actual_plugins = {
        path.name for path in PLUGINS_ROOT.iterdir() if path.is_dir()
    }
    if actual_plugins != plugin_names:
        errors.append(
            "plugins directory must match catalog: "
            f"missing={sorted(plugin_names - actual_plugins)}, "
            f"extra={sorted(actual_plugins - plugin_names)}"
        )
    if errors:
        raise ValueError("invalid catalog:\n- " + "\n- ".join(errors))


def unique(items: list[str]) -> list[str]:
    return list(dict.fromkeys(items))


def plugin_keywords(plugin: dict[str, Any]) -> list[str]:
    return unique(
        [
            "volcengine",
            "cloud",
            *plugin.get("keywords", []),
            *(skill["name"] for skill in plugin["skills"]),
        ]
    )


def codex_manifest(plugin: dict[str, Any], version: str) -> dict[str, Any]:
    is_core = bool(plugin.get("default"))
    manifest: dict[str, Any] = {
        "name": plugin["name"],
        "version": version,
        "description": plugin["description"],
        "author": AUTHOR,
        "homepage": HOMEPAGE,
        "repository": HOMEPAGE,
        "license": "MIT",
        "keywords": plugin_keywords(plugin),
        "skills": "./skills/",
        "interface": {
            "displayName": plugin["display_name"],
            "shortDescription": plugin["short_description"],
            "longDescription": plugin["description"],
            "developerName": AUTHOR["name"],
            "category": plugin.get("category", "Cloud"),
            "capabilities": ["Interactive", "Read", "Write"],
            "defaultPrompt": plugin["default_prompts"],
            "websiteURL": HOMEPAGE,
            "privacyPolicyURL": PRIVACY_URL,
            "termsOfServiceURL": TERMS_URL,
            "brandColor": BRAND_COLOR,
        },
    }
    if is_core:
        manifest["interface"]["composerIcon"] = "./assets/logo.svg"
        manifest["interface"]["logo"] = "./assets/logo.svg"
    return manifest


def claude_manifest(plugin: dict[str, Any], version: str) -> dict[str, Any]:
    return {
        "name": plugin["name"],
        "description": plugin["description"],
        "version": version,
        "author": {"name": AUTHOR["name"]},
        "homepage": HOMEPAGE,
        "repository": HOMEPAGE,
        "license": "MIT",
        "keywords": plugin_keywords(plugin),
        "skills": ["./skills/"],
    }


def cursor_manifest(plugin: dict[str, Any], version: str) -> dict[str, Any]:
    is_core = bool(plugin.get("default"))
    manifest: dict[str, Any] = {
        "name": plugin["name"],
        "displayName": plugin["display_name"],
        "description": plugin["description"],
        "version": version,
        "author": {"name": AUTHOR["name"], "email": AUTHOR["email"]},
        "homepage": HOMEPAGE,
        "repository": HOMEPAGE,
        "license": "MIT",
        "keywords": plugin_keywords(plugin),
        "skills": "./skills/",
    }
    if is_core:
        manifest["logo"] = "assets/logo.svg"
        manifest["hooks"] = "./hooks/hooks-cursor.json"
    return manifest


def marketplace_manifests(
    catalog: dict[str, Any], version: str
) -> dict[Path, dict[str, Any]]:
    plugins = catalog["plugins"]
    codex_entries = []
    claude_entries = []
    cursor_entries = []
    for plugin in plugins:
        source_path = f"./plugins/{plugin['name']}"
        codex_entries.append(
            {
                "name": plugin["name"],
                "source": {"source": "local", "path": source_path},
                "policy": {
                    "installation": "INSTALLED_BY_DEFAULT"
                    if plugin.get("default")
                    else "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": plugin.get("category", "Cloud"),
            }
        )
        shared = {
            "name": plugin["name"],
            "source": source_path,
            "description": plugin["description"],
            "version": version,
            "author": {"name": AUTHOR["name"]},
            "homepage": HOMEPAGE,
            "repository": HOMEPAGE,
            "license": "MIT",
            "keywords": plugin_keywords(plugin),
            "category": plugin["domain_en"].lower().replace(" ", "-"),
        }
        claude_entries.append(shared)
        cursor_entries.append(
            {
                "name": plugin["name"],
                "source": source_path,
                "description": plugin["description"],
            }
        )
    return {
        REPO_ROOT / ".agents" / "plugins" / "marketplace.json": {
            "name": catalog["marketplace"],
            "interface": {"displayName": "Volcengine Skills"},
            "plugins": codex_entries,
        },
        REPO_ROOT / ".claude-plugin" / "marketplace.json": {
            "name": catalog["marketplace"],
            "owner": {"name": AUTHOR["name"]},
            "metadata": {
                "description": "Volcengine skills marketplace organized by official product domain."
            },
            "plugins": claude_entries,
        },
        REPO_ROOT / ".cursor-plugin" / "marketplace.json": {
            "name": catalog["marketplace"],
            "owner": {"name": AUTHOR["name"], "email": AUTHOR["email"]},
            "metadata": {
                "description": "Volcengine skills marketplace organized by official product domain."
            },
            "plugins": cursor_entries,
        },
    }


def generated_json(catalog: dict[str, Any], version: str) -> dict[Path, dict[str, Any]]:
    outputs = marketplace_manifests(catalog, version)
    for plugin in catalog["plugins"]:
        plugin_root = PLUGINS_ROOT / plugin["name"]
        outputs[plugin_root / ".codex-plugin" / "plugin.json"] = codex_manifest(
            plugin, version
        )
        outputs[plugin_root / ".claude-plugin" / "plugin.json"] = claude_manifest(
            plugin, version
        )
        outputs[plugin_root / ".cursor-plugin" / "plugin.json"] = cursor_manifest(
            plugin, version
        )
    return outputs


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_hashes(root: Path) -> dict[str, str]:
    if not root.is_dir():
        return {}
    return {
        path.relative_to(root).as_posix(): file_hash(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def sync_core_skill_tree(
    catalog: dict[str, Any], check: bool, mismatches: list[str]
) -> None:
    plugin = next(item for item in catalog["plugins"] if item.get("default"))
    plugin_root = safe_plugin_root(CORE_PLUGIN)
    destination = plugin_root / "skills"
    expected_names = [skill["name"] for skill in plugin["skills"]]
    if check:
        actual_names = (
            sorted(path.name for path in destination.iterdir() if path.is_dir())
            if destination.is_dir()
            else []
        )
        if actual_names != sorted(expected_names):
            mismatches.append(
                f"{destination.relative_to(REPO_ROOT)} has {actual_names}, expected {sorted(expected_names)}"
            )
        for skill in plugin["skills"]:
            source = REPO_ROOT / skill["path"]
            target = destination / skill["name"]
            if tree_hashes(source) != tree_hashes(target):
                mismatches.append(
                    f"{target.relative_to(REPO_ROOT)} is not synced from {skill['path']}"
                )
        return

    temporary = plugin_root / ".skills-sync"
    if temporary.is_symlink() or destination.is_symlink():
        raise ValueError(f"plugin sync directories must not be symlinks: {plugin_root}")
    if temporary.exists():
        shutil.rmtree(temporary)
    temporary.mkdir(parents=True)
    for skill in plugin["skills"]:
        source = (REPO_ROOT / skill["path"]).resolve()
        target = temporary / skill["name"]
        if (
            not source.is_dir()
            or source.parent != (REPO_ROOT / "skills" / "core").resolve()
        ):
            raise ValueError(f"invalid core skill path: {skill['path']}")
        if (
            target.parent.resolve() != temporary.resolve()
            or target.name != skill["name"]
        ):
            raise ValueError(f"unsafe skill destination: {target}")
        shutil.copytree(source, target)
    if destination.exists():
        shutil.rmtree(destination)
    temporary.rename(destination)


def sync_core_support(check: bool, mismatches: list[str]) -> None:
    core_root = safe_plugin_root(CORE_PLUGIN)
    expected_files = {
        f"hooks/{name}": REPO_ROOT / "hooks" / name for name in CORE_HOOK_FILES
    }
    expected_files["assets/logo.svg"] = REPO_ROOT / "docs" / "logo.svg"
    for relative, source in expected_files.items():
        target = core_root / relative
        if check:
            if not target.is_file() or file_hash(source) != file_hash(target):
                mismatches.append(
                    f"{target.relative_to(REPO_ROOT)} is not synced from {source.relative_to(REPO_ROOT)}"
                )
        else:
            ensure_safe_output(target)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def sync_json_files(
    outputs: dict[Path, dict[str, Any]], check: bool, mismatches: list[str]
) -> None:
    for path, payload in outputs.items():
        expected = json_text(payload)
        if check:
            if not path.is_file() or path.read_text(encoding="utf-8") != expected:
                mismatches.append(
                    f"{path.relative_to(REPO_ROOT)} is not generated from the catalog"
                )
        else:
            ensure_safe_output(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Check generated files without writing"
    )
    args = parser.parse_args()

    catalog = load_json(CATALOG_PATH)
    validate_catalog(catalog)
    version = load_json(REPO_ROOT / "package.json").get("version")
    if not isinstance(version, str) or not version:
        raise ValueError("package.json version must be a non-empty string")
    mismatches: list[str] = []
    sync_core_skill_tree(catalog, args.check, mismatches)
    sync_core_support(args.check, mismatches)
    sync_json_files(generated_json(catalog, version), args.check, mismatches)

    if mismatches:
        for mismatch in mismatches:
            print(f"ERROR: {mismatch}", file=sys.stderr)
        raise SystemExit(1)
    if args.check:
        print("Plugin packages are synchronized with the authoritative catalog.")
    else:
        print(f"Synchronized {len(catalog['plugins'])} plugin packages.")


if __name__ == "__main__":
    main()
