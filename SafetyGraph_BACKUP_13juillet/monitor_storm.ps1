# Monitor STORM Continuous Deployment
while ($true) {
    Clear-Host
    Write-Host "STORM MONITORING DASHBOARD" -ForegroundColor Green
    Write-Host "=" * 50
    Write-Host "Date: $(Get-Date)"
    Write-Host ""
    
    # Vérifier processus Python
    $pythonProcs = Get-Process python -ErrorAction SilentlyContinue
    if ($pythonProcs) {
        $count = ($pythonProcs | Measure-Object).Count
        Write-Host "Processus Python actifs: $count" -ForegroundColor Green
        foreach ($proc in $pythonProcs) {
            Write-Host "  ID: $($proc.Id) | CPU: $($proc.CPU) | Memoire: $($proc.WorkingSet64/1MB) MB" -ForegroundColor Gray
        }
    } else {
        Write-Host "Aucun processus Python detecte" -ForegroundColor Red
    }
    
    Write-Host ""
    
    # Vérifier derniers fichiers
    $latestCorpus = Get-ChildItem "data\storm_knowledge\*.json" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($latestCorpus) {
        $age = (Get-Date) - $latestCorpus.LastWriteTime
        Write-Host "Dernier corpus: $($latestCorpus.Name)" -ForegroundColor Yellow
        Write-Host "Age: $($age.ToString('dd\.hh\:mm\:ss'))" -ForegroundColor Yellow
    }
    
    # Vérifier logs
    $logFile = "logs\storm_continuous.log"
    if (Test-Path $logFile) {
        $logSize = (Get-Item $logFile).Length
        Write-Host "Log STORM: $($logSize) bytes" -ForegroundColor Cyan
    }
    
    Write-Host ""
    Write-Host "Prochaine mise a jour dans 30 secondes (Ctrl+C pour arreter)" -ForegroundColor White
    Start-Sleep 30
}
