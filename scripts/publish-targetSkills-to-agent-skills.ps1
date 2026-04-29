$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "publish-targetSkills-to-agent-skills.ps1 is now an agentskill.sh publish alias."
Write-Host "It rebuilds/syncs agentskill-sh-release into baofeng-tech/agent-skills (default local checkout: ..\agent-skills-own)."

& (Join-Path $ScriptDir "publish-agentskill-sh-release.ps1") @args
