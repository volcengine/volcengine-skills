#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import http2 from "node:http2";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { fileURLToPath, pathToFileURL } from "node:url";

// gRPC status codes that are deterministic — retrying them on the same payload
// cannot succeed, so the export fails fast instead of burning the retry budget.
const NON_RETRYABLE_GRPC_STATUS = new Set([
  "3", // INVALID_ARGUMENT
  "5", // NOT_FOUND
  "7", // PERMISSION_DENIED
  "12", // UNIMPLEMENTED
  "16", // UNAUTHENTICATED
]);

const DEFAULT_ENDPOINT = "apmplus-cn-beijing.volces.com:4317";
const DEFAULT_APPKEY = "aafb2d32cc4bdd19d4366379635ef172";
const DEFAULT_SERVICE_NAME = "volcengine-skills";
const REPORTER_NAME = "volcengine-apmplus-hook-reporter";
const EVENT_SCHEMA_VERSION = "1.0.0";

// Default per-attempt OTLP export timeout. 1s is the documented default ceiling
// for a single attempt; users widen it via VOLCENGINE_TELEMETRY_TIMEOUT.
const DEFAULT_TIMEOUT_MS = 1000;
// Default export attempts. The hook dispatches the reporter asynchronously (in
// the background), so the host flow is never blocked by the export — that frees
// the reporter to retry on the warmed connection. The cold first RPC on a fresh
// HTTP/2 connection is the slow path; subsequent RPCs settle to a low, stable
// RTT, so a few retries (each still bounded by the 1s per-attempt timeout) lift
// the success rate well above a single attempt. Tune via
// VOLCENGINE_TELEMETRY_ATTEMPTS / --attempts.
const DEFAULT_ATTEMPTS = 3;
// Hard watchdog margin on top of attempts * timeout. Even if a socket wedges
// below the OS/network layer, the process force-exits so nothing can hang.
const WATCHDOG_MARGIN_MS = 750;

const SEVERITY_INFO = 9;

// Extensible event registry. Each definition maps a semantic event name to its
// aggregation-friendly type, action verb, and subject type. Adding a new event
// is purely declarative: register a definition here and a detector in
// normalizeEvent(); the envelope, attribute flattening, and OTLP export all
// derive their behavior from this table.
const EVENT_DEFINITIONS = {
  "volcengine.skill.invoked": {
    eventType: "skill_invocation",
    action: "invoke",
    subjectType: "skill",
  },
};

function parseArgs(argv) {
  const args = {
    agent: "auto",
    appkey: process.env.APMPLUS_APPKEY || DEFAULT_APPKEY,
    clientId: process.env.APMPLUS_CLIENT_ID || "",
    debug: truthy(process.env.APMPLUS_DEBUG),
    dryRun: false,
    endpoint: process.env.APMPLUS_ENDPOINT || DEFAULT_ENDPOINT,
    inputFile: "",
    mockExport: truthy(process.env.VOLCENGINE_HOOK_MOCK_EXPORT),
    mode: "auto",
    serviceName: process.env.APMPLUS_SERVICE_NAME || DEFAULT_SERVICE_NAME,
    strict: false,
    timeoutMs: resolveTimeoutMs(),
    attempts: resolveAttempts(),
    unlinkInputFile: false,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    const next = () => {
      i += 1;
      return argv[i] || "";
    };
    if (arg === "--agent") args.agent = next();
    else if (arg === "--appkey") args.appkey = next();
    else if (arg === "--client-id") args.clientId = next();
    else if (arg === "--debug") args.debug = true;
    else if (arg === "--dry-run") args.dryRun = true;
    else if (arg === "--endpoint") args.endpoint = next();
    else if (arg === "--input-file") args.inputFile = next();
    else if (arg === "--mock-export") args.mockExport = true;
    else if (arg === "--mode") args.mode = next();
    else if (arg === "--service-name") args.serviceName = next();
    else if (arg === "--strict") args.strict = true;
    else if (arg === "--timeout-ms") args.timeoutMs = normalizeTimeout(Number(next()));
    else if (arg === "--attempts") args.attempts = normalizeAttempts(Number(next()));
    else if (arg === "--unlink-input-file") args.unlinkInputFile = true;
    else if (arg === "--help" || arg === "-h") {
      printHelp();
      process.exit(0);
    }
  }

  if (!["auto", "skill"].includes(args.mode)) {
    args.mode = "auto";
  }
  return args;
}

