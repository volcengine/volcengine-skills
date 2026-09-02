"""Offline tests for skills/core/volcengine-cli/scripts/call_extend_api.py.

Covers registry scope (only query+body APIs), free mode, request shaping and
signing. No network: requests are built but never sent.
"""

from __future__ import annotations

import datetime
import importlib.util
import json
import sys
import unittest
from unittest import mock
from argparse import Namespace
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "core" / "volcengine-cli" / "scripts" / "call_extend_api.py"
SPEC = importlib.util.spec_from_file_location("call_extend_api", SCRIPT)
assert SPEC and SPEC.loader
CEA = importlib.util.module_from_spec(SPEC)
sys.modules["call_extend_api"] = CEA  # dataclasses need the module registered before exec
SPEC.loader.exec_module(CEA)

FIXED_NOW = datetime.datetime(2026, 1, 2, 3, 4, 5, tzinfo=datetime.timezone.utc)


def make_args(**overrides) -> Namespace:
    base = dict(
        api_name=None,
        params="{}",
        service=None,
        version=None,
        query_keys=None,
        body_keys_also=None,
        method=None,
        region=None,
        host=None,
        scheme=None,
        content_type=None,
        session_token=None,
        profile=None,
        output="json",
        show_headers=False,
        list=False,
        describe=None,
    )
    base.update(overrides)
    return Namespace(**base)


class RegistryScopeTest(unittest.TestCase):
    def test_registry_only_holds_query_body_apis(self) -> None:
        self.assertEqual(len(CEA.API_REGISTRY), 16)
        for entry in CEA.API_REGISTRY:
            self.assertTrue(entry["query_keys"], entry["name"])
            self.assertEqual(entry["method"], "POST", entry["name"])
        self.assertEqual(sum(e["service"] == "vmp" for e in CEA.API_REGISTRY), 5)
        self.assertEqual(sum(e["service"] == "flink" for e in CEA.API_REGISTRY), 11)

    def test_registry_names_are_unique(self) -> None:
        names = [e["name"] for e in CEA.API_REGISTRY]
        self.assertEqual(len(names), len(set(names)))

    def test_unknown_api_points_to_ve_force(self) -> None:
        with self.assertRaises(SystemExit) as ctx:
            CEA.resolve_api("DescribeSomething", None)
        self.assertIn("--force", str(ctx.exception))

    def test_parser_accepts_free_mode_flags(self) -> None:
        parser = CEA.build_parser()
        args = parser.parse_args(
            ["--api", "X", "--service", "svc", "--version", "2024-01-01", "--query-keys", "a,b", "--body-keys-also", "a"]
        )
        self.assertEqual(args.query_keys, "a,b")
        self.assertEqual(args.body_keys_also, "a")


class SplitQueryBodyTest(unittest.TestCase):
    def test_split_moves_query_keys_out_of_body(self) -> None:
        query, body = CEA.split_query_body({"ProjectId": "p1", "Name": "n"}, ["ProjectId"])
        self.assertEqual(query, {"ProjectId": "p1"})
        self.assertEqual(body, {"Name": "n"})

    def test_preserve_keeps_key_in_both(self) -> None:
        query, body = CEA.split_query_body({"ProjectId": "p1", "Name": "n"}, ["ProjectId"], ["ProjectId"])
        self.assertEqual(query, {"ProjectId": "p1"})
        self.assertEqual(body, {"ProjectId": "p1", "Name": "n"})

    def test_no_query_keys_means_everything_in_body(self) -> None:
        query, body = CEA.split_query_body({"a": 1}, None)
        self.assertEqual((query, body), ({}, {"a": 1}))


