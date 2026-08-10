from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SYNC_PATH = REPO_ROOT / "scripts" / "sync_plugins.py"
SPEC = importlib.util.spec_from_file_location("sync_plugins", SYNC_PATH)
assert SPEC and SPEC.loader
SYNC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SYNC)


class SyncCatalogSafetyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = json.loads(SYNC.CATALOG_PATH.read_text(encoding="utf-8"))

    def assert_rejected(self, catalog: dict) -> None:
        with self.assertRaises(ValueError):
            SYNC.validate_catalog(catalog)

    def test_current_catalog_is_safe(self) -> None:
        SYNC.validate_catalog(self.catalog)

    def test_plugin_path_traversal_is_rejected(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["plugins"][1]["name"] = "foo/../volcengine-skills"
        self.assert_rejected(catalog)

    def test_plugin_without_required_prefix_is_rejected(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["plugins"][1]["name"] = "storage"
        self.assert_rejected(catalog)

    def test_skill_path_traversal_is_rejected(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["plugins"][1]["skills"][0]["name"] = "../../escaped"
        self.assert_rejected(catalog)

    def test_source_path_traversal_is_rejected(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["plugins"][1]["skills"][0]["path"] = "skills/../README.md"
        self.assert_rejected(catalog)

    def test_optional_skill_must_be_owned_by_its_plugin(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["plugins"][1]["skills"][0]["path"] = "skills/core/volcengine-tosutil"
        self.assert_rejected(catalog)

    def test_core_skill_must_live_in_core(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["plugins"][0]["skills"][0]["path"] = (
            "plugins/volcengine-core/skills/volcengine-cli"
        )
        self.assert_rejected(catalog)

    def test_only_volcengine_core_may_be_default(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["plugins"][0]["default"] = False
        catalog["plugins"][1]["default"] = True
        self.assert_rejected(catalog)

    def test_duplicate_plugin_is_rejected(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["plugins"].append(copy.deepcopy(catalog["plugins"][1]))
        self.assert_rejected(catalog)

    def test_output_outside_repository_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            SYNC.ensure_safe_output(REPO_ROOT.parent / "outside-volcengine-sync.json")


if __name__ == "__main__":
    unittest.main()
