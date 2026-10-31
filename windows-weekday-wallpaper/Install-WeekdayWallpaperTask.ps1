param(
    [string]$TaskName = "WeekdayWallpaper",
    [string]$ScriptPath = "$PSScriptRoot\\Set-WeekdayWallpaper.ps1",
    [datetime]$DailyTime = [datetime]::Parse("06:30")
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path $ScriptPath)) {
    throw "Script not found: $ScriptPath"
}

$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`""
$dailyTrigger = New-ScheduledTaskTrigger -Daily -At $DailyTime
$startupTrigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger @($dailyTrigger, $startupTrigger) -Settings $settings -Description "Auto switch wallpaper Monday-Friday (daily 06:30 + at startup)" -Force
Write-Host "Scheduled task '$TaskName' created/updated."
Write-Host "Triggers: every day at $($DailyTime.ToString('HH:mm')) and at computer startup."
