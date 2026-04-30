#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE_DIR="$REPO_ROOT/hermes-release"
DEST_DIR="${PUBLISH_HERMES_DEST:-${REPO_ROOT}/../Aisa-One-Skills-Hermes}"
PUBLISH_MODE="${PUBLISH_HERMES_MODE:-repo-sync}"
TARGET_REPO="${HERMES_PUBLISH_REPO:-}"
SKIP_BUILD=0

usage() {
  cat <<USAGE
Usage:
  $(basename "$0") [--dest <path>] [--mode repo-sync|cli] [--repo <owner/repo>] [--skip-build]

Options:
  --dest <path>   Destination git repo path. Default: ../Aisa-One-Skills-Hermes
  --mode <mode>   Publish mode: repo-sync (default) or cli
  --repo <repo>   Required when --mode cli, for example baofeng-tech/Aisa-One-Skills-Hermes
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
    --mode)
      PUBLISH_MODE="$2"
      shift 2
      ;;
    --repo)
      TARGET_REPO="$2"
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

if [[ "$PUBLISH_MODE" == "cli" ]]; then
  if ! command -v hermes >/dev/null 2>&1; then
    echo "Hermes CLI not found on PATH." >&2
    exit 1
  fi
  if [[ -z "$TARGET_REPO" ]]; then
    echo "Missing Hermes publish repo. Use --repo <owner/repo> or HERMES_PUBLISH_REPO." >&2
    exit 1
  fi

  mapfile -t SKILL_DIRS < <(find "$SOURCE_DIR" -mindepth 2 -maxdepth 2 -type f -name 'SKILL.md' -printf '%h\n' | sort)
  if [[ "${#SKILL_DIRS[@]}" -eq 0 ]]; then
    echo "No Hermes skill directories found under $SOURCE_DIR" >&2
    exit 1
  fi

  echo "[2/3] Publishing ${#SKILL_DIRS[@]} Hermes skills via CLI to $TARGET_REPO ..."
  for skill_dir in "${SKILL_DIRS[@]}"; do
    echo "  hermes skills publish $skill_dir --to github --repo $TARGET_REPO"
    hermes skills publish "$skill_dir" --to github --repo "$TARGET_REPO"
  done

  echo "[3/3] Done."
  echo
  echo "Hermes CLI publish completed for $TARGET_REPO."
  exit 0
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
