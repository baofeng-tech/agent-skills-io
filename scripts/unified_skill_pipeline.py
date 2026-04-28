#!/usr/bin/env python3
"""Sync upstream skills into targetSkills, rebuild release layers, and optionally publish."""

from __future__ import annotations

import argparse
import fnmatch
import json
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_UPSTREAM_URL = "https://github.com/AIsa-team/agent-skills.git"
DEFAULT_UPSTREAM_BRANCH = "main"
DEFAULT_UPSTREAM_CACHE = REPO_ROOT / ".cache" / "upstream-agent-skills"
DEFAULT_TARGET_ROOT = REPO_ROOT / "targetSkills"
DEFAULT_STATE_FILE = REPO_ROOT / "targets" / "unified-pipeline-state.json"
DEFAULT_REPO_SKILL_SYNC = [
    "python3",
    "scripts/sync_codex_repo_skills.py",
    "--if-available",
]

ALLOWED_TOP_LEVEL_FILES = {
    "SKILL.md",
    "README.md",
    "LICENSE",
    "LICENSE.md",
    "LICENSE.txt",
}
ALLOWED_TOP_LEVEL_DIRS = {"scripts", "references", "assets"}
EXCLUDE_GLOBS = {
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    ".DS_Store",
    "*.pyc",
    "*.pyo",
    "*.log",
    "*.tmp",
    "*.sqlite",
    "*.db",
    "compare.sh",
    "generate-synthesis-inputs.py",
    "run-tests.sh",
    "sync.sh",
    "test-*.py",
    "test-*.sh",
    "verify_v3.py",
    "briefing.py",
    "run-briefing.sh",
    "run-watchlist.sh",
    "store.py",
    "watchlist.py",
    "setup_wizard.py",
}
BUILD_STEPS = [
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
MANUAL_REVIEW_RULES: dict[str, tuple[str, str]] = {}


@dataclass
class SkillPlan:
    name: str
    source: str
    target: str
    mode: str
    reason: str | None = None


@dataclass
class RunSummary:
    started_at: str
    source_mode: str
    upstream_root: str
    upstream_branch: str
    upstream_head: str
    baseline_commit: str | None
    selection: str
    include_working_tree: bool
    planned_skills: list[str] = field(default_factory=list)
    synced_skills: list[str] = field(default_factory=list)
    created_skills: list[str] = field(default_factory=list)
    skipped_skills: list[dict[str, str]] = field(default_factory=list)
    llm_steps: list[str] = field(default_factory=list)
    diagnosis_steps: list[str] = field(default_factory=list)
    publish_steps: list[str] = field(default_factory=list)
    completed_at: str | None = None


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_command(
    args: list[str],
    *,
    cwd: Path,
    timeout: int = 3600,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        args,
        cwd=str(cwd),
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


def read_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def write_state(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def extract_pending_manual_review_names(raw: Any) -> list[str]:
    if not isinstance(raw, list):
        return []
    names: list[str] = []
    seen: set[str] = set()
    for item in raw:
        if isinstance(item, dict):
            name = str(item.get("name") or "").strip()
        else:
            name = str(item or "").strip()
        if not name or name in seen:
            continue
        seen.add(name)
        names.append(name)
    return names


def ensure_upstream_repo(args: argparse.Namespace) -> tuple[Path, str]:
    if args.upstream_local_path:
        root = Path(args.upstream_local_path).resolve()
        if not root.exists():
            raise FileNotFoundError(f"Upstream local path not found: {root}")
        return root, "local"

    cache_root = Path(args.upstream_cache_dir).resolve()
    cache_root.parent.mkdir(parents=True, exist_ok=True)
    if not (cache_root / ".git").exists():
        run_command(
            ["git", "clone", "--branch", args.upstream_branch, "--single-branch", args.upstream_repo_url, str(cache_root)],
            cwd=REPO_ROOT,
            timeout=3600,
        )
    else:
        run_command(["git", "fetch", "origin", args.upstream_branch], cwd=cache_root, timeout=3600)
        run_command(["git", "checkout", args.upstream_branch], cwd=cache_root, timeout=3600)
        run_command(["git", "pull", "--ff-only", "origin", args.upstream_branch], cwd=cache_root, timeout=3600)
    return cache_root, "clone"


def git_stdout(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=str(repo),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def discover_skill_dirs(root: Path) -> dict[str, Path]:
    return {
        skill_dir.name: skill_dir
        for skill_dir in sorted(path for path in root.iterdir() if path.is_dir() and (path / "SKILL.md").exists())
    }


def collect_changed_files(
    repo: Path,
    *,
    baseline_commit: str | None,
    head_commit: str,
    include_working_tree: bool,
    selection: str,
) -> list[str]:
    if selection == "all" or not baseline_commit:
        return []

    changed: set[str] = set()
    diff = git_stdout(repo, "diff", "--name-only", baseline_commit, head_commit, "--")
    if diff:
        changed.update(path for path in diff.splitlines() if path.strip())

    if include_working_tree:
        for extra_args in (
            ("diff", "--name-only", "HEAD", "--"),
            ("diff", "--cached", "--name-only", "HEAD", "--"),
            ("ls-files", "--others", "--exclude-standard"),
        ):
            output = git_stdout(repo, *extra_args)
            if output:
                changed.update(path for path in output.splitlines() if path.strip())

    return sorted(changed)


def map_changed_skills(
    upstream_root: Path,
    *,
    baseline_commit: str | None,
    head_commit: str,
    selection: str,
    include_working_tree: bool,
    explicit_skills: list[str],
    pending_manual_review_skills: list[str],
) -> list[SkillPlan]:
    source_skills = discover_skill_dirs(upstream_root)

    if explicit_skills:
        skill_names = [name for name in explicit_skills if name in source_skills]
    elif selection == "all" or not baseline_commit:
        skill_names = sorted(source_skills)
    else:
        changed_files = collect_changed_files(
            upstream_root,
            baseline_commit=baseline_commit,
            head_commit=head_commit,
            include_working_tree=include_working_tree,
            selection=selection,
        )
        skill_names = sorted(
            {
                Path(path).parts[0]
                for path in changed_files
                if Path(path).parts and Path(path).parts[0] in source_skills
            }
        )
        if pending_manual_review_skills:
            skill_names = sorted(set(skill_names) | {name for name in pending_manual_review_skills if name in source_skills})

    plans: list[SkillPlan] = []
    for name in skill_names:
        mode = "copy"
        reason = None
        if name in MANUAL_REVIEW_RULES:
            mode, reason = MANUAL_REVIEW_RULES[name]
        plans.append(
            SkillPlan(
                name=name,
                source=str(source_skills[name]),
                target=str(DEFAULT_TARGET_ROOT / name),
                mode=mode,
                reason=reason,
            )
        )
    return plans


def matches_exclude(name: str) -> bool:
    return any(fnmatch.fnmatch(name, pattern) for pattern in EXCLUDE_GLOBS)


def copy_runtime_dir(src: Path, dst: Path) -> None:
    for path in src.rglob("*"):
        relative = path.relative_to(src)
        parts = relative.parts
        if any(matches_exclude(part) for part in parts):
            continue
        if path.is_dir():
            continue
        destination = dst / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)


def sync_skill(plan: SkillPlan, *, dry_run: bool) -> tuple[bool, bool]:
    src_dir = Path(plan.source)
    dst_dir = Path(plan.target)
    existed = dst_dir.exists()
    if dry_run:
        return existed, False

    temp_dir = dst_dir.parent / f".{dst_dir.name}.sync-tmp"
    shutil.rmtree(temp_dir, ignore_errors=True)
    temp_dir.mkdir(parents=True, exist_ok=True)

    for file_name in ALLOWED_TOP_LEVEL_FILES:
        src_file = src_dir / file_name
        if src_file.exists() and src_file.is_file():
            shutil.copy2(src_file, temp_dir / file_name)

    for dir_name in ALLOWED_TOP_LEVEL_DIRS:
        src_subdir = src_dir / dir_name
        if src_subdir.exists() and src_subdir.is_dir():
            copy_runtime_dir(src_subdir, temp_dir / dir_name)

    if not (temp_dir / "SKILL.md").exists():
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise RuntimeError(f"Refusing to sync {src_dir.name}: SKILL.md not copied into temp dir.")

    shutil.rmtree(dst_dir, ignore_errors=True)
    temp_dir.replace(dst_dir)
    return existed, True


def run_builds(*, skip_build: bool, skip_test: bool) -> None:
    if not skip_build:
        for command in BUILD_STEPS:
            run_command(command, cwd=REPO_ROOT, timeout=3600)
    if not skip_test:
        run_command(TEST_STEP, cwd=REPO_ROOT, timeout=3600)


def run_llm_step(args: argparse.Namespace, summary: RunSummary) -> None:
    if not args.run_llm_step or args.dry_run:
        return

    if args.sync_repo_skills:
        run_command(DEFAULT_REPO_SKILL_SYNC, cwd=REPO_ROOT, timeout=900, check=not args.llm_if_available)
        summary.llm_steps.append(" ".join(DEFAULT_REPO_SKILL_SYNC))

    candidate_skills: list[str] = []
    for name in summary.synced_skills:
        skill_file = DEFAULT_TARGET_ROOT / name / "SKILL.md"
        if not skill_file.exists():
            continue
        text = skill_file.read_text(encoding="utf-8")
        if name.startswith("aisa-") or "AISA_API_KEY" in text or "api.aisa.one" in text:
            candidate_skills.append(name)

    if not candidate_skills:
        return

    llm_command = [
        "python3",
        "scripts/llm_refine_aisa_skills.py",
        "--profile",
        "source",
        "--skills",
        ",".join(candidate_skills),
    ]
    if args.llm_apply:
        llm_command.append("--apply")
    if args.llm_if_available:
        llm_command.append("--if-available")
    run_command(llm_command, cwd=REPO_ROOT, timeout=7200)
    summary.llm_steps.append(" ".join(llm_command))


def run_publish_steps(args: argparse.Namespace, summary: RunSummary) -> None:
    if args.sync_adjacent_repos:
        commands = [
            ["bash", "scripts/publish-targetSkills-to-agent-skills.sh"],
            ["bash", "scripts/publish-agentskills-so-release.sh", "--skip-build"],
            ["bash", "scripts/publish-agentskill-sh-release.sh", "--skip-build"],
            ["bash", "scripts/publish-claude-release.sh", "--with-marketplace", "--skip-build"],
            ["bash", "scripts/publish-hermes-release.sh", "--skip-build"],
        ]
        for command in commands:
            run_command(command, cwd=REPO_ROOT, timeout=3600)
            summary.publish_steps.append(" ".join(command))

    if args.clawhub_publish != "none":
        clawhub_command = [
            "python3",
            "scripts/publish_clawhub_batch.py",
            "--targets",
            args.clawhub_publish,
        ]
        if args.clawhub_dry_run:
            clawhub_command.append("--dry-run")
        else:
            clawhub_command.extend(["--skip-build"])
        run_command(clawhub_command, cwd=REPO_ROOT, timeout=7200)
        summary.publish_steps.append(" ".join(clawhub_command))


def run_diagnosis_steps(args: argparse.Namespace, summary: RunSummary) -> None:
    if args.dry_run:
        return

    live_scan_command = [
        "python3",
        "scripts/clawhub_live_status.py",
        "--targets",
        "both",
        "--include-status",
        "published",
    ]
    live_scan_result = run_command(live_scan_command, cwd=REPO_ROOT, timeout=3600, check=False)
    if live_scan_result.returncode == 0:
        summary.diagnosis_steps.append(" ".join(live_scan_command))

    diagnosis_command = [
        "python3",
        "scripts/clawhub_suspicious_diagnosis.py",
        "--doc-mode",
        "update",
    ]
    diagnosis_result = run_command(diagnosis_command, cwd=REPO_ROOT, timeout=1800, check=False)
    if diagnosis_result.returncode == 0:
        summary.diagnosis_steps.append(" ".join(diagnosis_command))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Unified scheduler for upstream skill sync, release-layer rebuilds, tests, and optional publish steps.",
    )
    parser.add_argument(
        "--upstream-local-path",
        help="Use an already checked-out upstream repo path instead of cloning/fetching.",
    )
    parser.add_argument(
        "--upstream-repo-url",
        default=DEFAULT_UPSTREAM_URL,
        help="Git URL used when cloning/fetching the upstream repo.",
    )
    parser.add_argument(
        "--upstream-branch",
        default=DEFAULT_UPSTREAM_BRANCH,
        help="Upstream branch to diff against. Defaults to the AIsa upstream source branch `main`.",
    )
    parser.add_argument(
        "--upstream-cache-dir",
        default=str(DEFAULT_UPSTREAM_CACHE),
        help="Clone/fetch cache directory used when --upstream-local-path is not supplied.",
    )
    parser.add_argument(
        "--state-file",
        default=str(DEFAULT_STATE_FILE),
        help="JSON file that remembers the last synced upstream commit and last run summary.",
    )
    parser.add_argument(
        "--selection",
        choices=("changed", "all"),
        default="changed",
        help="Sync only changed skills since the last baseline commit, or force all upstream skills.",
    )
    parser.add_argument(
        "--skills",
        default="",
        help="Comma-separated skill names to sync explicitly. Overrides --selection.",
    )
    parser.add_argument(
        "--include-working-tree",
        action="store_true",
        help="Also treat uncommitted upstream changes as diff input.",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip release-layer rebuild steps after syncing.",
    )
    parser.add_argument(
        "--skip-test",
        action="store_true",
        help="Skip release-layer validation after rebuild.",
    )
    parser.add_argument(
        "--sync-repo-skills",
        action="store_true",
        help="Refresh repo-local .agents skills from the local Codex global skill directory when available.",
    )
    parser.add_argument(
        "--run-llm-step",
        action="store_true",
        help="Run the repo-local skill-refinement helper against changed AISA API target skills before rebuild.",
    )
    parser.add_argument(
        "--llm-apply",
        action="store_true",
        help="Allow the repo-local skill-refinement helper to write SKILL.md / README.md changes back into targetSkills/.",
    )
    parser.add_argument(
        "--llm-if-available",
        action="store_true",
        help="Do not fail when repo-skill sync or LLM credentials are unavailable.",
    )
    parser.add_argument(
        "--sync-adjacent-repos",
        action="store_true",
        help="After a successful build/test run, sync targetSkills/Claude/Hermes layers into sibling repos via existing publish scripts.",
    )
    parser.add_argument(
        "--clawhub-publish",
        choices=("none", "skill", "plugin", "both"),
        default="none",
        help="Optionally continue into publish_clawhub_batch.py after rebuild/test.",
    )
    parser.add_argument(
        "--clawhub-dry-run",
        action="store_true",
        help="Pass --dry-run to publish_clawhub_batch.py.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the sync plan without copying files or updating state.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    state_path = Path(args.state_file).resolve()
    state = read_state(state_path)
    previous_commit = state.get("last_synced_commit")
    pending_manual_review_names = extract_pending_manual_review_names(state.get("pending_manual_review"))
    explicit_skills = [item.strip() for item in args.skills.split(",") if item.strip()]

    upstream_root, source_mode = ensure_upstream_repo(args)
    upstream_head = git_stdout(upstream_root, "rev-parse", "HEAD")
    if not upstream_head:
        raise RuntimeError(f"Could not resolve HEAD for upstream repo: {upstream_root}")

    plans = map_changed_skills(
        upstream_root,
        baseline_commit=previous_commit,
        head_commit=upstream_head,
        selection=args.selection,
        include_working_tree=args.include_working_tree,
        explicit_skills=explicit_skills,
        pending_manual_review_skills=pending_manual_review_names,
    )

    summary = RunSummary(
        started_at=iso_now(),
        source_mode=source_mode,
        upstream_root=str(upstream_root),
        upstream_branch=args.upstream_branch,
        upstream_head=upstream_head,
        baseline_commit=previous_commit,
        selection=("manual" if explicit_skills else args.selection),
        include_working_tree=args.include_working_tree,
        planned_skills=[plan.name for plan in plans],
    )

    if not plans:
        print("No upstream skill changes detected.", flush=True)
        summary.completed_at = iso_now()
        if not state_path.exists():
            write_state(
                state_path,
                {
                    **state,
                    "last_synced_commit": previous_commit,
                    "last_run": asdict(summary),
                    "last_detected_commit": upstream_head,
                },
            )
        return 0

    print("Unified skill pipeline plan", flush=True)
    print(f"  upstream: {upstream_root}", flush=True)
    print(f"  baseline: {previous_commit or 'none'}", flush=True)
    print(f"  head:     {upstream_head}", flush=True)
    for plan in plans:
        reason = f" ({plan.reason})" if plan.reason else ""
        print(f"  - {plan.name}: {plan.mode}{reason}", flush=True)

    for plan in plans:
        if plan.mode != "copy":
            summary.skipped_skills.append({"name": plan.name, "reason": plan.reason or "manual review"})
            continue
        existed, copied = sync_skill(plan, dry_run=args.dry_run)
        if copied:
            summary.synced_skills.append(plan.name)
            if not existed:
                summary.created_skills.append(plan.name)

    if args.dry_run:
        summary.completed_at = iso_now()
        print("Dry run only; no files were modified.", flush=True)
        return 0

    if summary.synced_skills:
        run_llm_step(args, summary)
        run_builds(skip_build=args.skip_build, skip_test=args.skip_test)
    else:
        print("No skills were synced after applying manual-review rules; skipping build/test.", flush=True)

    run_publish_steps(args, summary)
    run_diagnosis_steps(args, summary)

    summary.completed_at = iso_now()
    next_state = {
        **state,
        "last_synced_commit": upstream_head,
        "last_detected_commit": upstream_head,
        "last_run": asdict(summary),
        "pending_manual_review": summary.skipped_skills,
    }
    write_state(state_path, next_state)

    print("", flush=True)
    print("Unified skill pipeline summary", flush=True)
    print(f"  synced:  {len(summary.synced_skills)}", flush=True)
    print(f"  created: {len(summary.created_skills)}", flush=True)
    print(f"  skipped: {len(summary.skipped_skills)}", flush=True)
    if summary.llm_steps:
        print(f"  llm:     {len(summary.llm_steps)} step(s)", flush=True)
    if summary.diagnosis_steps:
        print(f"  diag:    {len(summary.diagnosis_steps)} step(s)", flush=True)
    if summary.publish_steps:
        print(f"  publish: {len(summary.publish_steps)} step(s)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
