#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "publish-targetSkills-to-agent-skills.sh is now an agentskill.sh publish alias." >&2
echo "It rebuilds/syncs agentskill-sh-release into baofeng-tech/agent-skills (default local checkout: ../agent-skills-own)." >&2

exec bash "$SCRIPT_DIR/publish-agentskill-sh-release.sh" "$@"
