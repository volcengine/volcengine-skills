#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: MIT
"""火山引擎官方文档检索 / 全文获取工具（纯 Python 标准库实现）。

接口为公开文档服务，无需 AK/SK 鉴权。输出经过 parse + 裁剪 + 分页处理，
避免把上游「整篇正文 × N、单行几十~上百 KB」的原始 JSON 直接透传
（那会撑爆调用方上下文 / 触发会话中断）。与 AWS 文档 MCP server 同思路：
在本层解析、裁剪、清洗成 markdown 文本，不透传上游。

依赖：仅 Python3 标准库（urllib / json / html.parser），无需 curl / jq。
代理：urllib 默认读取环境变量 http_proxy / https_proxy。

用法:
  python3 volcengine_docs.py search "<查询关键词>" [返回数量] [产品编码1,产品编码2...]
  python3 volcengine_docs.py fetch  "<火山引擎文档链接>" [start_index] [max_length]
"""
import json
import os
import re
import sys
import textwrap
import urllib.request
import urllib.error
from html.parser import HTMLParser

API_BASE = "https://docs-api.cn-beijing.volces.com/api/v1/doc"
REQUEST_TIMEOUT = 15  # 秒

# 可调参数（环境变量覆盖）
SEARCH_SNIPPET_CHARS = int(os.environ.get("VOLC_SEARCH_SNIPPET", "600"))  # search 每条摘要字符数
FETCH_MAX_DEFAULT = int(os.environ.get("VOLC_FETCH_MAX", "5000"))          # fetch 单页字符数
FOLD_WIDTH = int(os.environ.get("VOLC_FOLD_WIDTH", "0"))                   # >0 时按字符折行；0=关闭
# stdout 预览上限（按 UTF-8 字节，因为 harness 按字节/体量判定；中文 3 字节/字）。
# 超过则把完整结果写入临时文件，stdout 只回预览 + 文件路径，
# 避免长输出触发 Claude Code 把 Bash 输出截断/落盘而打断任务。
PREVIEW_BYTES = int(os.environ.get("VOLC_PREVIEW_BYTES", "4000"))


def http_post(path, payload):
    """向文档服务发起 POST。返回 (data_dict_or_None, error_str_or_None)。"""
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        f"{API_BASE}/{path}",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except urllib.error.URLError as e:
        return None, f"请求失败: {e}"
    except Exception as e:  # noqa: BLE001
        return None, f"请求异常: {e}"
    if not raw:
        return None, "响应为空"
    try:
        return json.loads(raw), None
    except json.JSONDecodeError:
        return None, f"响应非 JSON: {raw[:200]}"


class _Stripper(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.buf = []

    def handle_data(self, d):
        self.buf.append(d)


def clean_html(text):
    """清掉 HTML 标签 + 反转义实体 + 折叠多余空行（正则去标签会留残渣，故用 html.parser）。"""
    if not text:
        return ""
    p = _Stripper()
    p.feed(text)
    t = "".join(p.buf)
    t = re.sub(r"\n[ \t]*\n[ \t]*(?:\n[ \t]*)+", "\n\n", t)  # 3+ 空行折成 1 个空行
    return t.strip()


def fold_text(text):
    """长行折行兜底（FOLD_WIDTH>0 时生效）。按字符折，CJK 安全。"""
    if FOLD_WIDTH <= 0:
        return text
    out = []
    for line in text.split("\n"):
        if len(line) <= FOLD_WIDTH:
            out.append(line)
        else:
            out.extend(
                textwrap.wrap(
                    line, width=FOLD_WIDTH, break_long_words=True, break_on_hyphens=False
                )
                or [""]
            )
    return "\n".join(out)


def emit(text):
    """短输出直接打印；长输出写临时文件，stdout 只回预览 + 路径（避免长 stdout 打断任务）。
    阈值按 UTF-8 字节判定。"""
    data = text.encode("utf-8")
    if len(data) <= PREVIEW_BYTES:
        print(text)
        return
    import tempfile
    d = os.path.join(tempfile.gettempdir(), "volcengine_docs")
    os.makedirs(d, exist_ok=True)
    fd, path = tempfile.mkstemp(prefix="vdoc_", suffix=".md", dir=d)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)
    preview = data[:PREVIEW_BYTES].decode("utf-8", "ignore")
    print(preview)
    print(
        f"\n\n…（完整 {len(data)} 字节已保存到：{path}\n"
        f"用 Read 工具读取该文件查看全文；文件较大时用 Read 的 offset/limit 分段读，"
        f"不要直接 cat 整个文件。）"
    )


