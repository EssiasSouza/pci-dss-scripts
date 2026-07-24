# Local
$localTime = [DateTime]::UtcNow
$localEpoch = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()

# Container
$containerTime = kubectl exec -n default gateway-6c84c64b5f-v6qmf -- date -u "+%Y-%m-%d %H:%M:%S UTC"
$containerEpoch = [long](kubectl exec -n default gateway-6c84c64b5f-v6qmf -- date -u +%s)

Write-Host ""
Write-Host "========== Time Synchronization Evidence =========="
Write-Host ("Local Time     : {0}" -f $localTime.ToString("yyyy-MM-dd HH:mm:ss 'UTC'"))
Write-Host ("Container Time : {0}" -f $containerTime)
Write-Host ""
Write-Host ("Local Epoch     : {0}" -f $localEpoch)
Write-Host ("Container Epoch : {0}" -f $containerEpoch)
Write-Host ("Difference      : {0} seconds" -f ($containerEpoch - $localEpoch))
Write-Host "==================================================="