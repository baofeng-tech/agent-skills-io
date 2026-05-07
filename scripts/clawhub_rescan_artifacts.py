#!/usr/bin/env python3
"""Request ClawHub rescans for selected live skill/plugin artifacts."""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ACCOUNTS_FILE = REPO_ROOT / "example" / "accounts"
DEFAULT_CONFIG_ROOT = REPO_ROOT / ".tmp-clawhub-auth" / "rescan"
DEFAULT_REPORT_FILE = REPO_ROOT / "targets" / "clawhub-rescan-artifacts.json"
TOKEN_KEY_PATTERN = re.compile(r"^clawhubapitoken(?P<index>\d*)$")
AUTH_FAILURE_PATTERNS = (
    re.compile(r"not\s+logged\s+in", re.IGNORECASE),
    re.compile(r"unauthori[sz]ed", re.IGNORECASE),
    re.compile(r"forbidden", re.IGNORECASE),
    re.compile(r"\b401\b"),
    re.compile(r"\b403\b"),
    re.compile(r"owner", re.IGNORECASE),
)


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in str(value or "").split(",") if item.strip()]


def normalize_key(raw: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", raw.lower())


def token_sort_key(key: str) -> tuple[int, str]:
    match = TOKEN_KEY_PATTERN.match(key)
    if not match:
        return (sys.maxsize, key)
    raw_index = match.group("index")
    return (int(raw_index) if raw_index else 1, key)


def parse_accounts_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        separator = "=" if "=" in line else ":" if ":" in line else None
        if not separator:
            continue
        key, value = line.split(separator, 1)
        key = key.strip()
        value = value.strip()
        if key and value:
            values[normalize_key(key)] = value
    return values


def extract_account_tokens(account_values: dict[str, str]) -> list[str]:
    return [
        account_values[key]
        for key in sorted(account_values, key=token_sort_key)
        if TOKEN_KEY_PATTERN.match(key)
    ]


def resolve_tokens(args: argparse.Namespace) -> list[str]:
    tokens: list[str] = []
    seen: set[str] = set()

    def add(token: str | None) -> None:
        if not token:
            return
        token = token.strip()
        if not token or token in seen:
            return
        seen.add(token)
        tokens.append(token)

    for token in args.token or []:
        add(token)

    env_tokens: list[tuple[int, str]] = []
    for env_name, value in os.environ.items():
        if not value:
            continue
        if env_name == "CLAWHUB_TOKEN":
            env_tokens.append((1, value))
            continue
        match = re.fullmatch(r"CLAWHUB_TOKEN_(\d+)", env_name)
        if match:
            env_tokens.append((int(match.group(1)), value))
    for _index, value in sorted(env_tokens, key=lambda item: item[0]):
        add(value)

    if args.accounts_file:
        for token in extract_account_tokens(parse_accounts_file(Path(args.accounts_file))):
            add(token)
    return tokens


def run_command(
    args: list[str],
    *,
    env: dict[str, str] | None = None,
    cwd: Path = REPO_ROOT,
    timeout: int = 120,
) -> subprocess.CompletedProcess[str]:
    if args and args[0] == "clawhub":
        clawhub_command = os.environ.get("CLAWHUB_COMMAND", "").strip()
        if clawhub_command:
            args = [*shlex.split(clawhub_command), *args[1:]]
        else:
            clawhub_bin = (
                os.environ.get("CLAWHUB_BIN", "").strip()
                or shutil.which("clawhub")
                or shutil.which("clawhub.cmd")
                or shutil.which("clawhub.exe")
            )
            if clawhub_bin:
                if os.name == "nt" and clawhub_bin.lower().endswith((".cmd", ".bat")):
                    args = ["cmd.exe", "/c", clawhub_bin, *args[1:]]
                else:
                    args = [clawhub_bin, *args[1:]]
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(
        args,
        cwd=str(cwd),
        env=merged_env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def parse_json_from_output(text: str) -> Any | None:
    stripped = text.strip()
    if not stripped:
        return None
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start >= 0 and end > start:
        try:
            return json.loads(stripped[start : end + 1])
        except json.JSONDecodeError:
            return None
    return None


def normalize_artifact_key(raw: str) -> tuple[str, str]:
    text = raw.strip()
    if ":" not in text:
        raise ValueError(f"Artifact key must be kind:name, got {raw!r}")
    kind, name = text.split(":", 1)
    kind = kind.strip().lower()
    name = name.strip()
    if kind not in {"skill", "plugin"} or not name:
        raise ValueError(f"Artifact key must be skill:<slug> or plugin:<name>, got {raw!r}")
    return kind, name


def auth_env_for_slot(config_root: Path, slot: int) -> dict[str, str]:
    config_path = config_root / f"token-{slot}.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    return {"CLAWHUB_CONFIG_PATH": str(config_path)}


def login_token(token: str, *, slot: int, config_root: Path, timeout: int) -> tuple[bool, str]:
    env = auth_env_for_slot(config_root, slot)
    try:
        result = run_command(["clawhub", "login", "--token", token, "--no-browser"], env=env, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, f"ClawHub login timed out for token-{slot}."
    if result.returncode != 0:
        return False, (result.stderr.strip() or result.stdout.strip() or "login failed")
    whoami = run_command(["clawhub", "whoami"], env=env, timeout=timeout)
    actor = whoami.stdout.strip() if whoami.returncode == 0 else f"token-{slot}"
    return True, actor


def classify_rescan_failure(message: str) -> str:
    lowered = message.lower()
    if "already in progress" in lowered:
        return "already_in_progress"
    if "rescan request limit reached" in lowered or "limit reached" in lowered:
        return "limit_reached"
    if "not found" in lowered or "404" in lowered:
        return "not_found"
    if any(pattern.search(message) for pattern in AUTH_FAILURE_PATTERNS):
        return "auth_failed"
    return "failed"


def request_rescan_with_token(kind: str, name: str, *, slot: int, config_root: Path, timeout: int) -> dict[str, Any]:
    env = auth_env_for_slot(config_root, slot)
    if kind == "skill":
        command = ["clawhub", "skill", "rescan", name, "--yes", "--json"]
    else:
        command = ["clawhub", "package", "rescan", name, "--yes", "--json"]
    result = run_command(command, env=env, timeout=timeout)
    output = "\n".join(part for part in (result.stdout, result.stderr) if part).strip()
    payload = parse_json_from_output(output)
    if result.returncode == 0:
        return {
            "status": "requested",
            "token_slot": f"token-{slot}",
            "message": "rescan requested",
            "response": payload,
        }
    status = classify_rescan_failure(output)
    return {
        "status": status,
        "token_slot": f"token-{slot}",
        "message": output[:1000],
        "response": payload,
    }


def inspect_artifact(kind: str, name: str, *, timeout: int) -> dict[str, Any]:
    if kind == "skill":
        command = ["clawhub", "inspect", name, "--json"]
    else:
        command = ["clawhub", "package", "inspect", name, "--json"]
    result = run_command(command, timeout=timeout)
    payload = parse_json_from_output(result.stdout)
    if result.returncode != 0 or not isinstance(payload, dict):
        return {
            "status": "inspect_failed",
            "message": (result.stderr.strip() or result.stdout.strip())[:1000],
        }
    if kind == "skill":
        moderation = payload.get("moderation")
        if isinstance(moderation, dict):
            verdict = str(moderation.get("verdict") or "").lower()
            if moderation.get("isSuspicious") or verdict in {"suspicious", "malicious", "review"}:
                return {"status": verdict or "suspicious", "raw": moderation}
        return {"status": "clean", "raw": moderation}
    package = payload.get("package") if isinstance(payload.get("package"), dict) else {}
    status = str(package.get("scanStatus") or "").lower() or "unknown"
    return {"status": status, "raw": {"scanStatus": package.get("scanStatus"), "latestVersion": package.get("latestVersion")}}


def request_rescan(kind: str, name: str, tokens: list[str], *, config_root: Path, timeout: int) -> dict[str, Any]:
    auth_failures: list[dict[str, Any]] = []
    for slot, token in enumerate(tokens, start=1):
        login_ok, actor = login_token(token, slot=slot, config_root=config_root, timeout=timeout)
        if not login_ok:
            auth_failures.append({"token_slot": f"token-{slot}", "message": actor[:300]})
            continue
        result = request_rescan_with_token(kind, name, slot=slot, config_root=config_root, timeout=timeout)
        result["actor"] = actor
        if result["status"] in {"auth_failed"}:
            auth_failures.append(result)
            continue
        if auth_failures:
            result["auth_attempts_before_success"] = len(auth_failures)
        return result
    return {
        "status": "auth_failed",
        "message": "No configured ClawHub token could request a rescan for this artifact.",
        "auth_failures": auth_failures,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Request ClawHub security rescans before remediation.")
    parser.add_argument("--artifacts", default="", help="Comma-separated artifact keys.")
    parser.add_argument("--artifact", action="append", default=[], help="Repeatable artifact key.")
    parser.add_argument("--accounts-file", default=str(DEFAULT_ACCOUNTS_FILE), help="Optional ClawHub token file.")
    parser.add_argument("--token", action="append", default=[], help="Explicit ClawHub token. Repeatable.")
    parser.add_argument("--config-root", default=str(DEFAULT_CONFIG_ROOT), help="Per-token ClawHub config directory.")
    parser.add_argument("--report-file", default=str(DEFAULT_REPORT_FILE), help="Where to write rescan results.")
    parser.add_argument("--wait-seconds", type=int, default=0, help="Optional delay before final inspect.")
    parser.add_argument("--poll-interval", type=int, default=30, help="Polling interval used during wait.")
    parser.add_argument("--timeout", type=int, default=120, help="Per-command timeout in seconds.")
    parser.add_argument("--inspect-after", action="store_true", help="Inspect artifacts after requesting rescans.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    raw_keys = [*split_csv(args.artifacts), *args.artifact]
    artifact_keys = [key for key in raw_keys if str(key).strip()]
    if not artifact_keys:
        raise SystemExit("No artifacts supplied.")
    tokens = resolve_tokens(args)
    if not tokens:
        raise SystemExit("No ClawHub tokens found. Provide --token, CLAWHUB_TOKEN*, or example/accounts.")

    config_root = Path(args.config_root).resolve()
    results: list[dict[str, Any]] = []
    for artifact_key in artifact_keys:
        kind, name = normalize_artifact_key(artifact_key)
        print(f"Requesting rescan for {artifact_key}", flush=True)
        result = request_rescan(kind, name, tokens, config_root=config_root, timeout=args.timeout)
        results.append({"key": artifact_key, "kind": kind, "name": name, "rescan": result})
        print(f"  {result.get('status')}", flush=True)

    if args.inspect_after and args.wait_seconds > 0:
        deadline = time.monotonic() + args.wait_seconds
        while time.monotonic() < deadline:
            remaining = max(0, int(deadline - time.monotonic()))
            print(f"Waiting for ClawHub scan updates ({remaining}s remaining)", flush=True)
            time.sleep(min(max(args.poll_interval, 1), remaining or 1))

    if args.inspect_after:
        for item in results:
            item["post_rescan_inspect"] = inspect_artifact(item["kind"], item["name"], timeout=args.timeout)

    report = {
        "summary": {
            "artifacts": len(results),
            "requested": sum(1 for item in results if item.get("rescan", {}).get("status") == "requested"),
            "already_in_progress": sum(
                1 for item in results if item.get("rescan", {}).get("status") == "already_in_progress"
            ),
            "limit_reached": sum(1 for item in results if item.get("rescan", {}).get("status") == "limit_reached"),
            "failed": sum(
                1
                for item in results
                if item.get("rescan", {}).get("status") not in {"requested", "already_in_progress", "limit_reached"}
            ),
        },
        "artifacts": results,
    }
    report_path = Path(args.report_file).resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {report_path.relative_to(REPO_ROOT) if report_path.is_relative_to(REPO_ROOT) else report_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
