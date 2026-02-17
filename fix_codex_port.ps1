# -*- coding: utf-8 -*-
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# ========================================
# 🚀 FIX CODEX PORT CONFLICT (3001 vs 3000)
# ========================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 FIX CODEX PORT CONFLICT (3001 vs 3000)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 1️⃣ Зупиняємо всі процеси на портах 3000 і 3001
Write-Host "🛑 Killing processes on ports 3000 and 3001..." -ForegroundColor Yellow
try {
    $port3000 = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
    if ($port3000) { Stop-Process -Id $port3000 -Force -ErrorAction SilentlyContinue }
    
    $port3001 = Get-NetTCPConnection -LocalPort 3001 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
    if ($port3001) { Stop-Process -Id $port3001 -Force -ErrorAction SilentlyContinue }
} catch {}

# 2️⃣ Зупиняємо Docker контейнери CODEX
Write-Host "🐳 Stopping CODEX Docker containers..." -ForegroundColor Yellow
try {
    docker compose down 2>$null
} catch {}

# 3️⃣ Встановлюємо правильний порт у .env
Write-Host "⚙️ Setting PORT=3001 in .env ..." -ForegroundColor Yellow
$envPath = ".env"
$envContent = Get-Content $envPath -ErrorAction SilentlyContinue

if ($envContent -match "PORT=") {
    $envContent = $envContent -replace "PORT=.*", "PORT=3001"
} else {
    $envContent += "`nPORT=3001"
}

if ($envContent -match "NEXT_PUBLIC_API_URL=") {
    $envContent = $envContent -replace "NEXT_PUBLIC_API_URL=.*", "NEXT_PUBLIC_API_URL=http://localhost:8001"
} else {
    $envContent += "`nNEXT_PUBLIC_API_URL=http://localhost:8001"
}

$envContent | Set-Content $envPath

# 4️⃣ Чистимо кеш та перевстановлюємо пакети
Write-Host "🧹 Cleaning cache in frontend..." -ForegroundColor Yellow
Set-Location frontend
Remove-Item -Recurse -Force .next, node_modules -ErrorAction SilentlyContinue

Write-Host "📦 Installing npm packages..." -ForegroundColor Yellow
npm install

# 5️⃣ Запускаємо CODEX на порту 3001
Write-Host "🚀 Starting CODEX on port 3001..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ CODEX should now be available at:" -ForegroundColor Green
Write-Host "👉 http://localhost:3001" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

npm run dev
