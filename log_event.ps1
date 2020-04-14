$time=[System.DateTime]::Now

 if(-not (Get-EventLog -Source CameraDetection -LogName Application))
 {
 New-EventLog -Source CameraDetection -LogName Application
 }

Write-EventLog -Source  CameraDetection -LogName Application -Message "Motion Detected at $($time)" -EventId 60000

