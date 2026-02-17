# PowerShell script to create desktop shortcut for Student platform

$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.Environment]::GetFolderPath('Desktop')
$ShortcutPath = Join-Path $DesktopPath "Launch Student.lnk"

$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "C:\Users\info\OneDrive\Dokumenty\Student\START_STUDENT_AUTO.bat"
$Shortcut.WorkingDirectory = "C:\Users\info\OneDrive\Dokumenty\Student"
$Shortcut.Description = "Launch Student Educational Platform"
$Shortcut.IconLocation = "C:\Windows\System32\imageres.dll,13"

$Shortcut.Save()

Write-Host "Desktop shortcut created successfully!" -ForegroundColor Green
Write-Host "Location: $ShortcutPath" -ForegroundColor Cyan
Write-Host "You can now launch Student platform from your desktop!" -ForegroundColor Yellow
