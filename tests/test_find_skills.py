from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import subprocess
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
FINDER_PATH = (
    REPO_ROOT
    / "skills"
    / "core"
    / "volcengine-find-skills"
    / "scripts"
    / "find_skills.py"
)
SPEC = importlib.util.spec_from_file_location("find_skills", FINDER_PATH)
assert SPEC and SPEC.loader
FINDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FINDER)


class FinderInstallVerificationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = FINDER.load_catalog()
        self.record = next(
            record
            for record in FINDER.iter_records(self.catalog)
            if record["name"] == "volcengine-tosutil"
        )

    def completed(self, returncode: int, stdout: str = "", stderr: str = ""):
        return subprocess.CompletedProcess([], returncode, stdout=stdout, stderr=stderr)

    def test_every_catalogued_skill_is_findable_and_maps_to_its_plugin(self) -> None:
        for record in FINDER.iter_records(self.catalog):
            with self.subTest(skill=record["name"]):
                matches = FINDER.search_records(self.catalog, record["name"])
                self.assertTrue(matches)
                self.assertEqual(matches[0]["name"], record["name"])
                plugin, resolved = FINDER.resolve_target(
                    self.catalog, record["name"]
                )
                self.assertEqual(plugin["name"], record["plugin"])
                self.assertEqual([item["name"] for item in resolved], [record["name"]])

    @mock.patch.object(FINDER.shutil, "which", return_value="/usr/bin/npx")
    @mock.patch.object(FINDER.subprocess, "run")
    def test_skills_install_is_verified_from_project_list(self, run, _which) -> None:
        run.side_effect = [
            self.completed(0),
            self.completed(
                0,
                json.dumps(
                    [
                        {
                            "name": "volcengine-tosutil",
                            "path": "<installed-skill-path>",
                            "scope": "project",
                            "agents": ["Codex"],
                        }
                    ]
                ),
            ),
        ]
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            FINDER.install_skills_cli(
                self.catalog,
                [self.record],
                "codex",
                "project",
                "<reviewed-repository>",
                False,
                True,
            )

        payload = json.loads(output.getvalue())
        self.assertTrue(payload["verified"])
        self.assertEqual(payload["scope"], "project")
        install_command = run.call_args_list[0].args[0]
        verify_command = run.call_args_list[1].args[0]
        self.assertNotIn("--global", install_command)
        self.assertIn("--full-depth", install_command)
        self.assertEqual(verify_command[-3:], ["--agent", "codex", "--json"])

    @mock.patch.object(FINDER.shutil, "which", return_value="/usr/bin/npx")
    @mock.patch.object(FINDER.subprocess, "run")
    def test_skills_install_fails_when_post_check_cannot_find_skill(
        self, run, _which
    ) -> None:
        run.side_effect = [self.completed(0), self.completed(0, "[]")]
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            FINDER.install_skills_cli(
                self.catalog,
                [self.record],
                "codex",
                "global",
                None,
                False,
                True,
            )


if __name__ == "__main__":
    unittest.main()
