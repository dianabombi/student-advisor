# Enable Docker Desktop autostart on Windows login
Write-Host "Enabling Docker Desktop autostart..." -ForegroundColor Cyan

# Find Docker Desktop executable
$dockerPaths = @(
    "C:\Program Files\Docker\Docker\Docker Desktop.exe",
    "$env:ProgramFiles\Docker\Docker\Docker Desktop.exe",
    "$env:LOCALAPPDATA\Programs\Docker\Docker\Docker Desktop.exe"
)

$dockerPath = $null
foreach ($path in $dockerPaths) {
    if (Test-Path $path) {
        $dockerPath = $path
        break
    }
}

if (-not $dockerPath) {
    Write-Host "ERROR: Docker Desktop not found!" -ForegroundColor Red
    Write-Host "Please install Docker Desktop first." -ForegroundColor Yellow
    exit 1
}

Write-Host "Found Docker Desktop at: $dockerPath" -ForegroundColor Green

# Create startup shortcut
$startupFolder = [System.Environment]::GetFolderPath('Startup')
$shortcutPath = Join-Path $startupFolder "Docker Desktop.lnk"

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($shortcutPath)
$Shortcut.TargetPath = $dockerPath
$Shortcut.WorkingDirectory = Split-Path $dockerPath
$Shortcut.Description = "Docker Desktop - Auto Start"
$Shortcut.Save()

Write-Host ""
Write-Host "SUCCESS! Docker Desktop will now start automatically when you log in." -ForegroundColor Green
Write-Host ""
Write-Host "Shortcut created at: $shortcutPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "Docker will start automatically on next login!" -ForegroundColor Yellow
