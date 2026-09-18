param(
  [Parameter(ValueFromRemainingArguments=$true)]
  [string[]]$Args
)

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path

if ($Args.Count -gt 0 -and $Args[0] -eq "resources") {
  $Rest = @()
  if ($Args.Count -gt 1) {
    $Rest = $Args[1..($Args.Count - 1)]
  }
  python (Join-Path $Here "resources.py") @Rest
} else {
  python (Join-Path $Here "gptbc.py") @Args
}

exit $LASTEXITCODE
