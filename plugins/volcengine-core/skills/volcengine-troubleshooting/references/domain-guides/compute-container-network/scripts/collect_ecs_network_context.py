#!/usr/bin/env python3
"""Collect read-only ECS and VPC context for connectivity troubleshooting.

Credentials are read only from environment variables:
VOLCENGINE_ACCESS_KEY / VOLCENGINE_SECRET_KEY / VOLCENGINE_REGION.
The script never writes credentials or changes cloud resources.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List

import volcenginesdkcore
import volcenginesdkecs
import volcenginesdkvpc
from volcenginesdkcore.rest import ApiException


def to_dict(value: Any) -> Any:
    if hasattr(value, "to_dict"):
        return value.to_dict()
    return value


def first(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return items[0] if items else {}


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"missing required environment variable: {name}")
    return value


def build_clients(region: str):
    cfg = volcenginesdkcore.Configuration()
    cfg.ak = require_env("VOLCENGINE_ACCESS_KEY")
    cfg.sk = require_env("VOLCENGINE_SECRET_KEY")
    cfg.region = region
    cfg.client_side_validation = True
    return (
        volcenginesdkecs.ECSApi(volcenginesdkcore.ApiClient(cfg)),
        volcenginesdkvpc.VPCApi(volcenginesdkcore.ApiClient(cfg)),
    )


def collect(region: str, instance_id: str) -> Dict[str, Any]:
    ecs, vpc = build_clients(region)

    result: Dict[str, Any] = {
        "region": region,
        "instance_id": instance_id,
        "summary": {},
        "raw": {},
        "findings": [],
    }

    instance_resp = to_dict(
        ecs.describe_instances(
            volcenginesdkecs.DescribeInstancesRequest(
                instance_ids=[instance_id],
                max_results=10,
            )
        )
    )
    result["raw"]["describe_instances"] = instance_resp
    instances = instance_resp.get("instances") or instance_resp.get("result", {}).get("instances", [])
    instance = first(instances)
    if not instance:
        result["findings"].append("ECS instance not found in this region.")
        return result

    result["summary"]["instance"] = {
        "status": instance.get("status"),
        "name": instance.get("instance_name"),
        "zone_id": instance.get("zone_id"),
        "vpc_id": instance.get("vpc_id"),
        "private_ip": None,
        "security_group_ids": [],
        "subnet_ids": [],
    }

    network_interfaces = instance.get("network_interfaces") or []
    subnet_ids = set()
    security_group_ids = set()
    for eni in network_interfaces:
        if eni.get("subnet_id"):
            subnet_ids.add(eni["subnet_id"])
        for sg_id in eni.get("security_group_ids") or []:
            security_group_ids.add(sg_id)
        if not result["summary"]["instance"]["private_ip"]:
            result["summary"]["instance"]["private_ip"] = eni.get("primary_ip_address")

    result["summary"]["instance"]["security_group_ids"] = sorted(security_group_ids)
    result["summary"]["instance"]["subnet_ids"] = sorted(subnet_ids)

    result["raw"]["describe_network_interfaces"] = to_dict(
        vpc.describe_network_interfaces(
            volcenginesdkvpc.DescribeNetworkInterfacesRequest(
                instance_id=instance_id,
                page_size=50,
            )
        )
    )

    security_groups = []
    for sg_id in sorted(security_group_ids):
        sg_resp = to_dict(
            vpc.describe_security_group_attributes(
                volcenginesdkvpc.DescribeSecurityGroupAttributesRequest(
                    security_group_id=sg_id,
                )
            )
        )
        security_groups.append(sg_resp.get("result", sg_resp))
    result["raw"]["security_groups"] = security_groups

    subnets = []
    route_table_ids = set()
    for subnet_id in sorted(subnet_ids):
        subnet_resp = to_dict(
            vpc.describe_subnets(
                volcenginesdkvpc.DescribeSubnetsRequest(
                    subnet_ids=[subnet_id],
                    page_size=20,
                )
            )
        )
        result_subnets = subnet_resp.get("subnets") or subnet_resp.get("result", {}).get("subnets", [])
        subnets.extend(result_subnets)
        for subnet in result_subnets:
            route_table = subnet.get("route_table") or {}
            if route_table.get("route_table_id"):
                route_table_ids.add(route_table["route_table_id"])
    result["raw"]["subnets"] = subnets

    route_tables = []
    for route_table_id in sorted(route_table_ids):
        route_tables.append(
            {
                "route_table_id": route_table_id,
                "route_table": (
                    to_dict(
                        vpc.describe_route_table_list(
                            volcenginesdkvpc.DescribeRouteTableListRequest(
                                route_table_id=route_table_id,
                                page_size=20,
                            )
                        )
                    )
                ),
                "route_entries": (
                    to_dict(
                        vpc.describe_route_entry_list(
                            volcenginesdkvpc.DescribeRouteEntryListRequest(
                                route_table_id=route_table_id,
                                page_size=100,
                            )
                        )
                    )
                ),
            }
        )
    result["raw"]["route_tables"] = route_tables

    if instance.get("status") != "RUNNING":
        result["findings"].append("Instance is not RUNNING; check lifecycle state before network path.")
    if not security_group_ids:
        result["findings"].append("No security group was found on the ECS network interface.")
    if not route_table_ids:
        result["findings"].append("No route table was discovered from subnet metadata.")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect ECS/VPC read-only context.")
    parser.add_argument("--region", default=os.environ.get("VOLCENGINE_REGION", "cn-beijing"))
    parser.add_argument("--instance-id", required=True)
    args = parser.parse_args()

    try:
        print(json.dumps(collect(args.region, args.instance_id), ensure_ascii=False, indent=2))
        return 0
    except ApiException as exc:
        print(json.dumps({"error": "api_exception", "status": exc.status, "reason": exc.reason}, ensure_ascii=False), file=sys.stderr)
        return 2
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
