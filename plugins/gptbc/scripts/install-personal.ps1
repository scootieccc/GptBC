$ErrorActionPreference = "Stop"

$PluginRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$TargetRoot = Join-Path $HOME "plugins"
$Target = Join-Path $TargetRoot "gptbc"
$MarketplaceDir = Join-Path $HOME ".agents\plugins"
$Marketplace = Join-Path $MarketplaceDir "marketplace.json"

New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null
New-Item -ItemType Directory -Force -Path $MarketplaceDir | Out-Null

if (Test-Path $Target) {
  $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
  Copy-Item $Target "$Target.backup-$stamp" -Recurse
  Remove-Item $Target -Recurse -Force
}
Copy-Item $PluginRoot $Target -Recurse

if (Test-Path $Marketplace) {
  $m = Get-Content $Marketplace -Raw | ConvertFrom-Json
} else {
  $m = [pscustomobject]@{
    name = "personal"
    interface = [pscustomobject]@{ displayName = "Personal" }
    plugins = @()
  }
}

$existing = @($m.plugins | Where-Object { $_.name -eq "gptbc" })
if ($existing.Count -eq 0) {
  $entry = [pscustomobject]@{
    name = "gptbc"
    source = [pscustomobject]@{ source = "local"; path = "./plugins/gptbc" }
    policy = [pscustomobject]@{ installation = "AVAILABLE"; authentication = "ON_INSTALL" }
    category = "Developer Tools"
  }
  $m.plugins = @($m.plugins) + $entry
}

$m | ConvertTo-Json -Depth 12 | Set-Content $Marketplace -Encoding UTF8
Write-Host "Installed GptBC to $Target"
Write-Host "Marketplace: $Marketplace"
Write-Host "Restart Codex so the plugin is rediscovered."
