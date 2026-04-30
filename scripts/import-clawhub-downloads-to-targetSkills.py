#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = REPO_ROOT.parent / "skillGet" / "public" / "downloads" / "clawHub"
DEFAULT_DEST = REPO_ROOT / "targetSkills"


def slugify(value: str) -> str:
    text = value.strip().lower()
    text = text.replace("&", " and ")
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text or "imported-skill"


def parse_frontmatter_name(skill_text: str) -> str | None:
    match = re.search(r"(?m)^name:\s*(.+?)\s*$", skill_text)
    if not match:
        return None
    return match.group(1).strip().strip("'\"")


def find_skill_entry(names: list[str]) -> str | None:
    candidates = [name for name in names if name.lower().endswith("skill.md")]
    if not candidates:
        return None
    candidates.sort(key=lambda item: (item.count("/"), len(item)))
    return candidates[0]


def build_existing_names(dest_dir: Path) -> set[str]:
    names = {slugify(path.name) for path in dest_dir.iterdir() if path.is_dir()}
    for skill_path in dest_dir.glob("*/SKILL.md"):
        try:
            name = parse_frontmatter_name(skill_path.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            continue
        if name:
            names.add(slugify(name))
    return names


def normalize_extracted_tree(dest: Path) -> None:
    for root, dirs, files in os.walk(dest, topdown=False):
        root_path = Path(root)

        for directory in list(dirs):
            if directory == "__MACOSX":
                shutil.rmtree(root_path / directory, ignore_errors=True)

        for filename in files:
            file_path = root_path / filename
            lower_name = filename.lower()
            if lower_name == "_meta.json" or lower_name == "claude.md":
                file_path.unlink(missing_ok=True)
                continue
            if lower_name == "skill.md" and filename != "SKILL.md":
                target = root_path / "SKILL.md"
                if not target.exists():
                    file_path.rename(target)
                else:
                    file_path.unlink(missing_ok=True)
                continue
            if lower_name == "readme.md" and filename != "README.md":
                target = root_path / "README.md"
                if not target.exists():
                    file_path.rename(target)
                else:
                    file_path.unlink(missing_ok=True)


def rewrite_skill_name(skill_path: Path, new_name: str) -> None:
    text = skill_path.read_text(encoding="utf-8")
    text = re.sub(r"(?m)^name:\s*.+?$", f"name: {new_name}", text, count=1)
    skill_path.write_text(text, encoding="utf-8")


def flatten_single_root(dest: Path) -> None:
    children = [child for child in dest.iterdir() if child.name != "__MACOSX"]
    if len(children) != 1 or not children[0].is_dir():
        return

    only_child = children[0]
    if not any(item.name.lower() == "skill.md" for item in only_child.rglob("*")):
        return

    temp_dir = dest.parent / f".tmp-flatten-{dest.name}"
    temp_dir.mkdir(parents=True, exist_ok=True)
    for item in only_child.iterdir():
        shutil.move(str(item), temp_dir / item.name)
    shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)
    for item in temp_dir.iterdir():
        shutil.move(str(item), dest / item.name)
    temp_dir.rmdir()


def import_zip(zip_path: Path, dest_dir: Path, existing_names: set[str], overwrite: bool) -> tuple[str, str]:
    with zipfile.ZipFile(zip_path) as archive:
        skill_entry = find_skill_entry(archive.namelist())
        if not skill_entry:
            return ("skip", f"{zip_path.name}: no SKILL.md/skill.md found")

        skill_text = archive.read(skill_entry).decode("utf-8", errors="ignore")
        source_name = parse_frontmatter_name(skill_text) or zip_path.stem
        target_name = slugify(source_name)
        zip_name = slugify(zip_path.stem)

        if not overwrite and zip_name in existing_names:
            return ("skip", f"{zip_path.name}: duplicate zip name `{zip_name}`")
        if not overwrite and target_name in existing_names:
            return ("skip", f"{zip_path.name}: duplicate skill name `{target_name}`")

        target_dir = dest_dir / target_name
        if target_dir.exists() and not overwrite:
            return ("skip", f"{zip_path.name}: target directory already exists `{target_name}`")

        if target_dir.exists():
            shutil.rmtree(target_dir)

        target_dir.mkdir(parents=True, exist_ok=True)
        archive.extractall(target_dir)
        flatten_single_root(target_dir)
        normalize_extracted_tree(target_dir)

        skill_path = target_dir / "SKILL.md"
        if not skill_path.exists():
            nested = list(target_dir.rglob("SKILL.md"))
            if len(nested) == 1:
                temp_root = Path(tempfile.mkdtemp(prefix="skill-import-", dir=str(dest_dir)))
                for item in nested[0].parent.iterdir():
                    shutil.move(str(item), temp_root / item.name)
                shutil.rmtree(target_dir)
                target_dir.mkdir(parents=True, exist_ok=True)
                for item in temp_root.iterdir():
                    shutil.move(str(item), target_dir / item.name)
                temp_root.rmdir()
                skill_path = target_dir / "SKILL.md"

        if not skill_path.exists():
            shutil.rmtree(target_dir, ignore_errors=True)
            return ("skip", f"{zip_path.name}: extracted package still has no SKILL.md")

        rewrite_skill_name(skill_path, target_name)
        existing_names.add(zip_name)
        existing_names.add(target_name)
        return ("import", f"{zip_path.name}: imported as `{target_name}`")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Import missing ClawHub zip packages into targetSkills as AgentSkills-style directories."
    )
    parser.add_argument("--source", default=str(DEFAULT_SOURCE), help="Source clawHub downloads directory")
    parser.add_argument("--dest", default=str(DEFAULT_DEST), help="Destination targetSkills directory")
    parser.add_argument("--overwrite-existing", action="store_true", help="Overwrite existing target directories")
    args = parser.parse_args()

    source_dir = Path(args.source).resolve()
    dest_dir = Path(args.dest).resolve()

    if not source_dir.exists():
        print(f"Source directory not found: {source_dir}", file=sys.stderr)
        return 1

    dest_dir.mkdir(parents=True, exist_ok=True)
    existing_names = build_existing_names(dest_dir)
    zip_paths = sorted(source_dir.rglob("*.zip"))

    imported = 0
    skipped = 0

    for zip_path in zip_paths:
        status, message = import_zip(zip_path, dest_dir, existing_names, args.overwrite_existing)
        print(message)
        if status == "import":
            imported += 1
        else:
            skipped += 1

    print(f"Finished: imported={imported}, skipped={skipped}, source={source_dir}, dest={dest_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
