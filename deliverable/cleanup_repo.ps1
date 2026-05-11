# Cleanup script: removes all files and folders in the repo root except the deliverable folder.
Set-StrictMode -Version Latest
cd $PSScriptRoot\..

# Confirm
Write-Host "This will remove all files and folders except 'deliverable' in:`n$(Get-Location)` - proceed? (Y/N)" -ForegroundColor Yellow
$ans = Read-Host
if ($ans -ne 'Y') { Write-Host "Aborted."; exit }

Get-ChildItem -Force | Where-Object { $_.Name -ne 'deliverable' -and $_.Name -ne '.' -and $_.Name -ne '..' } | ForEach-Object {
    try {
        if ($_.PSIsContainer) { Remove-Item $_.FullName -Recurse -Force -ErrorAction Stop }
        else { Remove-Item $_.FullName -Force -ErrorAction Stop }
        Write-Host "Deleted: $_.FullName"
    } catch {
        Write-Host "Failed to delete: $_.FullName - $_" -ForegroundColor Red
    }
}

Write-Host "Cleanup finished. Only 'deliverable' remains." -ForegroundColor Green