class FreeModeTest(unittest.TestCase):
    def test_free_mode_requires_service_and_version(self) -> None:
        with self.assertRaises(SystemExit) as ctx:
            CEA.resolve_entry(make_args(api_name="Foo", query_keys="a"))
        self.assertIn("--service", str(ctx.exception))
        self.assertIn("--version", str(ctx.exception))

    def test_free_mode_without_query_keys_redirects_to_ve_force(self) -> None:
        with self.assertRaises(SystemExit) as ctx:
            CEA.resolve_entry(make_args(api_name="Foo", service="svc", version="2024-01-01"))
        self.assertIn("ve svc Foo --version 2024-01-01", str(ctx.exception))
        self.assertIn("--force", str(ctx.exception))

    def test_free_mode_host_defaults_to_open_endpoint(self) -> None:
        with mock.patch.object(CEA, "env", lambda name, default="": ""):
            args = make_args(api_name="Foo", service="svc", version="2024-01-01", query_keys="a", params='{"a":1,"b":2}')
            shape = CEA.prepare_request_shape(CEA.resolve_entry(args), args)
        self.assertEqual(shape["host"], "open.volcengineapi.com")

    def test_free_mode_uses_endpoint_env_when_set(self) -> None:
        with mock.patch.object(CEA, "env", lambda name, default="": "env.example" if name == "VOLCENGINE_ENDPOINT" else ""):
            args = make_args(api_name="Foo", service="svc", version="2024-01-01", query_keys="a", params='{"a":1,"b":2}')
            shape = CEA.prepare_request_shape(CEA.resolve_entry(args), args)
        self.assertEqual(shape["host"], "env.example")

    def test_free_mode_builds_entry(self) -> None:
        entry = CEA.resolve_entry(
            make_args(api_name="Foo", service="svc", version="2024-01-01", query_keys="a, b", body_keys_also="a", method="post", host="h.example")
        )
        self.assertEqual(entry["service"], "svc")
        self.assertEqual(entry["version"], "2024-01-01")
        self.assertEqual(entry["query_keys"], ["a", "b"])
        self.assertEqual(entry["preserve_query_keys_in_body"], ["a"])
        self.assertEqual(entry["method"], "POST")
        self.assertTrue(entry["free_mode"])

    def test_body_keys_also_must_be_subset_of_query_keys(self) -> None:
        with self.assertRaises(SystemExit) as ctx:
            CEA.resolve_entry(make_args(api_name="Foo", service="svc", version="v", query_keys="a", body_keys_also="z", host="h.example"))
        self.assertIn("z", str(ctx.exception))

    def test_registered_api_rejects_query_keys_override(self) -> None:
        with self.assertRaises(SystemExit) as ctx:
            CEA.resolve_entry(make_args(api_name="QueryMetrics", query_keys="workspace"))
        self.assertIn("Drop --query-keys", str(ctx.exception))

    def test_registered_api_rejects_method_change(self) -> None:
        entry = CEA.resolve_entry(make_args(api_name="QueryMetrics"))
        with self.assertRaises(SystemExit):
            CEA.prepare_request_shape(entry, make_args(api_name="QueryMetrics", method="GET"))


class RequestShapeTest(unittest.TestCase):
    def test_vmp_shape_uses_region_host_and_form_body(self) -> None:
        args = make_args(api_name="QueryMetrics", params='{"workspace":"ws-1","query":"up"}', region="cn-shanghai")
        entry = CEA.resolve_entry(args)
        shape = CEA.prepare_request_shape(entry, args)
        self.assertEqual(shape["host"], "vmp.cn-shanghai.volcengineapi.com")
        self.assertEqual(shape["content_type"], CEA.FORM_CONTENT_TYPE)
        self.assertEqual(shape["query"], {"workspace": "ws-1"})
        self.assertEqual(shape["body"], {"query": "up"})
        self.assertEqual(shape["region"], "cn-shanghai")

    def test_flink_shape_keeps_project_id_in_both_when_preserved(self) -> None:
        args = make_args(api_name="CreateGWSApplicationDraft", params='{"ProjectId":"p1","Name":"job"}')
        shape = CEA.prepare_request_shape(CEA.resolve_entry(args), args)
        self.assertEqual(shape["host"], "open.volcengineapi.com")
        self.assertEqual(shape["query"], {"ProjectId": "p1"})
        self.assertEqual(shape["body"], {"ProjectId": "p1", "Name": "job"})
        self.assertEqual(shape["content_type"], CEA.JSON_CONTENT_TYPE)

    def test_explicit_host_and_content_type_override(self) -> None:
        args = make_args(api_name="GetLabels", params='{"workspace":"ws"}', host="example.internal", content_type="application/json")
        shape = CEA.prepare_request_shape(CEA.resolve_entry(args), args)
        self.assertEqual(shape["host"], "example.internal")
        self.assertEqual(shape["content_type"], "application/json")

    def test_free_mode_uses_explicit_host(self) -> None:
        args = make_args(api_name="Foo", service="svc", version="2024-01-01", query_keys="Id", host="svc.example", params='{"Id":"x","Body":1}')
        shape = CEA.prepare_request_shape(CEA.resolve_entry(args), args)
        self.assertEqual(shape["host"], "svc.example")
        self.assertEqual(shape["query"], {"Id": "x"})
        self.assertEqual(shape["body"], {"Body": 1})

    def test_non_https_scheme_is_rejected(self) -> None:
        args = make_args(api_name="GetLabels", params='{"workspace":"ws"}', scheme="http")
        with self.assertRaises(SystemExit):
            CEA.prepare_request_shape(CEA.resolve_entry(args), args)


class ResponseFailedTest(unittest.TestCase):
    def test_http_error_fails(self) -> None:
        self.assertTrue(CEA.response_failed({"ResponseMetadata": {}}, 403))

    def test_error_inside_http_200_fails(self) -> None:
        self.assertTrue(CEA.response_failed({"ResponseMetadata": {"Error": {"Code": "AccessDenied"}}}, 200))

    def test_success_and_non_json_pass(self) -> None:
        self.assertFalse(CEA.response_failed({"ResponseMetadata": {"RequestId": "x"}, "Result": {}}, 200))
        self.assertFalse(CEA.response_failed({"ResponseMetadata": {"Error": None}}, 200))
        self.assertFalse(CEA.response_failed("plain text", 200))


