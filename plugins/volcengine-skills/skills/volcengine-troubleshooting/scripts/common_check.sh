#!/usr/bin/env bash
# Local read-only environment checks for volcengine-troubleshooting.

echo "=== volcengine-troubleshooting: basic environment check ==="

missing_required_env=0
missing_required_bin=0
auth_check_failed=0

first_line() {
  local text="$1"
  printf '%s' "${text%%$'\n'*}"
}

for var in VOLCENGINE_ACCESS_KEY VOLCENGINE_SECRET_KEY VOLCENGINE_REGION; do
  if [ -z "${!var:-}" ]; then
    echo "[WARN] Missing required environment variable: ${var}"
    missing_required_env=1
  else
    echo "[OK] ${var} is set"
  fi
done

if [ -n "${VOLCENGINE_SESSION_TOKEN:-}" ]; then
  echo "[OK] VOLCENGINE_SESSION_TOKEN is set for temporary credentials"
else
  echo "[INFO] VOLCENGINE_SESSION_TOKEN is not set; this is fine for long-term AK/SK"
fi

for bin in ve tosutil python3; do
  if command -v "${bin}" >/dev/null 2>&1; then
    version="$(first_line "$("${bin}" --version 2>/dev/null)")"
    case "${version}" in
    *"operation not permitted"*|*"Operation not permitted"*)
      echo "[OK] ${bin} is available; version check returned a local permission warning"
      ;;
    *)
    if [ -n "${version}" ]; then
      echo "[OK] ${bin}: ${version}"
    else
      echo "[OK] ${bin} is available"
    fi
      ;;
    esac
  else
    echo "[ERROR] Required command not found: ${bin}"
    missing_required_bin=1
  fi
done

if python3 -c "import volcenginesdkcore" >/dev/null 2>&1; then
  echo "[OK] Python SDK import works: volcenginesdkcore (volcengine-python-sdk)"
elif python3 -c "import volcengine" >/dev/null 2>&1; then
  echo "[OK] Python SDK import works: volcengine (volc-sdk-python)"
else
  echo "[INFO] Python SDK import failed: volcenginesdkcore/volcengine; advanced SDK aggregation checks may be unavailable"
fi

if command -v ve >/dev/null 2>&1; then
  if [ "${missing_required_env}" -eq 0 ]; then
    if ve sts GetCallerIdentity >/dev/null 2>&1; then
      echo "[OK] ve authentication check passed: sts GetCallerIdentity"
    else
      echo "[WARN] ve authentication check failed: sts GetCallerIdentity"
      auth_check_failed=1
    fi
  else
    echo "[INFO] Skip ve authentication check until required environment variables are set"
  fi
fi

echo "=== check complete ==="

if [ "${missing_required_env}" -ne 0 ] || [ "${missing_required_bin}" -ne 0 ] || [ "${auth_check_failed}" -ne 0 ]; then
  exit 1
fi
