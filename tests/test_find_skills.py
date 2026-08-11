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

    def test_list_contains_every_catalogued_skill_and_maps_to_its_plugin(self) -> None:
        records = list(FINDER.iter_records(self.catalog))
        expected_names = [
            skill["name"]
            for plugin in self.catalog["plugins"]
            for skill in plugin["skills"]
        ]
        self.assertEqual([record["name"] for record in records], expected_names)
        for record in records:
            with self.subTest(skill=record["name"]):
                plugin, resolved = FINDER.resolve_target(
                    self.catalog, record["name"]
                )
                self.assertEqual(plugin["name"], record["plugin"])
                self.assertEqual([item["name"] for item in resolved], [record["name"]])

    def test_search_subcommand_is_not_available(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(
            SystemExit
        ) as raised:
            FINDER.build_parser().parse_args(["search", "object storage"])
        self.assertEqual(raised.exception.code, 2)

    def test_install_accepts_exact_skills_only(self) -> None:
        records = FINDER.resolve_skills(
            self.catalog, ["volcengine-iac", "volcengine-tosutil"]
        )
        self.assertEqual(
            [record["name"] for record in records],
            ["volcengine-iac", "volcengine-tosutil"],
        )
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            FINDER.resolve_skills(self.catalog, ["volcengine-service-support"])

    def test_install_parser_has_no_plugin_method(self) -> None:
        args = FINDER.build_parser().parse_args(
            ["install", "volcengine-iac", "--agent", "codex", "--dry-run"]
        )
        self.assertEqual(args.targets, ["volcengine-iac"])
        self.assertFalse(hasattr(args, "method"))

    @mock.patch.object(FINDER.subprocess, "run")
    def test_json_reader_retries_truncated_success_output(self, run) -> None:
        run.side_effect = [
            self.completed(0, '[{"name": "incomplete"}'),
            self.completed(0, '[{"name": "volcengine-iac"}]'),
        ]
        completed, payload = FINDER.run_json(["npx", "skills", "list"])
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(payload, [{"name": "volcengine-iac"}])
        self.assertEqual(run.call_count, 2)

    @mock.patch.object(FINDER.subprocess, "run")
    def test_installed_skill_reader_falls_back_to_plain_output(self, run) -> None:
        run.side_effect = [
            self.completed(0, "["),
            self.completed(0, "["),
            self.completed(0, "["),
            self.completed(
                0,
                "  \x1b[36mvolcengine-iac\x1b[0m  "
                "~/.agents/skills/volcengine-iac  Agents: Codex\n",
            ),
        ]
        installed = FINDER.installed_skill_names(self.catalog, "codex", "global")
        self.assertEqual(installed, {"volcengine-iac"})
        self.assertEqual(run.call_count, 4)

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
        self.assertEqual(install_command[:4], ["npx", "--yes", "skills", "add"])
        self.assertNotIn("--global", install_command)
        self.assertIn("--full-depth", install_command)
        self.assertIn("volcengine-tosutil", install_command)
        self.assertNotIn("volcengine-storage", install_command)
        self.assertEqual(verify_command[-3:], ["--agent", "codex", "--json"])

    @mock.patch.object(FINDER.shutil, "which", return_value="/usr/bin/npx")
    @mock.patch.object(FINDER.subprocess, "run")
    def test_skills_install_fails_when_post_check_cannot_find_skill(
        self, run, _which
    ) -> None:
        run.side_effect = [
            self.completed(0),
            self.completed(0, "[]"),
        ]
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

    @mock.patch.object(FINDER.shutil, "which", return_value="/usr/bin/npx")
    @mock.patch.object(FINDER.subprocess, "run")
    def test_status_reports_installed_skills_instead_of_plugins(
        self, run, _which
    ) -> None:
        run.return_value = self.completed(
            0, json.dumps([{"name": "volcengine-tosutil"}])
        )
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            FINDER.show_status(self.catalog, "codex", "global", True)

        rows = json.loads(output.getvalue())
        states = {row["skill"]: row["state"] for row in rows}
        self.assertEqual(states["volcengine-tosutil"], "installed")
        self.assertEqual(states["volcengine-iac"], "not_installed")
        command = run.call_args.args[0]
        self.assertEqual(command[:4], ["npx", "--yes", "skills", "list"])
        self.assertNotIn("plugin", command)


if __name__ == "__main__":
    unittest.main()