def cmd_search(query, limit=10, codes=""):
    payload = {"Query": query, "Limit": int(limit)}
    code_list = [c.strip() for c in codes.split(",") if c.strip()] if codes else []
    if code_list:
        payload["ServiceCodes"] = code_list

    data, err = http_post("search", payload)
    if err:
        return json.dumps({"error": err}, ensure_ascii=False), 1

    doc_list = (((data or {}).get("Result") or {}).get("DocList")) or []
    if not doc_list:
        # 后端抖动（DownstreamError）或确实无结果：回显精简信息，便于判断是否重试
        meta = (data or {}).get("ResponseMetadata", {})
        be = meta.get("Error") if isinstance(meta, dict) else None
        note = {"info": "无结果或后端抖动，建议重试或更换 query", "backend_error": be}
        return json.dumps(note, ensure_ascii=False), 0

    blocks = []
    for i, d in enumerate(doc_list):
        title = d.get("Title") or ""
        url = d.get("Url") or ""
        svc = ", ".join(d.get("ServiceCodes") or [])
        # DocList[].Content 是一个 JSON 字符串，内层才有 markdown 正文
        inner_md = ""
        raw_c = d.get("Content")
        if isinstance(raw_c, str):
            try:
                inner = json.loads(raw_c)
                title = title or inner.get("Title", "")
                inner_md = inner.get("Content", "")
            except json.JSONDecodeError:
                inner_md = raw_c
        snippet = clean_html(inner_md)[:SEARCH_SNIPPET_CHARS]
        blocks.append(
            f"## {i + 1}. {title or '无标题'}\n{url}\nServiceCodes: {svc}\n\n{snippet}\n"
        )
    return fold_text("\n---\n".join(blocks)), 0


def cmd_fetch(url, start_index=0, max_length=FETCH_MAX_DEFAULT):
    clean_url = url.split("#", 1)[0].split("?", 1)[0]
    start_index = max(0, int(start_index))
    max_length = int(max_length) if int(max_length) > 0 else FETCH_MAX_DEFAULT

    data, err = http_post("fetch", {"Url": clean_url})
    if err:
        return json.dumps({"error": err, "CleanUrl": clean_url}, ensure_ascii=False), 1

    result = ((data or {}).get("Result")) or {}
    title = result.get("Title") or ""
    content = result.get("Content") or ""
    if not content:
        # 一级导航页 / 空响应：没有正文可取
        note = {
            "info": "该链接无正文（可能是产品文档导航首页，而非具体文章；或后端抖动）",
            "CleanUrl": clean_url,
        }
        return json.dumps(note, ensure_ascii=False), 0

    full = clean_html(content)
    total = len(full)
    page = full[start_index : start_index + max_length]
    header = f"# {title}\n{clean_url}\n\n" if title else f"{clean_url}\n\n"
    body = header + page
    remaining = total - (start_index + len(page))
    if remaining > 0:
        nxt = start_index + len(page)
        body += f"\n\n【续读】还有 {remaining} 字。重新调用 fetch 并加参数 start_index={nxt} 继续读。"
    return fold_text(body), 0


HELP = """\
volcengine-docs 火山引擎文档查询工具（纯 Python）
用法:
  search <查询关键词> [返回数量] [产品编码1,产品编码2...]
      检索文档，每条命中只回 Title / Url / ServiceCodes / 正文摘要(默认前 600 字)
      例: python3 volcengine_docs.py search "tos是什么" 3 tos
  fetch <火山引擎文档链接> [start_index] [max_length]
      取单篇全文，清成 markdown 文本，按 max_length/start_index 分页(默认 0/5000)
      例: python3 volcengine_docs.py fetch "https://www.volcengine.com/docs/6349/162514" 0 5000
环境变量: VOLC_SEARCH_SNIPPET(默认600) / VOLC_FETCH_MAX(默认5000) / VOLC_FOLD_WIDTH(默认0关闭)
"""


def main(argv):
    if not argv:
        print(HELP)
        return 1
    action, rest = argv[0], argv[1:]
    if action in ("-h", "--help", "help"):
        print(HELP)
        return 0
    if action == "search":
        if not rest:
            print(json.dumps({"error": "缺少查询关键词"}, ensure_ascii=False))
            return 1
        query = rest[0]
        limit = rest[1] if len(rest) > 1 else 10
        codes = rest[2] if len(rest) > 2 else ""
        try:
            int(limit)
        except (TypeError, ValueError):
            print(json.dumps({"error": "返回数量必须是数字"}, ensure_ascii=False))
            return 1
        out, rc = cmd_search(query, limit, codes)
        emit(out) if rc == 0 else print(out)
        return rc
    if action == "fetch":
        if not rest:
            print(json.dumps({"error": "缺少文档URL"}, ensure_ascii=False))
            return 1
        url = rest[0]
        start = rest[1] if len(rest) > 1 else 0
        mx = rest[2] if len(rest) > 2 else FETCH_MAX_DEFAULT
        out, rc = cmd_fetch(url, start, mx)
        emit(out) if rc == 0 else print(out)
        return rc
    print(json.dumps({"error": f"未知操作 {action}", "help": "支持: search, fetch"}, ensure_ascii=False))
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
