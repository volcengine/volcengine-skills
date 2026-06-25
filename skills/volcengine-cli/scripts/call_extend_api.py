#!/usr/bin/env python3
# Copyright (c) 2026 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: MIT
"""
Call selected Volcengine extension APIs.

This helper intentionally keeps request signing inline.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import hmac
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from typing import Any
from urllib import error as urllib_error
from urllib import request as urllib_request
from urllib.parse import quote, urlencode


DEFAULT_REGION = "cn-beijing"
DEFAULT_HOST = "open.volcengineapi.com"
CLI_CONFIG_FILE_ENV = "VOLCENGINE_CLI_CONFIG_FILE"
LOGIN_CACHE_DIRECTORY_ENV = "VOLCENGINE_LOGIN_CACHE_DIRECTORY"


@dataclass(frozen=True)
class ResolvedCredentials:
    ak: str
    sk: str
    session_token: str = ""
    provider_name: str = ""


class CredentialResolutionError(RuntimeError):
    pass


API_REGISTRY: list[dict[str, Any]] = [
    {
        "name": "GetVerifyInfo",
        "service": "account_verify",
        "version": "2018-01-01",
        "method": "POST",
        "content_type": "application/json",
        "host": "open.volcengineapi.com",
        "scheme": "https",
        "call_style": "action_version",
        "summary": "Check account real-name verification status.",
    },
    {
        "name": "DescribeOriginTopStatisticalData",
        "service": "CDN",
        "version": "2021-03-01",
        "method": "POST",
        "content_type": "application/json",
        "host": "cdn.volcengineapi.com",
        "scheme": "https",
        "call_style": "action_version",
        "summary": "CDN origin-side top statistical data.",
    },
    {
        "name": "ListPipelineRunStagesInner",
        "service": "cp",
        "version": "2023-05-01",
        "method": "POST",
        "content_type": "application/json",
        "call_style": "universal",
        "summary": "CodePipeline internal stage list for a pipeline run, used to inspect failed stages/tasks.",
    },
    {
        "name": "DescribeRealtimeData",
        "service": "dcdn",
        "version": "2021-04-01",
        "method": "POST",
        "content_type": "application/json",
        "host": "open.volcengineapi.com",
        "scheme": "https",
        "call_style": "action_version",
        "summary": "DCDN realtime edge data.",
    },
    {
        "name": "DescribeOriginRealtimeData",
        "service": "dcdn",
        "version": "2021-04-01",
        "method": "POST",
        "content_type": "application/json",
        "host": "open.volcengineapi.com",
        "scheme": "https",
        "call_style": "action_version",
        "summary": "DCDN realtime origin data.",
    },
    {
        "name": "DescribeTopIPs",
        "service": "dcdn",
        "version": "2021-04-01",
        "method": "POST",
        "content_type": "application/json",
        "host": "open.volcengineapi.com",
        "scheme": "https",
        "call_style": "action_version",
        "summary": "DCDN top client IP ranking.",
    },
    {
        "name": "DescribeTopReferers",
        "service": "dcdn",
        "version": "2021-04-01",
        "method": "POST",
        "content_type": "application/json",
        "host": "open.volcengineapi.com",
        "scheme": "https",
        "call_style": "action_version",
        "summary": "DCDN top referer ranking.",
    },
    {
        "name": "DescribeTopUrls",
        "service": "dcdn",
        "version": "2021-04-01",
        "method": "POST",
        "content_type": "application/json",
        "host": "open.volcengineapi.com",
        "scheme": "https",
        "call_style": "action_version",
        "summary": "DCDN top URL ranking.",
    },
    {
        "name": "DescribeListenerLogs",
        "service": "ga",
        "version": "2022-03-01",
        "method": "POST",
        "content_type": "application/json",
        "host": "open.volcengineapi.com",
        "scheme": "https",
        "call_style": "action_version",
        "summary": "Global Accelerator listener logs.",
    },
    {
        "name": "GetAcceleratorDimension",
        "service": "ga",
        "version": "2022-03-01",
        "method": "POST",
        "content_type": "application/json",
        "host": "open.volcengineapi.com",
        "scheme": "https",
        "call_style": "action_version",
        "summary": "Global Accelerator metric dimensions for accelerator resources.",
    },
    {
        "name": "GetBandwidthPackage",
        "service": "ga",
        "version": "2022-03-01",
        "method": "POST",
        "content_type": "application/json",
        "host": "open.volcengineapi.com",
        "scheme": "https",
        "call_style": "action_version",
        "summary": "Global Accelerator bandwidth package detail.",
    },
    {
        "name": "GetBasicEndpointRelatedAccInstanceInfos",
        "service": "ga",
        "version": "2022-03-01",
        "method": "POST",
        "content_type": "application/json",
        "host": "open.volcengineapi.com",
        "scheme": "https",
        "call_style": "action_version",
        "summary": "Global Accelerator related basic accelerator instance info for an endpoint.",
    },
    {
        "name": "GetEndpointRelatedAccInstanceInfos",
        "service": "ga",
        "version": "2022-03-01",
        "method": "POST",
        "content_type": "application/json",
        "host": "open.volcengineapi.com",
        "scheme": "https",
        "call_style": "action_version",
        "summary": "Global Accelerator related accelerator instance info for an endpoint.",
    },
    {
        "name": "ListAccelerateAreas",
        "service": "ga",
        "version": "2022-03-01",
        "method": "GET",
        "content_type": "text/plain",
        "host": "open.volcengineapi.com",
        "scheme": "https",
        "call_style": "action_version",
        "summary": "List Global Accelerator acceleration areas.",
    },
    {
        "name": "ListBandwidthPackages",
        "service": "ga",
        "version": "2022-03-01",
        "method": "POST",
        "content_type": "application/json",
        "host": "open.volcengineapi.com",
        "scheme": "https",
        "call_style": "action_version",
        "summary": "List Global Accelerator bandwidth packages.",
    },
    {
        "name": "DescribeLiveBatchStreamTranscodeData",
        "service": "live",
        "version": "2023-01-01",
        "method": "POST",
        "content_type": "application/json",
        "host": "live.volcengineapi.com",
        "scheme": "https",
        "call_style": "action_version",
        "summary": "Live batch stream transcode data.",
    },
    {
        "name": "DescribeLiveBatchStreamSessionData",
        "service": "live",
        "version": "2023-01-01",
        "method": "POST",
        "content_type": "application/json",
        "host": "live.volcengineapi.com",
        "scheme": "https",
        "call_style": "action_version",
        "summary": "Live batch stream session data.",
    },
    {
        "name": "DescribeCdnDomainConfig",
        "service": "mcdn",
        "version": "2022-03-01",
        "method": "GET",
        "content_type": "text/plain",
        "host": "open.volcengineapi.com",
        "scheme": "https",
        "call_style": "action_version",
        "summary": "MCDN CDN domain configuration.",
    },
    {
        "name": "CreateVirtualNode",
        "service": "vke",
        "version": "2022-05-12",
        "method": "POST",
        "content_type": "application/json",
        "call_style": "universal",
        "summary": "Create a VKE virtual node.",
    },
    {
        "name": "ListVirtualNodes",
        "service": "vke",
        "version": "2022-05-12",
        "method": "POST",
        "content_type": "application/json",
        "call_style": "universal",
        "summary": "List VKE virtual nodes.",
    },
    {
        "name": "QueryMetrics",
        "service": "vmp",
        "version": "2021-03-03",
        "method": "POST",
        "content_type": "application/x-www-form-urlencoded",
        "query_keys": ["workspace"],
        "host_template": "vmp.{region}.volcengineapi.com",
        "scheme": "https",
        "summary": "VMP instant PromQL query for a workspace.",
    },
    {
        "name": "QueryMetricsRange",
        "service": "vmp",
        "version": "2021-03-03",
        "method": "POST",
        "content_type": "application/x-www-form-urlencoded",
        "query_keys": ["workspace"],
        "host_template": "vmp.{region}.volcengineapi.com",
        "scheme": "https",
        "summary": "VMP range PromQL query for a workspace.",
    },
    {
        "name": "GetLabelValues",
        "service": "vmp",
        "version": "2021-03-03",
        "method": "POST",
        "content_type": "application/x-www-form-urlencoded",
        "query_keys": ["workspace", "label"],
        "host_template": "vmp.{region}.volcengineapi.com",
        "scheme": "https",
        "summary": "VMP label values query.",
    },
    {
        "name": "GetLabels",
        "service": "vmp",
        "version": "2021-03-03",
        "method": "POST",
        "content_type": "application/x-www-form-urlencoded",
        "query_keys": ["workspace"],
        "host_template": "vmp.{region}.volcengineapi.com",
        "scheme": "https",
        "summary": "VMP label names query.",
    },
    {
        "name": "GetSeries",
        "service": "vmp",
        "version": "2021-03-03",
        "method": "POST",
        "content_type": "application/x-www-form-urlencoded",
        "query_keys": ["workspace"],
        "host_template": "vmp.{region}.volcengineapi.com",
        "scheme": "https",
        "summary": "VMP series query.",
    },
]


def add_actions(
    names: list[str],
    *,
    service: str,
    version: str,
    method: str,
    summary_prefix: str,
    content_type: str = "application/json",
    host: str | None = None,
    host_template: str | None = None,
    scheme: str | None = None,
    call_style: str = "action_version",
    query_keys: list[str] | None = None,
    preserve_query_keys_in_body: list[str] | None = None,
    test_only: bool = False,
) -> None:
    for name in names:
        entry = {
            "name": name,
            "service": service,
            "version": version,
            "method": method,
            "content_type": content_type,
            "call_style": call_style,
            "summary": f"{summary_prefix}: {name}.",
        }
        if host:
            entry["host"] = host
        if host_template:
            entry["host_template"] = host_template
        if scheme:
            entry["scheme"] = scheme
        if query_keys:
            entry["query_keys"] = query_keys
        if preserve_query_keys_in_body:
            entry["preserve_query_keys_in_body"] = preserve_query_keys_in_body
        if test_only:
            entry["test_only"] = True
        API_REGISTRY.append(entry)


add_actions(
    [
        "RunAlertInvestigator",
        "RunPcapAnalyzer",
        "RunAlertFormatter",
        "RunThreatIntelProducer",
        "RunWebRiskAssessor",
        "RunDlpScreenshotAnalyzer",
        "RunSensitiveDataDetector",
    ],
    service="sec_agent",
    version="2025-01-01",
    method="POST",
    summary_prefix="Security intelligent workflow",
    host="open.volcengineapi.com",
    scheme="https",
)

add_actions(
    ["CheckFee", "GetDomain", "GetAsyncTask", "GetTemplate", "ListDomains", "ListTemplates"],
    service="domain_openapi",
    version="2022-12-12",
    method="GET",
    summary_prefix="Domain service",
    content_type="text/plain",
    host="open.volcengineapi.com",
    scheme="https",
)
add_actions(
    ["RegisterDomain"],
    service="domain_openapi",
    version="2022-12-12",
    method="POST",
    summary_prefix="Domain service",
    host="open.volcengineapi.com",
    scheme="https",
)

add_actions(
    [
        "CallService",
        "GetAllLastDevicePropertyValue",
        "GetCustomTopicList",
        "GetDeviceDetail",
        "GetDeviceEventRecordList",
        "GetDeviceList",
        "GetDeviceOverview",
        "GetDeviceStatus",
        "GetDeviceServiceCallRecordList",
        "GetInstanceDetail",
        "GetInstanceEndpoints",
        "GetInstanceList",
        "GetLastDevicePropertyValue",
        "GetProductList",
        "GetProductDetail",
        "GetPropertyValuesByTime",
        "GetThingModel",
        "SetProperty",
    ],
    service="iot",
    version="2021-12-14",
    method="POST",
    summary_prefix="IoT device or instance operation",
    host="iot.cn-shanghai.volcengineapi.com",
    scheme="https",
)

add_actions(
    ["GetApplicant", "GetTrademark", "ListApplicants", "GetRequirement", "ListRequirements", "ListTrademarks", "ListBarrierTrademarks"],
    service="trademark",
    version="2023-06-01",
    method="GET",
    summary_prefix="Trademark query",
    content_type="text/plain",
    host="open.volcengineapi.com",
    scheme="https",
)
add_actions(
    ["SearchTrademarkInfo", "SearchTrademark"],
    service="trademark",
    version="2023-06-01",
    method="POST",
    summary_prefix="Trademark search",
    host="open.volcengineapi.com",
    scheme="https",
)

add_actions(
    ["ListWorkspace", "GetWorkspaceInfo", "ListQueryClusters", "GetQueryCluster", "ListPreagg", "InfluxQuery", "MetricsQuery"],
    service="metrics",
    version="2024-06-29",
    method="POST",
    summary_prefix="Volcengine Metrics service",
    host_template="metrics.{region}.volcengineapi.com",
    scheme="https",
)

add_actions(
    [
        "StartCloudServer",
        "StopCloudServer",
        "RebootCloudServer",
    ],
    service="veenedge",
    version="2021-04-30",
    method="POST",
    summary_prefix="VEEN edge cloud mutation",
    host="veenedge.volcengineapi.com",
)
add_actions(
    [
        "GetVEENInstanceUsage",
        "GetVEEWInstanceUsage",
        "GetBandwidthUsage",
        "GetBillingUsageDetail",
    ],
    service="veenedge",
    version="2021-04-30",
    method="GET",
    summary_prefix="VEEN edge cloud query",
    content_type="text/plain",
    host="veenedge.volcengineapi.com",
)

add_actions(
    ["ListGMSProject", "GetGMSProjectDetail", "GetGRSAppById"],
    service="flink",
    version="2021-06-01",
    method="GET",
    summary_prefix="Flink management query",
    content_type="text/plain",
    host="open.volcengineapi.com",
    scheme="https",
    call_style="flink_path",
)
add_actions(
    ["ListGMCSResourcePool"],
    service="flink",
    version="2022-06-01",
    method="GET",
    summary_prefix="Flink management query",
    content_type="text/plain",
    host="open.volcengineapi.com",
    scheme="https",
    call_style="flink_path",
)
add_actions(
    ["ListGASLogs", "GetGWSApplication"],
    service="flink",
    version="2021-06-01",
    method="POST",
    summary_prefix="Flink GWS/GAS operation",
    host="open.volcengineapi.com",
    scheme="https",
    call_style="flink_path",
)
add_actions(
    ["ListGWSDirectory"],
    service="flink",
    version="2021-06-01",
    method="POST",
    summary_prefix="Flink GWS/GAS operation",
    host="open.volcengineapi.com",
    scheme="https",
    call_style="flink_path",
    query_keys=["ProjectId", "Type"],
)
add_actions(
    ["GetGWSApplicationDraft", "DeleteGWSApplication", "GWSGetEventList", "StartGWSApplication", "CancelGWSApplication", "RestartGWSApplication"],
    service="flink",
    version="2021-06-01",
    method="POST",
    summary_prefix="Flink GWS/GAS operation",
    host="open.volcengineapi.com",
    scheme="https",
    call_style="flink_path",
    query_keys=["ProjectId"],
)
add_actions(
    ["CreateGWSApplicationDraft", "UpdateGWSApplicationDraft"],
    service="flink",
    version="2021-06-01",
    method="POST",
    summary_prefix="Flink GWS/GAS operation",
    host="open.volcengineapi.com",
    scheme="https",
    call_style="flink_path",
    query_keys=["ProjectId"],
    preserve_query_keys_in_body=["ProjectId"],
)
add_actions(
    ["DeployGWSApplicationDraft"],
    service="flink",
    version="2021-06-01",
    method="POST",
    summary_prefix="Flink GWS/GAS operation",
    host="open.volcengineapi.com",
    scheme="https",
    call_style="flink_path",
    query_keys=["ProjectId", "Id"],
)
add_actions(
    ["ListGWSApplication"],
    service="flink",
    version="2021-06-01",
    method="POST",
    summary_prefix="Flink GWS/GAS operation",
    host="open.volcengineapi.com",
    scheme="https",
    call_style="flink_path",
    query_keys=["PageSize", "PageNum", "SortField", "SortOrder"],
)
add_actions(
    ["GetGMSUserToken"],
    service="flink",
    version="2021-06-01",
    method="GET",
    summary_prefix="Flink test-only token query",
    content_type="text/plain",
    host="open.volcengineapi.com",
    scheme="https",
    call_style="flink_path",
    test_only=True,
)


_REGION_BY_SERVICE = {
    "CDN": "cn-north-1",
    "dcdn": "cn-north-1",
    "ga": "cn-north-1",
    "live": "cn-north-1",
    "mcdn": "cn-north-1",
    "domain_openapi": "cn-north-1",
    "trademark": "cn-north-1",
    "veenedge": "cn-north-1",
    "iot": "cn-shanghai",
}
for _entry in API_REGISTRY:
    _region = _REGION_BY_SERVICE.get(_entry["service"])
    if _region:
        _entry["region"] = _region


def parse_json_value(raw: str | None) -> dict[str, Any]:
    if raw is None or raw == "":
        return {}
    if raw.startswith("@"):
        with open(raw[1:], "r", encoding="utf-8") as f:
            raw = f.read()
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON for --params: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit("--params must be a JSON object")
    return value


def env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def _env_value(env_getter, name: str) -> str:
    try:
        value = env_getter(name, "")
    except TypeError:
        value = env_getter(name)
    if value is None:
        return ""
    return str(value).strip()


def check_ve_login_status() -> str:
    try:
        completed = subprocess.run(
            ["ve", "sts", "GetCallerIdentity"],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except FileNotFoundError:
        return "`ve` command not found."
    except subprocess.TimeoutExpired:
        return "`ve sts GetCallerIdentity` timed out."

    output = "\n".join(part.strip() for part in (completed.stdout, completed.stderr) if part and part.strip())
    if completed.returncode == 0:
        return "`ve sts GetCallerIdentity` succeeded; current ve credentials are usable."
    return output or f"`ve sts GetCallerIdentity` failed with exit code {completed.returncode}."


def _config_path(env_getter=env) -> str:
    return _env_value(env_getter, CLI_CONFIG_FILE_ENV) or os.path.expanduser("~/.volcengine/config.json")


def _load_cli_config(env_getter=env) -> tuple[dict[str, Any], str]:
    path = _config_path(env_getter)
    if not os.path.isfile(path):
        raise CredentialResolutionError(f"Volcengine CLI config file not found at {path}.")
    try:
        with open(path, "r", encoding="utf-8") as f:
            value = json.load(f)
    except OSError as exc:
        raise CredentialResolutionError(f"Failed to read Volcengine CLI config file {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise CredentialResolutionError(f"Failed to parse Volcengine CLI config file {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CredentialResolutionError(f"Volcengine CLI config file {path} must contain a JSON object.")
    return value, path


def _select_profile_name(
    config: dict[str, Any],
    *,
    profile: str | None,
    env_getter=env,
) -> tuple[str, str]:
    explicit_profile = str(profile).strip() if profile else ""
    if explicit_profile:
        return explicit_profile, "--profile"
    current = config.get("current")
    if isinstance(current, str) and current.strip():
        return current.strip(), "current"
    env_profile = _env_value(env_getter, "VOLCENGINE_PROFILE")
    if env_profile:
        return env_profile, "VOLCENGINE_PROFILE"
    stack_profile = _env_value(env_getter, "VOLCSTACK_PROFILE")
    if stack_profile:
        return stack_profile, "VOLCSTACK_PROFILE"
    raise CredentialResolutionError(
        "No active Volcengine CLI profile is configured. Run `ve configure profile --profile <name>`, "
        "pass --profile after the user selects one, or set VOLCENGINE_ACCESS_KEY and VOLCENGINE_SECRET_KEY."
    )


def _get_profile(config: dict[str, Any], profile_name: str, profile_source: str) -> dict[str, Any]:
    profiles = config.get("profiles")
    if not isinstance(profiles, dict):
        raise CredentialResolutionError("Volcengine CLI config does not contain a valid profiles object.")
    profile = profiles.get(profile_name)
    if not isinstance(profile, dict):
        raise CredentialResolutionError(
            f"Volcengine CLI profile {profile_name!r} from {profile_source} was not found in config."
        )
    return profile


def _profile_value(profile: dict[str, Any], key: str) -> str:
    value = profile.get(key)
    return value.strip() if isinstance(value, str) else ""


def _login_cache_filename(login_session: str) -> str:
    return hashlib.sha1(login_session.encode("utf-8")).hexdigest() + ".json"


def _login_cache_dir(config_path: str, env_getter=env) -> str:
    custom = _env_value(env_getter, LOGIN_CACHE_DIRECTORY_ENV)
    if custom:
        return custom
    return os.path.join(os.path.dirname(config_path), "login", "cache")


def _parse_rfc3339(value: str) -> datetime.datetime:
    raw = value.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    parsed = datetime.datetime.fromisoformat(raw)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=datetime.timezone.utc)
    return parsed.astimezone(datetime.timezone.utc)


def _parse_console_login_access_token(access_token: Any, cache_path: str) -> tuple[str, str, str]:
    if isinstance(access_token, dict):
        creds = access_token
    elif isinstance(access_token, str):
        try:
            parsed = json.loads(access_token)
        except json.JSONDecodeError as exc:
            raise CredentialResolutionError(f"Failed to parse console-login access_token in {cache_path}: {exc}") from exc
        if not isinstance(parsed, dict):
            raise CredentialResolutionError(f"console-login access_token in {cache_path} is not a JSON object.")
        creds = parsed
    else:
        raise CredentialResolutionError(f"console-login token cache {cache_path} does not contain valid access_token.")

    ak = creds.get("access_key_id")
    sk = creds.get("secret_access_key")
    token = creds.get("session_token")
    ak = ak.strip() if isinstance(ak, str) else ""
    sk = sk.strip() if isinstance(sk, str) else ""
    token = token.strip() if isinstance(token, str) else ""
    if not ak or not sk or not token:
        raise CredentialResolutionError(f"console-login access_token in {cache_path} is missing STS credential fields.")
    return ak, sk, token


def _read_console_login_cache(
    *,
    profile_name: str,
    profile: dict[str, Any],
    config_path: str,
    env_getter=env,
) -> ResolvedCredentials:
    login_session = _profile_value(profile, "login-session")
    if not login_session:
        raise CredentialResolutionError(
            f"Volcengine CLI profile {profile_name!r} does not contain usable access-key/secret-key "
            "or login-session. Run `ve login` or `ve configure set` first."
        )
    cache_path = os.path.join(_login_cache_dir(config_path, env_getter), _login_cache_filename(login_session))
    try:
        with open(cache_path, "r", encoding="utf-8") as f:
            cache = json.load(f)
    except OSError as exc:
        raise CredentialResolutionError(
            f"Failed to read console-login cache for profile {profile_name!r} at {cache_path}: {exc}. "
            "Run `ve login` first."
        ) from exc
    except json.JSONDecodeError as exc:
        raise CredentialResolutionError(f"Failed to parse console-login cache {cache_path}: {exc}") from exc
    if not isinstance(cache, dict):
        raise CredentialResolutionError(f"console-login cache {cache_path} must contain a JSON object.")

    issued_at_raw = cache.get("issued_at")
    issued_at = issued_at_raw.strip() if isinstance(issued_at_raw, str) else ""
    try:
        expires_in = int(cache.get("expires_in", 0))
    except (TypeError, ValueError):
        expires_in = 0
    if not issued_at or expires_in <= 0:
        raise CredentialResolutionError(f"console-login cache {cache_path} is missing valid issued_at/expires_in.")
    try:
        expiration = _parse_rfc3339(issued_at) + datetime.timedelta(seconds=expires_in)
    except ValueError as exc:
        raise CredentialResolutionError(f"Failed to parse issued_at in console-login cache {cache_path}: {exc}") from exc
    if utc_now() >= expiration - datetime.timedelta(seconds=60):
        raise CredentialResolutionError(
            f"console-login cache for profile {profile_name!r} is expired. Run `ve login` to refresh it."
        )

    ak, sk, token = _parse_console_login_access_token(cache.get("access_token"), cache_path)
    return ResolvedCredentials(
        ak=ak,
        sk=sk,
        session_token=token,
        provider_name="VolcengineCLIConsoleLoginCache",
    )


def resolve_volcengine_credentials(
    *,
    profile: str | None = None,
    session_token: str | None = None,
    env_getter=env,
    notify=None,
) -> ResolvedCredentials:
    """Resolve AK/SK from env first, then from existing Volcengine CLI credentials."""
    env_ak = _env_value(env_getter, "VOLCENGINE_ACCESS_KEY")
    env_sk = _env_value(env_getter, "VOLCENGINE_SECRET_KEY")
    if env_ak and env_sk:
        return ResolvedCredentials(
            ak=env_ak,
            sk=env_sk,
            session_token=(
                str(session_token).strip()
                if session_token is not None
                else _env_value(env_getter, "VOLCENGINE_SESSION_TOKEN")
            ),
            provider_name="EnvironmentVariableCredentialProvider",
        )

    if notify:
        missing = []
        if not env_ak:
            missing.append("VOLCENGINE_ACCESS_KEY")
        if not env_sk:
            missing.append("VOLCENGINE_SECRET_KEY")
        notify(
            "{} not detected; checking `ve sts GetCallerIdentity` before reading existing ve profile/login-cache credentials.".format(
                " and ".join(missing)
            )
        )
        ve_status = check_ve_login_status()
        notify(f"ve credential check: {ve_status}")

    try:
        config, resolved_config_path = _load_cli_config(env_getter)
        profile_name, profile_source = _select_profile_name(config, profile=profile, env_getter=env_getter)
        selected_profile = _get_profile(config, profile_name, profile_source)

        ak = _profile_value(selected_profile, "access-key")
        sk = _profile_value(selected_profile, "secret-key")
        if ak and sk:
            return ResolvedCredentials(
                ak=ak,
                sk=sk,
                session_token=(
                    str(session_token).strip()
                    if session_token is not None
                    else _profile_value(selected_profile, "session-token")
                ),
                provider_name=f"VolcengineCLIProfile({profile_name})",
            )

        resolved = _read_console_login_cache(
            profile_name=profile_name,
            profile=selected_profile,
            config_path=resolved_config_path,
            env_getter=env_getter,
        )
    except CredentialResolutionError as exc:
        raise CredentialResolutionError(
            f"{exc} Run `ve login` or set VOLCENGINE_ACCESS_KEY and VOLCENGINE_SECRET_KEY environment variables."
        ) from exc

    if session_token is not None:
        return ResolvedCredentials(
            ak=resolved.ak,
            sk=resolved.sk,
            session_token=str(session_token).strip(),
            provider_name=resolved.provider_name,
        )
    return resolved


def split_query_body(
    params: dict[str, Any],
    query_keys: list[str] | None,
    preserve_query_keys_in_body: list[str] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if not query_keys:
        return {}, params
    preserve_query_keys_in_body = preserve_query_keys_in_body or []
    query: dict[str, Any] = {}
    body: dict[str, Any] = {}
    for key, value in params.items():
        if key in query_keys:
            query[key] = value
        if key not in query_keys or key in preserve_query_keys_in_body:
            body[key] = value
    return query, body


def norm_query(params: dict[str, Any]) -> str:
    query = ""
    for key in sorted(params.keys()):
        value = params[key]
        if isinstance(value, list):
            for item in value:
                query += quote(key, safe="-_.~") + "=" + quote(str(item), safe="-_.~") + "&"
        else:
            query += quote(key, safe="-_.~") + "=" + quote(str(value), safe="-_.~") + "&"
    return query[:-1].replace("+", "%20")


def hmac_sha256(key: bytes, content: str) -> bytes:
    return hmac.new(key, content.encode("utf-8"), hashlib.sha256).digest()


def hash_sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def signed_post_with_query(
    *,
    ak: str,
    sk: str,
    session_token: str,
    region: str,
    host: str,
    service: str,
    version: str,
    action: str,
    content_type: str,
    query: dict[str, Any],
    body: dict[str, Any],
    scheme: str,
) -> tuple[Any, int, dict[str, str]]:
    if content_type == "application/x-www-form-urlencoded":
        body_str = urlencode(body, doseq=True)
    else:
        body_str = json.dumps(body)

    request_query = {"Action": action, "Version": version, **query}
    x_date = utc_now().strftime("%Y%m%dT%H%M%SZ")
    short_x_date = x_date[:8]
    x_content_sha256 = hash_sha256(body_str)
    signed_headers = "content-type;host;x-content-sha256;x-date"
    canonical_request = "\n".join(
        [
            "POST",
            "/",
            norm_query(request_query),
            "\n".join(
                [
                    "content-type:" + content_type,
                    "host:" + host,
                    "x-content-sha256:" + x_content_sha256,
                    "x-date:" + x_date,
                ]
            ),
            "",
            signed_headers,
            x_content_sha256,
        ]
    )
    credential_scope = "/".join([short_x_date, region, service, "request"])
    string_to_sign = "\n".join(["HMAC-SHA256", x_date, credential_scope, hash_sha256(canonical_request)])
    k_date = hmac_sha256(sk.encode("utf-8"), short_x_date)
    k_region = hmac_sha256(k_date, region)
    k_service = hmac_sha256(k_region, service)
    k_signing = hmac_sha256(k_service, "request")
    signature = hmac_sha256(k_signing, string_to_sign).hex()
    headers = {
        "Host": host,
        "X-Content-Sha256": x_content_sha256,
        "X-Date": x_date,
        "Content-Type": content_type,
        "Authorization": (
            "HMAC-SHA256 Credential="
            + ak
            + "/"
            + credential_scope
            + ", SignedHeaders="
            + signed_headers
            + ", Signature="
            + signature
        ),
    }
    if session_token:
        headers["x-security-token"] = session_token

    url = f"{scheme}://{host}/?{norm_query(request_query)}"
    req = urllib_request.Request(
        url=url,
        data=body_str.encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib_request.urlopen(req, timeout=30) as response:
            status_code = response.status
            response_headers = dict(response.headers.items())
            response_text = response.read().decode("utf-8")
    except urllib_error.HTTPError as exc:
        status_code = exc.code
        response_headers = dict(exc.headers.items())
        response_text = exc.read().decode("utf-8")

    try:
        payload = json.loads(response_text)
    except json.JSONDecodeError:
        payload = response_text
    return payload, status_code, response_headers


def signed_action_version_request(
    *,
    ak: str,
    sk: str,
    session_token: str,
    region: str,
    host: str,
    service: str,
    version: str,
    action: str,
    method: str,
    content_type: str,
    query: dict[str, Any],
    body: dict[str, Any],
    scheme: str,
) -> tuple[Any, int, dict[str, str]]:
    method = method.upper()
    if method == "GET":
        request_query = {"Action": action, "Version": version, **body, **query}
        body_str = ""
    else:
        request_query = {"Action": action, "Version": version, **query}
        if content_type == "application/x-www-form-urlencoded":
            body_str = urlencode(body, doseq=True)
        else:
            body_str = json.dumps(body)

    x_date = utc_now().strftime("%Y%m%dT%H%M%SZ")
    short_x_date = x_date[:8]
    x_content_sha256 = hash_sha256(body_str)
    signed_headers = "content-type;host;x-content-sha256;x-date"
    canonical_request = "\n".join(
        [
            method,
            "/",
            norm_query(request_query),
            "\n".join(
                [
                    "content-type:" + content_type,
                    "host:" + host,
                    "x-content-sha256:" + x_content_sha256,
                    "x-date:" + x_date,
                ]
            ),
            "",
            signed_headers,
            x_content_sha256,
        ]
    )
    credential_scope = "/".join([short_x_date, region, service, "request"])
    string_to_sign = "\n".join(["HMAC-SHA256", x_date, credential_scope, hash_sha256(canonical_request)])
    k_date = hmac_sha256(sk.encode("utf-8"), short_x_date)
    k_region = hmac_sha256(k_date, region)
    k_service = hmac_sha256(k_region, service)
    k_signing = hmac_sha256(k_service, "request")
    signature = hmac_sha256(k_signing, string_to_sign).hex()
    headers = {
        "Host": host,
        "X-Content-Sha256": x_content_sha256,
        "X-Date": x_date,
        "Content-Type": content_type,
        "Authorization": (
            "HMAC-SHA256 Credential="
            + ak
            + "/"
            + credential_scope
            + ", SignedHeaders="
            + signed_headers
            + ", Signature="
            + signature
        ),
    }
    if session_token:
        headers["x-security-token"] = session_token

    url = f"{scheme}://{host}/?{norm_query(request_query)}"
    data = None if method == "GET" else body_str.encode("utf-8")
    req = urllib_request.Request(url=url, data=data, headers=headers, method=method)
    try:
        with urllib_request.urlopen(req, timeout=30) as response:
            status_code = response.status
            response_headers = dict(response.headers.items())
            response_text = response.read().decode("utf-8")
    except urllib_error.HTTPError as exc:
        status_code = exc.code
        response_headers = dict(exc.headers.items())
        response_text = exc.read().decode("utf-8")

    try:
        payload = json.loads(response_text)
    except json.JSONDecodeError:
        payload = response_text
    return payload, status_code, response_headers


def call_flink_path(
    *,
    ak: str,
    sk: str,
    session_token: str,
    region: str,
    host: str,
    service: str,
    version: str,
    action: str,
    method: str,
    content_type: str,
    params: dict[str, Any],
    query_keys: list[str] | None,
    preserve_query_keys_in_body: list[str] | None,
    scheme: str,
) -> tuple[Any, int, dict[str, str]]:
    if method == "GET":
        query = params
        body: dict[str, Any] = {}
    else:
        query, body = split_query_body(params, query_keys, preserve_query_keys_in_body)
    return signed_action_version_request(
        ak=ak,
        sk=sk,
        session_token=session_token,
        region=region,
        host=host,
        service=service,
        version=version,
        action=action,
        method=method,
        content_type=content_type,
        query=query,
        body=body,
        scheme=scheme,
    )


def resolve_host(entry: dict[str, Any], region: str, explicit_host: str | None) -> str:
    if explicit_host:
        return explicit_host
    if entry.get("host_template"):
        return entry["host_template"].format(region=region)
    if entry.get("host"):
        return entry["host"]
    return env("VOLCENGINE_ENDPOINT") or DEFAULT_HOST


def registry_by_name(include_test: bool = False) -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = {}
    for entry in API_REGISTRY:
        if entry.get("test_only") and not include_test:
            continue
        index.setdefault(entry["name"], []).append(entry)
    return index


def resolve_api(api_name: str, service: str | None, include_test: bool = False) -> dict[str, Any]:
    matches = registry_by_name(include_test).get(api_name, [])
    if service:
        matches = [entry for entry in matches if entry["service"] == service]
    if not matches:
        raise SystemExit(f"Unknown APIName: {api_name}. Use --list to inspect supported extension APIs.")
    if len(matches) > 1:
        services = ", ".join(sorted({entry["service"] for entry in matches}))
        raise SystemExit(f"APIName {api_name} is ambiguous across services: {services}. Pass --service.")
    return matches[0]


def action_kind(action: str) -> str:
    destructive_prefixes = ("Delete", "Terminate", "Release", "Revoke", "Modify", "Stop", "Detach", "Cancel")
    write_prefixes = ("Create", "Run", "Allocate", "Attach", "Associate", "Authorize", "Update", "Set", "Start", "Register", "Import")
    readonly_prefixes = ("Describe", "List", "Get", "Query", "Check", "Search")
    if action.startswith(destructive_prefixes):
        return "destructive"
    if action.startswith(write_prefixes):
        return "write"
    if action.startswith(readonly_prefixes):
        return "read"
    return "unknown"


def summarize_verify_info(payload: Any) -> dict[str, Any]:
    info = payload.get("Result", payload) if isinstance(payload, dict) else {}
    if not isinstance(info, dict):
        info = {}
    is_verified = info.get("IsVerified") is True
    identity_type = info.get("IdentityType")
    return {
        "is_verified": is_verified,
        "identity_type": identity_type,
        "individual_verified": is_verified and identity_type == "individual",
        "enterprise_verified": is_verified and identity_type == "enterprise",
    }


def derived_summary(entry: dict[str, Any], payload: Any) -> dict[str, Any] | None:
    if entry["service"] == "account_verify" and entry["name"] == "GetVerifyInfo":
        return {"verification": summarize_verify_info(payload)}
    return None


def print_list(include_test: bool = False) -> None:
    entries = [entry for entry in API_REGISTRY if include_test or not entry.get("test_only")]
    for entry in sorted(entries, key=lambda e: (e["service"], e["name"])):
        print(
            f"{entry['name']}\t{entry['service']}\t{entry['version']}\t"
            f"{entry['method']}\t{entry.get('summary', '')}"
        )


def print_describe(entry: dict[str, Any]) -> None:
    print(json.dumps(entry, ensure_ascii=False, indent=2))


def call_api(args: argparse.Namespace) -> int:
    entry = resolve_api(args.api_name, args.service, include_test=args.include_test)
    expected_method = entry["method"].upper()
    if args.method and args.method.upper() != expected_method:
        raise SystemExit(f"{entry['name']} uses method {expected_method}, not {args.method.upper()}")

    params = parse_json_value(args.params)
    query_params, body_params = split_query_body(params, entry.get("query_keys"), entry.get("preserve_query_keys_in_body"))
    region = args.region or entry.get("region") or env("VOLCENGINE_REGION") or DEFAULT_REGION
    host = resolve_host(entry, region, args.host)
    scheme = args.scheme or entry.get("scheme") or "https"
    if scheme != "https":
        raise SystemExit("Only HTTPS endpoints are supported by this helper.")
    content_type = args.content_type or entry.get("content_type") or "application/json"

    try:
        credentials = resolve_volcengine_credentials(
            profile=args.profile,
            session_token=args.session_token,
            notify=lambda message: print(message, file=sys.stderr),
        )
    except CredentialResolutionError as exc:
        raise SystemExit(str(exc)) from exc
    ak = credentials.ak
    sk = credentials.sk
    session_token = credentials.session_token

    if entry.get("call_style") == "flink_path":
        response, status_code, response_headers = call_flink_path(
            ak=ak,
            sk=sk,
            session_token=session_token,
            region=region,
            host=host,
            service=entry["service"],
            version=entry["version"],
            action=entry["name"],
            method=expected_method,
            content_type=content_type,
            params=params,
            query_keys=entry.get("query_keys"),
            preserve_query_keys_in_body=entry.get("preserve_query_keys_in_body"),
            scheme=scheme,
        )
    elif query_params and expected_method == "POST":
        response, status_code, response_headers = signed_post_with_query(
            ak=ak,
            sk=sk,
            session_token=session_token,
            region=region,
            host=host,
            service=entry["service"],
            version=entry["version"],
            action=entry["name"],
            content_type=content_type,
            query=query_params,
            body=body_params,
            scheme=scheme,
        )
    else:
        response, status_code, response_headers = signed_action_version_request(
            ak=ak,
            sk=sk,
            session_token=session_token,
            region=region,
            host=host,
            service=entry["service"],
            version=entry["version"],
            action=entry["name"],
            method=expected_method,
            content_type=content_type,
            query=query_params,
            body=body_params,
            scheme=scheme,
        )

    summary = derived_summary(entry, response)
    if args.output == "json":
        print(json.dumps(response, ensure_ascii=False))
    else:
        print(f"Status Code: {status_code}")
        print(json.dumps(response, ensure_ascii=False, indent=2))
        if summary:
            print("Derived Summary:")
            print(json.dumps(summary, ensure_ascii=False, indent=2))
        if args.show_headers:
            print("Response Headers:")
            print(json.dumps(dict(response_headers), ensure_ascii=False, indent=2, default=str))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Call Volcengine extension APIs")
    parser.add_argument("--api", "--api-name", dest="api_name", help="APIName/Action to call")
    parser.add_argument("--params", "--param", default="{}", help="JSON object or @file.json, default {}")
    parser.add_argument("--method", choices=["GET", "POST", "get", "post"], help="Optional method assertion")
    parser.add_argument("--service", help="ServiceCode disambiguator for duplicate API names")
    parser.add_argument("--region", help="Request region, default VOLCENGINE_REGION or cn-beijing")
    parser.add_argument("--host", help="Override endpoint host; otherwise uses the registry host or VOLCENGINE_ENDPOINT fallback")
    parser.add_argument("--scheme", choices=["https"], help="Override endpoint scheme; HTTPS only")
    parser.add_argument("--content-type", help="Override content type")
    parser.add_argument("--session-token", help="Override VOLCENGINE_SESSION_TOKEN")
    parser.add_argument("--profile", help="Volcengine CLI profile name for ve login/config credentials")
    parser.add_argument("--output", choices=["pretty", "json"], default="pretty")
    parser.add_argument("--show-headers", action="store_true")
    parser.add_argument("--include-test", action="store_true", help="Include test-only APIs in --list/--describe/calls")
    parser.add_argument("--list", action="store_true", help="List supported extension APIs")
    parser.add_argument("--describe", metavar="APIName", help="Print registry metadata for an API")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.list:
        print_list(include_test=args.include_test)
        return 0
    if args.describe:
        print_describe(resolve_api(args.describe, args.service, include_test=args.include_test))
        return 0
    if not args.api_name:
        parser.error("--api is required unless --list or --describe is used")
    return call_api(args)


if __name__ == "__main__":
    raise SystemExit(main())
