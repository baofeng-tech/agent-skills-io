#!/usr/bin/env python3
"""Sync selected global Codex skills into this repo's .agents/skills tree."""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE_ROOT = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills"
DEFAULT_DEST_ROOT = REPO_ROOT / ".agents" / "skills"
DEFAULT_SKILLS = (
    "clawhub-plugin-packager-all",
    "clawhub-security-auditor-all",
    "clawhub-skill-optimizer-all",
)
SKIP_NAMES = {"__pycache__", ".pytest_cache", ".DS_Store"}
SKIP_SUFFIXES = {".pyc", ".pyo"}


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def tree_fingerprint(root: Path) -> tuple[tuple[str, str], ...]:
    if not root.exists():
        return ()
    rows: list[tuple[str, str]] = []
    for path in sorted(root.rglob("*")):
        if any(part in SKIP_NAMES for part in path.parts):
            continue
        if path.is_dir() or path.suffix in SKIP_SUFFIXES:
            continue
        rows.append((str(path.relative_to(root)), file_digest(path)))
    return tuple(rows)


def copy_tree(src: Path, dst: Path, *, dry_run: bool) -> bool:
    src_fingerprint = tree_fingerprint(src)
    dst_fingerprint = tree_fingerprint(dst)
    if src_fingerprint == dst_fingerprint:
        return False
    if dry_run:
        return True

    temp_dir = dst.parent / f".{dst.name}.sync-tmp"
    shutil.rmtree(temp_dir, ignore_errors=True)
    shutil.copytree(
        src,
        temp_dir,
        ignore=shutil.ignore_patterns(*SKIP_NAMES, "*.pyc", "*.pyo"),
    )
    shutil.rmtree(dst, ignore_errors=True)
    temp_dir.replace(dst)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync selected Codex global skills into .agents/skills.")
    parser.add_argument(
        "--source-root",
        default=str(DEFAULT_SOURCE_ROOT),
        help="Global Codex skills directory. Defaults to $CODEX_HOME/skills or ~/.codex/skills.",
    )
    parser.add_argument(
        "--dest-root",
        default=str(DEFAULT_DEST_ROOT),
        help="Destination repo-local skills directory.",
    )
    parser.add_argument(
        "--skills",
        default=",".join(DEFAULT_SKILLS),
        help="Comma-separated skill names to sync.",
    )
    parser.add_argument(
        "--if-available",
        action="store_true",
        help="Exit successfully when the global skill root does not exist.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the sync plan without writing files.",
    )
    args = parser.parse_args()

    source_root = Path(args.source_root).expanduser().resolve()
    dest_root = Path(args.dest_root).expanduser().resolve()
    skills = [item.strip() for item in args.skills.split(",") if item.strip()]

    if not source_root.exists():
        if args.if_available:
            print(f"Skip skill sync: source root not found: {source_root}")
            return 0
        raise SystemExit(f"Global skill root not found: {source_root}")

    dest_root.mkdir(parents=True, exist_ok=True)
    changed = 0
    skipped = 0
    for skill_name in skills:
        src = source_root / skill_name
        dst = dest_root / skill_name
        if not src.exists():
            print(f"Skip {skill_name}: source skill not found at {src}")
            skipped += 1
            continue
        updated = copy_tree(src, dst, dry_run=args.dry_run)
        status = "update" if updated else "unchanged"
        print(f"{status}: {skill_name}")
        changed += int(updated)

    mode = "dry-run" if args.dry_run else "done"
    print(f"{mode}: {changed} changed, {skipped} skipped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
