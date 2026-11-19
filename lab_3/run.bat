@echo off
setlocal
cd /d "%~dp0"
if "%~1"=="circles" goto valid
if "%~1"=="mvc" goto valid
echo Usage: run.bat circles^|mvc
exit /b 2
:valid
if not "%~2"=="" exit /b 2
if not exist ".venv\Scripts\python.exe" (
    echo Run setup.bat first. Python 3.10 or newer is required.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" run.py "%~1"
set "LAB3_EXIT=%errorlevel%"
if not "%LAB3_EXIT%"=="0" pause
exit /b %LAB3_EXIT%
