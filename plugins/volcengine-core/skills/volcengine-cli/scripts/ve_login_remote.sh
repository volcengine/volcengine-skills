#!/usr/bin/env bash
# Copyright (c) 2026 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: MIT
# ve_login_remote.sh — orchestrate `ve login` (OAuth 2.0 Device Authorization
# Grant) across multiple tool invocations in agent contexts (OpenClaw, Feishu
# bots, sandboxed runners).
#
# The file name is historical; the flow it drives is the device-code login
# that every current `ve` ships: ve prints a verification URL plus a short
# user code, then polls the server until the user authorizes in a browser.
# NOTHING comes back from the user — when they say they are done, `verify`
# confirms the login landed.
#
# Why this script exists:
#   In agent contexts each tool call is a fresh shell, so the agent cannot
#   keep `ve` alive across the URL-print -> user-finishes-in-browser gap.
#   The device code lives only in the ve process's memory, so ve must survive
#   the whole browser round-trip — in practice several minutes of human
#   latency. `start` therefore detaches ve into its own session (PPID 1) so it
#   survives the launching tool call being killed and process-group cleanup.
#   `nohup` is NOT enough: it only ignores SIGHUP and leaves ve in the caller's
#   process group.
#
#   ve's stdin is bound to a named pipe (fifo). That is how the
#   `Replace the existing login_session? [y/N]:` prompt (asked when switching
#   accounts on a profile that already holds a session) gets its answer — with
#   stdin on /dev/null that prompt would hit EOF and fail the login *after*
#   the user had already authorized.
#
#   Detaching uses `setsid` where available (Linux). macOS ships no `setsid`,
#   so the script falls back to perl's POSIX::setsid, then to a plain
#   background launch.
#
# Subcommands:
#   start <region> [profile]
#                      Launch `ve login --no-browser --lang en` detached, record the URL
#                      and user code, print the KEY=value block, and return.
#                      Some sandbox runners do not consider a command finished
#                      while a descendant is alive, so this call may hang until
#                      the runner's own timeout. That is expected and harmless:
#                      ve, the fifo, and the recorded URL all survive. Do not
#                      retry — call `url` instead.
#   url                Print the same block and exit immediately. Never
#                      blocks. Prints PENDING (exit 11) if ve has not emitted
#                      the URL yet; exit 3 if ve is no longer alive (its URL is
#                      dead and must not be handed out).
#   status             Report whether the ve subprocess is still alive, whether
#                      the URL is available, and whether the device code has
#                      expired. Never blocks.
#   start-wait <region> [profile]
#                      `start`, then keep this wrapper alive until `ve login`
#                      exits, then `verify`. Only usable in a runtime that can
#                      hold a long-running tool session open for the entire
#                      browser round-trip (e.g. a background/async tool call
#                      whose interim output can be read while it runs).
#   verify [profile]   Check whether the login landed. Never blocks.
#                      Exit 0  = logged in and API-verified.
#                      Exit 11 = ve still running (user has not finished yet).
#                                The API is deliberately NOT consulted while ve
#                                lives: on an account switch the old session
#                                would answer and mask the pending login.
#                      Exit 13 = ve reported "Successfully logged in!" but the
#                                verification API call failed — a local
#                                network/proxy problem, NOT a login failure.
#                                Do not restart the login.
#                      Exit 10 = ve exited without a usable session (device
#                                code expired / authorization denied). Start
#                                over.
#   abort              Kill the running ve subprocess and clean up state.
#
# Pass [profile] to start/start-wait and to verify alike when the conversation
# has fixed a non-default profile — otherwise the login lands on `default` and
# the fixed profile stays broken.
#
# Output block printed by `start`, `start-wait` and `url` (one KEY=value per
# line, so callers can grep a key instead of parsing prose):
#   URL=<verification URL>
#   CODE=<user code>
#   LINK=<URL with the code prefilled>     hand THIS to the user; URL+CODE are
#                                          the fallback
#   EXPIRES_IN=<seconds>                   ve's own figure; the code is dead
#                                          after that
#   NEXT=<what to do next>
#
# State files (one set per UID for multi-user safety on shared hosts):
#   /tmp/ve_login_<uid>.fifo   fifo bound to ve's stdin
#   /tmp/ve_login_<uid>.pid    PID of running `ve login`
#   /tmp/ve_login_<uid>.log    Captured stdout+stderr of ve
#   /tmp/ve_login_<uid>.url    Login URL, once ve has emitted it
#   /tmp/ve_login_<uid>.start  Epoch seconds when ve was launched
#
# Environment overrides (seconds):
#   VE_LOGIN_URL_TIMEOUT       How long `start` waits for ve to emit the URL
#                              (default 30). On expiry `start` KILLS ve and
#                              wipes the state, so lowering this can destroy a
#                              session that was merely slow to start. It does
#                              not affect how long the `start` tool call itself
#                              appears to hang.

