#!/usr/bin/env python3
"""Collect read-only CLB/ALB listener, health, server group, and backend ECS context.

Credentials are read only from environment variables:
VOLCENGINE_ACCESS_KEY / VOLCENGINE_SECRET_KEY / VOLCENGINE_REGION.
The script never writes credentials or changes load balancer, listener, server
group, backend, or ECS resources.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, Iterable, List, Set

import volcenginesdkalb
import volcenginesdkclb
import volcenginesdkcore
import volcenginesdkecs
from volcenginesdkcore.rest import ApiException


def to_dict(value: Any) -> Any:
    if hasattr(value, "to_dict"):
        return value.to_dict()
    return value


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"missing required environment variable: {name}")
    return value


def build_cfg(region: str):
    cfg = volcenginesdkcore.Configuration()
    cfg.ak = require_env("VOLCENGINE_ACCESS_KEY")
    cfg.sk = require_env("VOLCENGINE_SECRET_KEY")
    cfg.region = region
    cfg.client_side_validation = True
    return cfg


def collect_values(obj: Any, key_names: Iterable[str]) -> Set[str]:
    keys = set(key_names)
    found: Set[str] = set()
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in keys and isinstance(value, str) and value:
                found.add(value)
            found.update(collect_values(value, keys))
    elif isinstance(obj, list):
        for item in obj:
            found.update(collect_values(item, keys))
    return found


def has_positive_counter(obj: Any, key_names: Iterable[str]) -> bool:
    keys = set(key_names)
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in keys:
                try:
                    if int(value) > 0:
                        return True
                except (TypeError, ValueError):
                    if isinstance(value, str) and value.lower() not in ("", "0", "false", "none", "null"):
                        return True
            if has_positive_counter(value, keys):
                return True
    elif isinstance(obj, list):
        return any(has_positive_counter(item, keys) for item in obj)
    return False


def list_from(resp: Dict[str, Any], *keys: str) -> List[Dict[str, Any]]:
    for key in keys:
        value = resp.get(key)
        if isinstance(value, list):
            return value
    result = resp.get("result") or {}
    for key in keys:
        value = result.get(key)
        if isinstance(value, list):
            return value
    return []


def describe_ecs(region: str, instance_ids: List[str]) -> Dict[str, Any]:
    if not instance_ids:
        return {"instances": []}
    ecs = volcenginesdkecs.ECSApi(volcenginesdkcore.ApiClient(build_cfg(region)))
    return to_dict(
        ecs.describe_instances(
            volcenginesdkecs.DescribeInstancesRequest(
                instance_ids=instance_ids[:100],
                max_results=100,
            )
        )
    )


def collect_clb(region: str, load_balancer_id: str, listener_id: str = "") -> Dict[str, Any]:
    clb = volcenginesdkclb.CLBApi(volcenginesdkcore.ApiClient(build_cfg(region)))
    lb_resp = to_dict(
        clb.describe_load_balancers(
            volcenginesdkclb.DescribeLoadBalancersRequest(
                load_balancer_ids=[load_balancer_id],
                page_size=20,
            )
        )
    )
    listeners_resp = to_dict(
        clb.describe_listeners(
            volcenginesdkclb.DescribeListenersRequest(
                load_balancer_id=load_balancer_id,
                listener_ids=[listener_id] if listener_id else None,
                page_size=100,
            )
        )
    )
    server_groups_resp = to_dict(
        clb.describe_server_groups(
            volcenginesdkclb.DescribeServerGroupsRequest(
                load_balancer_id=load_balancer_id,
                page_size=100,
            )
        )
    )
    listeners = list_from(listeners_resp, "listeners", "Listeners")
    server_groups = list_from(server_groups_resp, "server_groups", "ServerGroups")
    listener_ids = sorted(collect_values(listeners, ["listener_id", "ListenerId"]))
    server_group_ids = sorted(collect_values(server_groups, ["server_group_id", "ServerGroupId"]) | collect_values(listeners, ["server_group_id", "ServerGroupId"]))

    health = []
    for lid in listener_ids:
        health.append(to_dict(clb.describe_listener_health(volcenginesdkclb.DescribeListenerHealthRequest(listener_id=lid, page_size=100))))
    attrs = []
    for sgid in server_group_ids:
        attrs.append(to_dict(clb.describe_server_group_attributes(volcenginesdkclb.DescribeServerGroupAttributesRequest(server_group_id=sgid))))
    backend_instance_ids = sorted(collect_values(attrs, ["instance_id", "InstanceId"]))

    return {
        "load_balancers": lb_resp,
        "listeners": listeners_resp,
        "listener_health": health,
        "server_groups": server_groups_resp,
        "server_group_attributes": attrs,
        "backend_ecs": describe_ecs(region, backend_instance_ids),
    }


def collect_alb(region: str, load_balancer_id: str, listener_id: str = "") -> Dict[str, Any]:
    alb = volcenginesdkalb.ALBApi(volcenginesdkcore.ApiClient(build_cfg(region)))
    lb_resp = to_dict(
        alb.describe_load_balancers(
            volcenginesdkalb.DescribeLoadBalancersRequest(
                load_balancer_ids=[load_balancer_id],
                page_size=20,
            )
        )
    )
    lbs = list_from(lb_resp, "load_balancers", "LoadBalancers")
    vpc_id = (lbs[0].get("vpc_id") or lbs[0].get("VpcId")) if lbs else None
    listeners_resp = to_dict(
        alb.describe_listeners(
            volcenginesdkalb.DescribeListenersRequest(
                load_balancer_id=load_balancer_id,
                listener_ids=[listener_id] if listener_id else None,
                page_size=100,
            )
        )
    )
    server_groups_resp = to_dict(
        alb.describe_server_groups(
            volcenginesdkalb.DescribeServerGroupsRequest(
                vpc_id=vpc_id,
                page_size=100,
            )
        )
    )
    listeners = list_from(listeners_resp, "listeners", "Listeners")
    server_groups = list_from(server_groups_resp, "server_groups", "ServerGroups")
    listener_ids = sorted(collect_values(listeners, ["listener_id", "ListenerId"]))
    server_group_ids = sorted(collect_values(server_groups, ["server_group_id", "ServerGroupId"]) | collect_values(listeners, ["server_group_id", "ServerGroupId"]))

    health = []
    for lid in listener_ids:
        health.append(to_dict(alb.describe_listener_health(volcenginesdkalb.DescribeListenerHealthRequest(listener_ids=[lid], only_un_healthy=False))))
    attrs = []
    for sgid in server_group_ids:
        attrs.append(to_dict(alb.describe_server_group_attributes(volcenginesdkalb.DescribeServerGroupAttributesRequest(server_group_id=sgid))))
    backend_instance_ids = sorted(collect_values(attrs, ["instance_id", "InstanceId"]))

    return {
        "load_balancers": lb_resp,
        "listeners": listeners_resp,
        "listener_health": health,
        "server_groups": server_groups_resp,
        "server_group_attributes": attrs,
        "backend_ecs": describe_ecs(region, backend_instance_ids),
    }


def collect(region: str, lb_type: str, load_balancer_id: str, listener_id: str = "") -> Dict[str, Any]:
    raw = collect_alb(region, load_balancer_id, listener_id) if lb_type == "alb" else collect_clb(region, load_balancer_id, listener_id)
    listeners = list_from(raw["listeners"], "listeners", "Listeners")
    listener_health = raw["listener_health"]
    server_group_ids = sorted(collect_values(raw["server_group_attributes"], ["server_group_id", "ServerGroupId"]))
    backend_instance_ids = sorted(collect_values(raw["server_group_attributes"], ["instance_id", "InstanceId"]))

    findings = []
    if not listeners:
        findings.append("No listeners found for this load balancer; verify the load balancer ID and type.")
    if has_positive_counter(listener_health, ["un_healthy_count", "UnHealthyCount", "unhealthy_count", "UnhealthyCount"]):
        findings.append("Listener health response contains unhealthy counters; inspect raw.listener_health.")
    if not server_group_ids:
        findings.append("No server group IDs discovered from listeners/server groups.")
    if not backend_instance_ids:
        findings.append("No backend ECS instance IDs discovered from server group attributes.")

    return {
        "region": region,
        "load_balancer_type": lb_type,
        "load_balancer_id": load_balancer_id,
        "listener_id": listener_id,
        "summary": {
            "listener_count": len(listeners),
            "server_group_ids": server_group_ids,
            "backend_instance_ids": backend_instance_ids,
        },
        "raw": raw,
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect CLB/ALB read-only backend context.")
    parser.add_argument("--region", default=os.environ.get("VOLCENGINE_REGION", "cn-beijing"))
    parser.add_argument("--type", choices=["clb", "alb"], required=True)
    parser.add_argument("--load-balancer-id", required=True)
    parser.add_argument("--listener-id", default="")
    args = parser.parse_args()

    try:
        print(json.dumps(collect(args.region, args.type, args.load_balancer_id, args.listener_id), ensure_ascii=False, indent=2))
        return 0
    except ApiException as exc:
        print(json.dumps({"error": "api_exception", "status": exc.status, "reason": exc.reason}, ensure_ascii=False), file=sys.stderr)
        return 2
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
