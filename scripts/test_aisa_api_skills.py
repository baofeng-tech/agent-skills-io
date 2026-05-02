#!/usr/bin/env python3
"""Read-only regression checks for AISA-backed targetSkills."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET_ROOT = REPO_ROOT / "targetSkills"
DEFAULT_REPORT = REPO_ROOT / "targets" / "aisa-api-regression-report-2026-05-02.json"
ACCOUNTS_PATH = REPO_ROOT / "example" / "accounts"
API_MARKERS = ("AISA_API_KEY", "api.aisa.one")
PREVIEW_LIMIT = 6000
TRANSIENT_MARKERS = (
    "UNEXPECTED_EOF_WHILE_READING",
    "UND_ERR_CONNECT_TIMEOUT",
    "Connection reset",
    "Remote end closed connection",
    "Client network socket disconnected before secure TLS connection was established",
    "TypeError: fetch failed",
    "The read operation timed out",
    "timed out",
)


@dataclass
class CheckResult:
    skill: str
    kind: str
    command: list[str]
    code: int
    status: str
    application_error: bool
    attempts: int
    stdout_preview: str
    stderr_preview: str


def load_accounts_env(env: dict[str, str]) -> None:
    existing = (env.get("AISA_API_KEY") or "").strip()
    if existing:
        env["AISA_API_KEY"] = existing
        return
    if not ACCOUNTS_PATH.exists():
        return
    for line in ACCOUNTS_PATH.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        if key.strip() == "AISA_API_KEY" and value.strip():
            env["AISA_API_KEY"] = value.strip()
            return


def redact(text: str, env: dict[str, str]) -> str:
    api_key = (env.get("AISA_API_KEY") or "").strip()
    if api_key:
        text = text.replace(api_key, "***REDACTED_AISA_API_KEY***")
    return text


def is_text_file(path: Path) -> bool:
    try:
        path.read_text(encoding="utf-8")
        return True
    except UnicodeDecodeError:
        return False


def is_aisa_skill(skill_dir: Path) -> bool:
    for path in skill_dir.rglob("*"):
        if not path.is_file() or not is_text_file(path):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(marker in text for marker in API_MARKERS):
            return True
    return False


def discover_skills(names: list[str]) -> list[Path]:
    if names:
        return [TARGET_ROOT / name for name in names if (TARGET_ROOT / name / "SKILL.md").exists()]
    return [
        path
        for path in sorted(TARGET_ROOT.iterdir())
        if path.is_dir() and (path / "SKILL.md").exists() and is_aisa_skill(path)
    ]


def python_command(script_name: str) -> list[str] | None:
    commands = {
        "twitter_client.py": ["search", "--query", "OpenAI", "--type", "Latest"],
        "twitter_engagement_client.py": ["list-tweets", "--user", "OpenAI", "--limit", "1"],
        "twitter_oauth_client.py": ["--help"],
        "youtube_client.py": ["search", "--query", "OpenAI"],
        "search_client.py": ["web", "--query", "OpenAI", "--count", "1"],
        "perplexity_search_client.py": ["sonar", "--query", "Say OK."],
        "prediction_market_client.py": ["polymarket", "markets", "--limit", "1"],
        "market_client.py": ["stock", "prices", "--ticker", "AAPL", "--start", "2026-04-01", "--end", "2026-04-02"],
        "coingecko_client.py": ["simple", "price", "--ids", "bitcoin", "--vs", "usd"],
        "cn_llm_client.py": ["models"],
        "llm_router_client.py": ["models"],
        "media_gen_client.py": ["--help"],
        "analyze_stock.py": ["AAPL", "--output", "json", "--fast"],
        "dividends.py": ["AAPL", "--output", "json"],
        "hot_scanner.py": ["--focus", "stocks", "--output", "json"],
        "rumor_scanner.py": ["--focus", "analyst", "--output", "json"],
        "portfolio.py": ["list"],
        "stock_analyst.py": ["--ticker", "AAPL", "--depth", "quick", "--models", "gpt-4.1", "--json-only"],
        "arbitrage_finder.py": ["--help"],
        "last30days.py": ["OpenAI", "--quick", "--mock", "--emit", "json"],
    }
    return commands.get(script_name)


def python_executable(skill_dir: Path, script_name: str) -> str:
    if script_name == "last30days.py" and skill_dir.name.startswith("last30days"):
        return shutil.which("python3.12") or sys.executable
    return sys.executable


def command_specs(skill_dir: Path) -> list[tuple[str, list[str]]]:
    specs: list[tuple[str, list[str]]] = []
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.exists():
        return specs

    for path in sorted(scripts_dir.iterdir()):
        if not path.is_file():
            continue
        rel = path.relative_to(skill_dir).as_posix()
        if path.suffix == ".py":
            args = python_command(path.name)
            if args is not None:
                specs.append(("python", [python_executable(skill_dir, path.name), rel, *args]))
        elif path.name == "search.mjs":
            specs.append(("node", ["node", rel, "OpenAI", "-n", "1"]))
        elif path.name == "extract.mjs":
            specs.append(("node", ["node", rel, "https://example.com"]))
    return specs


def has_application_error(stdout: str, stderr: str) -> bool:
    combined = f"{stdout}\n{stderr}"
    hard_markers = (
        "Missing AISA_API_KEY",
        "Pre-deduction failed",
        "Insufficient credits",
        "API error",
        "Traceback (most recent call last)",
    )
    if any(marker in combined for marker in hard_markers):
        return True

    text = stdout.strip()
    if not text or text[0] not in "[{":
        return False
    try:
        payload: Any = json.loads(text)
    except json.JSONDecodeError:
        return False
    return payload_has_application_error(payload)


def payload_has_application_error(value: Any) -> bool:
    if isinstance(value, dict):
        if value.get("success") is False or value.get("ok") is False or value.get("error"):
            return True
        return any(payload_has_application_error(item) for item in value.values())
    if isinstance(value, list):
        return any(payload_has_application_error(item) for item in value)
    return False


def run_check(
    skill_dir: Path,
    kind: str,
    command: list[str],
    env: dict[str, str],
    timeout: int,
    retries: int,
) -> CheckResult:
    return run_check_with_retries(skill_dir, kind, command, env, timeout, retries=retries)


def is_transient_failure(stdout: str, stderr: str) -> bool:
    combined = f"{stdout}\n{stderr}"
    return any(marker in combined for marker in TRANSIENT_MARKERS)


def run_check_with_retries(
    skill_dir: Path,
    kind: str,
    command: list[str],
    env: dict[str, str],
    timeout: int,
    retries: int,
) -> CheckResult:
    attempts = 0
    last_result: subprocess.CompletedProcess[str] | None = None
    application_error = False
    status = "failed"
    while attempts <= retries:
        attempts += 1
        result = subprocess.run(
            command,
            cwd=str(skill_dir),
            env=env,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
        last_result = result
        application_error = has_application_error(result.stdout, result.stderr)
        status = "passed" if result.returncode == 0 and not application_error else "failed"
        if status == "passed" or not is_transient_failure(result.stdout, result.stderr):
            break
        if attempts <= retries:
            time.sleep(2)

    assert last_result is not None
    return CheckResult(
        skill=skill_dir.name,
        kind=kind,
        command=command,
        code=last_result.returncode,
        status=status,
        application_error=application_error,
        attempts=attempts,
        stdout_preview=redact(last_result.stdout, env)[:PREVIEW_LIMIT],
        stderr_preview=redact(last_result.stderr, env)[:PREVIEW_LIMIT],
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run read-only regression checks for AISA-backed targetSkills.")
    parser.add_argument("--skills", default="", help="Optional comma-separated skill names.")
    parser.add_argument("--report", default=str(DEFAULT_REPORT), help="JSON report path.")
    parser.add_argument("--timeout", type=int, default=120, help="Per-command timeout in seconds.")
    parser.add_argument("--retries", type=int, default=3, help="Retries for transient network failures.")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay in seconds between checks.")
    args = parser.parse_args()

    env = os.environ.copy()
    load_accounts_env(env)
    skill_names = [item.strip() for item in args.skills.split(",") if item.strip()]
    skills = discover_skills(skill_names)

    results: list[CheckResult] = []
    docs_only: list[str] = []
    for skill_dir in skills:
        specs = command_specs(skill_dir)
        if not specs:
            docs_only.append(skill_dir.name)
            continue
        for kind, command in specs:
            if results and args.delay > 0:
                time.sleep(args.delay)
            results.append(run_check(skill_dir, kind, command, env, args.timeout, args.retries))

    failures = [result for result in results if result.status != "passed"]
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "target_root": str(TARGET_ROOT.relative_to(REPO_ROOT)),
        "skill_count": len(skills),
        "docs_only_skills": docs_only,
        "check_count": len(results),
        "failure_count": len(failures),
        "results": [asdict(result) for result in results],
    }
    report_path = Path(args.report).resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"AISA API regression checked {len(skills)} skills with {len(results)} command(s).")
    print(f"Report: {report_path}")
    if docs_only:
        print(f"Docs-only skills: {', '.join(docs_only)}")
    if failures:
        print("Failures:")
        for failure in failures:
            print(f"  - {failure.skill}: {' '.join(failure.command)}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
