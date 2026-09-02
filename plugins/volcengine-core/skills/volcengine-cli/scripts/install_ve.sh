#!/bin/sh
# Copyright (c) 2026 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: MIT
#
# install_ve.sh — install the Volcengine CLI (`ve`) from the Volcengine CDN.
#
# Use this when `npm i -g @volcengine/cli` is not possible (no Node.js, npm
# registry unreachable, locked-down runner). It mirrors what the npm package's
# install.js does: pick the platform/arch archive, download it from the CDN,
# verify its SHA-256 against the published SHA256SUMS file, unpack, install,
# then run `ve skills update`.
#
#   curl -fsSL https://cloudcache.volccdn.com/ve/install.sh | sh
#   wget -qO- https://cloudcache.volccdn.com/ve/install.sh | sh
#
# Options (also settable through the environment):
#   --version <ver>        Install this version instead of the CDN "latest" file.
#                          Env: VE_VERSION
#   --install-dir <dir>    Where to put the `ve` binary. Default: /usr/local/bin
#                          when writable, otherwise ~/.local/bin. Never sudo.
#                          Env: VE_INSTALL_DIR
#   --dry-run              Resolve version/target/URLs and print them as
#                          KEY=value lines without downloading or installing.
#   -h, --help             Show this help.
#
# Environment:
#   VOLCENGINE_CLI_DOWNLOAD_BASE_URL   Base URL of the release files
#                                      (default https://cloudcache.volccdn.com/ve).
#                                      A plain directory path (no "://") is read
#                                      from the local filesystem — for mirrors
#                                      and tests.
#   VOLCENGINE_CLI_SKIP_SKILLS=1       Do not run `ve skills update` after install.
#
# Layout expected under the base URL (same as the npm installer):
#   latest                                            -> "1.1.5" or "v1.1.5"
#   v<ver>/volcengine-cli_<ver>_<os>_<arch>.zip
#   v<ver>/volcengine-cli_<ver>_SHA256SUMS            -> "<sha256>  <zip name>" lines
#
# Windows is not handled here; use `npm i -g @volcengine/cli` or the GitHub
# release page instead.

set -eu

DEFAULT_BASE_URL="https://cloudcache.volccdn.com/ve"
RELEASES_URL="https://github.com/volcengine/volcengine-cli/releases"

base_url="${VOLCENGINE_CLI_DOWNLOAD_BASE_URL:-$DEFAULT_BASE_URL}"
version="${VE_VERSION:-}"
install_dir="${VE_INSTALL_DIR:-}"
dry_run=0
tmp_dir=""

log() { printf '%s\n' "$*" >&2; }
die() { log "ERROR: $*"; exit 1; }
have() { command -v "$1" >/dev/null 2>&1; }

usage() {
  cat >&2 <<'USAGE'
Usage: install_ve.sh [--version <ver>] [--install-dir <dir>] [--dry-run]

  --version <ver>       Install this version instead of the CDN "latest" (env VE_VERSION)
  --install-dir <dir>   Target directory; default /usr/local/bin if writable, else ~/.local/bin (env VE_INSTALL_DIR)
  --dry-run             Print VERSION/OS/ARCH/ARCHIVE_URL/CHECKSUM_URL/INSTALL_DIR and exit

Env: VOLCENGINE_CLI_DOWNLOAD_BASE_URL (default https://cloudcache.volccdn.com/ve),
     VOLCENGINE_CLI_SKIP_SKILLS=1 to skip 've skills update'.
USAGE
  exit "${1:-0}"
}

while [ $# -gt 0 ]; do
  case "$1" in
    --version)
      [ $# -ge 2 ] || die "--version needs a value"
      version="$2"; shift 2 ;;
    --version=*) version="${1#--version=}"; shift ;;
    --install-dir)
      [ $# -ge 2 ] || die "--install-dir needs a value"
      install_dir="$2"; shift 2 ;;
    --install-dir=*) install_dir="${1#--install-dir=}"; shift ;;
    --dry-run) dry_run=1; shift ;;
    -h|--help) usage 0 ;;
    *) log "Unknown option: $1"; usage 2 ;;
  esac
done

# Strip trailing slashes so "$base_url/v1.2.3" never doubles a slash.
base_url="$(printf '%s' "$base_url" | sed 's:/*$::')"
[ -n "$base_url" ] || die "VOLCENGINE_CLI_DOWNLOAD_BASE_URL is empty"

cleanup() {
  if [ -n "$tmp_dir" ] && [ -d "$tmp_dir" ]; then
    rm -rf "$tmp_dir"
  fi
}
trap cleanup EXIT INT TERM HUP

