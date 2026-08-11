#!/usr/bin/env bash
#
# Shared Volcengine APMPlus hook dispatcher (asynchronous APMPlus direct export).
#
# Dispatch mode (default): read the hook payload, log dispatch, then launch the
# reporter DETACHED in a new session (setsid/nohup) and return immediately, so
# the host flow is never blocked and the export survives a host process-group
# exit within its short window. The reporter is run via `node` from the bundled
# sibling file (VOLCENGINE_HOOK_REPORTER_BIN overrides it for tests).
#
# Worker mode (--bg-worker): this same script re-exec'd in the detached session;
# it runs the chosen reporter, records the result, and cleans up the tmp payload.
#
# Reporting success, failure, or timeout is never allowed to fail the host flow.

set +e

lower() {
  printf '%s' "${1:-}" | tr '[:upper:]' '[:lower:]'
}

# GNU `timeout` is absent on stock macOS (only `gtimeout` after brew coreutils).
# Fall back to running the reporter bare — it has its own hard watchdog.
timeout_bin() {
  if command -v timeout >/dev/null 2>&1; then
    echo "timeout"
  elif command -v gtimeout >/dev/null 2>&1; then
    echo "gtimeout"
  else
    echo ""
  fi
}

MODE="auto"
BG_WORKER=0
REQUIRE_SKILL_MD=0
while [ "$#" -gt 0 ]; do
  case "$1" in
    --bg-worker) BG_WORKER=1; shift ;;
    --mode) MODE="${2:-auto}"; shift 2 ;;
    --mode=*) MODE="${1#--mode=}"; shift ;;
    --require-skill-md) REQUIRE_SKILL_MD=1; shift ;;
    *) shift ;;
  esac
done

LOGFILE="${VOLCENGINE_HOOK_LOG:-${APMPLUS_HOOK_LOG:-${TMPDIR:-/tmp}/volcengine-apmplus-hook.log}}"

log_done() {
  printf '%s\tmode=%s\taction=done\ttransport=%s\tstatus=%s\n' \
    "$(date '+%Y-%m-%dT%H:%M:%S%z')" "$MODE" "$1" "$2" \
    >>"$LOGFILE" 2>/dev/null
}

# ---------------------------------------------------------------------------
# Worker mode: detached; carries state via exported VHK_* env vars.
# ---------------------------------------------------------------------------
if [ "$BG_WORKER" = 1 ]; then
  TO="$(timeout_bin)"
  run_bounded() {
    if [ -n "$TO" ]; then
      "$TO" "$VHK_TO" "$@"
    else
      "$@"
    fi
  }
  case "$VHK_TRANSPORT" in
    bin)
      run_bounded "$VHK_REPORTER_BIN" --input-file "$VHK_INPUT" --mode "$MODE" >>"$LOGFILE" 2>&1
      ;;
    *)
      run_bounded "$VHK_NODE" "$VHK_BUNDLED" --input-file "$VHK_INPUT" --mode "$MODE" >>"$LOGFILE" 2>&1
      ;;
  esac
  log_done "$VHK_TRANSPORT" "$?"
  rm -f "$VHK_INPUT" 2>/dev/null
  exit 0
fi

# ---------------------------------------------------------------------------
# Dispatch mode.
# ---------------------------------------------------------------------------
case "$(lower "$VOLCENGINE_TELEMETRY_DISABLED")" in
  1|true|yes|on) exit 0 ;;
esac

if [ -t 0 ]; then
  exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NODE_BIN="${VOLCENGINE_HOOK_NODE_BIN:-node}"
REPORTER_BIN="${VOLCENGINE_HOOK_REPORTER_BIN:-}"
BUNDLED_REPORTER="$SCRIPT_DIR/volcengine-apmplus-hook-reporter.mjs"

# Outer shell timeout (seconds). Keep it >= the reporter's own budget
# (per-attempt timeout_ms * attempts) so the shell timeout never pre-empts the
# reporter's retry/watchdog logic when the user widens VOLCENGINE_TELEMETRY_*.
TMO="${VOLCENGINE_TELEMETRY_TIMEOUT:-1000}"
ATT="${VOLCENGINE_TELEMETRY_ATTEMPTS:-3}"
case "$TMO" in ''|*[!0-9]*) TMO=1000 ;; esac
case "$ATT" in ''|*[!0-9]*) ATT=3 ;; esac
BUDGET=$(( (TMO * ATT + 999) / 1000 + 1 ))
REPORTER_TIMEOUT_SECONDS="${VOLCENGINE_HOOK_REPORTER_TIMEOUT_SECONDS:-5}"
case "$REPORTER_TIMEOUT_SECONDS" in ''|*[!0-9]*) REPORTER_TIMEOUT_SECONDS=5 ;; esac
if [ "$BUDGET" -gt "$REPORTER_TIMEOUT_SECONDS" ]; then
  REPORTER_TIMEOUT_SECONDS="$BUDGET"
fi

if [ -n "$REPORTER_BIN" ]; then
  TRANSPORT="bin"
else
  TRANSPORT="node"
fi

RAW="$(cat 2>/dev/null)"
if [ -z "$RAW" ]; then
  exit 0
fi

# Cheap guard for the Codex shell-tool hook: skill loads there appear as a shell
# command that reads a SKILL.md, but the matcher fires on every shell command.
# Skip dispatch (no node spawn) unless the payload even mentions SKILL.md.
if [ "$REQUIRE_SKILL_MD" = 1 ]; then
  case "$RAW" in
    *SKILL.md*|*skill.md*) ;;
    *) exit 0 ;;
  esac
fi

umask 077
# No literal suffix after the X's: BSD/macOS mktemp requires the template to end
# in consecutive X's. The reporter reads via --input-file, so the name is opaque.
INPUT_FILE="$(mktemp "${TMPDIR:-/tmp}/volcengine-hook.XXXXXX" 2>/dev/null)"
if [ -z "$INPUT_FILE" ]; then
  exit 0
fi
printf '%s' "$RAW" >"$INPUT_FILE" 2>/dev/null || {
  rm -f "$INPUT_FILE" 2>/dev/null
  exit 0
}

printf '%s\tmode=%s\taction=dispatch\ttransport=%s\n' \
  "$(date '+%Y-%m-%dT%H:%M:%S%z')" "$MODE" "$TRANSPORT" \
  >>"$LOGFILE" 2>/dev/null

# State for the detached worker (re-exec of this script with --bg-worker).
export VHK_TRANSPORT="$TRANSPORT"
export VHK_INPUT="$INPUT_FILE"
export VHK_TO="$REPORTER_TIMEOUT_SECONDS"
export VHK_NODE="$NODE_BIN"
export VHK_BUNDLED="$BUNDLED_REPORTER"
export VHK_REPORTER_BIN="$REPORTER_BIN"
export VOLCENGINE_HOOK_LOG="$LOGFILE"

# Detach into a new session so the export survives a host process-group exit /
# SIGHUP within its short window; fall back through nohup to a plain background.
WORKER_CMD=(bash "${BASH_SOURCE[0]}" --bg-worker --mode "$MODE")
if command -v setsid >/dev/null 2>&1; then
  setsid "${WORKER_CMD[@]}" </dev/null >/dev/null 2>&1 &
elif command -v nohup >/dev/null 2>&1; then
  nohup "${WORKER_CMD[@]}" </dev/null >/dev/null 2>&1 &
else
  "${WORKER_CMD[@]}" </dev/null >/dev/null 2>&1 &
fi
disown 2>/dev/null

exit 0
