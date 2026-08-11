// Volcengine skill-load telemetry for OpenClaw.
//
// OpenClaw has no skill tool: only the <available_skills> metadata catalog is
// injected into the prompt, and the model loads a skill by `read`-ing its
// SKILL.md. We observe that via the `before_tool_call` typed hook and, when the
// read targets a volcengine-*/SKILL.md, hand a normalized payload to the shared
// reporter (hooks/run-apmplus-reporter.sh) — reusing the same opt-out / async
// dispatch / OTLP-to-APMPlus path as the Claude / Codex / Cursor / OpenCode
// integrations.
//
// Wired in via package.json:
//   "openclaw": { "extensions": ["./hooks/openclaw-telemetry.js"] }
// Detection + dispatch live in the SDK-free, unit-tested ./openclaw-skill-detect.js.
//
// Best-effort and non-blocking. Opt out with VOLCENGINE_TELEMETRY_DISABLED=1.

import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { onBeforeToolCall } from "./openclaw-skill-detect.js";

export default definePluginEntry({
  id: "volcengine-skills",
  name: "Volcengine Skills Telemetry",
  description:
    "Reports volcengine-* skill loads to Volcengine APMPlus (opt-out via VOLCENGINE_TELEMETRY_DISABLED=1).",
  register(api) {
    // Observe only; return nothing so the tool call is never mutated or blocked.
    api.on("before_tool_call", async (event) => {
      onBeforeToolCall(event);
    });
  },
});
