param(
    [string]$SourceDir = ".\targetSkills",
    [string]$DestinationDir = "..\agent-skills-own"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $SourceDir)) {
    throw "Source directory not found: $SourceDir"
}

New-Item -ItemType Directory -Force $DestinationDir | Out-Null

Get-ChildItem $SourceDir -Directory | ForEach-Object {
    $target = Join-Path $DestinationDir $_.Name
    if (Test-Path $target) {
        Remove-Item $target -Recurse -Force
    }
    Copy-Item $_.FullName -Destination $DestinationDir -Recurse -Force
}

Get-ChildItem $SourceDir -File | Where-Object { $_.Name -ne "PUBLISHING.md" } | ForEach-Object {
    Copy-Item $_.FullName -Destination $DestinationDir -Force
}

Write-Host "Published targetSkills contents to $DestinationDir"
