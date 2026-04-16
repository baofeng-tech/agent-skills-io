#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = REPO_ROOT.parent / "skillGet" / "public" / "downloads" / "github"
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


def rewrite_skill_name(skill_path: Path, new_name: str) -> None:
    text = skill_path.read_text(encoding="utf-8")
    if re.search(r"(?m)^name:\s*.+?$", text):
        text = re.sub(r"(?m)^name:\s*.+?$", f"name: {new_name}", text, count=1)
    else:
        text = f"---\nname: {new_name}\n---\n\n{text}"
    skill_path.write_text(text, encoding="utf-8")


def extract_archive(archive_path: Path, target_dir: Path) -> None:
    if archive_path.name.lower().endswith(".zip"):
        with zipfile.ZipFile(archive_path) as archive:
            archive.extractall(target_dir)
        return

    if archive_path.name.lower().endswith((".tar.gz", ".tgz", ".tar")):
        with tarfile.open(archive_path, "r:*") as archive:
            archive.extractall(target_dir)
        return

    raise ValueError(f"Unsupported archive format: {archive_path}")


def read_skill_text_from_archive(archive_path: Path) -> tuple[str | None, str | None]:
    if archive_path.name.lower().endswith(".zip"):
        with zipfile.ZipFile(archive_path) as archive:
            names = archive.namelist()
            skill_entries = sorted(
                (name for name in names if name.lower().endswith("skill.md")),
                key=lambda item: (item.count("/"), len(item)),
            )
            if not skill_entries:
                return (None, None)
            skill_entry = skill_entries[0]
            root_name = skill_entry.split("/")[0]
            skill_text = archive.read(skill_entry).decode("utf-8", errors="ignore")
            return (root_name, skill_text)

    if archive_path.name.lower().endswith((".tar.gz", ".tgz", ".tar")):
        with tarfile.open(archive_path, "r:*") as archive:
            members = [member for member in archive.getmembers() if member.name.lower().endswith("skill.md")]
            members.sort(key=lambda item: (item.name.count("/"), len(item.name)))
            if not members:
                return (None, None)
            skill_member = members[0]
            root_name = skill_member.name.split("/")[0]
            extracted = archive.extractfile(skill_member)
            if extracted is None:
                return (None, None)
            skill_text = extracted.read().decode("utf-8", errors="ignore")
            return (root_name, skill_text)

    return (None, None)


def extract_skill_root(dest_dir: Path, target_dir: Path) -> Path | None:
    skill_path = target_dir / "SKILL.md"
    if skill_path.exists():
        return target_dir

    nested = list(target_dir.rglob("SKILL.md"))
    if len(nested) != 1:
        return None

    skill_root = nested[0].parent
    temp_root = Path(tempfile.mkdtemp(prefix="skill-import-", dir=str(dest_dir)))
    for item in skill_root.iterdir():
        shutil.move(str(item), temp_root / item.name)
    shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    for item in temp_root.iterdir():
        shutil.move(str(item), target_dir / item.name)
    temp_root.rmdir()
    return target_dir


def import_archive(archive_path: Path, dest_dir: Path, existing_names: set[str], overwrite: bool) -> tuple[str, str]:
    source_folder_name, skill_text = read_skill_text_from_archive(archive_path)
    if not skill_text:
        return ("skip", f"{archive_path.name}: no SKILL.md/skill.md found")

    source_folder_slug = slugify(source_folder_name or archive_path.stem)
    source_skill_name = parse_frontmatter_name(skill_text) or source_folder_name or archive_path.stem
    source_skill_slug = slugify(source_skill_name)

    if not overwrite and source_folder_slug in existing_names:
        return ("skip", f"{archive_path.name}: duplicate folder name `{source_folder_slug}`")
    if not overwrite and source_skill_slug in existing_names:
        return ("skip", f"{archive_path.name}: duplicate skill name `{source_skill_slug}`")

    target_name = source_skill_slug
    target_dir = dest_dir / target_name
    if target_dir.exists() and not overwrite:
        return ("skip", f"{archive_path.name}: target directory already exists `{target_name}`")

    if target_dir.exists():
        shutil.rmtree(target_dir)

    target_dir.mkdir(parents=True, exist_ok=True)
    extract_archive(archive_path, target_dir)
    flatten_single_root(target_dir)
    normalize_extracted_tree(target_dir)

    if not extract_skill_root(dest_dir, target_dir):
        shutil.rmtree(target_dir, ignore_errors=True)
        return ("skip", f"{archive_path.name}: extracted package still has no SKILL.md")

    skill_path = target_dir / "SKILL.md"
    rewrite_skill_name(skill_path, target_name)

    existing_names.add(source_folder_slug)
    existing_names.add(source_skill_slug)
    existing_names.add(target_name)
    return (
        "import",
        f"{archive_path.name}: imported as `{target_name}` (folder=`{source_folder_slug}`, skill=`{source_skill_slug}`)",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Import missing GitHub-downloaded skill archives into targetSkills as AgentSkills-style directories."
    )
    parser.add_argument("--source", default=str(DEFAULT_SOURCE), help="Source github downloads directory")
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
    archive_paths = sorted(
        list(source_dir.rglob("*.tar.gz")) + list(source_dir.rglob("*.tgz")) + list(source_dir.rglob("*.zip"))
    )

    imported = 0
    skipped = 0

    for archive_path in archive_paths:
        status, message = import_archive(archive_path, dest_dir, existing_names, args.overwrite_existing)
        print(message)
        if status == "import":
            imported += 1
        else:
            skipped += 1

    print(f"Finished: imported={imported}, skipped={skipped}, source={source_dir}, dest={dest_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
