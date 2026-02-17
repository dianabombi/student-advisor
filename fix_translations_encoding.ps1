# Fix Translation Encoding Issues
# This script fixes UTF-8 encoding problems in translation files

Write-Host "Fixing translation encoding issues..." -ForegroundColor Green

$localesPath = "C:\Users\info\OneDrive\Dokumenty\CODEX\frontend\locales"

# Function to fix encoding
function Fix-FileEncoding {
    param (
        [string]$FilePath
    )
    
    Write-Host "Processing: $FilePath" -ForegroundColor Yellow
    
    # Read file with UTF-8 encoding
    $content = Get-Content -Path $FilePath -Raw -Encoding UTF8
    
    # Write back with UTF-8 encoding (without BOM)
    [System.IO.File]::WriteAllText($FilePath, $content, [System.Text.UTF8Encoding]::new($false))
    
    Write-Host "Fixed: $FilePath" -ForegroundColor Green
}

# Fix Slovak
Fix-FileEncoding -FilePath "$localesPath\sk\common.json"

# Fix Czech  
Fix-FileEncoding -FilePath "$localesPath\cs\common.json"

# Fix Russian
Fix-FileEncoding -FilePath "$localesPath\ru\common.json"

# Fix Polish
Fix-FileEncoding -FilePath "$localesPath\pl\common.json"

# Fix Ukrainian
Fix-FileEncoding -FilePath "$localesPath\uk\common.json"

Write-Host ""
Write-Host "All translation files have been re-encoded with proper UTF-8!" -ForegroundColor Green
Write-Host "Please restart the Next.js development server for changes to take effect." -ForegroundColor Cyan
