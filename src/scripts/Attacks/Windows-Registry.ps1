<#
This script tests the alerting of registry edits in Windows.
This is meant to emulate attacks that use the registry to establish persistence and for other malicious tasks.

It sets the registry key enabling developer mode to 1, waits 2 hours to allow the log and the alert to be generated, and sets it back to 0.

These commands can also be run by hand if any execution issues are found.
#>

Set-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\AppModelUnlock" -Name "AllowAllTrustedApps" -Value 1
Start-Sleep 7200
Set-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\AppModelUnlock" -Name "AllowAllTrustedApps" -Value 0
