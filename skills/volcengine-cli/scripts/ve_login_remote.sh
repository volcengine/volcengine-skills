#!/usr/bin/env bash
# Copyright (c) 2026 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: MIT
# ve_login_remote.sh — orchestrate `ve login --remote` across multiple tool
# invocations in agent contexts (OpenClaw, Feishu bots, etc.).
#
# Why this script exists:
#   `ve login --remote` prints a cross-device OAuth URL, then waits for the
#   user to paste back the "Authorization code" shown in the browser. In
#   agent contexts each tool call is a fresh shell, so the agent cannot
#   keep `ve` alive across the URL-print -> user-replies-with-code gap.
#   This script bridges that gap with a named pipe (fifo) bound to ve's
#   stdin: `start` launches ve in background and prints the URL, `complete`
#   writes the code into the fifo so the still-running ve picks it up.
#
# Subcommands:
#   start <region> [profile]
#                      Launch `ve login --remote --region <region>` and
#                      print the login URL to stdout. Pass [profile] when
#                      the conversation has fixed a non-default profile —
#                      otherwise the login lands on `default` and the
#                      fixed profile stays broken.
#   complete <code> [profile]
#                      Feed <code> to the waiting ve subprocess via fifo,
#                      then verify with `ve sts GetCallerIdentity`. Pass
#                      the same [profile] as start so the verification
#                      hits the profile that was just logged in.
#   abort              Kill the running ve subprocess and clean up state.
#
# State files (one set per UID for multi-user safety on shared hosts):
#   /tmp/ve_login_<uid>.fifo   fifo bound to ve's stdin
#   /tmp/ve_login_<uid>.pid    PID of running `ve login --remote`
#   /tmp/ve_login_<uid>.log    Captured stdout+stderr of ve

set -euo pipefail

uid_tag="$(id -u)"
fifo="/tmp/ve_login_${uid_tag}.fifo"
pid_file="/tmp/ve_login_${uid_tag}.pid"
log_file="/tmp/ve_login_${uid_tag}.log"
url_timeout=30        # seconds to wait for ve to print the URL
complete_timeout=120  # seconds to wait for ve to exit after code is fed

usage() {
  cat <<EOF >&2
Usage:
  $0 start <region> [profile]     Launch ve login --remote; print the URL.
  $0 complete <code> [profile]    Feed authorization code to the running
                                  ve; verify. Same [profile] as start.
  $0 abort                        Kill the running ve and clean up.

Pass [profile] iff the conversation fixed a non-default profile.
EOF
  exit 2
}

is_alive() {
  [[ -f "$pid_file" ]] && kill -0 "$(cat "$pid_file" 2>/dev/null)" 2>/dev/null
}

cleanup_state() {
  rm -f "$fifo" "$pid_file" "$log_file"
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
    echo "ERROR: 've' command not found in PATH. Install with 'npm i -g @volcengine/cli'." >&2
    exit 4
  fi

  mkfifo -m 600 "$fifo"

  # Open fifo read+write on fd 3 so the launcher does not block waiting
  # for a writer. Child ve inherits fd 0 from fd 3 via `<&3`.
  exec 3<>"$fifo"

  # Launch ve in background; capture stdout+stderr. `ve login` is a CLI
  # management command, so --profile takes two hyphens.
  ve login --remote --region "$region" ${profile:+--profile "$profile"} <&3 >"$log_file" 2>&1 &
  local pid=$!
  echo "$pid" > "$pid_file"

  # Parent shell will close fd 3 on exit; ve keeps its own inherited copy.
  # Poll the log for the OAuth URL.
  local elapsed=0
  while (( elapsed < url_timeout )); do
    if [[ -s "$log_file" ]]; then
      local url
      url=$(grep -oE 'https://signin\.volcengine\.com/[^[:space:]]+' "$log_file" 2>/dev/null | head -1 || true)
      if [[ -n "$url" ]]; then
        printf '%s\n' "$url"
        return 0
      fi
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

cmd_complete() {
  local code="${1:-}"
  local profile="${2:-}"
  if [[ -z "$code" ]]; then
    echo "ERROR: authorization code required" >&2
    exit 2
  fi

  if ! is_alive; then
    echo "ERROR: no running ve login subprocess. Call '$0 start <region>' first." >&2
    exit 3
  fi

  local pid
  pid=$(cat "$pid_file")

  # Write the authorization code to the fifo.
  if ! printf '%s\n' "$code" > "$fifo"; then
    echo "ERROR: failed to write code to fifo ($fifo)" >&2
    exit 7
  fi

  # Wait for ve to exit. We cannot `wait` because ve is not a child of
  # this fresh shell — fall back to kill -0 polling.
  # While waiting, watch for the "Replace the existing login_session?" prompt
  # that appears when switching to a different account, and auto-confirm with "y".
  local replied_replace=false
  local elapsed=0
  while kill -0 "$pid" 2>/dev/null; do
    if (( elapsed >= complete_timeout )); then
      echo "ERROR: timeout (${complete_timeout}s) waiting for ve to exit after code submission. Log:" >&2
      cat "$log_file" >&2 || true
      exit 8
    fi
    # Auto-confirm session replacement if prompted.
    if [[ "$replied_replace" == false ]] && grep -q 'Replace the existing login_session' "$log_file" 2>/dev/null; then
      printf 'y\n' > "$fifo" 2>/dev/null || true
      replied_replace=true
    fi
    sleep 1
    elapsed=$((elapsed + 1))
  done

  # Heuristic error check on captured log.
  if grep -qiE 'invalid|expired|error|fail' "$log_file" 2>/dev/null; then
    echo "ERROR: ve login finished with possible errors. Log:" >&2
    cat "$log_file" >&2 || true
    cleanup_state
    exit 9
  fi

  cleanup_state

  # Verify the profile that was just logged in is now usable. Ordinary
  # service API calls address profiles with a three-hyphen flag.
  if ve sts GetCallerIdentity ${profile:+---profile "$profile"} >/dev/null 2>&1; then
    echo "OK: ve login succeeded; GetCallerIdentity verified${profile:+ for profile '$profile'}."
    return 0
  else
    echo "ERROR: GetCallerIdentity failed after login. Try 've sts GetCallerIdentity${profile:+ ---profile $profile}' manually." >&2
    exit 10
  fi
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
  start)    shift; cmd_start "${1:-}" "${2:-}" ;;
  complete) shift; cmd_complete "${1:-}" "${2:-}" ;;
  abort)    shift; cmd_abort ;;
  *)        usage ;;
esac