set -euo pipefail

# The log holds the live login URL and user code; on a shared host anyone who
# can read it can authorize the device with their own account. Keep every
# state file owner-only (the fifo already is via mkfifo -m 600).
umask 077

uid_tag="$(id -u)"
fifo="/tmp/ve_login_${uid_tag}.fifo"
pid_file="/tmp/ve_login_${uid_tag}.pid"
log_file="/tmp/ve_login_${uid_tag}.log"
url_file="/tmp/ve_login_${uid_tag}.url"
start_file="/tmp/ve_login_${uid_tag}.start"
replaced_marker="/tmp/ve_login_${uid_tag}.replaced"
url_timeout="${VE_LOGIN_URL_TIMEOUT:-30}"

usage() {
  cat <<USAGE >&2
Usage:
  $0 start <region> [profile]     Launch ve login detached, print URL/CODE/LINK.
                                  May hang until the runner's timeout; that is
                                  expected. Do not retry — call 'url' next.
  $0 url                          Print the URL/CODE/LINK block. Never blocks.
  $0 status                       Report subprocess liveness. Never blocks.
  $0 start-wait <region> [profile]
                                  start, block until ve login exits, verify.
                                  Needs a runtime that holds long tool sessions.
  $0 verify [profile]             Check the login landed. Never blocks.
                                  0 ok, 11 still running, 13 logged in but API
                                  unreachable, 10 ve gone without a session.
  $0 abort                        Kill the running ve and clean up.

Pass [profile] iff the conversation fixed a non-default profile.
USAGE
  exit 2
}

is_alive() {
  [[ -f "$pid_file" ]] && kill -0 "$(cat "$pid_file" 2>/dev/null)" 2>/dev/null
}

cleanup_state() {
  rm -f "$fifo" "$pid_file" "$log_file" "$url_file" "$start_file" "$replaced_marker"
}

# The device-code flow is identified by `--no-browser` in `ve login --help`.
# A ve without it is too old for this helper; the fix is to upgrade, not to
# fall back to an older flow.
check_login_supported() {
  local help
  help="$(ve login --help 2>&1 || true)"
  grep -q -- '--no-browser' <<<"$help"
}

extract_url() {
  # ve prints the verification URL on its own line. Skip any prefill line
  # (`...&user_code=...`) so URL stays the plain form.
  grep -oE 'https://signin\.volcengine\.com/[^[:space:]]+' "$log_file" 2>/dev/null \
    | grep -v 'user_code=' | head -1 || true
}

extract_prefill_url() {
  # ve prints "Alternatively, open the following URL to prefill the code:"
  # followed by verification_uri_complete when the server returns one.
  awk '/prefill the code/{f=1; next} f && /^https:\/\//{print; exit}' "$log_file" 2>/dev/null || true
}

extract_code() {
  # The first non-empty line after "Then enter the code:".
  awk '/Then enter the code:/{f=1; next} f && NF{print; exit}' "$log_file" 2>/dev/null || true
}

