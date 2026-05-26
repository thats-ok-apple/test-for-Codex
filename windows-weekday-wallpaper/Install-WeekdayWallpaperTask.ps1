param(
    [string]$TaskName = "WeekdayWallpaper",
    [string]$ScriptPath = "$PSScriptRoot\\Set-WeekdayWallpaper.ps1"
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path $ScriptPath)) {
    throw "Script not found: $ScriptPath"
}

$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`""
$trigger = New-ScheduledTaskTrigger -Daily -At 08:00AM
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Description "Auto switch wallpaper Monday-Friday" -Force
Write-Host "Scheduled task '$TaskName' created/updated."
