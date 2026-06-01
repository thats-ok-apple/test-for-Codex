param(
    [string]$WallpapersDir = "$PSScriptRoot\\wallpapers"
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path $WallpapersDir)) {
    throw "Wallpapers directory not found: $WallpapersDir"
}

Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Wallpaper {
    [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
    public static extern int SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni);
}
"@

$map = @{
    "Monday"    = "monday.jpg"
    "Tuesday"   = "tuesday.jpg"
    "Wednesday" = "wednesday.jpg"
    "Thursday"  = "thursday.jpg"
    "Friday"    = "friday.jpg"
}

$today = (Get-Date).DayOfWeek.ToString()

if (-not $map.ContainsKey($today)) {
    Write-Host "Today is $today, no weekday wallpaper update needed."
    exit 0
}

$target = Join-Path $WallpapersDir $map[$today]
if (-not (Test-Path $target)) {
    throw "Wallpaper file missing for $today: $target"
}

# 10 = SPI_SETDESKWALLPAPER, 0x01|0x02 = update profile + broadcast change
$result = [Wallpaper]::SystemParametersInfo(20, 0, $target, 0x01 -bor 0x02)
if ($result -ne 1) {
    throw "Failed to set wallpaper. Win32Error: $([Runtime.InteropServices.Marshal]::GetLastWin32Error())"
}

Write-Host "Wallpaper changed to $target"
