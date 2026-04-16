#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="${1:-../agent-skills-own}"
DEST_DIR="${2:-targetSkills}"
OVERWRITE_EXISTING="${OVERWRITE_EXISTING:-0}"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Source directory not found: $SOURCE_DIR" >&2
  exit 1
fi

mkdir -p "$DEST_DIR"

find "$SOURCE_DIR" -mindepth 1 -maxdepth 1 -type d -print0 | while IFS= read -r -d '' dir; do
  if [[ ! -f "$dir/SKILL.md" ]]; then
    continue
  fi

  name="$(basename "$dir")"
  target="$DEST_DIR/$name"

  if [[ -e "$target" && "$OVERWRITE_EXISTING" != "1" ]]; then
    echo "Skip existing skill: $name"
    continue
  fi

  rm -rf "$target"
  cp -R "$dir" "$DEST_DIR/"
  echo "Imported skill: $name"
done

echo "Imported skills from $SOURCE_DIR to $DEST_DIR"
