#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CLAUDE_SOURCE="$REPO_ROOT/claude-release"
MARKET_SOURCE="$REPO_ROOT/claude-marketplace"
CLAUDE_DEST="${PUBLISH_CLAUDE_DEST:-${REPO_ROOT}/../Aisa-One-Skills-Claude}"
MARKET_DEST="${PUBLISH_CLAUDE_MARKETPLACE_DEST:-${REPO_ROOT}/../Aisa-One-Plugins-Claude}"
SKIP_BUILD=0
WITH_MARKETPLACE=0

usage() {
  cat <<USAGE
Usage:
  $(basename "$0") [--dest <path>] [--with-marketplace] [--market-dest <path>] [--skip-build]

Options:
  --dest <path>           Destination repo for claude-release. Default: ../Aisa-One-Skills-Claude
  --with-marketplace      Also build/sync claude-marketplace
  --market-dest <path>    Destination repo for claude-marketplace. Default: ../Aisa-One-Plugins-Claude
  --skip-build            Skip running build scripts
  -h, --help              Show this help
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dest)
      CLAUDE_DEST="$2"
      shift 2
      ;;
    --with-marketplace)
      WITH_MARKETPLACE=1
      shift
      ;;
    --market-dest)
      MARKET_DEST="$2"
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
  echo "[1/4] Building claude-release..."
  python3 "$REPO_ROOT/scripts/build_claude_release.py"
  if [[ "$WITH_MARKETPLACE" -eq 1 ]]; then
    echo "[2/4] Building claude-marketplace..."
    python3 "$REPO_ROOT/scripts/build_claude_marketplace.py"
  fi
else
  echo "[1/4] Skip build (requested)."
fi

if [[ ! -d "$CLAUDE_SOURCE" ]]; then
  echo "Source directory not found: $CLAUDE_SOURCE" >&2
  exit 1
fi

mkdir -p "$CLAUDE_DEST"

echo "[3/4] Syncing $CLAUDE_SOURCE -> $CLAUDE_DEST ..."
find "$CLAUDE_DEST" -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -R "$CLAUDE_SOURCE"/. "$CLAUDE_DEST"/

if [[ "$WITH_MARKETPLACE" -eq 1 ]]; then
  if [[ ! -d "$MARKET_SOURCE" ]]; then
    echo "Source directory not found: $MARKET_SOURCE" >&2
    exit 1
  fi
  mkdir -p "$MARKET_DEST"
  echo "[4/4] Syncing $MARKET_SOURCE -> $MARKET_DEST ..."
  find "$MARKET_DEST" -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
  cp -R "$MARKET_SOURCE"/. "$MARKET_DEST"/
else
  echo "[4/4] Marketplace sync skipped."
fi

echo "Done."
echo
echo "Next steps (claude-release):"
echo "  cd \"$CLAUDE_DEST\""
echo "  git add ."
echo "  git commit -m 'chore: publish claude-release'"
echo "  git push"
echo
echo "Optional install hints:"
echo "  skills.sh <owner>/<repo>/<skill-name>"
echo "  claude --print \"/skills\""

if [[ "$WITH_MARKETPLACE" -eq 1 ]]; then
  echo
  echo "Next steps (claude-marketplace):"
  echo "  cd \"$MARKET_DEST\""
  echo "  git add ."
  echo "  git commit -m 'chore: publish claude-marketplace'"
  echo "  git push"
  echo
  echo "Marketplace hints:"
  echo "  /plugin marketplace add <owner>/<repo>"
  echo "  /plugin install aisa-multi-search-engine@aisa-claude-marketplace"
fi