# ---------------------------------------------------------------------------
# Transport: HTTP(S) via curl or wget; a local directory when the base URL has
# no scheme. Both fetch helpers print to stdout / write to a file and return
# non-zero on any failure (including HTTP errors).
# ---------------------------------------------------------------------------
is_local_base() {
  case "$base_url" in
    *://*) return 1 ;;
    *) return 0 ;;
  esac
}

fetch_to_file() {
  # $1 = URL or local path, $2 = destination file
  if is_local_base; then
    [ -f "$1" ] || return 1
    cp "$1" "$2"
  elif have curl; then
    curl -fsSL --retry 2 -o "$2" "$1"
  elif have wget; then
    wget -q -O "$2" "$1"
  else
    die "need curl or wget to download $1"
  fi
}

fetch_to_stdout() {
  if is_local_base; then
    [ -f "$1" ] || return 1
    cat "$1"
  elif have curl; then
    curl -fsSL --retry 2 "$1"
  elif have wget; then
    wget -q -O - "$1"
  else
    die "need curl or wget to download $1"
  fi
}

# ---------------------------------------------------------------------------
# Target detection (same matrix as the npm installer's SUPPORTED_TARGETS).
# ---------------------------------------------------------------------------
detect_os() {
  case "$(uname -s)" in
    Darwin) echo darwin ;;
    Linux) echo linux ;;
    FreeBSD) echo freebsd ;;
    MINGW*|MSYS*|CYGWIN*|Windows_NT)
      die "Windows is not supported by this installer. Use 'npm i -g @volcengine/cli' or download from $RELEASES_URL" ;;
    *) die "Unsupported operating system: $(uname -s)" ;;
  esac
}

detect_arch() {
  case "$(uname -m)" in
    x86_64|amd64) echo amd64 ;;
    aarch64|arm64) echo arm64 ;;
    i386|i486|i586|i686|x86) echo 386 ;;
    armv6l|armv7l|armv7|arm) echo arm ;;
    *) die "Unsupported CPU architecture: $(uname -m)" ;;
  esac
}

check_target_supported() {
  # $1 = os, $2 = arch
  case "$1/$2" in
    darwin/amd64|darwin/arm64) return 0 ;;
    linux/amd64|linux/386|linux/arm|linux/arm64) return 0 ;;
    freebsd/amd64|freebsd/386|freebsd/arm|freebsd/arm64) return 0 ;;
    *) die "No Volcengine CLI build for $1/$2. See $RELEASES_URL" ;;
  esac
}

# ---------------------------------------------------------------------------
# Version resolution: --version / VE_VERSION wins; otherwise read "<base>/latest".
# Accepts "1.1.5" or "v1.1.5"; anything else is rejected rather than guessed.
# ---------------------------------------------------------------------------
normalize_version() {
  v="$(printf '%s' "$1" | tr -d '[:space:]')"
  v="${v#v}"
  case "$v" in
    [0-9]*.[0-9]*.[0-9]*) printf '%s' "$v" ;;
    *) return 1 ;;
  esac
}

resolve_version() {
  if [ -n "$version" ]; then
    normalize_version "$version" || die "Invalid version '$version' (expected e.g. 1.1.5)"
    return
  fi
  latest_raw="$(fetch_to_stdout "$base_url/latest" 2>/dev/null)" \
    || die "Cannot read $base_url/latest. Pass --version <ver>, or install with 'npm i -g @volcengine/cli', or download from $RELEASES_URL"
  latest_line="$(printf '%s\n' "$latest_raw" | sed -n '1p')"
  normalize_version "$latest_line" || die "Unexpected content in $base_url/latest: '$latest_line'"
}

# ---------------------------------------------------------------------------
# Checksum
# ---------------------------------------------------------------------------
sha256_file() {
  if have sha256sum; then
    sha256sum "$1" | awk '{print $1}'
  elif have shasum; then
    shasum -a 256 "$1" | awk '{print $1}'
  elif have openssl; then
    openssl dgst -sha256 "$1" | awk '{print $NF}'
  else
    die "need sha256sum, shasum, or openssl to verify the download"
  fi
}

# Print the expected hash for archive $2 from SHA256SUMS file $1.
# Lines look like "<hex>  <name>" or "<hex> *<name>"; the name may carry a path.
expected_sha256() {
  awk -v want="$2" '
    NF >= 2 && length($1) == 64 && $1 ~ /^[0-9A-Fa-f]+$/ {
      name = $2
      sub(/^\*/, "", name)
      n = split(name, parts, "/")
      if (name == want || parts[n] == want) { print tolower($1); exit }
    }' "$1"
}

