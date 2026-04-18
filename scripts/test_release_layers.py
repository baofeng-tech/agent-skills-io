#!/usr/bin/env python3
"""Validate generated Claude/Hermes release layers and run smoke tests."""

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
    timeout: int = 30,
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
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{mode}: failed to parse {skill_path.relative_to(REPO_ROOT)}: {exc}")
    return errors


def smoke_tests() -> list[dict[str, object]]:
    aisa_key = load_aisa_key()
    env = os.environ.copy()
    if aisa_key:
        env["AISA_API_KEY"] = aisa_key
    python_exe = os.environ.get("PYTHON_EXE") or shutil.which("python3.9") or shutil.which("python3") or "python3"

    tests = [
        ("claude", "aisa-twitter-command-center", [python_exe, "scripts/twitter_client.py", "search", "--query", "OpenAI", "--type", "Latest"]),
        ("claude", "aisa-youtube-serp-scout", [python_exe, "scripts/youtube_client.py", "search", "--query", "OpenAI"]),
        ("claude", "search", [python_exe, "scripts/search_client.py", "web", "--query", "OpenAI latest", "--count", "1"]),
        ("claude", "prediction-market", [python_exe, "scripts/prediction_market_client.py", "polymarket", "markets", "--limit", "1"]),
        ("claude", "stock-analysis", [python_exe, "scripts/analyze_stock.py", "AAPL", "--fast", "--output", "json"]),
        ("claude", "stock-watchlist", [python_exe, "scripts/watchlist.py", "list"]),
        ("claude", "stock-portfolio", [python_exe, "scripts/portfolio.py", "list"]),
        ("claude", "llm-router", [python_exe, "scripts/llm_router_client.py", "models"]),
        ("claude", "last30days", [python_exe, "scripts/test-aisa-provider.py"]),
        ("claude", "last30days-zh", [python_exe, "scripts/test-aisa-provider.py"]),
        ("hermes", "communication/aisa-twitter-command-center", [python_exe, "scripts/twitter_client.py", "search", "--query", "OpenAI", "--type", "Latest"]),
        ("hermes", "research/aisa-youtube-serp-scout", [python_exe, "scripts/youtube_client.py", "search", "--query", "OpenAI"]),
        ("hermes", "research/search", [python_exe, "scripts/search_client.py", "web", "--query", "OpenAI latest", "--count", "1"]),
        ("hermes", "finance/prediction-market", [python_exe, "scripts/prediction_market_client.py", "polymarket", "markets", "--limit", "1"]),
        ("hermes", "finance/stock-analysis", [python_exe, "scripts/analyze_stock.py", "AAPL", "--fast", "--output", "json"]),
        ("hermes", "finance/stock-watchlist", [python_exe, "scripts/watchlist.py", "list"]),
        ("hermes", "finance/stock-portfolio", [python_exe, "scripts/portfolio.py", "list"]),
        ("hermes", "ai/llm-router", [python_exe, "scripts/llm_router_client.py", "models"]),
    ]

    results: list[dict[str, object]] = []
    for layer, rel_path, cmd in tests:
        base_dir = CLAUDE_ROOT if layer == "claude" else HERMES_ROOT
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
    report: dict[str, object] = {
        "structure": {
            "claude_errors": validate_skill_tree(CLAUDE_ROOT, "claude"),
            "hermes_errors": validate_skill_tree(HERMES_ROOT, "hermes"),
        },
        "smoke_tests": smoke_tests(),
    }
    report_path = REPO_ROOT / "targets" / "release-layer-test-report-2026-04-17.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(report_path.relative_to(REPO_ROOT))


if __name__ == "__main__":
    main()
