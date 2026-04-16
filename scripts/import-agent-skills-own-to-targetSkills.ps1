param(
    [string]$SourceDir = "..\agent-skills-own",
    [string]$DestinationDir = ".\targetSkills",
    [switch]$OverwriteExisting
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $SourceDir)) {
    throw "Source directory not found: $SourceDir"
}

New-Item -ItemType Directory -Force $DestinationDir | Out-Null

Get-ChildItem $SourceDir -Directory | ForEach-Object {
    $skillFile = Join-Path $_.FullName "SKILL.md"
    if (-not (Test-Path $skillFile)) {
        return
    }

    $target = Join-Path $DestinationDir $_.Name
    if ((Test-Path $target) -and (-not $OverwriteExisting)) {
        Write-Host "Skip existing skill: $($_.Name)"
        return
    }

    if (Test-Path $target) {
        Remove-Item $target -Recurse -Force
    }

    Copy-Item $_.FullName -Destination $DestinationDir -Recurse -Force
    Write-Host "Imported skill: $($_.Name)"
}

Write-Host "Imported skills from $SourceDir to $DestinationDir"