extract_expires_in() {
  grep -oE 'expires in [0-9]+ seconds' "$log_file" 2>/dev/null | grep -oE '[0-9]+' | head -1 || true
}

login_succeeded_in_log() {
  grep -q 'Successfully logged in' "$log_file" 2>/dev/null
}

# Writing to a fifo with `> "$fifo"` blocks until a reader appears. If ve has
# died the caller would hang forever, so open the fifo read+write instead —
# that never blocks — and let the buffered bytes wait for ve to pick them up.
write_fifo() {
  [[ -p "$fifo" ]] || return 1
  { printf '%s\n' "$1" >&4; } 4<>"$fifo" 2>/dev/null || return 1
  return 0
}

# `ve` asks `Replace the existing login_session? [y/N]:` when switching to a
# different account. Answer it once, whenever we notice it. Safe to call from
# any subcommand: the marker file makes it idempotent.
answer_replace_prompt() {
  [[ -f "$replaced_marker" ]] && return 0
  if grep -q 'Replace the existing login_session' "$log_file" 2>/dev/null; then
    write_fifo 'y' || true
    : > "$replaced_marker"
  fi
  return 0
}

# Print the KEY=value block. Returns 1 if the URL or the code is not in the
# log yet.
print_login_block() {
  local profile="${1:-}"
  local url code link expires prefill
  url="$(extract_url)"
  [[ -n "$url" ]] || return 1
  code="$(extract_code)"
  [[ -n "$code" ]] || return 1
  printf '%s\n' "$url" > "$url_file"

  prefill="$(extract_prefill_url)"
  if [[ -n "$prefill" ]]; then
    link="$prefill"
  elif [[ "$url" == *\?* ]]; then
    link="${url}&user_code=${code}"
  else
    link="${url}?user_code=${code}"
  fi
  expires="$(extract_expires_in)"
  echo "URL=${url}"
  echo "CODE=${code}"
  echo "LINK=${link}"
  echo "EXPIRES_IN=${expires:-unknown}"
  echo "NEXT=Send the user LINK (with URL and CODE as a fallback) and end the turn. Nothing comes back from the user. When they say they have authorized, run: $0 verify${profile:+ $profile}"
  return 0
}