# ---------------------------------------------------------------------------
# Install location: never sudo. /usr/local/bin only if we can already write
# there; otherwise ~/.local/bin.
# ---------------------------------------------------------------------------
choose_install_dir() {
  if [ -n "$install_dir" ]; then
    printf '%s' "$install_dir"
  elif [ -d /usr/local/bin ] && [ -w /usr/local/bin ]; then
    printf '%s' /usr/local/bin
  else
    printf '%s' "${HOME:?HOME is not set}/.local/bin"
  fi
}

path_contains() {
  case ":${PATH:-}:" in
    *":$1:"*) return 0 ;;
    *) return 1 ;;
  esac
}

extract_archive() {
  # $1 = zip path, $2 = destination dir
  if have unzip; then
    unzip -o -q "$1" -d "$2"
  elif have python3; then
    python3 -c 'import sys, zipfile; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])' "$1" "$2"
  else
    die "need unzip or python3 to extract $1"
  fi
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
os="$(detect_os)"
arch="$(detect_arch)"
check_target_supported "$os" "$arch"
ver="$(resolve_version)"

archive_name="volcengine-cli_${ver}_${os}_${arch}.zip"
sums_name="volcengine-cli_${ver}_SHA256SUMS"
archive_url="$base_url/v$ver/$archive_name"
sums_url="$base_url/v$ver/$sums_name"
target_dir="$(choose_install_dir)"

if [ "$dry_run" -eq 1 ]; then
  printf 'VERSION=%s\n' "$ver"
  printf 'OS=%s\n' "$os"
  printf 'ARCH=%s\n' "$arch"
  printf 'ARCHIVE_URL=%s\n' "$archive_url"
  printf 'CHECKSUM_URL=%s\n' "$sums_url"
  printf 'INSTALL_DIR=%s\n' "$target_dir"
  exit 0
fi

tmp_dir="$(mktemp -d 2>/dev/null || mktemp -d -t ve-install)"
archive_path="$tmp_dir/$archive_name"
sums_path="$tmp_dir/$sums_name"

log "Downloading $archive_name ..."
fetch_to_file "$archive_url" "$archive_path" \
  || die "Download failed: $archive_url. Please download Volcengine CLI from $RELEASES_URL"
fetch_to_file "$sums_url" "$sums_path" \
  || die "Checksum file not found: $sums_url. Refusing to install an unverified binary; download from $RELEASES_URL"

expected="$(expected_sha256 "$sums_path" "$archive_name")"
[ -n "$expected" ] || die "No entry for $archive_name in $sums_url. Refusing to install an unverified binary."
actual="$(sha256_file "$archive_path")"
if [ "$expected" != "$actual" ]; then
  die "Checksum mismatch for $archive_name: expected $expected, got $actual. The download may have been tampered with. Download from $RELEASES_URL"
fi
log "Checksum OK."

extract_dir="$tmp_dir/extract"
mkdir -p "$extract_dir"
extract_archive "$archive_path" "$extract_dir"
binary="$extract_dir/ve"
if [ ! -f "$binary" ]; then
  binary="$(find "$extract_dir" -type f -name ve | head -n 1)"
fi
[ -n "$binary" ] && [ -f "$binary" ] || die "'ve' binary not found inside $archive_name"

mkdir -p "$target_dir" || die "Cannot create $target_dir (set VE_INSTALL_DIR to a writable directory)"
[ -w "$target_dir" ] || die "$target_dir is not writable (set VE_INSTALL_DIR to a writable directory; this installer never uses sudo)"

# Stage next to the destination, prove the staged binary runs and reports the
# expected version, and only then rename over the old `ve`. A broken download
# must never replace a working install.
staged="$target_dir/.ve.install.$$"
cp "$binary" "$staged"
chmod 755 "$staged"
if [ "$os" = "darwin" ] && have xattr; then
  xattr -d com.apple.quarantine "$staged" 2>/dev/null || true
fi
if ! reported="$("$staged" --version </dev/null 2>&1)"; then
  rm -f "$staged"
  die "the downloaded ve does not run on this host ($os/$arch): $reported. Existing install left untouched."
fi
case "$reported" in
  *"$ver"*) : ;;
  *)
    rm -f "$staged"
    die "the downloaded ve reports '$reported', not $ver. Existing install left untouched." ;;
esac
mv -f "$staged" "$target_dir/ve"

log "Volcengine CLI v$ver installed to $target_dir/ve ($os/$arch)"

if ! path_contains "$target_dir"; then
  log "NOTE: $target_dir is not in PATH. Add it, e.g.:"
  log "  export PATH=\"$target_dir:\$PATH\""
fi

if [ "${VOLCENGINE_CLI_SKIP_SKILLS:-}" != "1" ]; then
  if ! "$target_dir/ve" skills update </dev/null; then
    log "Volcengine CLI installed, but Skill installation was skipped. Run 've skills update' to retry."
  fi
fi
