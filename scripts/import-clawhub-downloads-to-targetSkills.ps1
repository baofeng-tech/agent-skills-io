param(
    [string]$SourceDir = "..\skillGet\public\downloads\clawHub",
    [string]$DestinationDir = ".\targetSkills",
    [switch]$OverwriteExisting
)

$ErrorActionPreference = "Stop"

$scriptPath = Join-Path $PSScriptRoot "import-clawhub-downloads-to-targetSkills.py"
$arguments = @("--source", $SourceDir, "--dest", $DestinationDir)

if ($OverwriteExisting) {
    $arguments += "--overwrite-existing"
}

python $scriptPath @arguments
