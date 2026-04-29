#!/usr/bin/env python3
"""Plan or run the dedicated ClawHub breakout rollout lane."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from unified_skill_pipeline import adjacent_sync_commands, parse_adjacent_targets


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_VARIANTS_FILE = REPO_ROOT / "targets" / "clawhub-breakout-variants.json"
DEFAULT_REPORT_FILE = REPO_ROOT / "targets" / "clawhub-breakout-rollout.json"
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
    ["python3", "scripts/build_claude_release.py"],
    ["python3", "scripts/build_claude_marketplace.py"],
    ["python3", "scripts/build_hermes_release.py"],
    ["python3", "scripts/build_agentskills_so_release.py"],
    ["python3", "scripts/build_agentskill_sh_release.py"],
]
TEST_STEP = ["python3", "scripts/test_release_layers.py"]


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


def load_variants(path: Path) -> list[dict[str, str]]:
    payload = load_json(path)
    variants = payload.get("variants") or []
    return [item for item in variants if isinstance(item, dict)]


def select_variants(variants: list[dict[str, str]], source_skills: list[str]) -> list[dict[str, str]]:
    if not source_skills:
        return variants
    requested = set(source_skills)
    return [item for item in variants if str(item.get("source") or "") in requested]


def build_report(variants: list[dict[str, str]]) -> dict[str, Any]:
    artifact_keys: list[str] = []
    for item in variants:
        slug = str(item.get("slug") or "").strip()
        if not slug:
            continue
        artifact_keys.extend([f"skill:{slug}", f"plugin:{slug}-plugin"])
    return {
        "summary": {
            "variants": len(variants),
            "sources": sorted({str(item.get("source") or "").strip() for item in variants if str(item.get("source") or "").strip()}),
            "artifact_keys": artifact_keys,
        },
        "variants": variants,
    }


def run_builds(*, skip_build: bool, skip_test: bool) -> None:
    if not skip_build:
        for command in FULL_BUILD_STEPS:
            run_command(command, timeout=7200)
    if not skip_test:
        run_command(TEST_STEP, timeout=7200)


def run_adjacent_sync(selected_targets: list[str]) -> None:
    for command in adjacent_sync_commands(selected_targets):
        run_command(command, timeout=7200)


def run_targeted_publish(args: argparse.Namespace, variants: list[dict[str, str]]) -> None:
    if args.clawhub_publish == "none":
        return

    artifact_keys: list[str] = []
    for item in variants:
        slug = str(item.get("slug") or "").strip()
        if not slug:
            continue
        if args.clawhub_publish in {"skill", "both"}:
            artifact_keys.append(f"skill:{slug}")
        if args.clawhub_publish in {"plugin", "both"}:
            artifact_keys.append(f"plugin:{slug}-plugin")

    if not artifact_keys:
        return

    command = [
        "python3",
        "scripts/publish_clawhub_batch.py",
        "--targets",
        args.clawhub_publish,
        "--skip-build",
        "--force",
    ]
    if args.post_publish_scan:
        command.append("--post-publish-scan")
    if args.clawhub_dry_run:
        command.append("--dry-run")
    for key in artifact_keys:
        command.extend(["--artifact", key])
    run_command(command, timeout=7200)


def refresh_live_state(variants: list[dict[str, str]]) -> None:
    artifact_keys: list[str] = []
    for item in variants:
        slug = str(item.get("slug") or "").strip()
        if not slug:
            continue
        artifact_keys.extend([f"skill:{slug}", f"plugin:{slug}-plugin"])
    if not artifact_keys:
        return

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
        description="Plan or execute the dedicated ClawHub breakout rollout lane.",
    )
    parser.add_argument(
        "--variants-file",
        default=str(DEFAULT_VARIANTS_FILE),
        help="Breakout variants declaration JSON, usually targets/clawhub-breakout-variants.json.",
    )
    parser.add_argument(
        "--report-file",
        default=str(DEFAULT_REPORT_FILE),
        help="Where the selected breakout rollout plan is written.",
    )
    parser.add_argument(
        "--skills",
        default="",
        help="Optional comma-separated source skill names to limit the rollout. Defaults to all declared breakout variants.",
    )
    parser.add_argument(
        "--plan",
        action="store_true",
        help="Write the breakout rollout plan only; do not modify files or publish.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply breakout-profile refinement, rebuild release layers, and continue into optional sync/publish steps.",
    )
    parser.add_argument(
        "--sync-repo-skills",
        action="store_true",
        help="Refresh repo-local .agents skills from the global Codex skill directory before breakout refinement.",
    )
    parser.add_argument(
        "--llm-if-available",
        action="store_true",
        help="Do not fail when the LLM credentials or global skill source are unavailable.",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip release-layer rebuild after applying breakout refinement.",
    )
    parser.add_argument(
        "--skip-test",
        action="store_true",
        help="Skip scripts/test_release_layers.py after rebuilding.",
    )
    parser.add_argument(
        "--sync-adjacent-repos",
        action="store_true",
        help="After rebuilding, sync downstream public publish repos via the existing publish scripts.",
    )
    parser.add_argument(
        "--adjacent-targets",
        default="all",
        help=(
            "Comma-separated downstream publish targets used with --sync-adjacent-repos. "
            "Supported values: all, agentskills-so, agentskill-sh, claude, claude-marketplace, hermes."
        ),
    )
    parser.add_argument(
        "--clawhub-publish",
        choices=("none", "skill", "plugin", "both"),
        default="none",
        help="Optionally publish the selected breakout variants through publish_clawhub_batch.py.",
    )
    parser.add_argument(
        "--clawhub-dry-run",
        action="store_true",
        help="When publishing, pass --dry-run to publish_clawhub_batch.py.",
    )
    parser.add_argument(
        "--post-publish-scan",
        action="store_true",
        help="When publishing, immediately probe live ClawHub scan status after publish.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    variants = load_variants(Path(args.variants_file).resolve())
    selected_variants = select_variants(variants, split_csv(args.skills))
    report = build_report(selected_variants)
    write_json(Path(args.report_file).resolve(), report)

    print("ClawHub breakout rollout plan", flush=True)
    print(f"  variants: {len(selected_variants)}", flush=True)
    for item in selected_variants:
        source = str(item.get("source") or "").strip()
        slug = str(item.get("slug") or "").strip()
        version = str(item.get("version") or "").strip()
        print(f"  - {source} -> {slug}{f' @ {version}' if version else ''}", flush=True)

    if args.plan or not args.apply:
        return 0

    source_skills = report["summary"]["sources"]
    if not source_skills:
        print("No breakout variants matched the requested source skills.", flush=True)
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
        run_adjacent_sync(parse_adjacent_targets(args.adjacent_targets))

    run_targeted_publish(args, selected_variants)
    refresh_live_state(selected_variants)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
