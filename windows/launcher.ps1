$ScriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvMitm   = Join-Path $ScriptDir "..\venv\Scripts\mitmdump.exe"
$ProxyScript = Join-Path $ScriptDir "..\pastebin_fix.py"

$proxy = Start-Process -PassThru -WindowStyle Hidden `
    -FilePath $VenvMitm `
    -ArgumentList "-p 8080 -s `"$ProxyScript`" --quiet"

Start-Sleep -Seconds 2

$env:HTTP_PROXY  = "http://127.0.0.1:8080"
$env:HTTPS_PROXY = "http://127.0.0.1:8080"

$game = Start-Process -PassThru -FilePath $args[0] -ArgumentList $args[1..($args.Length-1)]
$game.WaitForExit()

Stop-Process -Id $proxy.Id -ErrorAction SilentlyContinue
