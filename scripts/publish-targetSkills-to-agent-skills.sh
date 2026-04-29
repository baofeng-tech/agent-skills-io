#!/usr/bin/env bash
set -euo pipefail

cat >&2 <<'EOF'
Blocked by repo policy:

This repository may read from AIsa-team/agent-skills as an upstream baseline,
but it must never sync, commit, or push targetSkills back into that upstream
repository again.

Use this repo for:
- upstream read-only sync into targetSkills/
- release-layer rebuilds
- downstream platform publish repos
- ClawHub / Claude / Hermes publish flows

Do not invoke publish-targetSkills-to-agent-skills.sh from automation.
EOF
exit 1
