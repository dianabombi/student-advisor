# Automatic University Scraping Monitor
# Monitors progress and launches groups sequentially

$groups = @(
    @{Name="Group 1 (SK,CZ,PL)"; Script="scrape_sk_cz_pl.py"; Codes="'SK','CZ','PL'"; Done=$true},
    @{Name="Group 2 (AT,DE,CH)"; Script="scrape_at_de_ch.py"; Codes="'AT','DE','CH'"; Done=$false},
    @{Name="Group 3 (FR,BE,LU,MC)"; Script="scrape_fr_be_lu_mc.py"; Codes="'FR','BE','LU','MC'"; Done=$false},
    @{Name="Group 4 (IT,VA,SM)"; Script="scrape_it_va_sm.py"; Codes="'IT','VA','SM'"; Done=$false},
    @{Name="Group 5 (ES,AD,PT)"; Script="scrape_es_ad_pt.py"; Codes="'ES','AD','PT'"; Done=$false},
    @{Name="Group 6 (GB,IE)"; Script="scrape_gb_ie.py"; Codes="'GB','IE'"; Done=$false},
    @{Name="Group 7 (FI,SE,DK,NO)"; Script="scrape_fi_se_dk_no.py"; Codes="'FI','SE','DK','NO'"; Done=$false},
    @{Name="Group 8 (Others)"; Script="scrape_remaining.py"; Codes="'HU','SI','HR','GR','LI','NL'"; Done=$false}
)

Write-Host "=== University Scraping Monitor ===" -ForegroundColor Cyan
Write-Host "Starting at: $(Get-Date)" -ForegroundColor Yellow
Write-Host ""

$currentGroup = 1  # Start with Group 2 (Group 1 already done)

while ($currentGroup -lt $groups.Count) {
    $group = $groups[$currentGroup]
    
    Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] Checking $($group.Name)..." -ForegroundColor Cyan
    
    # Check status
    $statusQuery = "SELECT scraping_status, COUNT(*) FROM university_scraping_status uss JOIN universities u ON uss.university_id = u.id WHERE u.jurisdiction_id IN (SELECT id FROM jurisdictions WHERE code IN ($($group.Codes))) GROUP BY scraping_status;"
    $status = docker exec student-db-1 psql -U user -d codex_db -c $statusQuery 2>&1
    
    Write-Host $status
    
    # Check if group is complete (no pending or in_progress)
    if ($status -notmatch "pending" -and $status -notmatch "in_progress") {
        Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] $($group.Name) COMPLETED!" -ForegroundColor Green
        
        # Launch next group
        $currentGroup++
        if ($currentGroup -lt $groups.Count) {
            $nextGroup = $groups[$currentGroup]
            Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] Launching $($nextGroup.Name)..." -ForegroundColor Yellow
            docker exec student-backend-1 python /app/$($nextGroup.Script)
            Start-Sleep -Seconds 10
        }
    } else {
        Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] $($group.Name) still processing..." -ForegroundColor Yellow
    }
    
    Write-Host ""
    Start-Sleep -Seconds 120  # Check every 2 minutes
}

Write-Host "=== ALL GROUPS COMPLETED ===" -ForegroundColor Green
Write-Host "Finished at: $(Get-Date)" -ForegroundColor Yellow

# Final retry of failed
Write-Host ""
Write-Host "Retrying failed universities..." -ForegroundColor Cyan
docker exec student-db-1 psql -U user -d codex_db -c "UPDATE university_scraping_status SET scraping_status = 'pending', error_message = NULL WHERE scraping_status = 'failed';"
docker exec student-backend-1 python /app/scrape_sk_cz_pl.py
docker exec student-backend-1 python /app/scrape_at_de_ch.py

Write-Host ""
Write-Host "=== SCRAPING COMPLETE ===" -ForegroundColor Green
