#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE_DIR="$REPO_ROOT/agentskills-so-release"
DEST_DIR="${PUBLISH_AGENTSKILLS_SO_DEST:-${REPO_ROOT}/../agent-skills-so}"
SKIP_BUILD=0

usage() {
  cat <<USAGE
Usage:
  $(basename "$0") [--dest <path>] [--skip-build]

Options:
  --dest <path>   Destination git repo path. Default: ../agent-skills-so
  --skip-build    Skip normalize/build steps
  -h, --help      Show this help
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dest)
      DEST_DIR="$2"
      shift 2
      ;;
    --skip-build)
      SKIP_BUILD=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ "$SKIP_BUILD" -eq 0 ]]; then
  echo "[1/2] Normalizing target skills..."
  python3 "$REPO_ROOT/scripts/normalize_target_skills.py"
  echo "[2/2] Building agentskills-so-release..."
  python3 "$REPO_ROOT/scripts/build_agentskills_so_release.py"
else
  echo "[1/2] Skip build (requested)."
fi

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Source directory not found: $SOURCE_DIR" >&2
  exit 1
fi

mkdir -p "$DEST_DIR"

echo "[2/2] Syncing $SOURCE_DIR -> $DEST_DIR ..."
find "$DEST_DIR" -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -R "$SOURCE_DIR"/. "$DEST_DIR"/

echo
echo "AgentSkills.so release is ready at:"
echo "  $SOURCE_DIR"
echo
echo "Recommended next steps:"
echo "  1. Push $DEST_DIR"
echo "  2. Submit that repo to agentskills.so"
echo "  3. Reuse the same repo URL for agentskill.sh when you want GitHub-based indexing"
