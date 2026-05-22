@echo off
set VENV=%~dp0..\venv

echo Creating virtual environment...
python -m venv "%VENV%"

echo Installing mitmproxy...
"%VENV%\Scripts\pip" install mitmproxy

echo Generating certificates...
start /b "" "%VENV%\Scripts\mitmdump.exe" -p 8080
timeout /t 3 >nul
taskkill /f /im mitmdump.exe >nul 2>&1

echo Installing mitmproxy CA certificate...
certutil -addstore root "%USERPROFILE%\.mitmproxy\mitmproxy-ca-cert.cer"

echo Done!

echo Generating Steam launch option...
echo powershell -ExecutionPolicy Bypass -File "%~dp0launcher.ps1" %%command%% > "%~dp0..\steam_launch_option.txt"
echo.
echo ============================================
echo Paste this into Steam Launch Options:
type "%~dp0..\steam_launch_option.txt"
echo ============================================
pause
