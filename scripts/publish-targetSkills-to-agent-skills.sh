#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="${1:-targetSkills}"
DEST_DIR="${2:-../agent-skills}"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Source directory not found: $SOURCE_DIR" >&2
  exit 1
fi

mkdir -p "$DEST_DIR"

find "$SOURCE_DIR" -mindepth 1 -maxdepth 1 -type d -print0 | while IFS= read -r -d '' dir; do
  name="$(basename "$dir")"
  rm -rf "$DEST_DIR/$name"
  cp -R "$dir" "$DEST_DIR/"
done

find "$SOURCE_DIR" -mindepth 1 -maxdepth 1 -type f ! -name 'PUBLISHING.md' -print0 | while IFS= read -r -d '' file; do
  cp -f "$file" "$DEST_DIR/"
done

echo "Published targetSkills contents to $DEST_DIR"
