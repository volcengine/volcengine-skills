#!/usr/bin/env python3
"""Collect read-only billing context for Volcengine troubleshooting.

SDK source: volcengine-python-sdk / volcenginesdkbilling.
Credentials are read only from environment variables:
VOLCENGINE_ACCESS_KEY / VOLCENGINE_SECRET_KEY / VOLCENGINE_SESSION_TOKEN.

The script only calls read actions:
QueryBalanceAcct, ListOrders, ListBill, ListBillDetail,
ListBillOverviewByProd, ListResourcePackages.
It never pays, purchases, renews, unsubscribes, or changes billing settings.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Callable, Dict, List, Optional

import volcenginesdkbilling as billing
import volcenginesdkcore
from volcenginesdkbilling.api.billing_api import BILLINGApi
from volcenginesdkcore.rest import ApiException


SCRIPT_VERSION = "0.1.1"


def to_dict(value: Any) -> Any:
    if hasattr(value, "to_dict"):
        return value.to_dict()
    return value


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"missing required environment variable: {name}")
    return value


def build_client(region: str) -> BILLINGApi:
    cfg = volcenginesdkcore.Configuration()
    cfg.ak = require_env("VOLCENGINE_ACCESS_KEY")
    cfg.sk = require_env("VOLCENGINE_SECRET_KEY")
    cfg.region = region
    token = os.environ.get("VOLCENGINE_SESSION_TOKEN")
    if token:
        cfg.session_token = token
    cfg.client_side_validation = True
    return BILLINGApi(volcenginesdkcore.ApiClient(cfg))


def compact_error(exc: Exception) -> Dict[str, Any]:
    if isinstance(exc, ApiException):
        return {
            "error": "api_exception",
            "status": exc.status,
            "reason": str(exc.reason)[:500],
        }
    return {"error": type(exc).__name__, "reason": str(exc)[:500]}


def raw_summary(data: Any) -> Dict[str, Any]:
    if isinstance(data, dict):
        items = first_list(data)
        return {
            "omitted": True,
            "type": "dict",
            "top_level_keys": sorted(data.keys())[:20],
            "list_count_in_page": len(items),
        }
    return {"omitted": True, "type": type(data).__name__}


def try_call(result: Dict[str, Any], key: str, fn: Callable[[], Any], include_raw: bool) -> Optional[Any]:
    try:
        data = to_dict(fn())
        result["raw"][key] = data if include_raw else raw_summary(data)
        return data
    except Exception as exc:  # Keep going so one failed bill query does not hide balance/order evidence.
        result["raw"][key] = compact_error(exc)
        result["findings"].append(f"{key} query failed: {result['raw'][key].get('reason')}")
        return None


def first_list(data: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not isinstance(data, dict):
        return []
    items = data.get("list") or data.get("order_infos") or data.get("result", {}).get("list") or []
    return items if isinstance(items, list) else []


def next_token(data: Optional[Dict[str, Any]]) -> Optional[str]:
    if not isinstance(data, dict):
        return None
    token = data.get("next_token") or data.get("NextToken") or data.get("result", {}).get("next_token")
    return str(token) if token else None


def total_count(data: Optional[Dict[str, Any]]) -> Optional[int]:
    if not isinstance(data, dict):
        return None
    for key in ("total", "total_count", "record_num", "total_record_num", "Total", "TotalCount"):
        value = data.get(key)
        if isinstance(value, int):
            return value
        if isinstance(value, str) and value.isdigit():
            return int(value)
    nested = data.get("result")
    if isinstance(nested, dict):
        return total_count(nested)
    return None


def collect_offset_pages(
    result: Dict[str, Any],
    key: str,
    page_size: int,
    max_pages: int,
    include_raw: bool,
    fn: Callable[[int], Any],
) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    pages = 0
    totals: List[int] = []
    last_error = None
    for page in range(max_pages):
        offset = page * page_size
        data = try_call(result, f"{key}_page_{page + 1}", lambda offset=offset: fn(offset), include_raw)
        if not isinstance(data, dict):
            last_error = result["raw"].get(f"{key}_page_{page + 1}")
            break
        page_rows = first_list(data)
        rows.extend(page_rows)
        pages += 1
        total = total_count(data)
        if total is not None:
            totals.append(total)
        if len(page_rows) < page_size:
            break
    expected_total = totals[-1] if totals else None
    return {
        "rows": rows,
        "pages_fetched": pages,
        "page_size": page_size,
        "max_pages": max_pages,
        "expected_total": expected_total,
        "is_complete": expected_total is not None and len(rows) >= expected_total or pages < max_pages,
        "last_error": last_error,
    }


def collect_token_pages(
    result: Dict[str, Any],
    key: str,
    page_size: int,
    max_pages: int,
    include_raw: bool,
    fn: Callable[[Optional[str]], Any],
) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    pages = 0
    token: Optional[str] = None
    last_error = None
    for page in range(max_pages):
        data = try_call(result, f"{key}_page_{page + 1}", lambda token=token: fn(token), include_raw)
        if not isinstance(data, dict):
            last_error = result["raw"].get(f"{key}_page_{page + 1}")
            break
        rows.extend(first_list(data))
        pages += 1
        token = next_token(data)
        if not token:
            break
    return {
        "rows": rows,
        "pages_fetched": pages,
        "page_size": page_size,
        "max_pages": max_pages,
        "next_token": token,
        "is_complete": not bool(token),
        "last_error": last_error,
    }


def summarize_money_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    compact = []
    for row in rows[:10]:
        compact.append(
            {
                "product": row.get("product") or row.get("Product"),
                "product_zh": row.get("product_zh") or row.get("ProductZh"),
                "instance_no": row.get("instance_no") or row.get("InstanceNo"),
                "bill_period": row.get("bill_period") or row.get("BillPeriod"),
                "payable_amount": row.get("payable_amount") or row.get("PayableAmount"),
                "original_bill_amount": row.get("original_bill_amount") or row.get("OriginalBillAmount"),
                "coupon_amount": row.get("coupon_amount") or row.get("CouponAmount"),
                "pay_status": row.get("pay_status") or row.get("PayStatus"),
            }
        )
    return compact


def build_headline(result: Dict[str, Any]) -> Dict[str, Any]:
    summary = result.get("summary", {})
    balance = summary.get("balance", {})
    return {
        "balance": {
            "available_balance": balance.get("available_balance"),
            "arrears_balance": balance.get("arrears_balance"),
            "credit_limit": balance.get("credit_limit"),
        },
        "bill_overview": {
            "items_returned": len(summary.get("bill_overview_by_prod", [])),
            "pagination": summary.get("bill_overview_pagination"),
        },
        "bill_detail": {
            "items_returned": len(summary.get("bill_detail", [])),
            "pagination": summary.get("bill_detail_pagination"),
        },
        "resource_packages": {
            "items_returned": len(summary.get("resource_packages", [])),
            "pagination": summary.get("resource_packages_pagination"),
        },
    }


def collect(
    region: str,
    bill_period: Optional[str],
    max_results: int,
    all_pages: bool,
    max_pages: int,
    include_bill_detail: bool,
    include_packages: bool,
    include_orders: bool,
    include_raw: bool,
) -> Dict[str, Any]:
    requested_max_results = max_results
    if max_results < 1:
        max_results = 1
    if max_results > 100:
        max_results = 100
    if requested_max_results > max_results and not all_pages:
        all_pages = True
    if bill_period and include_bill_detail and max_results >= 100 and not all_pages:
        all_pages = True

    api = build_client(region)
    result: Dict[str, Any] = {
        "script_version": SCRIPT_VERSION,
        "region": region,
        "bill_period": bill_period,
        "pagination": {
            "all_pages": all_pages,
            "page_size": max_results,
            "requested_page_size": requested_max_results,
            "max_pages": max_pages,
        },
        "findings": [],
        "headline": {},
        "summary": {},
        "raw": {},
    }
    if requested_max_results != max_results:
        result["findings"].append(
            f"max_results was clamped from {requested_max_results} to {max_results}; billing list APIs are safest at 100 or fewer per page."
        )
    if requested_max_results > max_results:
        result["findings"].append("all_pages was enabled automatically because requested_max_results exceeded the safe page size.")
    if bill_period and include_bill_detail and max_results >= 100 and all_pages:
        result["findings"].append("all_pages is enabled for bill detail because page_size is 100 and bill_period/include_bill_detail were provided.")

    balance = try_call(
        result,
        "query_balance_acct",
        lambda: api.query_balance_acct(billing.QueryBalanceAcctRequest()),
        include_raw,
    )
    if isinstance(balance, dict):
        result["summary"]["balance"] = {
            "account_id": balance.get("account_id"),
            "available_balance": balance.get("available_balance"),
            "cash_balance": balance.get("cash_balance"),
            "arrears_balance": balance.get("arrears_balance"),
            "freeze_amount": balance.get("freeze_amount"),
            "credit_limit": balance.get("credit_limit"),
        }
        if str(balance.get("arrears_balance", "0")) not in ("0", "0.0", "0.00", ""):
            result["findings"].append("Account has arrears balance; billing state may block service use.")
        if str(balance.get("available_balance", "0")) in ("0", "0.0", "0.00", ""):
            result["findings"].append("Available balance is zero; precharge or purchase may fail.")

    if include_orders:
        if all_pages:
            orders_page = collect_token_pages(
                result,
                "list_orders",
                max_results,
                max_pages,
                include_raw,
                lambda token: api.list_orders(
                    billing.ListOrdersRequest(max_results=max_results, next_token=token)
                ),
            )
            order_rows = orders_page["rows"]
            result["summary"]["orders_pagination"] = {
                k: v for k, v in orders_page.items() if k != "rows"
            }
        else:
            orders = try_call(
                result,
                "list_orders",
                lambda: api.list_orders(billing.ListOrdersRequest(max_results=max_results)),
                include_raw,
            )
            order_rows = first_list(orders)
            result["summary"]["orders_pagination"] = {
                "pages_fetched": 1 if isinstance(orders, dict) else 0,
                "page_size": max_results,
                "next_token": next_token(orders),
                "is_complete": not bool(next_token(orders)),
            }
        result["summary"]["orders"] = {
            "count_collected": len(order_rows),
            "sample_status": [row.get("status") for row in order_rows[:5]],
        }

    if bill_period:
        if all_pages:
            overview_page = collect_offset_pages(
                result,
                "list_bill_overview_by_prod",
                max_results,
                max_pages,
                include_raw,
                lambda offset: api.list_bill_overview_by_prod(
                    billing.ListBillOverviewByProdRequest(
                        bill_period=bill_period,
                        limit=max_results,
                        offset=offset,
                        need_record_num=1,
                    )
                ),
            )
            overview_rows = overview_page["rows"]
            result["summary"]["bill_overview_pagination"] = {
                k: v for k, v in overview_page.items() if k != "rows"
            }
        else:
            bill_overview = try_call(
                result,
                "list_bill_overview_by_prod",
                lambda: api.list_bill_overview_by_prod(
                    billing.ListBillOverviewByProdRequest(
                        bill_period=bill_period,
                        limit=max_results,
                        offset=0,
                        need_record_num=1,
                    )
                ),
                include_raw,
            )
            overview_rows = first_list(bill_overview)
            result["summary"]["bill_overview_pagination"] = {
                "pages_fetched": 1 if isinstance(bill_overview, dict) else 0,
                "page_size": max_results,
                "expected_total": total_count(bill_overview),
                "is_complete": len(overview_rows) < max_results,
            }
        result["summary"]["bill_overview_by_prod"] = summarize_money_rows(overview_rows)

        if include_bill_detail:
            if all_pages:
                detail_page = collect_offset_pages(
                    result,
                    "list_bill_detail",
                    max_results,
                    max_pages,
                    include_raw,
                    lambda offset: api.list_bill_detail(
                        billing.ListBillDetailRequest(
                            bill_period=bill_period,
                            limit=max_results,
                            offset=offset,
                            need_record_num=1,
                        )
                    ),
                )
                detail_rows = detail_page["rows"]
                result["summary"]["bill_detail_pagination"] = {
                    k: v for k, v in detail_page.items() if k != "rows"
                }
            else:
                bill_detail = try_call(
                    result,
                    "list_bill_detail",
                    lambda: api.list_bill_detail(
                        billing.ListBillDetailRequest(
                            bill_period=bill_period,
                            limit=max_results,
                            offset=0,
                            need_record_num=1,
                        )
                    ),
                    include_raw,
                )
                detail_rows = first_list(bill_detail)
                result["summary"]["bill_detail_pagination"] = {
                    "pages_fetched": 1 if isinstance(bill_detail, dict) else 0,
                    "page_size": max_results,
                    "expected_total": total_count(bill_detail),
                    "is_complete": len(detail_rows) < max_results,
                }
            result["summary"]["bill_detail"] = summarize_money_rows(detail_rows)

    if include_packages:
        package_page_size = min(max_results, 20)
        if package_page_size != max_results:
            result["findings"].append(
                f"resource package page size was clamped from {max_results} to {package_page_size}; ListResourcePackages is safest at 20 or fewer per page."
            )
        if all_pages:
            package_page = collect_token_pages(
                result,
                "list_resource_packages",
                package_page_size,
                max_pages,
                include_raw,
                lambda token: api.list_resource_packages(
                    billing.ListResourcePackagesRequest(
                        max_results=str(package_page_size),
                        next_token=token,
                        resource_type="Package",
                    )
                ),
            )
            package_rows = package_page["rows"]
            result["summary"]["resource_packages_pagination"] = {
                k: v for k, v in package_page.items() if k != "rows"
            }
        else:
            packages = try_call(
                result,
                "list_resource_packages",
                lambda: api.list_resource_packages(
                    billing.ListResourcePackagesRequest(
                        max_results=str(package_page_size),
                        resource_type="Package",
                    )
                ),
                include_raw,
            )
            package_rows = first_list(packages)
            result["summary"]["resource_packages_pagination"] = {
                "pages_fetched": 1 if isinstance(packages, dict) else 0,
                "page_size": package_page_size,
                "next_token": next_token(packages),
                "is_complete": not bool(next_token(packages)),
            }
        result["summary"]["resource_packages"] = [
            {
                "instance_no": row.get("instance_no"),
                "product": row.get("product"),
                "product_name": row.get("product_name"),
                "region_code": row.get("region_code"),
                "status": row.get("status"),
                "available_amount": row.get("available_amount"),
                "total_amount": row.get("total_amount"),
                "unit": row.get("unit"),
                "effective_time": row.get("effective_time"),
                "expiry_time": row.get("expiry_time"),
            }
            for row in package_rows[:10]
        ]

    result["headline"] = build_headline(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect read-only Volcengine billing context.")
    parser.add_argument("--region", default=os.environ.get("VOLCENGINE_REGION", "cn-beijing"))
    parser.add_argument("--bill-period", help="Billing period in yyyy-MM, for bill overview/detail queries.")
    parser.add_argument("--max-results", type=int, default=5)
    parser.add_argument("--all-pages", action="store_true", help="Fetch multiple pages for supported list queries.")
    parser.add_argument("--max-pages", type=int, default=3, help="Maximum pages to fetch when --all-pages is set.")
    parser.add_argument("--include-bill-detail", action="store_true")
    parser.add_argument("--include-packages", action="store_true")
    parser.add_argument("--include-orders", action="store_true")
    parser.add_argument("--include-raw", action="store_true", help="Include full raw SDK responses. Use only when needed.")
    args = parser.parse_args()

    try:
        data = collect(
            region=args.region,
            bill_period=args.bill_period,
            max_results=args.max_results,
            all_pages=args.all_pages,
            max_pages=args.max_pages,
            include_bill_detail=args.include_bill_detail,
            include_packages=args.include_packages,
            include_orders=args.include_orders,
            include_raw=args.include_raw,
        )
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps(compact_error(exc), ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
