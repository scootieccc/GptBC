param(
  [Parameter(ValueFromRemainingArguments=$true)]
  [string[]]$Args
)
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $Here "gptbc.py") @Args
exit $LASTEXITCODE
