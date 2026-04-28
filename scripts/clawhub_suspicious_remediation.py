#!/usr/bin/env python3
"""Diagnose, minimally remediate, and optionally republish suspicious ClawHub artifacts."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DIAGNOSIS_FILE = REPO_ROOT / "targets" / "clawhub-suspicious-diagnosis.json"
DEFAULT_REPORT_FILE = REPO_ROOT / "targets" / "clawhub-suspicious-remediation.json"
DEFAULT_REPO_SKILL_SYNC = [
    "python3",
    "scripts/sync_codex_repo_skills.py",
    "--if-available",
]
FULL_BUILD_STEPS = [
    ["python3", "scripts/normalize_target_skills.py"],
    ["python3", "scripts/build_targetskills_catalog.py"],
    ["python3", "scripts/build_clawhub_release.py"],
    ["python3", "scripts/build_clawhub_plugin_release.py"],
]
TEST_STEP = ["python3", "scripts/test_release_layers.py"]
ADJACENT_SYNC_STEPS = [
    ["bash", "scripts/publish-targetSkills-to-agent-skills.sh"],
    ["bash", "scripts/publish-agentskills-so-release.sh", "--skip-build"],
    ["bash", "scripts/publish-agentskill-sh-release.sh", "--skip-build"],
    ["bash", "scripts/publish-claude-release.sh", "--with-marketplace", "--skip-build"],
    ["bash", "scripts/publish-hermes-release.sh", "--skip-build"],
]


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in str(value or "").split(",") if item.strip()]


def run_command(
    args: list[str],
    *,
    timeout: int = 3600,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        args,
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(args)}")
    return result


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def matches_status(item: dict[str, Any], status: str) -> bool:
    if status == "any":
        return True
    if status == "pending":
        return bool(item.get("pending"))
    if status == "suspicious":
        return bool(item.get("suspicious")) or str(item.get("scan_status") or "").lower() in {"suspicious", "malicious"}
    return False


def matches_contains(item: dict[str, Any], contains_tokens: list[str]) -> bool:
    if not contains_tokens:
        return True
    haystack = " ".join(
        [
            str(item.get("key") or ""),
            str(item.get("kind") or ""),
            str(item.get("name") or ""),
            str(item.get("local_path") or ""),
            str(item.get("reason") or ""),
            " ".join(str(value) for value in (item.get("rule_ids") or [])),
        ]
    ).lower()
    return any(token.lower() in haystack for token in contains_tokens)


def select_artifacts(
    payload: dict[str, Any],
    *,
    exact_keys: list[str],
    contains_tokens: list[str],
    severity: str,
    status: str,
) -> list[dict[str, Any]]:
    requested = [key for key in exact_keys if key]
    requested_set = set(requested)
    matched: list[dict[str, Any]] = []
    seen: set[str] = set()

    for item in payload.get("artifacts") or []:
        if not isinstance(item, dict):
            continue
        key = str(item.get("key") or "").strip()
        if not key or key in seen:
            continue
        if severity != "all" and str(item.get("severity") or "") != severity:
            continue
        if not matches_status(item, status):
            continue
        if requested_set and key not in requested_set:
            continue
        if not matches_contains(item, contains_tokens):
            continue
        seen.add(key)
        matched.append(item)

    if requested:
        order = {key: index for index, key in enumerate(requested)}
        matched.sort(key=lambda item: order.get(str(item.get("key") or ""), len(order)))
    else:
        matched.sort(key=lambda item: (str(item.get("kind") or ""), str(item.get("name") or "")))
    return matched


def normalize_local_path(raw: str) -> Path:
    text = str(raw or "").strip().replace("\\", "/")
    path = Path(text)
    if path.is_absolute():
        return path
    return (REPO_ROOT / path).resolve()


def resolve_source_skill(item: dict[str, Any]) -> str | None:
    kind = str(item.get("kind") or "").strip()
    name = str(item.get("name") or "").strip()

    if kind == "skill" and name:
        return name

    local_path = normalize_local_path(str(item.get("local_path") or ""))
    if local_path.exists():
        embedded = sorted(path.parent.name for path in local_path.glob("skills/*/SKILL.md"))
        if embedded:
            return embedded[0]

    if kind == "plugin" and name.endswith("-plugin"):
        return name[: -len("-plugin")]
    return name or None


def resolve_source_skills(items: list[dict[str, Any]]) -> list[str]:
    names: list[str] = []
    seen: set[str] = set()
    for item in items:
        name = resolve_source_skill(item)
        if not name or name in seen:
            continue
        skill_dir = REPO_ROOT / "targetSkills" / name
        if skill_dir.exists():
            seen.add(name)
            names.append(name)
    return names


def build_report(items: list[dict[str, Any]], source_skills: list[str]) -> dict[str, Any]:
    return {
        "summary": {
            "artifacts": len(items),
            "source_skills": len(source_skills),
            "artifact_keys": [str(item.get("key") or "") for item in items],
            "source_skill_names": source_skills,
        },
        "artifacts": [
            {
                "key": item.get("key"),
                "kind": item.get("kind"),
                "name": item.get("name"),
                "severity": item.get("severity"),
                "scan_status": item.get("scan_status"),
                "rule_ids": item.get("rule_ids") or [],
                "reason": item.get("reason"),
                "local_path": item.get("local_path"),
            }
            for item in items
        ],
    }


def run_builds(*, skip_build: bool, skip_test: bool) -> None:
    if not skip_build:
        for command in FULL_BUILD_STEPS:
            run_command(command, timeout=7200)
    if not skip_test:
        run_command(TEST_STEP, timeout=7200)


def run_adjacent_sync() -> None:
    for command in ADJACENT_SYNC_STEPS:
        run_command(command, timeout=7200)


def run_targeted_publish(args: argparse.Namespace, items: list[dict[str, Any]]) -> None:
    artifact_keys = [str(item.get("key") or "").strip() for item in items if str(item.get("key") or "").strip()]
    if not artifact_keys or args.clawhub_publish == "none":
        return

    publish_command = [
        "python3",
        "scripts/publish_clawhub_batch.py",
        "--targets",
        args.clawhub_publish,
        "--skip-build",
        "--force",
    ]
    if args.post_publish_scan:
        publish_command.append("--post-publish-scan")
    if args.clawhub_dry_run:
        publish_command.append("--dry-run")
    for key in artifact_keys:
        publish_command.extend(["--artifact", key])
    run_command(publish_command, timeout=7200)


def refresh_diagnosis(items: list[dict[str, Any]]) -> None:
    artifact_keys = [str(item.get("key") or "").strip() for item in items if str(item.get("key") or "").strip()]
    live_scan_command = [
        "python3",
        "scripts/clawhub_live_status.py",
        "--targets",
        "both",
        "--include-status",
        "published",
    ]
    for key in artifact_keys:
        live_scan_command.extend(["--artifact", key])
    run_command(live_scan_command, timeout=3600, check=False)
    run_command(
        ["python3", "scripts/clawhub_suspicious_diagnosis.py", "--doc-mode", "update"],
        timeout=1800,
        check=False,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Use the repo-local skill-refinement helper plus targeted ClawHub republish for suspicious blocker remediation.",
    )
    parser.add_argument(
        "--diagnosis-file",
        default=str(DEFAULT_DIAGNOSIS_FILE),
        help="Structured diagnosis JSON generated by scripts/clawhub_suspicious_diagnosis.py.",
    )
    parser.add_argument(
        "--report-file",
        default=str(DEFAULT_REPORT_FILE),
        help="Where the selected artifact/source-skill remediation plan is written.",
    )
    parser.add_argument(
        "--artifacts",
        default="",
        help="Comma-separated exact artifact keys such as skill:aisa-twitter-api-command-center,plugin:aisa-twitter-engagement-suite-plugin.",
    )
    parser.add_argument(
        "--contains",
        default="",
        help="Comma-separated substrings matched against key/name/reason/local_path when selecting artifacts.",
    )
    parser.add_argument(
        "--severity",
        choices=("blocker", "warning", "all"),
        default="blocker",
        help="Which diagnosis severity to target.",
    )
    parser.add_argument(
        "--status",
        choices=("suspicious", "pending", "any"),
        default="suspicious",
        help="Which live scan state to target.",
    )
    parser.add_argument(
        "--plan",
        action="store_true",
        help="Write the remediation plan only; do not modify files or publish.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply LLM refinement, rebuild release layers, and continue into optional sync/publish steps.",
    )
    parser.add_argument(
        "--sync-repo-skills",
        action="store_true",
        help="Refresh repo-local .agents skills from the global Codex skill directory before remediation.",
    )
    parser.add_argument(
        "--llm-if-available",
        action="store_true",
        help="Do not fail when the LLM credentials or global skill source are unavailable.",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip release-layer rebuild after applying LLM changes.",
    )
    parser.add_argument(
        "--skip-test",
        action="store_true",
        help="Skip scripts/test_release_layers.py after rebuilding.",
    )
    parser.add_argument(
        "--sync-adjacent-repos",
        action="store_true",
        help="After rebuilding, sync downstream publish repos via the existing publish scripts.",
    )
    parser.add_argument(
        "--clawhub-publish",
        choices=("none", "skill", "plugin", "both"),
        default="none",
        help="Optionally republish the selected suspicious artifacts through publish_clawhub_batch.py.",
    )
    parser.add_argument(
        "--clawhub-dry-run",
        action="store_true",
        help="When republishing, pass --dry-run to publish_clawhub_batch.py.",
    )
    parser.add_argument(
        "--post-publish-scan",
        action="store_true",
        help="When republishing, immediately probe live ClawHub scan status after publish.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    diagnosis_payload = load_json(Path(args.diagnosis_file).resolve())
    exact_keys = split_csv(args.artifacts)
    contains_tokens = split_csv(args.contains)
    items = select_artifacts(
        diagnosis_payload,
        exact_keys=exact_keys,
        contains_tokens=contains_tokens,
        severity=args.severity,
        status=args.status,
    )
    source_skills = resolve_source_skills(items)
    report = build_report(items, source_skills)
    write_json(Path(args.report_file).resolve(), report)

    print("Suspicious remediation plan", flush=True)
    print(f"  artifacts: {len(items)}", flush=True)
    print(f"  source skills: {len(source_skills)}", flush=True)
    for skill_name in source_skills:
        print(f"  - {skill_name}", flush=True)

    if args.plan or not args.apply:
        return 0

    if not source_skills:
        print("No matching suspicious source skills were selected; nothing to remediate.", flush=True)
        return 0

    if args.sync_repo_skills:
        run_command(DEFAULT_REPO_SKILL_SYNC, timeout=900, check=not args.llm_if_available)

    llm_command = [
        "python3",
        "scripts/llm_refine_aisa_skills.py",
        "--profile",
        "clawhub_breakout",
        "--skills",
        ",".join(source_skills),
        "--apply",
    ]
    if args.llm_if_available:
        llm_command.append("--if-available")
    run_command(llm_command, timeout=7200)

    run_builds(skip_build=args.skip_build, skip_test=args.skip_test)

    if args.sync_adjacent_repos:
        run_adjacent_sync()

    run_targeted_publish(args, items)
    refresh_diagnosis(items)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
