@echo off
setlocal
cd /d "%~dp0"
if not exist build\lab2.exe goto missing
echo Running bundled demo. Source changes require run.bat to rebuild.
build\lab2.exe
set "LAB2_EXIT_CODE=%errorlevel%"
if /i "%~1"=="--no-pause" exit /b %LAB2_EXIT_CODE%
pause
exit /b %LAB2_EXIT_CODE%

:missing
echo Bundled program not found. Run run.bat to build it first.
if /i "%~1"=="--no-pause" exit /b 1
pause
exit /b 1