// Timeout precedence: VOLCENGINE_TELEMETRY_TIMEOUT (ms) > APMPLUS_TIMEOUT_MS
// (legacy alias) > DEFAULT_TIMEOUT_MS. A bare `--timeout-ms` flag overrides all.
function resolveTimeoutMs() {
  const candidates = [
    process.env.VOLCENGINE_TELEMETRY_TIMEOUT,
    process.env.APMPLUS_TIMEOUT_MS,
  ];
  for (const candidate of candidates) {
    if (candidate === undefined || candidate === null || candidate === "") continue;
    return normalizeTimeout(Number(candidate));
  }
  return DEFAULT_TIMEOUT_MS;
}

function normalizeTimeout(value) {
  if (!Number.isFinite(value) || value <= 0) return DEFAULT_TIMEOUT_MS;
  // Floor avoids fractional timers; the upper bound is a sanity cap, not the
  // documented default. Users who explicitly widen the timeout get their value
  // up to 60s.
  return Math.min(Math.floor(value), 60000);
}

// Export attempts on a single warmed connection. VOLCENGINE_TELEMETRY_ATTEMPTS
// overrides the default; --attempts overrides the env.
function resolveAttempts() {
  const raw = process.env.VOLCENGINE_TELEMETRY_ATTEMPTS;
  if (raw === undefined || raw === null || raw === "") return DEFAULT_ATTEMPTS;
  return normalizeAttempts(Number(raw));
}

function normalizeAttempts(value) {
  if (!Number.isFinite(value) || value < 1) return DEFAULT_ATTEMPTS;
  // Cap retries so a wedged endpoint can never keep the background reporter
  // alive for an unbounded time even before the watchdog fires.
  return Math.min(Math.floor(value), 10);
}

function printHelp() {
  console.log(`Usage: ${REPORTER_NAME} [options]

Read a Claude Code / Codex / Cursor hook payload (or an OpenCode / OpenClaw
skill-load event), normalize safe metadata for Volcengine skill loads, and
export one OTLP log event directly to APMPlus over gRPC. Reporting is
best-effort and never blocks the host flow.

Options:
  --input-file <path>   Read hook JSON from a file instead of stdin.
  --mode <auto|skill>   Detection mode (only skill-load events are reported).
  --agent <auto|claude-code|codex|cursor|opencode|openclaw>
                        Override host-agent detection.
  --service-name <name> OTLP resource service.name.
  --endpoint <host:port>
                        APMPlus OTLP gRPC endpoint.
  --appkey <key>        APMPlus app key header value.
  --client-id <id>      Optional stable client identifier.
  --timeout-ms <n>      Per-attempt gRPC export timeout in ms. Default: ${DEFAULT_TIMEOUT_MS}.
  --attempts <n>        Export attempts on one warmed connection. Default: ${DEFAULT_ATTEMPTS}.
  --dry-run             Print the normalized event JSON and skip export.
  --mock-export         Build the event and return success without network I/O.
  --strict              Exit non-zero when export fails. Hooks should not use it.
  --debug               Print diagnostic messages to stderr.
  --unlink-input-file   Delete --input-file after reading it.

Environment:
  VOLCENGINE_TELEMETRY_DISABLED   Disable reporting (1/true/yes/on).
  VOLCENGINE_TELEMETRY_TIMEOUT    Per-attempt export timeout in ms. Default: ${DEFAULT_TIMEOUT_MS}.
  VOLCENGINE_TELEMETRY_ATTEMPTS   Export attempts. Default: ${DEFAULT_ATTEMPTS}.
  APMPLUS_APPKEY                  Override the APMPlus app key.
  APMPLUS_ENDPOINT                Override the APMPlus OTLP gRPC endpoint.
`);
}

function truthy(value) {
  return ["1", "true", "yes", "on"].includes(String(value || "").toLowerCase());
}

function telemetryDisabled() {
  return truthy(process.env.VOLCENGINE_TELEMETRY_DISABLED);
}

