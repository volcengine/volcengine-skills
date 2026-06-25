// Core skill-load detection + telemetry dispatch for the OpenClaw plugin.
//
// Kept free of any OpenClaw SDK import so it stays unit-testable; the thin entry
// (openclaw-telemetry.js) wires this into `api.on("before_tool_call", ...)`.
//
// OpenClaw has no `skill` tool — only an <available_skills> metadata catalog is
// injected into the prompt, and the model loads a skill by `read`-ing its
// SKILL.md. So a volcengine skill load surfaces as a tool call whose params /
// derivedPaths contain a `volcengine-*/SKILL.md` path. We hand that path to the
// shared reporter, which reuses the same opt-out / async dispatch / OTLP export
// as the other agents.

import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// run-apmplus-reporter.sh is a sibling of this file (both under hooks/).
const REPORTER_SH = resolve(
  dirname(fileURLToPath(import.meta.url)),
  "run-apmplus-reporter.sh",
);

// The `read` tool's path arg key varies by build (file_path / path / filePath),
// so scan candidate string values rather than hard-coding a key.
const SKILL_MD_RE = /(?:^|[/\\])volcengine-[^/\\]+[/\\]skill\.md$/i;

export function findVolcengineSkillMdPath(event) {
  if (!event || typeof event !== "object") return "";
  const candidates = [];
  const params = event.params;
  if (params && typeof params === "object") {
    for (const v of Object.values(params)) {
      if (typeof v === "string") candidates.push(v);
    }
  }
  if (Array.isArray(event.derivedPaths)) {
    for (const p of event.derivedPaths) {
      if (typeof p === "string") candidates.push(p);
    }
  }
  return candidates.find((p) => SKILL_MD_RE.test(p)) || "";
}

export function dispatchSkillLoad(filePath) {
  if (!existsSync(REPORTER_SH)) return false;
  // The reporter's Read-tool path extracts the skill from tool_input.file_path.
  const payload = JSON.stringify({
    hook_event_name: "before_tool_call",
    tool_name: "read",
    tool_input: { file_path: filePath },
  });
  const child = spawn("bash", [REPORTER_SH, "--mode", "skill"], {
    env: { ...process.env, VOLCENGINE_HOOK_AGENT: "openclaw" },
    stdio: ["pipe", "ignore", "ignore"],
    detached: true,
  });
  child.on("error", () => {});
  child.stdin.on("error", () => {});
  child.stdin.write(payload);
  child.stdin.end();
  child.unref();
  return true;
}

// before_tool_call hook body: best-effort, never throws, returns nothing (so it
// never mutates or blocks the observed tool call).
export function onBeforeToolCall(event) {
  try {
    const filePath = findVolcengineSkillMdPath(event);
    if (filePath) dispatchSkillLoad(filePath);
  } catch {
    // best-effort; never block the agent
  }
}
