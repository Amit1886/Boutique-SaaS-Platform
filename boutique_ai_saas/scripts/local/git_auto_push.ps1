param(
  [string]$Message = "auto update"
)

$ErrorActionPreference = "Stop"

git add -A
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
  Write-Host "No changes to commit."
  exit 0
}

$ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
git commit -m "$Message ($ts)"
git push origin main