function readInput(args) {
  if (args.inputFile) {
    try {
      return fs.readFileSync(args.inputFile, "utf8");
    } finally {
      if (args.unlinkInputFile) {
        fs.rmSync(args.inputFile, { force: true });
      }
    }
  }
  if (process.stdin.isTTY) {
    return "";
  }
  return fs.readFileSync(0, "utf8");
}

function parseJson(raw) {
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function pick(object, paths) {
  for (const item of paths) {
    const parts = Array.isArray(item) ? item : String(item).split(".");
    let current = object;
    for (const part of parts) {
      if (!current || typeof current !== "object" || !(part in current)) {
        current = undefined;
        break;
      }
      current = current[part];
    }
    if (current !== undefined && current !== null && current !== "") {
      return current;
    }
  }
  return "";
}

function asString(value) {
  if (value === undefined || value === null) return "";
  if (typeof value === "string") return value;
  if (typeof value === "number" || typeof value === "boolean") return String(value);
  return "";
}

function inputObject(raw) {
  const input = pick(raw, [
    "tool_input",
    "toolInput",
    "input",
    "arguments",
    "tool.input",
    "tool.arguments",
  ]);
  return input && typeof input === "object" && !Array.isArray(input) ? input : {};
}

function normalizeSkillName(value) {
  let name = asString(value).trim();
  if (!name) return "";
  name = name.split(":").pop();
  name = name.split("/").pop();
  return name;
}

function skillFromPath(value) {
  const filePath = asString(value);
  const match = filePath.match(/(?:^|[/\\])(volcengine-[^/\\]+)[/\\][Ss][Kk][Ii][Ll][Ll]\.md$/);
  return match ? match[1] : "";
}

// Extract a `volcengine-*/SKILL.md` skill name from anywhere inside a shell
// command string. Codex loads a skill by shelling out to read its SKILL.md
// (e.g. `sed -n '1,220p' .../skills/volcengine-api/SKILL.md`), which surfaces as
// a Bash PostToolUse event rather than a Read/Skill tool — this recovers the
// skill name from that command. Non-anchored (the path is mid-string).
function skillFromCommand(value) {
  const command = asString(value);
  const match = command.match(/(?:^|[/\\])(volcengine-[^/\\\s'"]+)[/\\][Ss][Kk][Ii][Ll][Ll]\.md(?![A-Za-z0-9])/);
  return match ? match[1] : "";
}

// Detectors map a raw hook payload to one of the registered EVENT_DEFINITIONS.
// Returning null means the payload is not a reportable Volcengine event.
//
// Only skill-load events are reported. Four detection paths:
//   1. `Skill` tool invoking a `volcengine-*` skill (Claude Code).
//   2. `Read` tool reading a `volcengine-*/SKILL.md` via `tool_input.file_path`
//      (Claude Code).
//   3. shell/`Bash` command that reads a `volcengine-*/SKILL.md` — this is how
//      Codex loads a skill (it shells out to read SKILL.md), so it recovers the
//      skill name from the command string.
//   4. top-level `file_path` reading a `volcengine-*/SKILL.md` — Cursor's
//      `beforeReadFile` lifecycle event carries the path at the top level, with
//      no tool_name/tool_input wrapper.
function normalizeEvent(raw, args) {
  const toolName = asString(
    pick(raw, ["tool_name", "toolName", "tool.name", "tool", "name"]),
  );
  const hookEventName = asString(
    pick(raw, ["hook_event_name", "hookEventName", "event_name", "eventName", "event"]),
  ) || "PostToolUse";
  const input = inputObject(raw);

  let skillName = "";
  if (/^Skill$/i.test(toolName)) {
    skillName = normalizeSkillName(
      pick(input, ["command", "name", "skill", "skill_name", "skillName", "id"]),
    );
  }
  if (!skillName && /^Read$/i.test(toolName)) {
    skillName = skillFromPath(pick(input, ["file_path", "filePath", "path"]));
  }
  // Cursor's `beforeReadFile` event has the path at the top level (`file_path`),
  // not inside a tool_input wrapper, and carries no tool_name.
  if (!skillName) {
    skillName = skillFromPath(pick(raw, ["file_path", "filePath", "path"]));
  }
  if (!skillName) {
    skillName = skillFromCommand(pick(input, ["command", "cmd", "shell_command", "shellCommand"]));
  }
  if (skillName.startsWith("volcengine-")) {
    return {
      eventName: "volcengine.skill.invoked",
      hookEventName,
      input,
      subject: {
        name: skillName,
        namespace: "volcengine",
        type: "skill",
      },
      toolName: toolName || "unknown",
    };
  }

  return null;
}

function detectAgent(raw, override) {
  if (override && override !== "auto") return override;
  // Explicit hint set by the hook command (most deterministic).
  const envHint = String(process.env.VOLCENGINE_HOOK_AGENT || "").toLowerCase();
  if (/claude/.test(envHint)) return "claude-code";
  if (/codex/.test(envHint)) return "codex";
  if (/cursor/.test(envHint)) return "cursor";
  if (/opencode/.test(envHint)) return "opencode";
  if (/openclaw/.test(envHint)) return "openclaw";
  const explicit = asString(pick(raw, ["agent", "agent.name", "host", "host_agent"]));
  if (/claude/i.test(explicit)) return "claude-code";
  if (/codex/i.test(explicit)) return "codex";
  if (/cursor/i.test(explicit)) return "cursor";
  if (/opencode/i.test(explicit)) return "opencode";
  if (/openclaw/i.test(explicit)) return "openclaw";
  // Host-set environment signals. Check Cursor before Claude: Cursor sets a
  // CLAUDE_PROJECT_DIR compat var but NOT CLAUDE_PLUGIN_ROOT/CLAUDE_CODE_ENTRYPOINT.
  if (process.env.CURSOR_VERSION || process.env.CURSOR_TRANSCRIPT_PATH || process.env.CURSOR_PROJECT_DIR) {
    return "cursor";
  }
  if (process.env.CODEX_THREAD_ID || process.env.CODEX_HOME || process.env.CODEX_MANAGED_BY_NPM) {
    return "codex";
  }
  if (process.env.CLAUDE_PLUGIN_ROOT || process.env.CLAUDE_CODE_ENTRYPOINT) {
    return "claude-code";
  }
  return "unknown";
}

function packageInfo() {
  try {
    const here = path.dirname(fileURLToPath(import.meta.url));
    const packagePath = path.resolve(here, "..", "package.json");
    const parsed = JSON.parse(fs.readFileSync(packagePath, "utf8"));
    return {
      name: parsed.name || "volcengine-skills",
      version: parsed.version || "0.0.0",
    };
  } catch {
    return { name: "volcengine-skills", version: "0.0.0" };
  }
}

// A stable, anonymous per-install client id so events can be deduplicated and
// aggregated by machine. Persisted under the user cache; best-effort — falls
// back to a per-process random id if the cache is not writable.
function resolveClientId(args) {
  if (args.clientId) return args.clientId;
  try {
    const dir = path.join(os.homedir(), ".cache", "volcengine-skills");
    const file = path.join(dir, "telemetry-client-id");
    const existing = fs.readFileSync(file, "utf8").trim();
    if (existing) return existing;
  } catch {
    // not created yet or unreadable — fall through to create it
  }
  const id = `client-${crypto.randomUUID()}`;
  try {
    const dir = path.join(os.homedir(), ".cache", "volcengine-skills");
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, "telemetry-client-id"), `${id}\n`, { mode: 0o600 });
  } catch {
    // best-effort; a non-persisted random id is still acceptable
  }
  return id;
}

function buildEnvelope(raw, normalized, args) {
  const now = new Date();
  const pkg = packageInfo();
  const definition = EVENT_DEFINITIONS[normalized.eventName];
  const inputKeys = Object.keys(normalized.input || {})
    .filter((key) => /^[A-Za-z0-9_.:-]{1,80}$/.test(key))
    .sort();
  const clientId = resolveClientId(args);
  const agentName = detectAgent(raw, args.agent);

  const envelope = {
    schema_version: EVENT_SCHEMA_VERSION,
    event_id: crypto.randomUUID(),
    event_time: now.toISOString(),
    event_name: normalized.eventName,
    event_type: definition.eventType,
    source: "volcengine-skills.hooks",
    action: definition.action,
    agent: {
      name: agentName,
    },
    hook: {
      event_name: normalized.hookEventName,
      mode: args.mode,
    },
    package: pkg,
    subject: normalized.subject,
    telemetry: {
      client_id: clientId,
      reporter: REPORTER_NAME,
      reporter_version: pkg.version,
      transport: "otlp_grpc",
    },
    tool: {
      input_keys: inputKeys,
      name: normalized.toolName,
    },
    // Reserved, forward-compatible bag for additive event metadata. Consumers
    // must tolerate unknown keys; the schema_version gates breaking changes.
    extensions: {},
  };

  return envelope;
}

function flattenAttributes(event) {
  const attrs = {
    "agent.name": event.agent.name,
    "event.action": event.action,
    "event.id": event.event_id,
    "event.name": event.event_name,
    "event.schema_version": event.schema_version,
    "event.source": event.source,
    "event.type": event.event_type,
    "hook.event_name": event.hook.event_name,
    "hook.mode": event.hook.mode,
    "package.name": event.package.name,
    "package.version": event.package.version,
    "subject.name": event.subject.name,
    "subject.namespace": event.subject.namespace,
    "subject.type": event.subject.type,
    "telemetry.client_id": event.telemetry.client_id,
    "telemetry.reporter": event.telemetry.reporter,
    "telemetry.transport": event.telemetry.transport,
    "tool.name": event.tool.name,
  };
  if (event.subject.command) attrs["subject.command"] = event.subject.command;
  if (event.subject.service) attrs["subject.service"] = event.subject.service;
  if (event.tool.input_keys.length) attrs["tool.input_keys"] = event.tool.input_keys.join(",");
  return attrs;
}

function varint(value) {
  let n = BigInt(value);
  const bytes = [];
  while (n >= 0x80n) {
    bytes.push(Number((n & 0x7fn) | 0x80n));
    n >>= 7n;
  }
  bytes.push(Number(n));
  return Buffer.from(bytes);
}

function fieldKey(fieldNumber, wireType) {
  return varint((BigInt(fieldNumber) << 3n) | BigInt(wireType));
}

function fieldVarint(fieldNumber, value) {
  return Buffer.concat([fieldKey(fieldNumber, 0), varint(value)]);
}

function fieldFixed64(fieldNumber, value) {
  const body = Buffer.alloc(8);
  body.writeBigUInt64LE(BigInt(value));
  return Buffer.concat([fieldKey(fieldNumber, 1), body]);
}

function fieldBytes(fieldNumber, value) {
  const body = Buffer.isBuffer(value) ? value : Buffer.from(String(value), "utf8");
  return Buffer.concat([fieldKey(fieldNumber, 2), varint(body.length), body]);
}

function message(fieldNumber, chunks) {
  return fieldBytes(fieldNumber, Buffer.concat(chunks.filter(Boolean)));
}

function anyString(value) {
  return Buffer.concat([fieldBytes(1, String(value))]);
}

function keyValue(key, value) {
  return Buffer.concat([
    fieldBytes(1, key),
    message(2, [anyString(value)]),
  ]);
}

function repeatedKeyValues(fieldNumber, attrs) {
  return Object.entries(attrs)
    .filter(([, value]) => value !== undefined && value !== null && value !== "")
    .map(([key, value]) => message(fieldNumber, [keyValue(key, value)]));
}

function otlpLogsRequest(event, serviceName) {
  const nowNanos = BigInt(Date.parse(event.event_time)) * 1_000_000n;
  const attrs = flattenAttributes(event);
  // OTLP Resource must stay low-cardinality (it identifies the producing entity).
  // Per-event high-cardinality dimensions (event.name, subject.name) live only in
  // the LogRecord attributes; here we keep stable/constant and 2-valued grouping
  // keys so events aggregate cleanly by service/agent without resource explosion.
  const resourceAttrs = {
    "agent.name": event.agent.name,
    "event.schema_version": event.schema_version,
    "event.source": event.source,
    "event.type": event.event_type,
    "package.name": event.package.name,
    "package.version": event.package.version,
    "service.name": serviceName,
    "subject.type": event.subject.type,
    "telemetry.reporter": event.telemetry.reporter,
  };
  const resource = message(1, repeatedKeyValues(1, resourceAttrs));
  const scope = message(1, [
    fieldBytes(1, REPORTER_NAME),
    fieldBytes(2, event.package.version),
  ]);
  const logRecord = message(2, [
    fieldFixed64(1, nowNanos),
    fieldVarint(2, SEVERITY_INFO),
    fieldBytes(3, "INFO"),
    message(5, [anyString(JSON.stringify(event))]),
    ...repeatedKeyValues(6, attrs),
    fieldFixed64(11, nowNanos),
  ]);
  const scopeLogs = message(2, [scope, logRecord]);
  const resourceLogs = message(1, [resource, scopeLogs]);
  return Buffer.concat([resourceLogs]);
}

function grpcFrame(protobufBody) {
  const frame = Buffer.alloc(5);
  frame[0] = 0;
  frame.writeUInt32BE(protobufBody.length, 1);
  return Buffer.concat([frame, protobufBody]);
}

function parseEndpoint(endpoint) {
  if (/^https?:\/\//i.test(endpoint)) return new URL(endpoint);
  return new URL(`http://${endpoint}`);
}

// Timeouts and transient/unknown failures are worth retrying on the warmed
// connection; deterministic application errors (4xx, auth/arg/permission) are
// not.
function isRetryable(error) {
  if (!error) return true;
  if (typeof error.httpStatus === "number" && error.httpStatus >= 400 && error.httpStatus < 500) {
    return false;
  }
  if (error.grpcStatus && NON_RETRYABLE_GRPC_STATUS.has(String(error.grpcStatus))) {
    return false;
  }
  return true;
}

// One Export RPC bounded by a per-attempt timeout. On timeout the stream is
// closed but the shared client stays alive so the next attempt reuses the
// already-warmed connection (the cheap path).
function exportOnce(client, { appkey, body, timeoutMs }) {
  return new Promise((resolve, reject) => {
    let headers = {};
    let trailers = {};
    let settled = false;
    let stream;

    const done = (error) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      if (stream && !stream.closed) {
        try {
          stream.close();
        } catch {
          // best-effort; the client is destroyed by the caller anyway
        }
      }
      if (error) reject(error);
      else resolve();
    };

    const timer = setTimeout(() => {
      done(new Error(`OTLP gRPC export attempt timed out after ${timeoutMs}ms`));
    }, timeoutMs);

    try {
      stream = client.request({
        ":method": "POST",
        ":path": "/opentelemetry.proto.collector.logs.v1.LogsService/Export",
        "content-type": "application/grpc",
        "grpc-accept-encoding": "identity",
        "grpc-encoding": "identity",
        "te": "trailers",
        "user-agent": `${REPORTER_NAME}/1.0`,
        "x-byteapm-appkey": appkey,
      });
    } catch (error) {
      done(error);
      return;
    }

    stream.on("response", (value) => {
      headers = value;
    });
    stream.on("trailers", (value) => {
      trailers = value;
    });
    stream.on("data", () => {});
    stream.on("error", (error) => done(error));
    stream.on("end", () => {
      const httpStatus = Number(headers[":status"] || 0);
      const grpcStatus = String(trailers["grpc-status"] ?? headers["grpc-status"] ?? "");
      if (httpStatus !== 200) {
        done(Object.assign(new Error(`OTLP gRPC HTTP status ${httpStatus || "unknown"}`), { httpStatus }));
        return;
      }
      // A gRPC response without a status is, per spec, an UNKNOWN failure — do
      // not silently count it as success (it would mask dropped data).
      if (grpcStatus === "") {
        done(new Error("OTLP gRPC response missing grpc-status"));
        return;
      }
      if (grpcStatus !== "0") {
        const messageText = trailers["grpc-message"] || headers["grpc-message"] || "unknown";
        done(Object.assign(new Error(`OTLP gRPC status ${grpcStatus}: ${messageText}`), { grpcStatus }));
        return;
      }
      done();
    });
    stream.end(body);
  });
}

function exportGrpc({ appkey, attempts, endpoint, event, serviceName, timeoutMs }) {
  return new Promise((resolve, reject) => {
    const endpointUrl = parseEndpoint(endpoint);
    const client = http2.connect(endpointUrl.origin);
    const body = grpcFrame(otlpLogsRequest(event, serviceName));
    let clientError = null;
    let finished = false;

    const finish = (error) => {
      if (finished) return;
      finished = true;
      // destroy() (not close()) aborts sockets stuck mid-connect so a
      // network-layer stall cannot keep the event loop alive past the deadline.
      client.destroy();
      if (error) reject(error);
      else resolve();
    };

    client.on("error", (error) => {
      clientError = error;
    });

    (async () => {
      let lastError = clientError;
      for (let attempt = 0; attempt < attempts; attempt += 1) {
        if (client.destroyed) break;
        try {
          await exportOnce(client, { appkey, body, timeoutMs });
          finish();
          return;
        } catch (error) {
          lastError = error;
          // A connection-level error tears down the client; retrying on it is
          // pointless, so surface immediately.
          if (clientError || client.destroyed) {
            finish(clientError || error);
            return;
          }
          // Deterministic application errors (auth/argument/permission, HTTP 4xx)
          // will fail identically on retry — stop early instead of burning the
          // remaining attempts (and N× the load on the ingestion endpoint).
          if (!isRetryable(error)) {
            finish(error);
            return;
          }
        }
      }
      finish(lastError || new Error("OTLP gRPC export failed"));
    })();
  });
}

function debug(args, message) {
  if (args.debug) {
    console.error(`[${REPORTER_NAME}] ${message}`);
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (telemetryDisabled()) {
    debug(args, "telemetry disabled by environment");
    return 0;
  }

  // Hard non-blocking guarantee: regardless of what the export or runtime does,
  // force a clean exit once the total deadline (all attempts) plus a small
  // cleanup margin elapses. unref() keeps this backstop from holding the
  // process open on its own.
  const watchdog = setTimeout(() => {
    if (args.debug) console.error(`[${REPORTER_NAME}] watchdog fired; exiting`);
    process.exit(args.strict ? 1 : 0);
  }, args.timeoutMs * args.attempts + WATCHDOG_MARGIN_MS);
  watchdog.unref();

  const rawInput = readInput(args);
  if (!rawInput.trim()) {
    debug(args, "empty hook payload");
    return 0;
  }

  const raw = parseJson(rawInput);
  if (!raw) {
    debug(args, "invalid hook payload JSON");
    return 0;
  }

  const normalized = normalizeEvent(raw, args);
  if (!normalized) {
    debug(args, "hook payload did not match a reportable Volcengine event");
    return 0;
  }

  const event = buildEnvelope(raw, normalized, args);
  if (args.dryRun) {
    console.log(JSON.stringify(event, null, 2));
    return 0;
  }
  if (args.mockExport) {
    debug(args, `mock reported ${event.event_name} ${event.subject.name}`);
    return 0;
  }

  try {
    await exportGrpc({
      appkey: args.appkey,
      attempts: args.attempts,
      endpoint: args.endpoint,
      event,
      serviceName: args.serviceName,
      timeoutMs: args.timeoutMs,
    });
    debug(args, `reported ${event.event_name} ${event.subject.name}`);
  } catch (error) {
    const message = error && error.message ? error.message : String(error);
    if (args.debug || args.strict) {
      console.error(`[${REPORTER_NAME}] report failed: ${message}`);
    }
    if (args.strict) {
      // Exit promptly once the network settles instead of waiting on the
      // lingering HTTP/2 socket teardown, so the background reporter does not
      // outlive its work. No stdout is pending on the export path.
      process.exit(1);
    }
  }
  process.exit(0);
}

// Only run when invoked as a program, not when imported (e.g. by unit tests of
// the pure encoding/normalization helpers below).
const invokedDirectly =
  process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href;

if (invokedDirectly) {
  main()
    .then((code) => {
      process.exitCode = code;
    })
    .catch((error) => {
      // Any unexpected failure is swallowed: telemetry must never break the host.
      console.error(`[${REPORTER_NAME}] unexpected failure: ${error.message || error}`);
      process.exitCode = 0;
    });
}

export {
  EVENT_DEFINITIONS,
  buildEnvelope,
  detectAgent,
  flattenAttributes,
  isRetryable,
  normalizeEvent,
  otlpLogsRequest,
};
