#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "[1/10] Normalize source skills"
python3 "$REPO_ROOT/scripts/normalize_target_skills.py"

echo "[2/10] Build clawhub release"
python3 "$REPO_ROOT/scripts/build_clawhub_release.py"

echo "[3/10] Build clawhub plugin release"
python3 "$REPO_ROOT/scripts/build_clawhub_plugin_release.py"

echo "[4/10] Build claude release"
python3 "$REPO_ROOT/scripts/build_claude_release.py"

echo "[5/10] Build claude marketplace"
python3 "$REPO_ROOT/scripts/build_claude_marketplace.py"

echo "[6/10] Build hermes release"
python3 "$REPO_ROOT/scripts/build_hermes_release.py"

echo "[7/10] Build agentskills.so release"
python3 "$REPO_ROOT/scripts/build_agentskills_so_release.py"

echo "[8/10] Build agentskill.sh release"
python3 "$REPO_ROOT/scripts/build_agentskill_sh_release.py"

echo "[9/10] Run release-layer validation"
python3 "$REPO_ROOT/scripts/test_release_layers.py"

echo "[10/10] Sync existing external Git repos"
bash "$REPO_ROOT/scripts/publish-claude-release.sh" --with-marketplace --skip-build
bash "$REPO_ROOT/scripts/publish-hermes-release.sh" --skip-build
bash "$REPO_ROOT/scripts/publish-clawhub-release.sh" --skip-build

echo
echo "All release layers rebuilt. Existing external Git sync has been run for Claude / Hermes / ClawHub skill layers."
echo "ClawHub plugin, AgentSkills.so, and agentskill.sh publishing should continue from their generated local bundles."
