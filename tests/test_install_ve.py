"""Tests for skills/core/volcengine-cli/scripts/install_ve.sh.

The installer is exercised end to end against a local "CDN" directory
(VOLCENGINE_CLI_DOWNLOAD_BASE_URL without a scheme), a fake `uname` placed
ahead in PATH, and a throwaway install directory. No network is used.
"""

from __future__ import annotations

import hashlib
import os
import stat
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "core" / "volcengine-cli" / "scripts" / "install_ve.sh"


def parse_kv(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            result[key] = value
    return result


class InstallVeHarness(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.cdn = self.root / "cdn"
        self.cdn.mkdir()
        self.fake_bin = self.root / "fakebin"
        self.fake_bin.mkdir()
        self.install_dir = self.root / "install"
        self.home = self.root / "home"
        self.home.mkdir()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def fake_uname(self, system: str, machine: str) -> None:
        script = self.fake_bin / "uname"
        script.write_text(
            "#!/bin/sh\n"
            f'case "$1" in -s) echo "{system}" ;; -m) echo "{machine}" ;; *) echo "{system}" ;; esac\n',
            encoding="utf-8",
        )
        script.chmod(script.stat().st_mode | stat.S_IXUSR)

    def publish_release(self, version: str, os_name: str, arch: str, *, corrupt_sum: bool = False,
                        omit_sum_entry: bool = False, binary_body: str | None = None) -> str:
        release_dir = self.cdn / f"v{version}"
        release_dir.mkdir(parents=True, exist_ok=True)
        archive_name = f"volcengine-cli_{version}_{os_name}_{arch}.zip"
        archive_path = release_dir / archive_name
        body = binary_body if binary_body is not None else f'#!/bin/sh\necho "fake ve {version}"\n'
        with zipfile.ZipFile(archive_path, "w") as zf:
            info = zipfile.ZipInfo("ve")
            info.external_attr = 0o755 << 16
            zf.writestr(info, body)
        digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
        if corrupt_sum:
            digest = "0" * 64
        lines = [f"{'f' * 64}  volcengine-cli_{version}_other_arch.zip"]
        if not omit_sum_entry:
            lines.append(f"{digest}  {archive_name}")
        (release_dir / f"volcengine-cli_{version}_SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")
        return archive_name

    def run_installer(self, *args: str, env_extra: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        env = {
            "PATH": f"{self.fake_bin}{os.pathsep}{os.environ.get('PATH', '')}",
            "HOME": str(self.home),
            "VOLCENGINE_CLI_DOWNLOAD_BASE_URL": str(self.cdn),
            "VOLCENGINE_CLI_SKIP_SKILLS": "1",
            "VE_INSTALL_DIR": str(self.install_dir),
        }
        if env_extra:
            env.update(env_extra)
        return subprocess.run(
            ["sh", str(SCRIPT), *args],
            capture_output=True,
            text=True,
            env=env,
            timeout=60,
        )


class DryRunResolutionTest(InstallVeHarness):
    def test_linux_x86_64_maps_to_amd64(self) -> None:
        self.fake_uname("Linux", "x86_64")
        result = self.run_installer("--dry-run", "--version", "1.1.5")
        self.assertEqual(result.returncode, 0, result.stderr)
        kv = parse_kv(result.stdout)
        self.assertEqual(kv["VERSION"], "1.1.5")
        self.assertEqual(kv["OS"], "linux")
        self.assertEqual(kv["ARCH"], "amd64")
        self.assertEqual(kv["ARCHIVE_URL"], f"{self.cdn}/v1.1.5/volcengine-cli_1.1.5_linux_amd64.zip")
        self.assertEqual(kv["CHECKSUM_URL"], f"{self.cdn}/v1.1.5/volcengine-cli_1.1.5_SHA256SUMS")
        self.assertEqual(kv["INSTALL_DIR"], str(self.install_dir))

    def test_darwin_arm64_maps_to_arm64(self) -> None:
        self.fake_uname("Darwin", "arm64")
        result = self.run_installer("--dry-run", "--version", "v1.1.5")
        self.assertEqual(result.returncode, 0, result.stderr)
        kv = parse_kv(result.stdout)
        self.assertEqual((kv["OS"], kv["ARCH"], kv["VERSION"]), ("darwin", "arm64", "1.1.5"))

    def test_linux_i686_maps_to_386(self) -> None:
        self.fake_uname("Linux", "i686")
        result = self.run_installer("--dry-run", "--version", "1.1.5")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(parse_kv(result.stdout)["ARCH"], "386")

    def test_darwin_386_is_rejected(self) -> None:
        self.fake_uname("Darwin", "i686")
        result = self.run_installer("--dry-run", "--version", "1.1.5")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("No Volcengine CLI build for darwin/386", result.stderr)

    def test_windows_points_to_npm(self) -> None:
        self.fake_uname("MINGW64_NT-10.0", "x86_64")
        result = self.run_installer("--dry-run", "--version", "1.1.5")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("npm i -g @volcengine/cli", result.stderr)

    def test_latest_file_with_v_prefix_and_newline(self) -> None:
        self.fake_uname("Linux", "aarch64")
        (self.cdn / "latest").write_text("v1.2.3\n", encoding="utf-8")
        result = self.run_installer("--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        kv = parse_kv(result.stdout)
        self.assertEqual(kv["VERSION"], "1.2.3")
        self.assertTrue(kv["ARCHIVE_URL"].endswith("/v1.2.3/volcengine-cli_1.2.3_linux_arm64.zip"))

    def test_latest_file_garbage_is_rejected(self) -> None:
        self.fake_uname("Linux", "x86_64")
        (self.cdn / "latest").write_text("<html>oops</html>\n", encoding="utf-8")
        result = self.run_installer("--dry-run")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unexpected content", result.stderr)

    def test_missing_latest_file_asks_for_version(self) -> None:
        self.fake_uname("Linux", "x86_64")
        result = self.run_installer("--dry-run")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--version", result.stderr)

    def test_invalid_explicit_version_is_rejected(self) -> None:
        self.fake_uname("Linux", "x86_64")
        result = self.run_installer("--dry-run", "--version", "latest")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Invalid version", result.stderr)

    def test_env_version_and_trailing_slash_base_url(self) -> None:
        self.fake_uname("FreeBSD", "amd64")
        result = self.run_installer(
            "--dry-run",
            env_extra={"VE_VERSION": "1.1.5", "VOLCENGINE_CLI_DOWNLOAD_BASE_URL": f"{self.cdn}///"},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        kv = parse_kv(result.stdout)
        self.assertEqual(kv["OS"], "freebsd")
        self.assertEqual(kv["ARCHIVE_URL"], f"{self.cdn}/v1.1.5/volcengine-cli_1.1.5_freebsd_amd64.zip")

    def test_default_install_dir_falls_back_to_home_local_bin(self) -> None:
        self.fake_uname("Linux", "x86_64")
        env = {"VE_INSTALL_DIR": ""}
        result = self.run_installer("--dry-run", "--version", "1.1.5", env_extra=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        install_dir = parse_kv(result.stdout)["INSTALL_DIR"]
        self.assertIn(install_dir, {"/usr/local/bin", str(self.home / ".local" / "bin")})
        if install_dir == "/usr/local/bin":
            self.assertTrue(os.access("/usr/local/bin", os.W_OK))


class InstallFlowTest(InstallVeHarness):
    def test_install_from_local_cdn(self) -> None:
        self.fake_uname("Linux", "x86_64")
        self.publish_release("1.1.5", "linux", "amd64")
        result = self.run_installer("--version", "1.1.5")
        self.assertEqual(result.returncode, 0, result.stderr)
        binary = self.install_dir / "ve"
        self.assertTrue(binary.is_file())
        self.assertTrue(os.access(binary, os.X_OK))
        self.assertEqual(subprocess.run([str(binary), "--version"], capture_output=True, text=True).stdout.strip(), "fake ve 1.1.5")
        self.assertIn("Checksum OK", result.stderr)
        self.assertIn("not in PATH", result.stderr)
        self.assertFalse(list(self.install_dir.glob(".ve.install.*")), "staging file must not be left behind")

    def test_install_uses_latest_when_no_version_given(self) -> None:
        self.fake_uname("Linux", "aarch64")
        (self.cdn / "latest").write_text("1.1.5", encoding="utf-8")
        self.publish_release("1.1.5", "linux", "arm64")
        result = self.run_installer()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.install_dir / "ve").is_file())

    def test_install_replaces_existing_binary(self) -> None:
        self.fake_uname("Linux", "x86_64")
        self.install_dir.mkdir()
        (self.install_dir / "ve").write_text("#!/bin/sh\necho old\n", encoding="utf-8")
        self.publish_release("1.1.6", "linux", "amd64")
        result = self.run_installer("--version", "1.1.6")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("fake ve 1.1.6", (self.install_dir / "ve").read_text(encoding="utf-8"))

    def test_broken_binary_never_replaces_existing_ve(self) -> None:
        self.fake_uname("Linux", "x86_64")
        self.install_dir.mkdir()
        (self.install_dir / "ve").write_text("#!/bin/sh\necho old-ve 1.1.4\n", encoding="utf-8")
        self.publish_release("1.1.5", "linux", "amd64", binary_body="this is not an executable program\n")
        result = self.run_installer("--version", "1.1.5")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not run on this host", result.stderr)
        self.assertIn("old-ve 1.1.4", (self.install_dir / "ve").read_text(encoding="utf-8"))
        self.assertFalse(list(self.install_dir.glob(".ve.install.*")), "staging file must be removed")

    def test_version_mismatch_never_replaces_existing_ve(self) -> None:
        self.fake_uname("Linux", "x86_64")
        self.install_dir.mkdir()
        (self.install_dir / "ve").write_text("#!/bin/sh\necho old-ve 1.1.4\n", encoding="utf-8")
        self.publish_release("1.1.5", "linux", "amd64", binary_body="#!/bin/sh\necho 9.9.9\n")
        result = self.run_installer("--version", "1.1.5")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not 1.1.5", result.stderr)
        self.assertIn("old-ve 1.1.4", (self.install_dir / "ve").read_text(encoding="utf-8"))

    def test_checksum_mismatch_aborts_without_installing(self) -> None:
        self.fake_uname("Linux", "x86_64")
        self.publish_release("1.1.5", "linux", "amd64", corrupt_sum=True)
        result = self.run_installer("--version", "1.1.5")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Checksum mismatch", result.stderr)
        self.assertFalse((self.install_dir / "ve").exists())

    def test_missing_checksum_entry_aborts(self) -> None:
        self.fake_uname("Linux", "x86_64")
        self.publish_release("1.1.5", "linux", "amd64", omit_sum_entry=True)
        result = self.run_installer("--version", "1.1.5")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("No entry for volcengine-cli_1.1.5_linux_amd64.zip", result.stderr)
        self.assertFalse((self.install_dir / "ve").exists())

    def test_missing_checksum_file_aborts(self) -> None:
        self.fake_uname("Linux", "x86_64")
        self.publish_release("1.1.5", "linux", "amd64")
        (self.cdn / "v1.1.5" / "volcengine-cli_1.1.5_SHA256SUMS").unlink()
        result = self.run_installer("--version", "1.1.5")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Checksum file not found", result.stderr)
        self.assertFalse((self.install_dir / "ve").exists())

    def test_missing_archive_reports_download_failure(self) -> None:
        self.fake_uname("Linux", "x86_64")
        result = self.run_installer("--version", "9.9.9")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Download failed", result.stderr)

    def test_archive_without_ve_binary_is_rejected(self) -> None:
        self.fake_uname("Linux", "x86_64")
        release_dir = self.cdn / "v1.1.5"
        release_dir.mkdir()
        archive = release_dir / "volcengine-cli_1.1.5_linux_amd64.zip"
        with zipfile.ZipFile(archive, "w") as zf:
            zf.writestr("README", "no binary here")
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        (release_dir / "volcengine-cli_1.1.5_SHA256SUMS").write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
        result = self.run_installer("--version", "1.1.5")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("'ve' binary not found", result.stderr)
        self.assertFalse((self.install_dir / "ve").exists())

    def test_unwritable_install_dir_never_sudoes(self) -> None:
        if os.geteuid() == 0:
            self.skipTest("root can write anywhere")
        self.fake_uname("Linux", "x86_64")
        self.publish_release("1.1.5", "linux", "amd64")
        locked = self.root / "locked"
        locked.mkdir()
        locked.chmod(0o555)
        try:
            result = self.run_installer("--version", "1.1.5", env_extra={"VE_INSTALL_DIR": str(locked)})
        finally:
            locked.chmod(0o755)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not writable", result.stderr)
        self.assertNotIn("sudo ", result.stdout)

    def test_help_does_not_need_script_path(self) -> None:
        # `curl ... | sh` runs with $0 == "sh"; help must still print.
        result = subprocess.run(["sh", "-s", "--", "--help"], input=SCRIPT.read_text(encoding="utf-8"),
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--dry-run", result.stderr)


if __name__ == "__main__":
    unittest.main()