class SigningTest(unittest.TestCase):
    def build(self, **overrides):
        kwargs = dict(
            ak="AKTEST",
            sk="SKTEST",
            session_token="",
            region="cn-beijing",
            host="open.volcengineapi.com",
            service="flink",
            version="2021-06-01",
            action="ListGWSDirectory",
            method="POST",
            content_type=CEA.JSON_CONTENT_TYPE,
            query={"ProjectId": "p1", "Type": "dir"},
            body={"Path": "/a b"},
            now=FIXED_NOW,
        )
        kwargs.update(overrides)
        return CEA.build_signed_request(**kwargs)

    def test_post_puts_query_keys_in_url_and_rest_in_json_body(self) -> None:
        req = self.build()
        parts = urlsplit(req.full_url)
        self.assertEqual(parts.scheme, "https")
        self.assertEqual(parts.netloc, "open.volcengineapi.com")
        qs = parse_qs(parts.query)
        self.assertEqual(qs["Action"], ["ListGWSDirectory"])
        self.assertEqual(qs["Version"], ["2021-06-01"])
        self.assertEqual(qs["ProjectId"], ["p1"])
        self.assertNotIn("Path", qs)
        self.assertEqual(json.loads(req.data.decode("utf-8")), {"Path": "/a b"})
        self.assertEqual(req.get_method(), "POST")

    def test_form_body_is_urlencoded(self) -> None:
        req = self.build(
            host="vmp.cn-beijing.volcengineapi.com",
            service="vmp",
            version="2021-03-03",
            action="QueryMetrics",
            content_type=CEA.FORM_CONTENT_TYPE,
            query={"workspace": "ws"},
            body={"query": "up{job=\"a\"}"},
        )
        self.assertEqual(req.data.decode("utf-8"), "query=up%7Bjob%3D%22a%22%7D")
        self.assertEqual(req.get_header("Content-type"), CEA.FORM_CONTENT_TYPE)

    def test_get_folds_body_into_query_and_sends_no_data(self) -> None:
        req = self.build(method="GET", query={"Id": "1"}, body={"Extra": "x"})
        qs = parse_qs(urlsplit(req.full_url).query)
        self.assertEqual(qs["Extra"], ["x"])
        self.assertEqual(qs["Id"], ["1"])
        self.assertIsNone(req.data)
        self.assertEqual(req.get_method(), "GET")

    def test_signature_headers_and_golden_value(self) -> None:
        req = self.build()
        self.assertEqual(req.get_header("X-date"), "20260102T030405Z")
        self.assertEqual(req.get_header("Host"), "open.volcengineapi.com")
        auth = req.get_header("Authorization")
        self.assertTrue(auth.startswith("HMAC-SHA256 Credential=AKTEST/20260102/cn-beijing/flink/request, "))
        self.assertIn("SignedHeaders=content-type;host;x-content-sha256;x-date", auth)
        self.assertEqual(req.get_header("X-content-sha256"), CEA.hash_sha256(json.dumps({"Path": "/a b"})))
        # Any change to canonicalisation or key derivation must be deliberate.
        self.assertEqual(auth.rsplit("Signature=", 1)[1], self.expected_signature(req))

    def expected_signature(self, req) -> str:
        # Recompute independently from the request pieces so the golden test
        # is self-validating rather than a pasted constant.
        canonical_query = urlsplit(req.full_url).query
        body = (req.data or b"").decode("utf-8")
        x_date = req.get_header("X-date")
        content_sha = CEA.hash_sha256(body)
        canonical = "\n".join(
            [
                req.get_method(),
                "/",
                canonical_query,
                "\n".join(
                    [
                        "content-type:" + req.get_header("Content-type"),
                        "host:" + req.get_header("Host"),
                        "x-content-sha256:" + content_sha,
                        "x-date:" + x_date,
                    ]
                ),
                "",
                "content-type;host;x-content-sha256;x-date",
                content_sha,
            ]
        )
        scope = f"{x_date[:8]}/cn-beijing/flink/request"
        string_to_sign = "\n".join(["HMAC-SHA256", x_date, scope, CEA.hash_sha256(canonical)])
        k = CEA.hmac_sha256(b"SKTEST", x_date[:8])
        k = CEA.hmac_sha256(k, "cn-beijing")
        k = CEA.hmac_sha256(k, "flink")
        k = CEA.hmac_sha256(k, "request")
        return CEA.hmac_sha256(k, string_to_sign).hex()

    def test_session_token_header(self) -> None:
        req = self.build(session_token="STS-TOKEN")
        self.assertEqual(req.get_header("X-security-token"), "STS-TOKEN")

    def test_norm_query_sorts_and_encodes(self) -> None:
        self.assertEqual(CEA.norm_query({"b": "x y", "a": ["1", "2"]}), "a=1&a=2&b=x%20y")


if __name__ == "__main__":
    unittest.main()
