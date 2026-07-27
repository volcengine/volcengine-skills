---
name: volcengine-knowledge-search
description: "火山引擎官方文档检索与全文获取技能：对火山引擎官方文档站（www.volcengine.com/docs）做语义检索并抓取正文。Use when 用户咨询火山引擎产品的概念、用法、计费规则、部署步骤、最佳实践、服务条款/协议等可在官方文档中找到解释的问题，或用户直接给出火山引擎官方文档链接（www.volcengine.com/docs/...）需要取全文时。"
license: MIT
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# volcengine-knowledge-search 火山引擎文档检索技能

火山引擎官方文档综合查询技能，提供 **search（检索）** 与 **fetch（全文获取）** 两个能力。火山引擎文档是火山最权威的官方数据，覆盖全产品使用全链路。接口为公开文档服务，**无需 AK/SK 鉴权**，脚本用 **Python3 标准库**实现（仅依赖 `python3`，无需 curl/jq）。

> 脚本会在本地把上游响应 **解析 + 裁剪 + 清洗成干净 markdown 文本**再输出（search 每条只回摘要、fetch 按页返回），避免把「整篇正文 × N、单行几十~上百 KB」的原始 JSON 灌进上下文。所以**脚本输出可直接阅读/引用，不需要你再解析 JSON**。

## 什么时候用

- 用户咨询火山引擎产品的概念、用法、计费规则、部署步骤、最佳实践、服务条款/协议等可在官方文档中找到解释的问题
- 用户给出一条火山引擎官方文档链接（`https://www.volcengine.com/docs/...`），需要取该文档全文
- 用户消息里出现「火山」「火山引擎」「volcengine」且属于查官方文档 / 读文档全文的场景

## 命令速查

脚本位于 `scripts/volcengine_docs.py`，命令均相对本 skill 目录根执行。

| 子命令 | 用途 | 形式 |
|--------|------|------|
| `search` | 关键词检索文档 | `search "<关键词>" [返回数量] [产品编码1,产品编码2...]` |
| `fetch` | 取单篇文档全文(分页) | `fetch "<火山引擎文档链接>" [start_index] [max_length]` |

### search

```bash
python3 scripts/volcengine_docs.py search "tos 怎么计费" 3
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| 查询关键词 | 是 | 完整的自然语言问题/描述,贴近文档正式表述;**不是**关键词堆砌或英文缩写(见下方「如何写好 query」) |
| 返回数量 | 否 | 检索返回文档数，默认 10 |
| 产品编码 | 否 | 逗号分隔，限定仅查某几个产品；编码取自上一次返回的 `ServiceCodes` |

**输出**：已整理好的 markdown 文本，每条命中一段：

```text
## 1. <标题>
<纯净URL>
ServiceCodes: <产品编码,逗号分隔>

<正文摘要，默认前 600 字，已清掉 HTML 标签>
---
```

直接阅读/引用即可，无需再解析 JSON。摘要字数可用环境变量 `VOLC_SEARCH_SNIPPET` 调整。`ServiceCodes` 行用于二次精搜（见示例 4）。

#### 如何写好 query —— 这是「向量语义检索」,不是关键词精确匹配

本接口底层是**向量库语义检索（embedding 召回）**,而非倒排索引的关键词精确匹配。query 写得好不好,直接决定召回质量。把握一个核心:**让 query 在语义上尽量贴近目标文档里的正式表述**。

写 query 的要点:

- **用完整的自然语言描述,而非孤立短词。** 例如查产品订阅价格,写「火山方舟 Coding Plan AI 编程订阅套餐 价格 计费」,而不是只写「Coding Plan」。短词/单个英文缩写语义太稀疏,极易召回跑偏(实测只搜「Coding Plan」会召回 DataFinder、RTC 等完全无关文档)。
- **补全产品全称与上下文。** 用户常用简称、营销名、口语词(如「方舟」「豆包编程」「code plan」);先在 query 里补上官方全称 + 所属产品 + 具体方向(如「火山方舟大模型服务 模型推理 计费规则」),让向量更聚焦。
- **优先用「问题 / 描述」句式,而非命令式。** 向量更亲近文档正文的陈述语气,「TOS 跨区域复制如何配置」优于「配 TOS 复制」。
- **首搜跑偏就换语义等价的说法重写,而不是重试同一句。** 同一概念可能有多种表述,换近义描述(中英、全称/简称、功能动词)往往能召回到正确文档。
- **专有新名词(新产品、新功能、营销活动名)召回差时**,把它「翻译」成它实际属于的产品 + 能力描述再搜,定位到正确产品后,可用返回的 `ServiceCodes` 带产品编码二次精搜(见示例 4)。

**真实对比(实测)**:用户问「火山引擎 Coding Plan 什么价格、如何接入」。

```bash
# 坏 query:直接用短英文营销词,语义稀疏 → 召回空 / 命中 DataFinder、RTC 等完全无关产品
python3 scripts/volcengine_docs.py search "Coding Plan" 5