cmd_start() {
  local region="${1:-}"
  local profile="${2:-}"
  if [[ -z "$region" ]]; then
    echo "ERROR: region required (e.g., cn-beijing)" >&2
    exit 2
  fi

  if is_alive; then
    echo "ERROR: ve login already running (PID $(cat "$pid_file")). Call '$0 abort' first." >&2
    exit 3
  fi

  # Clean any stale leftovers from a previous crashed run.
  cleanup_state

  if ! command -v ve >/dev/null 2>&1; then
    echo "ERROR: 've' command not found in PATH. Install with 'npm i -g @volcengine/cli' (or scripts/install_ve.sh)." >&2
    exit 4
  fi

  if ! check_login_supported; then
    echo "ERROR: this 've' has no device-code login ('ve login --help' lacks --no-browser). Upgrade with 'npm i -g @volcengine/cli@latest' (or scripts/install_ve.sh)." >&2
    exit 4
  fi

  mkfifo -m 600 "$fifo"

  # Open fifo read+write on fd 3 so the launcher does not block waiting for a
  # writer. Child ve inherits fd 0 from fd 3 via `<&3`, which keeps a writer
  # open on ve's own stdin — that is why ve never sees EOF and keeps waiting
  # after this launcher exits.
  exec 3<>"$fifo"

  # `--no-browser` always: this helper hands the link to a human who may be on
  # another machine, and letting ve pop a browser on the agent host is at best
  # useless and at worst hijacks the user's desktop session.
  #
  # `--lang en` always: ve follows the system locale (zh_CN prints Chinese),
  # and every anchor this script greps for — "Then enter the code:",
  # "expires in N seconds", "Successfully logged in", the login_session
  # replacement prompt — is English. The link/code handed to the user are
  # language-neutral, so pinning the language costs nothing.
  #
  # Detach ve into its own session (PPID 1) so it outlives this call being
  # killed and any process-group cleanup the runner performs. `3>&-` drops the
  # spare fifo descriptor; fd 0 still holds the read+write handle.
  local detach=()
  if command -v setsid >/dev/null 2>&1; then
    detach=(setsid)
  elif command -v perl >/dev/null 2>&1; then
    # macOS has no setsid(1) but always ships perl.
    detach=(perl -MPOSIX -e 'POSIX::setsid(); exec @ARGV or die "exec failed: $!\n";' --)
  fi
  # `${detach[@]+...}` keeps an empty array safe under `set -u` on bash 3.2.
  ${detach[@]+"${detach[@]}"} ve login --no-browser --lang en --region "$region" ${profile:+--profile "$profile"} <&3 3>&- >"$log_file" 2>&1 &
  local pid=$!
  echo "$pid" > "$pid_file"
  date +%s > "$start_file"

  # ve reads stdin exactly once, and only after the user has authorized: the
  # account-replacement prompt. Pre-answer it so ve never sits on that prompt
  # waiting for a `status`/`verify` call that may not come. (--region is always
  # passed, so the region prompt never consumes it.)
  write_fifo 'y' || true
  : > "$replaced_marker"

  # Poll the log for the URL and code and record them, so a later `url` call
  # can recover them even if this invocation never gets to return.
  local elapsed=0
  while (( elapsed < url_timeout )); do
    if print_login_block "$profile"; then
      return 0
    fi
    if ! kill -0 "$pid" 2>/dev/null; then
      echo "ERROR: ve login exited before printing URL. Log:" >&2
      cat "$log_file" >&2 || true
      cleanup_state
      exit 5
    fi
    sleep 1
    elapsed=$((elapsed + 1))
  done

  echo "ERROR: timeout (${url_timeout}s) waiting for URL. Log:" >&2
  cat "$log_file" >&2 || true
  kill "$pid" 2>/dev/null || true
  cleanup_state
  exit 6
}

cmd_url() {
  local profile="${1:-}"
  # A URL is only usable while its ve process lives: the device code that
  # matches it exists nowhere else. Never hand back a recorded URL whose
  # process has gone — that link is dead and the user cannot complete it.
  if ! is_alive; then
    echo "ERROR: no running ve login subprocess. Any previously recorded URL is dead" >&2
    echo "(its device code died with the process). Run '$0 start <region>' for a fresh URL." >&2
    exit 3
  fi
  if print_login_block "$profile"; then
    return 0
  fi
  echo "PENDING"
  exit 11
}

cmd_status() {
  if ! is_alive; then
    echo "DEAD: no running ve login subprocess."
    exit 3
  fi
  answer_replace_prompt
  local has_url="no" age="" note=""
  if [[ -n "$(extract_url)" ]]; then
    has_url="yes"
  fi
  if [[ -s "$start_file" ]]; then
    age=$(( $(date +%s) - $(cat "$start_file") ))
    local expires
    expires="$(extract_expires_in)"
    if [[ -n "$expires" ]] && (( age >= expires )); then
      note=" note=device-code-expired-run-abort-then-start"
    fi
  fi
  echo "ALIVE: pid=$(cat "$pid_file") url=${has_url}${age:+ age=${age}s}${note}"
}

cmd_start_wait() {
  local region="${1:-}"
  local profile="${2:-}"
  local pid

  cmd_start "$region" "$profile"
  pid=$(cat "$pid_file")

  # Managed command runners may kill background descendants when the
  # launching command returns. Keep this wrapper alive until completion.
  trap 'kill "$pid" 2>/dev/null || true; cleanup_state; exit 130' HUP INT TERM

  # ve is a child of this shell only via the detached launcher; `wait` cannot
  # see it, so poll. Answer the replacement prompt if it shows up meanwhile.
  while kill -0 "$pid" 2>/dev/null; do
    answer_replace_prompt
    sleep 2
  done
  trap - HUP INT TERM

  cmd_verify "$profile"
}

