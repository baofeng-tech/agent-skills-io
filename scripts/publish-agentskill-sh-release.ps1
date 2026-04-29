$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
$SourceDir = Join-Path $RepoRoot "agentskill-sh-release"
$DestDir = if ($env:PUBLISH_AGENTSKILL_SH_DEST) {
    $env:PUBLISH_AGENTSKILL_SH_DEST
} elseif ($env:PUBLISH_AGENT_SKILLS_DEST) {
    $env:PUBLISH_AGENT_SKILLS_DEST
} else {
    Join-Path $RepoRoot "..\agent-skills-own"
}
$SkipBuild = $false

function Show-Usage {
    @"
Usage:
  $(Split-Path -Leaf $MyInvocation.MyCommand.Path) [--dest <path>] [--skip-build]

Options:
  --dest <path>   Destination git repo path. Default: ..\agent-skills-own
  --skip-build    Skip normalize/build steps
  -h, --help      Show this help
"@
}

for ($i = 0; $i -lt $args.Count; $i++) {
    switch ($args[$i]) {
        "--dest" {
            if ($i + 1 -ge $args.Count) {
                throw "Missing value for --dest"
            }
            $DestDir = $args[$i + 1]
            $i++
        }
        "--skip-build" {
            $SkipBuild = $true
        }
        "-h" {
            Show-Usage
            exit 0
        }
        "--help" {
            Show-Usage
            exit 0
        }
        default {
            throw "Unknown argument: $($args[$i])"
        }
    }
}

if (-not $SkipBuild) {
    Write-Host "[1/2] Normalizing target skills..."
    python3 (Join-Path $RepoRoot "scripts/normalize_target_skills.py")
    Write-Host "[2/2] Building agentskill.sh release..."
    python3 (Join-Path $RepoRoot "scripts/build_agentskill_sh_release.py")
} else {
    Write-Host "[1/2] Skip build (requested)."
}

if (-not (Test-Path $SourceDir)) {
    throw "Source directory not found: $SourceDir"
}

if (-not (Test-Path $DestDir)) {
    New-Item -ItemType Directory -Force -Path $DestDir | Out-Null
}

Write-Host "[2/2] Syncing $SourceDir -> $DestDir ..."
Get-ChildItem -Force $DestDir | Where-Object { $_.Name -ne ".git" } | Remove-Item -Recurse -Force
Copy-Item -Path (Join-Path $SourceDir "*") -Destination $DestDir -Recurse -Force

Write-Host ""
Write-Host "agentskill.sh release is ready at:"
Write-Host "  $SourceDir"
Write-Host ""
Write-Host "Recommended next steps:"
Write-Host "  1. Push $DestDir"
Write-Host "  2. Open https://agentskill.sh/submit"
Write-Host "  3. Paste the repo URL into Analyze & Import"
Write-Host "  4. Optionally add webhook https://agentskill.sh/api/webhooks/github"
