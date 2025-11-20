# PowerShell script to check PostgreSQL status on Windows

Write-Host "Checking PostgreSQL service status..." -ForegroundColor Cyan

# Check if PostgreSQL service exists and is running
$service = Get-Service -Name postgresql* -ErrorAction SilentlyContinue

if ($service) {
    foreach ($s in $service) {
        Write-Host "`nService: $($s.Name)" -ForegroundColor Yellow
        Write-Host "Status: $($s.Status)" -ForegroundColor $(if ($s.Status -eq 'Running') { 'Green' } else { 'Red' })
        Write-Host "Display Name: $($s.DisplayName)"
    }
    
    $running = $service | Where-Object { $_.Status -eq 'Running' }
    if (-not $running) {
        Write-Host "`n⚠️  PostgreSQL service is not running!" -ForegroundColor Red
        Write-Host "To start it, run: Start-Service -Name '<service-name>'" -ForegroundColor Yellow
        Write-Host "Or use: net start <service-name>" -ForegroundColor Yellow
    }
} else {
    Write-Host "`n⚠️  PostgreSQL service not found!" -ForegroundColor Red
    Write-Host "This might mean PostgreSQL is not installed, or the service has a different name." -ForegroundColor Yellow
}

Write-Host "`nChecking if PostgreSQL is listening on port 5432..." -ForegroundColor Cyan
$portCheck = Get-NetTCPConnection -LocalPort 5432 -ErrorAction SilentlyContinue
if ($portCheck) {
    Write-Host "✅ Port 5432 is in use (PostgreSQL might be running)" -ForegroundColor Green
} else {
    Write-Host "❌ Port 5432 is not in use (PostgreSQL is likely not running)" -ForegroundColor Red
}

