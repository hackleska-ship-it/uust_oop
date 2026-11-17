@echo off
setlocal
cd /d "%~dp0"
set "LAB2_SECTION=all"
set "LAB2_NO_PAUSE="
if not "%~3"=="" goto usage
if /i "%~1"=="--no-pause" (
    if not "%~2"=="" goto usage
    set "LAB2_NO_PAUSE=1"
) else (
    if not "%~1"=="" set "LAB2_SECTION=%~1"
    if not "%~2"=="" if /i not "%~2"=="--no-pause" goto usage
    if /i "%~2"=="--no-pause" set "LAB2_NO_PAUSE=1"
)
if not exist build\lab2.exe goto missing
echo Running the existing build. Use run.bat after source changes.
build\lab2.exe "%LAB2_SECTION%"
set "LAB2_EXIT_CODE=%errorlevel%"
if defined LAB2_NO_PAUSE exit /b %LAB2_EXIT_CODE%
pause
exit /b %LAB2_EXIT_CODE%

:missing
echo build\lab2.exe was not found. Run build.bat or run.bat first.
if defined LAB2_NO_PAUSE exit /b 1
pause
exit /b 1

:usage
echo Usage: demo.bat [all^|point^|plain^|inheritance^|value^|pointer] [--no-pause]
exit /b 2