api_check() {
  local profile="${1:-}"
  ve sts GetCallerIdentity ${profile:+--profile "$profile"} 2>&1
}

cmd_verify() {
  local profile="${1:-}"
  local api_out
  # While ve is alive the login has, by definition, not landed: ve exits as
  # soon as it caches the session. Never consult the API at this point — on an
  # account switch the *old* session still answers GetCallerIdentity, and
  # treating that as success would kill the in-progress login and leave the
  # user on the wrong account without noticing.
  if is_alive; then
    # A login can be parked on the account-replacement prompt. Answer it here as
    # well as in `status` so the PENDING -> `verify` path never waits forever
    # on a `y` that nobody sends.
    answer_replace_prompt
    local age expires
    echo "PENDING: ve is still running; the login has not landed yet."
    expires="$(extract_expires_in)"
    if [[ -s "$start_file" ]]; then
      age=$(( $(date +%s) - $(cat "$start_file") ))
      if [[ -n "$expires" ]] && (( age >= expires )); then
        echo "The device code has passed its ${expires}s lifetime; ve will exit shortly. Run '$0 abort' then '$0 start <region>' for a fresh LINK."
      else
        echo "The user has not finished authorizing in the browser${expires:+ (code valid for ${expires}s, ${age}s elapsed)}. Ask whether they completed it, then re-run '$0 verify${profile:+ $profile}'."
      fi
    fi
    exit 11
  fi
  # ve is gone. Its own "Successfully logged in!" line is the authoritative
  # signal that *this* login (not some earlier session) wrote the profile; the
  # API call then only checks the result is usable from here.
  if login_succeeded_in_log; then
    if api_out="$(api_check "$profile")"; then
      echo "OK: ve login succeeded; GetCallerIdentity verified${profile:+ for profile '$profile'}."
      cleanup_state
      return 0
    fi
    echo "LOGGED_IN_UNVERIFIED: ve reported 'Successfully logged in!'${profile:+ for profile '$profile'}, but GetCallerIdentity failed:"
    printf '%s\n' "$api_out" | sed 's/^/  /'
    echo "This is a local network/proxy problem reaching open.volcengineapi.com, not a login failure. Do NOT restart the login; fix connectivity (e.g. proxy / NO_PROXY) and retry the API call."
    cleanup_state
    exit 13
  fi
  echo "ERROR: ve exited without a usable session${profile:+ for profile '$profile'}. Log:" >&2
  cat "$log_file" >&2 || true
  echo "Run '$0 abort' then '$0 start <region>' to issue a fresh URL." >&2
  exit 10
}

cmd_abort() {
  if is_alive; then
    local pid
    pid=$(cat "$pid_file")
    kill "$pid" 2>/dev/null || true
    # Give it a moment to die, then SIGKILL if still alive.
    local elapsed=0
    while kill -0 "$pid" 2>/dev/null && (( elapsed < 3 )); do
      sleep 1
      elapsed=$((elapsed + 1))
    done
    kill -9 "$pid" 2>/dev/null || true
  fi
  cleanup_state
  echo "OK: aborted and cleaned up."
}

case "${1:-}" in
  start)      shift; cmd_start "${1:-}" "${2:-}" ;;
  url)        shift; cmd_url "${1:-}" ;;
  status)     shift; cmd_status ;;
  start-wait) shift; cmd_start_wait "${1:-}" "${2:-}" ;;
  verify)     shift; cmd_verify "${1:-}" ;;
  abort)      shift; cmd_abort ;;
  complete)
    echo "ERROR: 'complete' was removed: the device-code login has no authorization code to feed back." >&2
    echo "The user authorizes in the browser; run '$0 verify [profile]' once they say they are done." >&2
    exit 2 ;;
  *)          usage ;;
esac
