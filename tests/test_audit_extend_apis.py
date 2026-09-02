"""Offline tests for skills/core/volcengine-cli/scripts/audit_extend_apis.py.

`ve` is replaced by an injected runner that returns canned `ve <service>`
output, so the audit's parsing and classification are exercised without the
real CLI or any network.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "core" / "volcengine-cli" / "scripts" / "audit_extend_apis.py"
REFERENCE = REPO_ROOT / "skills" / "core" / "volcengine-cli" / "references" / "extend-apis.md"
SPEC = importlib.util.spec_from_file_location("audit_extend_apis", SCRIPT)
assert SPEC and SPEC.loader
AUDIT = importlib.util.module_from_spec(SPEC)
sys.modules["audit_extend_apis"] = AUDIT
SPEC.loader.exec_module(AUDIT)

KNOWN_SERVICE_HELP = """vmp

Usage:
  ve vmp [action] [params]

Available Actions:
  Action                Description
  ------                -----------
  CreateWorkspace       CreateWorkspace
  {extra}

Flags:
  -h, --help   Show help

Use "ve vmp [action] --help" for more information about an action.

Reserved double-dash controls (not API parameters):
  --header string      Add a custom HTTP header as Name=Value; repeatable.
  UnexpectedToken      must not be parsed as an action
"""

UNKNOWN_SERVICE_HELP = """Usage:
  ve domain_openapi <action> [--Param value ...] [system flags]
"""

SAMPLE_REFERENCE = """# Extended APIs

## 1. `ve --force`

| Service code | Version | `--endpoint` | `--region` | Method | Actions |
| --- | --- | --- | --- | --- | --- |
| `CDN` (uppercase) | `2021-03-01` | `cdn.volcengineapi.com` | `cn-north-1` | POST | `DescribeOriginTopStatisticalData` |
| `veenedge` | `2021-04-30` | `veenedge.volcengineapi.com` | `cn-north-1` | POST | `StopCloudServer`, `RebootCloudServer` (param `cloud_server_id`) |
| `vmp` | `2021-03-03` | `vmp.<region>.volcengineapi.com` | that region | POST | helper only (section 2) |

## 2. helper

| Service | Version | Endpoint | Body | Actions and URL query keys |
| --- | --- | --- | --- | --- |
| `vmp` | `2021-03-03` | x | y | `QueryMetrics` → `workspace` |
"""


def fake_runner(listing: dict[str, str]):
    def run(cmd, **kwargs):
        service = cmd[1]
        out = listing.get(service, UNKNOWN_SERVICE_HELP)
        return subprocess.CompletedProcess(cmd, 0, stdout=out, stderr="")
    return run


class ParseRecipesTest(unittest.TestCase):
    def test_parses_only_section_one_rows(self) -> None:
        recipes = AUDIT.parse_force_recipes(SAMPLE_REFERENCE)
        self.assertEqual(recipes["CDN"], {"DescribeOriginTopStatisticalData"})
        self.assertEqual(recipes["veenedge"], {"StopCloudServer", "RebootCloudServer"})
        self.assertNotIn("QueryMetrics", recipes.get("vmp", set()))
        self.assertNotIn("vmp", recipes, "helper-only row has no backticked actions")

    def test_real_reference_parses_and_has_no_helper_names_in_force_table(self) -> None:
        recipes = AUDIT.parse_force_recipes(REFERENCE.read_text(encoding="utf-8"))
        self.assertIn("dcdn", recipes)
        self.assertIn("DescribeRealtimeData", recipes["dcdn"])
        for helper_only in ("QueryMetrics", "ListGWSDirectory"):
            self.assertFalse(any(helper_only in actions for actions in recipes.values()), helper_only)


class CliActionsTest(unittest.TestCase):
    def test_known_service_lists_actions(self) -> None:
        runner = fake_runner({"vmp": KNOWN_SERVICE_HELP.format(extra="GetWorkspace          GetWorkspace")})
        self.assertEqual(AUDIT.cli_actions("vmp", runner), {"CreateWorkspace", "GetWorkspace"})

    def test_unknown_service_is_none_even_with_exit_zero(self) -> None:
        self.assertIsNone(AUDIT.cli_actions("domain_openapi", fake_runner({})))

    def test_uppercase_service_code_falls_back_to_lowercase_command(self) -> None:
        listing = {"cdn": KNOWN_SERVICE_HELP.format(extra="ListCdnDomains        ListCdnDomains")}
        self.assertEqual(AUDIT.cli_actions("CDN", fake_runner(listing)), {"CreateWorkspace", "ListCdnDomains"})

    def test_trailer_and_reserved_sections_are_not_actions(self) -> None:
        actions = AUDIT.parse_cli_actions(KNOWN_SERVICE_HELP.format(extra=""))
        self.assertEqual(actions, {"CreateWorkspace"})

    def test_missing_ve_is_reported(self) -> None:
        def run(cmd, **kwargs):
            raise FileNotFoundError("ve")
        with self.assertRaises(SystemExit):
            AUDIT.cli_actions("vmp", run)


class AuditReportTest(unittest.TestCase):
    def test_reports_actions_that_moved_into_cli(self) -> None:
        recipes = AUDIT.parse_force_recipes(SAMPLE_REFERENCE)
        helper = {"vmp": {"QueryMetrics"}}
        runner = fake_runner({
            "veenedge": KNOWN_SERVICE_HELP.format(extra="StopCloudServer       StopCloudServer"),
            "vmp": KNOWN_SERVICE_HELP.format(extra="QueryMetrics          QueryMetrics"),
        })
        report = AUDIT.audit(recipes, helper, runner)
        moved = {(i["service"], i["action"], i["via"]) for i in report["now_in_cli"]}
        self.assertEqual(moved, {("veenedge", "StopCloudServer", "force"), ("vmp", "QueryMetrics", "helper")})
        still = {(i["service"], i["action"]) for i in report["still_extension"]}
        self.assertIn(("veenedge", "RebootCloudServer"), still)
        self.assertIn(("CDN", "DescribeOriginTopStatisticalData"), still)
        self.assertEqual(report["unknown_service"], ["CDN"])

    def test_cdn_is_known_via_lowercase_but_action_still_missing(self) -> None:
        recipes = AUDIT.parse_force_recipes(SAMPLE_REFERENCE)
        runner = fake_runner({
            "cdn": KNOWN_SERVICE_HELP.format(extra=""),
            "veenedge": KNOWN_SERVICE_HELP.format(extra=""),
        })
        report = AUDIT.audit(recipes, {}, runner)
        self.assertEqual(report["unknown_service"], [])
        self.assertIn(("CDN", "DescribeOriginTopStatisticalData"), {(i["service"], i["action"]) for i in report["still_extension"]})

    def test_clean_report_when_nothing_moved(self) -> None:
        recipes = AUDIT.parse_force_recipes(SAMPLE_REFERENCE)
        report = AUDIT.audit(recipes, {}, fake_runner({"veenedge": KNOWN_SERVICE_HELP.format(extra="")}))
        self.assertEqual(report["now_in_cli"], [])


if __name__ == "__main__":
    unittest.main()
