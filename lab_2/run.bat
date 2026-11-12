@echo off
setlocal
cd /d "%~dp0"
call "%~dp0build.bat"
if errorlevel 1 goto failed
build\lab2.exe
set "LAB2_EXIT_CODE=%errorlevel%"
echo.
echo Program finished with exit code %LAB2_EXIT_CODE%.
if /i "%~1"=="--no-pause" exit /b %LAB2_EXIT_CODE%
pause
exit /b %LAB2_EXIT_CODE%

:failed
if /i "%~1"=="--no-pause" exit /b 1
pause
exit /b 1