# 好 query:补全产品全称(火山方舟)+ 能力(AI 编程订阅套餐)+ 方向(价格 计费)
python3 scripts/volcengine_docs.py search "火山方舟 Coding Plan AI 编程订阅套餐 价格 计费规则" 5
# → 5 条结果全部命中 ark 产品:套餐概览 / 接入三方工具 / 限时邀请活动 / 常见问题 / 模型价格
```

同一需求,只因 query 表述不同,召回质量天差地别。**遇到简称、英文缩写、营销名,先补成「产品全称 + 能力描述 + 具体方向」再搜。**

### fetch

```bash
python3 scripts/volcengine_docs.py fetch "https://www.volcengine.com/docs/6349/162514?lang=zh"
```

脚本会自动剥离 URL 的 query / fragment 参数（如 `?lang=zh`），只用纯净路径请求。**输出是整理好的 markdown 文本**：首行 `# 标题`、次行纯净链接、空行后是正文。

**分页**：正文按 `max_length`（默认 5000 字符）截断，未读完时结尾追加一行 `【续读】还有 N 字。…加参数 start_index=M 继续读。`。要续读就用同一 URL 再调一次并带上提示里的 `start_index`。单页字数可用 `VOLC_FETCH_MAX` 调整。

**先看链接结构再决定能不能 fetch**：

- `https://www.volcengine.com/docs/{产品编号}/{文档ID}`（**两级**，如 `docs/6349/162514`）才是**具体文章**，`fetch` 能取到正文。
- `https://www.volcengine.com/docs/{产品编号}`（**只有一级编号**，如 `docs/6459`）是某个产品的**文档中心首页 / 栏目导航页**，不是文章。对它 `fetch` 会返回一段提示 JSON（`{"info": "该链接无正文…", "CleanUrl": …}`，退出码 0），表示没有正文可取。遇到这种链接不要反复重试 fetch，按下面的兜底处理。

**一级导航页链接的兜底策略**：

1. 用 `search` 检索该产品名 / 用户真正关心的具体方向，从结果里定位到两级的具体文章链接，再对其 `fetch`。
2. 向用户说明：该链接是产品文档导航首页而非具体文章，并主动询问想深入了解哪个具体方向，再帮其定位。

## 决策逻辑

1. **用户直接给了文档链接** → 直接走 `fetch`，无需先检索。
2. **用户提问类需求** → 先把用户原话**改写成贴近文档表述的自然语言 query**(向量检索,见「如何写好 query」),再走 `search`（默认不带 `ServiceCodes`），用脚本输出的摘要直接回答。
3. **首次检索匹配度不高** → 取返回结果里的 `ServiceCodes`，带上对应产品编码做二次检索缩小范围。
4. **需要某篇文档完整正文** → 先 `search` 找到链接，再 `fetch` 取全文。

## 常见使用示例

下面每个场景对应一种典型用户提问，演示「怎么选命令 + 怎么回答」。命令均相对本 skill 目录根执行。

### 示例 1 · 产品概念 / 计费咨询（最常见，search 直接答）

> 用户：「火山引擎 TOS 是什么？怎么计费？」

直接检索，用脚本输出的摘要组织回答，末尾附官方链接：

```bash
python3 scripts/volcengine_docs.py search "对象存储 TOS 是什么 计费方式" 3
```

