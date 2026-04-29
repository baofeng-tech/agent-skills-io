$ErrorActionPreference = "Stop"

throw @"
Blocked by repo policy:

This repository may read from AIsa-team/agent-skills as an upstream baseline,
but it must never sync, commit, or push targetSkills back into that upstream
repository again.

Do not use publish-targetSkills-to-agent-skills.ps1 in automation.
"@
