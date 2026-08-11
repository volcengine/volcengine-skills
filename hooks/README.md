# Volcengine APMPlus 遥测 hook

当加载 `volcengine-*` skill 时，把低敏使用元数据上报到火山引擎 APMPlus。Claude Code / Codex / Cursor 通过生命周期 hook 接入，OpenCode / OpenClaw 通过插件接入，全部复用同一套 dispatcher + reporter。

本目录文件：

- `hooks.json` — Claude Code / Codex 共用的生命周期配置；使用 `${PLUGIN_ROOT}` / `${CLAUDE_PLUGIN_ROOT}` 解析安装后的核心插件目录，并显式设置 `async: false`
- `hooks-cursor.json` — Cursor 生命周期配置，由核心插件的 `.cursor-plugin/plugin.json` 引用；用 `${CURSOR_PLUGIN_ROOT}`（插件安装态）、事件 `beforeReadFile`、并以 `VOLCENGINE_HOOK_AGENT=cursor` 标记宿主。真正的使用信号来自“安装插件后在用户项目里加载了 `volcengine-*` skill”，因此不维护仅在打开本仓库时触发的项目级 hook
- `run-apmplus-reporter.sh` — dispatcher：开关判断、transport 选择、超时、异步派发等全部逻辑
- `volcengine-apmplus-hook-reporter.mjs` — reporter：解析 payload、归一化事件、OTLP gRPC 直连 APMPlus

同步脚本只把上述配置和执行文件复制到默认核心插件；可选产品域插件不重复注册 telemetry hook。

OpenCode 与 OpenClaw 不走生命周期 hook，而是用插件接入（复用上面的 dispatcher + reporter）：

- `../.opencode/plugin/volcengine-telemetry.js` — OpenCode 插件，监听原生 `skill` 工具的 `tool.execute.after`；当加载的是 `volcengine-*` skill 时，构造 `{tool_name:"skill",tool_input:{name}}` payload，以 `VOLCENGINE_HOOK_AGENT=opencode` 交给 `run-apmplus-reporter.sh` 异步上报。插件相对自身解析到 `hooks/`，找不到 reporter 时静默禁用。
- `openclaw-telemetry.js` + `openclaw-skill-detect.js` — OpenClaw 插件，经根 `package.json` 的 `"openclaw": { "extensions": ["./hooks/openclaw-telemetry.js"] }` 注册（清单 `openclaw.plugin.json` 只放元数据，并需 `configSchema`、`activation.onStartup: true`）。OpenClaw 没有 skill 工具，只把 `<available_skills>` 元数据注入 prompt，模型用 `read` 工具读 `volcengine-*/SKILL.md` 来加载 skill；入口在 `before_tool_call` 钩子里检测该 read（按值扫描 `params`/`derivedPaths`，不写死参数名），构造 `{tool_name:"read",tool_input:{file_path}}` payload，以 `VOLCENGINE_HOOK_AGENT=openclaw` 交给 reporter。检测/派发逻辑放在不依赖 OpenClaw SDK 的 `openclaw-skill-detect.js`（可单测）；reporter 为同目录兄弟文件，找不到时静默禁用。

## 遥测与隐私（请先阅读）

- **默认开启**（opt-out）：安装后，当你在 Claude Code / Codex / Cursor / OpenCode / OpenClaw 中加载某个 `volcengine-*` skill 时，会**异步**上报一条低敏使用元数据到火山引擎 APMPlus。上报在后台进行，**不阻塞**工作流，失败也不影响任何操作。

- **上报哪一种事件**：`volcengine.skill.invoked` —— 加载了某个 `volcengine-*` skill。

- **上报哪些字段**（仅元数据）：事件名/类型、UTC 时间、随机 `event_id`、宿主 agent 名（`claude-code`/`codex`/`cursor`/`opencode`/`openclaw`）、hook 名、包名与版本、**skill 名**（如 `volcengine-cli`）、宿主工具名（如 `Skill`/`Read`/`skill`/`read`）、工具输入的**字段名列表**（如 `command`，不含字段值）、一个**匿名且稳定**的 `client_id`（随机 UUID，按机器持久化，不含任何身份信息）。

- **不会收集敏感信息**：明确**不上报**——
  - 文件内容、文件路径内容（仅用于判断是否在读 `volcengine-*/SKILL.md`，不上报路径本身）；
  - 任何命令、命令参数及其**取值**；
  - 工具输入的**字段值**（只取字段名）；
  - 任何 token / 密钥 / AK / SK / 凭证；
  - session id / thread id / 会话记录路径 / 当前工作目录（即使宿主在 payload 里带了，reporter 也不会提取或转发）。

- **如何关闭**：设置环境变量即可彻底关闭（dispatch 都不会发生）：

  ```bash
  export VOLCENGINE_TELEMETRY_DISABLED=1
  ```

  接受 `1` / `true` / `yes` / `on`。

## 触发与识别

reporter 依次尝试四条识别路径，任一命中即上报；非 `volcengine-` 的 skill / 文件 / 命令一律静默跳过：

- `Skill` 工具调用 `volcengine-*` skill（Claude Code；OpenCode 的原生 `skill` 工具也走此路径，由插件转发）；
- `Read` 工具通过 `tool_input.file_path` 读取 `volcengine-*/SKILL.md`（Claude Code；OpenClaw 模型用 `read` 工具读 SKILL.md 加载 skill，由插件转成此路径）；
- shell 命令读取 `volcengine-*/SKILL.md`（Codex 用 `sed`/`cat` 读 SKILL.md 来加载 skill）；
- 顶层 `file_path` 读取 `volcengine-*/SKILL.md`（Cursor 的 `beforeReadFile` 事件，路径在 payload 顶层）。

## 主流程保护

- **异步后台派发**：主流程只做「读 stdin → 写 dispatch 日志 → 派发」，实测阻塞约 10–28ms；新会话使其在宿主进程组退出/SIGHUP 时仍能在窗口内跑完。
- reporter 单次 OTLP 导出默认 1s 超时，同连接默认重试 3 次，内置 `attempts*timeout+750ms` 看门狗硬退出；不可重试错误（鉴权/参数/4xx）快失败。
- reporter 成功、失败或超时都不影响 hook 退出码，hook 入口始终尽力 `exit 0`。

## 环境变量

| 环境变量 | 默认 | 说明 |
| --- | --- | --- |
| `VOLCENGINE_TELEMETRY_DISABLED` | 未设置 | `1`/`true`/`yes`/`on` 关闭上报 |
| `VOLCENGINE_TELEMETRY_TIMEOUT` | `1000` | 单次 OTLP 导出超时（毫秒） |
| `VOLCENGINE_TELEMETRY_ATTEMPTS` | `3` | 同连接导出重试次数 |
| `APMPLUS_ENDPOINT` | `apmplus-cn-beijing.volces.com:4317` | OTLP gRPC endpoint |
| `APMPLUS_APPKEY` | 内置 key | 覆盖 APMPlus appkey |
| `VOLCENGINE_HOOK_REPORTER_TIMEOUT_SECONDS` | `5` | 外层 shell 超时（秒，与上面自适应取大） |
| `VOLCENGINE_HOOK_LOG` | — | dispatcher 日志路径（不设则不写） |

测试专用：`VOLCENGINE_HOOK_MOCK_EXPORT=1`（构造事件不发网络）、`VOLCENGINE_HOOK_REPORTER_BIN`（指定 reporter 路径）。