### 示例 2 · 报错 / 故障排查（search 报错关键词）

> 用户：「调用火山 OpenAPI 返回 SignatureDoesNotMatch 是什么原因？」

把报错码 + 场景作为关键词检索，从结果里定位排查文档：

```bash
python3 scripts/volcengine_docs.py search "OpenAPI SignatureDoesNotMatch 签名错误 排查" 3
```

### 示例 3 · 用户直接给了文档链接（跳过 search，直接 fetch）

> 用户：「帮我读一下 https://www.volcengine.com/docs/6349/74820 这篇，讲了啥」

不需要检索，直接取全文，再用脚本输出的 markdown 正文总结（长文用 `start_index` 翻页）：

```bash
python3 scripts/volcengine_docs.py fetch "https://www.volcengine.com/docs/6349/74820"
```

### 示例 4 · 首次检索太宽 → 带产品编码二次缩范围

> 用户：「跨区域复制怎么做？」（问法宽泛，可能命中多个产品）

先宽泛检索，看首次结果里目标文档的 `ServiceCodes`（如对象存储是 `tos`），原样带上做二次检索：

```bash
python3 scripts/volcengine_docs.py search "跨区域复制 怎么配置" 5
python3 scripts/volcengine_docs.py search "跨区域复制 怎么配置" 3 tos
```

### 示例 5 · 要完整步骤 → 先 search 定位，再 fetch 取全文

> 用户：「给我用 TOS Browser 上传文件的完整步骤」

第 1 步检索找到最匹配的一篇，从输出里每条的 URL 行取链接；第 2 步对该链接 `fetch` 取全文，再整理成步骤：

```bash
python3 scripts/volcengine_docs.py search "TOS Browser 上传文件 步骤" 3
python3 scripts/volcengine_docs.py fetch "https://www.volcengine.com/docs/6349/162514"
```

## 结果处理规则

0. **stdout 是预览 + 落盘**：脚本把 stdout 限制在 ~4KB（`VOLC_PREVIEW_BYTES`），避免长输出打断任务。若结果超限，stdout 末尾会给 `…完整 N 字节已保存到：<临时文件路径>`，此时用 **Read 工具读该文件**（大文件用 `offset/limit` 分段，**不要 `cat` 整个文件**）获取全文；未超限则直接全量打印。
1. **优先用脚本输出的 markdown 文本回答**，它已解析裁剪好，无需再解析 JSON 或额外提炼。
2. **回答末尾必须附官方文档链接**作为来源，格式 `[文档标题](纯净URL)`，每条结果都要标注。
3. **链接用脚本输出里的纯净 URL**（已剥离 `?lang=zh` 等参数），禁止使用带参数的 URL。
4. 多个结果按相关性排序，最多展示 3 条最相关的，每条都带链接。

## 常见问题

- **请求超时 / 失败**：urllib 超时 15 秒，网络层失败时返回 `{"error": ...}` 并以非零退出码结束；可重试或换关键词。
- **search 输出 `{"info": "无结果或后端抖动…", "backend_error": …}`**：火山文档后端偶发抖动（`DownstreamError` / DocList 空，非脚本问题），退出码仍为 0，**重试一两次**即可恢复；`backend_error` 非空基本就是后端抖动。
- **fetch 输出 `{"info": "该链接无正文…"}`**：多半是传入了 `docs/{产品编号}` 这种**只有一级编号的导航首页**链接（不是具体文章，没有正文可取），**不是后端抖动，重试无用**。按 `fetch` 小节的「一级导航页链接的兜底策略」处理：改用 `search` 定位两级具体文章，并向用户说明这是导航首页。
- **检索结果不准 / 召回完全跑偏**：本接口是**向量语义检索**,跑偏多半是 query 太短、太英文缩写、太营销口语(如只搜「Coding Plan」会召回无关产品)。**先按「如何写好 query」把 query 重写成完整自然语言描述 + 产品全称**,再用首次返回的 `ServiceCodes` 做带产品编码的二次检索（见示例 4）。换语义等价说法重写,比重复同一句重试有效得多。
- **fetch 报错**：确认链接是 `https://www.volcengine.com/docs/...` 形式的官方文档链接。
