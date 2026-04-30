#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="${1:-../skillGet/public/downloads/github}"
DEST_DIR="${2:-targetSkills}"

ARGS=(--source "$SOURCE_DIR" --dest "$DEST_DIR")

if [[ "${OVERWRITE_EXISTING:-0}" == "1" ]]; then
  ARGS+=(--overwrite-existing)
fi

python3 "$(dirname "$0")/import-github-downloads-to-targetSkills.py" "${ARGS[@]}"
