#!/usr/bin/env python3
"""Deterministic ZIP helpers for generated release artifacts."""

from __future__ import annotations

import subprocess
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


FIXED_ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def _stable_mode(path: Path) -> int:
    result = subprocess.run(
        ["git", "ls-files", "--stage", "--", str(path)],
        cwd=str(path.parent),
        text=True,
        capture_output=True,
        check=False,
    )
    first = result.stdout.split(maxsplit=1)[0] if result.stdout.strip() else ""
    return 0o755 if first == "100755" else 0o644


def _zip_info(path: Path, arcname: str) -> ZipInfo:
    info = ZipInfo(arcname, FIXED_ZIP_TIMESTAMP)
    info.compress_type = ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = _stable_mode(path) << 16
    return info


def write_deterministic_zip(
    source_dir: Path,
    zip_path: Path,
    *,
    compresslevel: int | None = None,
) -> None:
    """Write a root-flat ZIP with stable ordering, timestamps, and permissions."""
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED, compresslevel=compresslevel) as archive:
        for path in sorted(source_dir.rglob("*"), key=lambda item: item.relative_to(source_dir).as_posix()):
            if not path.is_file():
                continue
            arcname = path.relative_to(source_dir).as_posix()
            archive.writestr(_zip_info(path, arcname), path.read_bytes())
