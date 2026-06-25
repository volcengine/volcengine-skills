// Volcengine skill-load telemetry for OpenCode.
//
// OpenCode loads a skill via its native `skill` tool (the model calls
// skill({ name })). That surfaces here as a `tool.execute.after` hook with
// input.tool === "skill" and the resolved skill name in output.metadata.name.
// When the loaded skill is a `volcengine-*` one, we hand a normalized payload to
// the shared dispatcher (hooks/run-apmplus-reporter.sh), which performs the
// opt-out check, detached async dispatch, transport, timeout and OTLP export to
// APMPlus — exactly the same path used by the Claude / Codex / Cursor hooks.
//
// Best-effort and non-blocking: every failure is swallowed so the agent flow is
// never affected. Opt out entirely with VOLCENGINE_TELEMETRY_DISABLED=1.

import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// hooks/run-apmplus-reporter.sh lives two levels up from .opencode/plugin/.
const REPORTER_SH = resolve(
  dirname(fileURLToPath(import.meta.url)),
  "../../hooks/run-apmplus-reporter.sh",
);

function reportSkillLoad(skillName) {
  // The reporter's `Skill` tool detection path reads tool_input.name.
  const payload = JSON.stringify({
    hook_event_name: "tool.execute.after",
    tool_name: "skill",
    tool_input: { name: skillName },
  });
  const child = spawn("bash", [REPORTER_SH, "--mode", "skill"], {
    env: { ...process.env, VOLCENGINE_HOOK_AGENT: "opencode" },
    stdio: ["pipe", "ignore", "ignore"],
    detached: true,
  });
  child.on("error", () => {});
  child.stdin.on("error", () => {});
  child.stdin.write(payload);
  child.stdin.end();
  child.unref();
}

export const VolcengineSkillTelemetry = async () => {
  // Graceful no-op when the bundled reporter isn't alongside this plugin
  // (e.g. the plugin was copied out of the repo on its own).
  const enabled = existsSync(REPORTER_SH);

  return {
    "tool.execute.after": async (input, output) => {
      try {
        if (!enabled) return;
        if (!input || input.tool !== "skill") return;
        const name =
          (output && output.metadata && output.metadata.name) ||
          (input.args && input.args.name);
        if (typeof name !== "string" || !name.startsWith("volcengine-")) return;
        reportSkillLoad(name);
      } catch {
        // best-effort; never block the agent
      }
    },
  };
};

export default VolcengineSkillTelemetry;
