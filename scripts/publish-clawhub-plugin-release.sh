#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKIP_BUILD=0

usage() {
  cat <<USAGE
Usage:
  $(basename "$0") [--skip-build]

Options:
  --skip-build    Skip normalize/build steps
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
  echo "[1/4] Normalizing target skills..."
  python3 "$REPO_ROOT/scripts/normalize_target_skills.py"
  echo "[2/4] Building clawhub-release..."
  python3 "$REPO_ROOT/scripts/build_clawhub_release.py"
  echo "[3/4] Building clawhub-plugin-release..."
  python3 "$REPO_ROOT/scripts/build_clawhub_plugin_release.py"
else
  echo "[1/4] Skip build (requested)."
fi

echo "[4/4] ClawHub bundle plugins are ready at:"
echo "  $REPO_ROOT/clawhub-plugin-release"
echo
echo "Dry-run publish loop:"
echo '  for dir in clawhub-plugin-release/plugins/*; do'
echo '    [ -d "$dir" ] || continue'
echo '    clawhub package publish "$dir" --dry-run'
echo '  done'
echo
echo "Real publish loop:"
echo '  for dir in clawhub-plugin-release/plugins/*; do'
echo '    [ -d "$dir" ] || continue'
echo '    clawhub package publish "$dir"'
echo '  done'
