#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE_DIR="$REPO_ROOT/hermes-release"
DEST_DIR="${REPO_ROOT}/../Aisa-One-Skills-Hermes"
SKIP_BUILD=0

usage() {
  cat <<USAGE
Usage:
  $(basename "$0") [--dest <path>] [--skip-build]

Options:
  --dest <path>   Destination git repo path. Default: ../Aisa-One-Skills-Hermes
  --skip-build    Skip running build_hermes_release.py
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
  echo "[1/3] Building hermes-release..."
  python3 "$REPO_ROOT/scripts/build_hermes_release.py"
else
  echo "[1/3] Skip build (requested)."
fi

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Source directory not found: $SOURCE_DIR" >&2
  exit 1
fi

mkdir -p "$DEST_DIR"

echo "[2/3] Syncing $SOURCE_DIR -> $DEST_DIR ..."
# Keep destination git metadata, replace everything else.
find "$DEST_DIR" -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -R "$SOURCE_DIR"/. "$DEST_DIR"/

echo "[3/3] Done."
echo
echo "Next steps:"
echo "  cd \"$DEST_DIR\""
echo "  git add ."
echo "  git commit -m 'chore: publish hermes-release'"
echo "  git push"
echo
echo "Install example after push:"
echo "  hermes skills install github:<owner>/<repo>/research/aisa-multi-search-engine"
