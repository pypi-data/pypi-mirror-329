git 

$token = Read-Host -Prompt "Enter your token" -AsSecureString 
uv build
Write-Host "Publishing... $($token | ConvertFrom-SecureString)"
uv publish --token "$($token | ConvertFrom-SecureString)"