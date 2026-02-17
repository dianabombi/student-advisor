# Script to merge marketplace translations into common.json files
# This merges the marketplace section into each language's common.json

$languages = @("cs", "pl", "ru")

foreach ($lang in $languages) {
    Write-Host "Processing $lang..."
    
    $commonFile = "frontend\locales\$lang\common.json"
    $marketplaceFile = "frontend\locales\marketplace_$lang.json"
    
    if (Test-Path $commonFile) {
        # Read both files
        $common = Get-Content $commonFile -Raw | ConvertFrom-Json
        $marketplace = Get-Content $marketplaceFile -Raw | ConvertFrom-Json
        
        # Add marketplace section
        $common | Add-Member -MemberType NoteProperty -Name "marketplace" -Value $marketplace.marketplace -Force
        
        # Write back
        $common | ConvertTo-Json -Depth 20 | Set-Content $commonFile -Encoding UTF8
        
        Write-Host "✓ Merged marketplace translations for $lang"
    } else {
        Write-Host "✗ File not found: $commonFile"
    }
}

Write-Host "`nDone! Merged translations for: $($languages -join ', ')"
