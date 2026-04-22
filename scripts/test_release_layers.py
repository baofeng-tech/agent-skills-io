#!/usr/bin/env python3
"""Validate generated Claude/Hermes/ClawHub release layers and run smoke tests."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
CLAUDE_ROOT = REPO_ROOT / "claude-release"
HERMES_ROOT = REPO_ROOT / "hermes-release"
CLAWHUB_ROOT = REPO_ROOT / "clawhub-release"
CLAWHUB_PLUGIN_ROOT = REPO_ROOT / "clawhub-plugin-release"
AGENTSKILLS_SO_ROOT = REPO_ROOT / "agentskills-so-release"
AGENTSKILL_SH_ROOT = REPO_ROOT / "agentskill-sh-release"
ACCOUNTS_PATH = REPO_ROOT / "example" / "accounts"


BANNED_NAMES = {"__pycache__", "compare.sh", "sync.sh", "test-v1-vs-v2.sh", "run-tests.sh"}


def load_aisa_key() -> str | None:
    env_key = os.environ.get("AISA_API_KEY")
    if env_key:
        return env_key
    text = ACCOUNTS_PATH.read_text(encoding="utf-8")
    match = re.search(r"(sk-[A-Za-z0-9]+)", text)
    return match.group(1) if match else None


def run(
    cmd: list[str],
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    timeout: int = 120,
) -> tuple[int, str, str]:
    proc = subprocess.Popen(
        cmd,
        cwd=str(cwd) if cwd else None,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
        return proc.returncode, stdout, stderr
    except subprocess.TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()
        return 124, stdout or "", (stderr or "") + "\nTimeoutExpired"


def validate_skill_tree(root: Path, mode: str) -> list[str]:
    errors: list[str] = []
    for path in root.rglob("*"):
        if path.name in BANNED_NAMES:
            errors.append(f"{mode}: banned file remained: {path.relative_to(REPO_ROOT)}")
    for skill_path in root.rglob("SKILL.md"):
        try:
            text = skill_path.read_text(encoding="utf-8")
            parts = text.split("---", 2)
            if len(parts) < 3:
                errors.append(f"{mode}: missing frontmatter fence in {skill_path.relative_to(REPO_ROOT)}")
                continue
            frontmatter = yaml.safe_load(parts[1]) or {}
            if "name" not in frontmatter or "description" not in frontmatter:
                errors.append(f"{mode}: missing name/description in {skill_path.relative_to(REPO_ROOT)}")
            if mode == "hermes":
                hermes = (((frontmatter.get("metadata") or {}).get("hermes")) or {})
                if not hermes.get("tags"):
                    errors.append(f"{mode}: missing metadata.hermes.tags in {skill_path.relative_to(REPO_ROOT)}")
            if mode == "clawhub":
                metadata = frontmatter.get("metadata") or {}
                if "aisa" not in metadata:
                    errors.append(f"{mode}: missing metadata.aisa in {skill_path.relative_to(REPO_ROOT)}")
                if frontmatter.get("primaryEnv") and "requires" not in frontmatter:
                    errors.append(f"{mode}: primaryEnv without requires in {skill_path.relative_to(REPO_ROOT)}")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{mode}: failed to parse {skill_path.relative_to(REPO_ROOT)}: {exc}")
    return errors


def validate_agentskills_so_tree(root: Path) -> list[str]:
    errors = validate_skill_tree(root, "agentskills-so")
    for skill_path in root.glob("*/SKILL.md"):
        try:
            text = skill_path.read_text(encoding="utf-8")
            parts = text.split("---", 2)
            if len(parts) < 3:
                continue
            frontmatter = yaml.safe_load(parts[1]) or {}
            metadata = frontmatter.get("metadata") or {}
            if any(isinstance(value, dict) for value in metadata.values()):
                errors.append(f"agentskills-so: nested metadata remained in {skill_path.relative_to(REPO_ROOT)}")
            if "compatibility" not in frontmatter:
                errors.append(f"agentskills-so: missing compatibility in {skill_path.relative_to(REPO_ROOT)}")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"agentskills-so: failed to parse {skill_path.relative_to(REPO_ROOT)}: {exc}")
    return errors


def validate_agentskill_sh_tree(root: Path) -> list[str]:
    errors = validate_agentskills_so_tree(root)
    normalized: list[str] = []
    for error in errors:
        normalized.append(error.replace("agentskills-so", "agentskill-sh"))
    return normalized


def validate_clawhub_plugin_tree(root: Path) -> list[str]:
    errors: list[str] = []
    plugin_root = root / "plugins"
    zip_root = root / "zips"
    plugin_dirs = sorted(path for path in plugin_root.iterdir() if path.is_dir()) if plugin_root.exists() else []
    zip_files = sorted(zip_root.glob("*.zip")) if zip_root.exists() else []

    if not plugin_root.exists():
        errors.append("clawhub-plugin: missing plugins/ directory")
        return errors
    if not zip_root.exists():
        errors.append("clawhub-plugin: missing zips/ directory")
        return errors

    if len(plugin_dirs) != len(zip_files):
        errors.append("clawhub-plugin: plugin directory count does not match zip count")

    for plugin_dir in plugin_dirs:
        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        openclaw_manifest_path = plugin_dir / "openclaw.plugin.json"
        package_path = plugin_dir / "package.json"
        entry_path = plugin_dir / "index.ts"
        readme_path = plugin_dir / "README.md"
        expected_zip = zip_root / f"{plugin_dir.name}.zip"
        if not manifest_path.exists():
            errors.append(f"clawhub-plugin: missing Claude bundle manifest in {plugin_dir.relative_to(REPO_ROOT)}")
        if not openclaw_manifest_path.exists():
            errors.append(f"clawhub-plugin: missing openclaw.plugin.json in {plugin_dir.relative_to(REPO_ROOT)}")
        if not package_path.exists():
            errors.append(f"clawhub-plugin: missing package.json in {plugin_dir.relative_to(REPO_ROOT)}")
        if not entry_path.exists():
            errors.append(f"clawhub-plugin: missing index.ts in {plugin_dir.relative_to(REPO_ROOT)}")
        if not readme_path.exists():
            errors.append(f"clawhub-plugin: missing README.md in {plugin_dir.relative_to(REPO_ROOT)}")
        if not expected_zip.exists():
            errors.append(f"clawhub-plugin: missing zip for {plugin_dir.relative_to(REPO_ROOT)}")
        embedded_skills = list((plugin_dir / "skills").glob("*/SKILL.md")) if (plugin_dir / "skills").exists() else []
        if len(embedded_skills) != 1:
            errors.append(f"clawhub-plugin: expected 1 embedded skill in {plugin_dir.relative_to(REPO_ROOT)}, got {len(embedded_skills)}")
        try:
            if openclaw_manifest_path.exists():
                manifest = json.loads(openclaw_manifest_path.read_text(encoding="utf-8"))
                if "configSchema" not in manifest:
                    errors.append(f"clawhub-plugin: missing configSchema in {openclaw_manifest_path.relative_to(REPO_ROOT)}")
                if "skills" not in manifest:
                    errors.append(f"clawhub-plugin: missing skills roots in {openclaw_manifest_path.relative_to(REPO_ROOT)}")
            if package_path.exists():
                package = json.loads(package_path.read_text(encoding="utf-8"))
                openclaw_block = package.get("openclaw") if isinstance(package, dict) else None
                if not isinstance(openclaw_block, dict):
                    errors.append(f"clawhub-plugin: missing openclaw block in {package_path.relative_to(REPO_ROOT)}")
                elif "extensions" not in openclaw_block:
                    errors.append(f"clawhub-plugin: missing openclaw.extensions in {package_path.relative_to(REPO_ROOT)}")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"clawhub-plugin: failed to parse manifests in {plugin_dir.relative_to(REPO_ROOT)}: {exc}")
    return errors


def remove_pycache_dirs(root: Path) -> None:
    for path in sorted(root.rglob("__pycache__"), reverse=True):
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)


def smoke_tests() -> list[dict[str, object]]:
    aisa_key = load_aisa_key()
    env = os.environ.copy()
    if aisa_key:
        env["AISA_API_KEY"] = aisa_key
    python_exe = (
        os.environ.get("PYTHON_EXE")
        or shutil.which("python3.12")
        or ("/usr/local/python3.12/bin/python3.12" if Path("/usr/local/python3.12/bin/python3.12").exists() else None)
        or shutil.which("python3.9")
        or shutil.which("python3")
        or "python3"
    )

    def maybe_with_api_key(cmd: list[str], *, explicit: bool = False) -> list[str]:
        if explicit and aisa_key:
            insert_at = 2 if len(cmd) >= 2 and cmd[1].endswith(".py") else len(cmd)
            return [*cmd[:insert_at], "--api-key", aisa_key, *cmd[insert_at:]]
        return cmd

    tests = [
        ("claude", "aisa-twitter-command-center", [python_exe, "scripts/twitter_client.py", "search", "--query", "OpenAI", "--type", "Latest"]),
        ("claude", "aisa-youtube-serp-scout", [python_exe, "scripts/youtube_client.py", "search", "--query", "OpenAI"]),
        ("claude", "search", [python_exe, "scripts/search_client.py", "web", "--query", "OpenAI latest", "--count", "1"]),
        ("claude", "prediction-market", [python_exe, "scripts/prediction_market_client.py", "polymarket", "markets", "--limit", "1"]),
        ("claude", "llm-router", [python_exe, "scripts/llm_router_client.py", "models"]),
        ("claude", "last30days", [python_exe, "scripts/last30days.py", "--help"]),
        ("claude", "last30days-zh", [python_exe, "scripts/last30days.py", "--help"]),
        ("hermes", "communication/aisa-twitter-command-center", maybe_with_api_key([python_exe, "scripts/twitter_client.py", "search", "--query", "OpenAI", "--type", "Latest"], explicit=True)),
        ("hermes", "research/aisa-youtube-serp-scout", maybe_with_api_key([python_exe, "scripts/youtube_client.py", "search", "--query", "OpenAI"], explicit=True)),
        ("hermes", "research/search", maybe_with_api_key([python_exe, "scripts/search_client.py", "web", "--query", "OpenAI latest", "--count", "1"], explicit=True)),
        ("hermes", "finance/prediction-market", maybe_with_api_key([python_exe, "scripts/prediction_market_client.py", "polymarket", "markets", "--limit", "1"], explicit=True)),
        ("hermes", "ai/llm-router", maybe_with_api_key([python_exe, "scripts/llm_router_client.py", "models"], explicit=True)),
        ("hermes", "communication/last30days", [python_exe, "scripts/last30days.py", "--help"]),
        ("clawhub", "aisa-twitter-command-center", [python_exe, "scripts/twitter_client.py", "search", "--query", "OpenAI", "--type", "Latest"]),
        ("clawhub", "aisa-youtube-serp-scout", [python_exe, "scripts/youtube_client.py", "search", "--query", "OpenAI"]),
        ("clawhub", "search", [python_exe, "scripts/search_client.py", "web", "--query", "OpenAI latest", "--count", "1"]),
        ("clawhub", "prediction-market", [python_exe, "scripts/prediction_market_client.py", "polymarket", "markets", "--limit", "1"]),
        ("clawhub", "last30days", [python_exe, "scripts/last30days.py", "--help"]),
    ]

    results: list[dict[str, object]] = []
    for layer, rel_path, cmd in tests:
        if layer == "claude":
            base_dir = CLAUDE_ROOT
        elif layer == "hermes":
            base_dir = HERMES_ROOT
        else:
            base_dir = CLAWHUB_ROOT
        cwd = base_dir / rel_path
        code, stdout, stderr = run(cmd, cwd=cwd, env=env)
        results.append(
            {
                "layer": layer,
                "path": rel_path,
                "command": cmd,
                "code": code,
                "stdout_preview": stdout[:400],
                "stderr_preview": stderr[:400],
            }
        )
    return results


def main() -> None:
    for root in (CLAUDE_ROOT, HERMES_ROOT, CLAWHUB_ROOT, AGENTSKILLS_SO_ROOT, AGENTSKILL_SH_ROOT):
        remove_pycache_dirs(root)
    report: dict[str, object] = {
        "structure": {
            "claude_errors": validate_skill_tree(CLAUDE_ROOT, "claude"),
            "hermes_errors": validate_skill_tree(HERMES_ROOT, "hermes"),
            "clawhub_errors": validate_skill_tree(CLAWHUB_ROOT, "clawhub"),
            "clawhub_plugin_errors": validate_clawhub_plugin_tree(CLAWHUB_PLUGIN_ROOT),
            "agentskills_so_errors": validate_agentskills_so_tree(AGENTSKILLS_SO_ROOT),
            "agentskill_sh_errors": validate_agentskill_sh_tree(AGENTSKILL_SH_ROOT),
        },
        "smoke_tests": smoke_tests(),
    }
    report_path = REPO_ROOT / "targets" / "release-layer-test-report-2026-04-17.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(report_path.relative_to(REPO_ROOT))


if __name__ == "__main__":
    main()
