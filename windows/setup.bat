@echo off
set VENV=%~dp0..\venv

echo Creating virtual environment...
python -m venv "%VENV%"

echo Generating Steam launch option...
echo powershell -ExecutionPolicy Bypass -File "%~dp0launcher.ps1" %%command%% > "%~dp0..\steam_launch_option.txt"

echo.
echo ============================================
echo Paste this into Steam Launch Options:
type "%~dp0..\steam_launch_option.txt"
echo ============================================
pause
