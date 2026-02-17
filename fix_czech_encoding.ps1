# Fix Czech Translation Encoding
# This script will properly convert Czech characters

$csFile = "C:\Users\info\OneDrive\Dokumenty\CODEX\frontend\locales\cs\common.json"

Write-Host "Reading Czech translation file..." -ForegroundColor Yellow

# Read the file as raw bytes
$bytes = [System.IO.File]::ReadAllBytes($csFile)

# Try to detect and fix encoding
$content = [System.Text.Encoding]::UTF8.GetString($bytes)

# Replace common Czech character encoding issues
$fixes = @{
    'PĹ™ehled' = 'Přehled'
    'PĹ™ihlĂˇĹˇenĂ­' = 'Přihlášení'
    'VĂ­tejte zpÄ›t!' = 'Vítejte zpět!'
    'PĹ™ihlaste se do svĂ©ho ĂşÄŤtu' = 'Přihlaste se do svého účtu'
    'PĹ™ihlĂˇsit se' = 'Přihlásit se'
    'PĹ™ihlaĹˇovĂˇnĂ­' = 'Přihlašování'
    'NemĂˇte ĂşÄŤet?' = 'Nemáte účet?'
    'NesprĂˇvnĂ˝' = 'Nesprávný'
    'pĹ™ipojenĂ­' = 'připojení'
    'ProsĂ­m, pĹ™ihlaste se k nĂˇkupu pĹ™edplatnĂ©ho' = 'Prosím, přihlaste se k nákupu předplatného'
    'VytvoĹ™it ĂşÄŤet' = 'Vytvořit účet'
    'ZaÄŤnÄ›te pouĹľĂ­vat' = 'Začněte používat'
    'JmĂ©no a pĹ™Ă­jmenĂ­' = 'Jméno a příjmení'
    'PotvrÄŹte heslo' = 'Potvrďte heslo'
    'JiĹľ mĂˇte ĂşÄŤet?' = 'Již máte účet?'
    'neshodujĂ­' = 'neshodují'
    'pĹ™ipojenĂ­' = 'připojení'
    'VaĹˇe jmĂ©no' = 'Vaše jméno'
    'â€˘â€˘â€˘â€˘â€˘â€˘â€˘â€˘' = '••••••••'
    'âš ď¸Ź PovinnĂ© potvrzenĂ­' = '⚠️ Povinné potvrzení'
    'RozumĂ­m, Ĺľe' = 'Rozumím, že'
    'nĂˇstroj' = 'nástroj'
    'prĂˇvnĂ­k' = 'právník'
    'NEPOSKYTUJE prĂˇvnĂ­ poradenstvĂ­' = 'NEPOSKYTUJE právní poradenství'
    'pouĹľĂ­vĂˇnĂ­' = 'používání'
    'NEVYTVĂĹĂŤ' = 'NEVYTVÁŘÍ'
    'advokĂˇt' = 'advokát'
    'pĹ™ijmout vĹˇechna potvrzenĂ­' = 'přijmout všechna potvrzení'
    'VĹˇechna potvrzenĂ­ jsou povinnĂˇ' = 'Všechna potvrzení jsou povinná'
    'mĹŻĹľete' = 'můžete'
    'ĂşspÄ›ĹˇnĂˇ' = 'úspěšná'
    'NynĂ­ se' = 'Nyní se'
}

foreach ($key in $fixes.Keys) {
    $content = $content -replace [regex]::Escape($key), $fixes[$key]
}

# Write back with proper UTF-8 encoding (without BOM)
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($csFile, $content, $utf8NoBom)

Write-Host "✓ Czech translation file fixed!" -ForegroundColor Green
Write-Host "Please restart the Next.js development server." -ForegroundColor Cyan
