#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE_DIR="$REPO_ROOT/clawhub-release"
SKIP_BUILD=0

usage() {
  cat <<USAGE
Usage:
  $(basename "$0") [--skip-build]

Options:
  --skip-build    Skip running normalize/build scripts
  -h, --help      Show this help
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
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
  echo "[1/3] Normalizing target skills..."
  python3 "$REPO_ROOT/scripts/normalize_target_skills.py"
  echo "[2/3] Building clawhub-release..."
  python3 "$REPO_ROOT/scripts/build_clawhub_release.py"
else
  echo "[1/3] Skip build (requested)."
fi

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Source directory not found: $SOURCE_DIR" >&2
  exit 1
fi

echo "[3/3] clawhub-release is ready at:"
echo "  $SOURCE_DIR"
echo
echo "Example publish loop:"
echo '  export CLAWHUB_TOKEN="<token>"'
echo '  for dir in clawhub-release/*; do'
echo '    [ -d "$dir" ] || continue'
echo '    clawhub skill publish "$dir"'
echo '  done'
