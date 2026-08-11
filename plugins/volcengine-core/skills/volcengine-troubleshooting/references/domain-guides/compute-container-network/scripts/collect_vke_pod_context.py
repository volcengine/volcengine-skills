#!/usr/bin/env python3
"""Collect read-only VKE control-plane context.

Cloud credentials are read only from environment variables:
VOLCENGINE_ACCESS_KEY / VOLCENGINE_SECRET_KEY / VOLCENGINE_REGION.

This script does not read local cluster config or execute cluster-side tools.
It only queries VolcEngine VKE OpenAPI through the supported Python SDK.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional

import volcenginesdkcore
import volcenginesdkvke
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


def build_client(region: str):
    cfg = volcenginesdkcore.Configuration()
    cfg.ak = require_env("VOLCENGINE_ACCESS_KEY")
    cfg.sk = require_env("VOLCENGINE_SECRET_KEY")
    cfg.region = region
    cfg.client_side_validation = True
    return volcenginesdkvke.VKEApi(volcenginesdkcore.ApiClient(cfg))


def list_items(resp: Dict[str, Any]) -> List[Dict[str, Any]]:
    return resp.get("items") or resp.get("Items") or resp.get("result", {}).get("items", []) or []


def phase_of(obj: Dict[str, Any]) -> str:
    status = obj.get("status") or obj.get("Status") or {}
    if isinstance(status, dict):
        return str(status.get("phase") or status.get("Phase") or status.get("conditions") or status.get("Conditions") or "")
    return str(status)


def collect(region: str, cluster_id: str, namespace: Optional[str], pod: Optional[str], node: Optional[str]) -> Dict[str, Any]:
    api = build_client(region)
    result: Dict[str, Any] = {
        "region": region,
        "cluster_id": cluster_id,
        "target": {"namespace": namespace, "pod": pod, "node": node},
        "summary": {},
        "raw": {},
        "findings": [],
    }

    cluster_filter = volcenginesdkvke.FilterForListClustersInput(ids=[cluster_id])
    node_pool_filter = volcenginesdkvke.FilterForListNodePoolsInput(cluster_ids=[cluster_id])
    node_filter = volcenginesdkvke.FilterForListNodesInput(cluster_ids=[cluster_id])
    addon_filter = volcenginesdkvke.FilterForListAddonsInput(cluster_ids=[cluster_id])

    # Keep page_size within the conservative cross-action limit accepted by VKE list APIs.
    clusters_resp = to_dict(api.list_clusters(volcenginesdkvke.ListClustersRequest(filter=cluster_filter, page_size=50)))
    node_pools_resp = to_dict(api.list_node_pools(volcenginesdkvke.ListNodePoolsRequest(filter=node_pool_filter, page_size=50)))
    nodes_resp = to_dict(api.list_nodes(volcenginesdkvke.ListNodesRequest(filter=node_filter, page_size=50)))
    addons_resp = to_dict(api.list_addons(volcenginesdkvke.ListAddonsRequest(filter=addon_filter, page_size=50)))

    clusters = list_items(clusters_resp)
    node_pools = list_items(node_pools_resp)
    nodes = list_items(nodes_resp)
    addons = list_items(addons_resp)

    result["raw"]["clusters"] = clusters_resp
    result["raw"]["node_pools"] = node_pools_resp
    result["raw"]["nodes"] = nodes_resp
    result["raw"]["addons"] = addons_resp

    cluster = clusters[0] if clusters else {}
    result["summary"] = {
        "cluster": {
            "id": cluster.get("id") or cluster.get("Id"),
            "name": cluster.get("name") or cluster.get("Name"),
            "phase": phase_of(cluster),
            "kubernetes_version": cluster.get("kubernetes_version") or cluster.get("KubernetesVersion"),
            "pod_network_mode": ((cluster.get("pods_config") or {}).get("pod_network_mode") if isinstance(cluster.get("pods_config"), dict) else None),
            "vpc_id": ((cluster.get("cluster_config") or {}).get("vpc_id") if isinstance(cluster.get("cluster_config"), dict) else None),
        },
        "counts": {
            "clusters": len(clusters),
            "node_pools": len(node_pools),
            "nodes": len(nodes),
            "addons": len(addons),
        },
    }

    if not clusters:
        result["findings"].append("Cluster not found in this region.")
    elif phase_of(cluster).lower() not in ("running", "ok", "['ok']", "[{'type': 'ok'}]"):
        result["findings"].append(f"Cluster phase is not clearly healthy: {phase_of(cluster)}")

    unhealthy_nodes = [n for n in nodes if "running" not in phase_of(n).lower() and "ready" not in phase_of(n).lower()]
    unhealthy_addons = [a for a in addons if "running" not in phase_of(a).lower() and "ok" not in phase_of(a).lower()]
    if unhealthy_nodes:
        result["findings"].append(f"{len(unhealthy_nodes)} VKE nodes are not clearly healthy; inspect raw.nodes.")
    if unhealthy_addons:
        result["findings"].append(f"{len(unhealthy_addons)} addons are not clearly healthy; inspect raw.addons.")

    if namespace or pod or node:
        result["findings"].append(
            "Namespace, pod, and node are recorded as user context only; this script only collects VolcEngine control-plane data. "
            "Use VKE control-plane evidence here and request application-side logs from the user when needed."
        )

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect VKE read-only control-plane context.")
    parser.add_argument("--region", default=os.environ.get("VOLCENGINE_REGION", "cn-beijing"))
    parser.add_argument("--cluster-id", required=True)
    parser.add_argument("--namespace")
    parser.add_argument("--pod")
    parser.add_argument("--node")
    args = parser.parse_args()

    try:
        print(json.dumps(collect(args.region, args.cluster_id, args.namespace, args.pod, args.node), ensure_ascii=False, indent=2))
        return 0
    except ApiException as exc:
        print(json.dumps({"error": "api_exception", "status": exc.status, "reason": exc.reason}, ensure_ascii=False), file=sys.stderr)
        return 2
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
