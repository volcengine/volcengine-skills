#!/usr/bin/env python3
"""Build the versioned core Skill bundle consumed by Volcengine CLI."""

import argparse
import hashlib
import json
import os
import stat
import sys
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CORE_ROOT = REPO_ROOT / "skills" / "core"
BUNDLE_NAME = "volcengine-skill-bundle.zip"
MAX_BUNDLE_BYTES = 50 * 1024 * 1024
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def load_package_version():
    package = json.loads((REPO_ROOT / "package.json").read_text(encoding="utf-8"))
    version = package.get("version")
    if not isinstance(version, str) or not version:
        raise ValueError("package.json version must be a non-empty string")
    return version


def core_skill_directories():
    skills = sorted(path for path in CORE_ROOT.iterdir() if path.is_dir())
    if not skills:
        raise ValueError("skills/core must contain at least one Skill")
    return skills


def skill_files(skill_dir):
    files = []
    for path in sorted(skill_dir.rglob("*")):
        if path.is_symlink():
            raise ValueError("symbolic links are not allowed in release bundle: %s" % path)
        if path.is_file():
            files.append(path)
    if skill_dir / "SKILL.md" not in files:
        raise ValueError("missing SKILL.md in %s" % skill_dir)
    return files


def content_digest(skill_dir, files):
    digest = hashlib.sha256()
    for path in files:
        relative = path.relative_to(skill_dir).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def zip_external_attributes(path):
    executable = os.access(path, os.X_OK)
    mode = 0o755 if executable else 0o644
    return (stat.S_IFREG | mode) << 16


def build_bundle(bundle_path, skills):
    skill_entries = []
    with zipfile.ZipFile(bundle_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for skill_dir in skills:
            files = skill_files(skill_dir)
            skill_entries.append(
                {
                    "name": skill_dir.name,
                    "sha256": content_digest(skill_dir, files),
                }
            )
            for path in files:
                archive_path = Path(skill_dir.name) / path.relative_to(skill_dir)
                info = zipfile.ZipInfo(archive_path.as_posix(), ZIP_TIMESTAMP)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = zip_external_attributes(path)
                archive.writestr(info, path.read_bytes())
    return skill_entries


def validate_bundle_size(size):
    if size > MAX_BUNDLE_BYTES:
        raise ValueError(
            "Skill bundle is larger than the 50 MiB CLI download limit: %d bytes" % size
        )


def write_manifest(path, manifest):
    path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def build_release(output_dir, version, cdn_base_url=None):
    package_version = load_package_version()
    if version and version != package_version:
        raise ValueError(
            "release version %s does not match package.json version %s"
            % (version, package_version)
        )
    version = package_version

    output_dir.mkdir(parents=True, exist_ok=True)
    bundle_path = output_dir / BUNDLE_NAME
    skills = build_bundle(bundle_path, core_skill_directories())
    bundle_bytes = bundle_path.read_bytes()
    validate_bundle_size(len(bundle_bytes))
    bundle_sha256 = hashlib.sha256(bundle_bytes).hexdigest()
    manifest = {
        "schemaVersion": 1,
        "version": version,
        "bundle": {
            "file": BUNDLE_NAME,
            "sha256": bundle_sha256,
            "size": len(bundle_bytes),
            "url": BUNDLE_NAME,
        },
        "skills": skills,
    }
    manifest_path = output_dir / "manifest.json"
    write_manifest(manifest_path, manifest)

    cdn_manifest_path = None
    if cdn_base_url:
        cdn_manifest = dict(manifest)
        cdn_manifest["bundle"] = dict(manifest["bundle"])
        cdn_manifest["bundle"]["url"] = "%s/v%s/%s" % (
            cdn_base_url.rstrip("/"),
            version,
            BUNDLE_NAME,
        )
        cdn_manifest_path = output_dir / "cdn-manifest.json"
        write_manifest(cdn_manifest_path, cdn_manifest)
    return manifest_path, bundle_path, cdn_manifest_path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--version")
    parser.add_argument("--cdn-base-url")
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        manifest_path, bundle_path, cdn_manifest_path = build_release(
            args.output_dir, args.version, args.cdn_base_url
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print("build release bundle failed: %s" % error, file=sys.stderr)
        return 1
    print(manifest_path)
    print(bundle_path)
    if cdn_manifest_path:
        print(cdn_manifest_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
