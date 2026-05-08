#!/usr/bin/env python3
"""Decide which publish/remediation lanes should continue after hosted validation."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STATE_FILE = REPO_ROOT / "targets" / "unified-pipeline-state.json"
DEFAULT_DIAGNOSIS_FILE = REPO_ROOT / "targets" / "clawhub-suspicious-diagnosis.json"
DEFAULT_BREAKOUT_FILE = REPO_ROOT / "targets" / "clawhub-breakout-variants.json"
DEFAULT_LIVE_STATUS_FILE = REPO_ROOT / "targets" / "clawhub-live-status.json"
DEFAULT_OWNER_HANDLES = ("baofeng-tech", "bibaofeng", "aisadocs")
GENERATED_RELEASE_PREFIXES = (
    "targetSkills/",
    "clawhub-release/",
    "clawhub-plugin-release/",
    "claude-release/",
    "claude-marketplace/",
    "hermes-release/",
    "agentskills-so-release/",
    "agentskill-sh-release/",
)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in str(value or "").split(",") if item.strip()]


def normalize_mode(value: str) -> str:
    normalized = str(value or "auto").strip().lower()
    if normalized in {"true", "1", "yes", "y", "on"}:
        return "true"
    if normalized in {"false", "0", "no", "n", "off", "none"}:
        return "false"
    return "auto"


def git_changed_paths() -> list[str]:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    paths: list[str] = []
    for line in result.stdout.splitlines():
        if len(line) < 4:
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.rsplit(" -> ", 1)[1].strip()
        if path:
            paths.append(path)
    return paths


def generated_release_dirty(paths: list[str]) -> bool:
    return any(path.startswith(GENERATED_RELEASE_PREFIXES) for path in paths)


def last_synced_skills(state: dict[str, Any]) -> list[str]:
    last_run = state.get("last_run")
    if not isinstance(last_run, dict):
        return []
    names: list[str] = []
    seen: set[str] = set()
    for field in ("synced_skills", "created_skills"):
        raw_names = last_run.get(field) or []
        if not isinstance(raw_names, list):
            continue
        for raw_name in raw_names:
            name = str(raw_name or "").strip()
            if name and name not in seen:
                seen.add(name)
                names.append(name)
    return names


def owned_suspicious_blockers(diagnosis: dict[str, Any], owner_handles: set[str]) -> list[str]:
    matched: list[str] = []
    for item in diagnosis.get("artifacts") or []:
        if not isinstance(item, dict):
            continue
        handle = str(item.get("publisher_handle") or "").strip().lstrip("@").lower()
        if handle not in owner_handles:
            continue
        if str(item.get("severity") or "") != "blocker":
            continue
        scan_status = str(item.get("scan_status") or "").strip().lower()
        suspicious = bool(item.get("suspicious")) or scan_status in {"suspicious", "malicious"}
        if suspicious:
            key = str(item.get("key") or "").strip()
            if key:
                matched.append(key)
    return matched


def live_status_by_key(live_status: dict[str, Any]) -> dict[str, dict[str, Any]]:
    by_key: dict[str, dict[str, Any]] = {}
    for item in live_status.get("artifacts") or []:
        if not isinstance(item, dict):
            continue
        key = str(item.get("key") or "").strip()
        if key:
            by_key[key] = item
    return by_key


def breakout_work_items(
    variants_payload: dict[str, Any],
    live_status: dict[str, Any],
    changed_sources: set[str],
) -> list[str]:
    variants = [item for item in variants_payload.get("variants") or [] if isinstance(item, dict)]
    live_items = live_status_by_key(live_status)
    has_live_snapshot = bool(live_items)
    work: list[str] = []
    seen: set[str] = set()

    for item in variants:
        source = str(item.get("source") or "").strip()
        slug = str(item.get("slug") or "").strip()
        if not slug:
            continue
        reason = ""
        if source and source in changed_sources:
            reason = f"{slug}: source {source} changed"
        elif has_live_snapshot:
            keys = (f"skill:{slug}", f"plugin:{slug}-plugin")
            for key in keys:
                live_item = live_items.get(key)
                if live_item is None:
                    reason = f"{slug}: missing live status for {key}"
                    break
                scan_status = str(live_item.get("scan_status") or "").strip().lower()
                if bool(live_item.get("suspicious")) or bool(live_item.get("pending")) or scan_status not in {"clean"}:
                    reason = f"{slug}: live scan is {scan_status or 'unresolved'}"
                    break
        if reason and slug not in seen:
            seen.add(slug)
            work.append(reason)
    return work


def resolve_request(mode: str, auto_value: bool, true_reason: str, false_reason: str, auto_reason: str) -> tuple[bool, str]:
    normalized = normalize_mode(mode)
    if normalized == "true":
        return True, true_reason
    if normalized == "false":
        return False, false_reason
    if auto_value:
        return True, auto_reason
    return False, auto_reason


def write_output(path: Path | None, values: dict[str, str]) -> None:
    lines = [f"{key}={value}" for key, value in values.items()]
    if path:
        with path.open("a", encoding="utf-8") as handle:
            for line in lines:
                handle.write(line + "\n")
    for line in lines:
        print(line)


def append_summary(path: Path | None, lines: list[str]) -> None:
    if not path:
        return
    with path.open("a", encoding="utf-8") as handle:
        for line in lines:
            handle.write(line + "\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Plan unified workflow continuation lanes.")
    parser.add_argument("--state-file", default=str(DEFAULT_STATE_FILE))
    parser.add_argument("--diagnosis-file", default=str(DEFAULT_DIAGNOSIS_FILE))
    parser.add_argument("--breakout-file", default=str(DEFAULT_BREAKOUT_FILE))
    parser.add_argument("--live-status-file", default=str(DEFAULT_LIVE_STATUS_FILE))
    parser.add_argument("--publish-mode", default="auto", help="auto, true, or false")
    parser.add_argument("--suspicious-mode", default="auto", help="auto, true, or false")
    parser.add_argument("--breakout-mode", default="auto", help="auto, true, or false")
    parser.add_argument("--owner-handles", default=",".join(DEFAULT_OWNER_HANDLES))
    parser.add_argument("--github-output", default=os.environ.get("GITHUB_OUTPUT", ""))
    parser.add_argument("--summary-file", default=os.environ.get("GITHUB_STEP_SUMMARY", ""))
    parser.add_argument(
        "--ignore-git-status",
        action="store_true",
        help="Ignore release-layer dirtiness when testing the planner.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    state = load_json(Path(args.state_file).resolve())
    diagnosis = load_json(Path(args.diagnosis_file).resolve())
    variants = load_json(Path(args.breakout_file).resolve())
    live_status = load_json(Path(args.live_status_file).resolve())

    changed_sources = set(last_synced_skills(state))
    changed_paths = [] if args.ignore_git_status else git_changed_paths()
    release_dirty = generated_release_dirty(changed_paths)
    owner_handles = {handle.lstrip("@").lower() for handle in split_csv(args.owner_handles)}

    publish_auto = bool(changed_sources or release_dirty)
    publish_detail = []
    if changed_sources:
        publish_detail.append(f"{len(changed_sources)} synced/created skill(s)")
    if release_dirty:
        publish_detail.append("generated release-layer changes are present")
    publish_reason_auto = "auto: " + (", ".join(publish_detail) if publish_detail else "no upstream or generated release changes")

    owned_blockers = owned_suspicious_blockers(diagnosis, owner_handles)
    suspicious_auto = bool(owned_blockers)
    suspicious_reason_auto = "auto: " + (
        f"{len(owned_blockers)} owned suspicious blocker(s): {', '.join(owned_blockers[:6])}"
        if owned_blockers
        else "no owned suspicious blockers after diagnosis"
    )

    breakout_items = breakout_work_items(variants, live_status, changed_sources)
    breakout_auto = bool(breakout_items)
    breakout_reason_auto = "auto: " + (
        "; ".join(breakout_items[:6]) if breakout_items else "no changed breakout source or live breakout scan issue"
    )

    publish_requested, publish_reason = resolve_request(
        args.publish_mode,
        publish_auto,
        "explicit true: publish continuation requested",
        "explicit false: publish continuation disabled",
        publish_reason_auto,
    )
    suspicious_requested, suspicious_reason = resolve_request(
        args.suspicious_mode,
        suspicious_auto,
        "explicit true: suspicious remediation requested",
        "explicit false: suspicious remediation disabled",
        suspicious_reason_auto,
    )
    breakout_requested, breakout_reason = resolve_request(
        args.breakout_mode,
        breakout_auto,
        "explicit true: breakout rollout requested",
        "explicit false: breakout rollout disabled",
        breakout_reason_auto,
    )
    any_requested = publish_requested or suspicious_requested or breakout_requested

    outputs = {
        "publish_requested": str(publish_requested).lower(),
        "suspicious_requested": str(suspicious_requested).lower(),
        "breakout_requested": str(breakout_requested).lower(),
        "any_requested": str(any_requested).lower(),
        "publish_reason": publish_reason,
        "suspicious_reason": suspicious_reason,
        "breakout_reason": breakout_reason,
        "synced_skill_count": str(len(changed_sources)),
        "owned_suspicious_blocker_count": str(len(owned_blockers)),
        "breakout_work_count": str(len(breakout_items)),
    }
    output_path = Path(args.github_output).resolve() if args.github_output else None
    write_output(output_path, outputs)

    summary_path = Path(args.summary_file).resolve() if args.summary_file else None
    append_summary(
        summary_path,
        [
            "### Continuation lane plan",
            "",
            f"- Publish lane requested: `{outputs['publish_requested']}`",
            f"- Publish reason: {publish_reason}",
            f"- Suspicious repair requested: `{outputs['suspicious_requested']}`",
            f"- Suspicious reason: {suspicious_reason}",
            f"- Breakout rollout requested: `{outputs['breakout_requested']}`",
            f"- Breakout reason: {breakout_reason}",
        ],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
