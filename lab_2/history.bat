@echo off
setlocal
where git >nul 2>nul
if errorlevel 1 goto missing
git -C "%~dp0.." log --oneline --reverse
set "LAB2_EXIT_CODE=%errorlevel%"
goto done

:missing
echo Git was not found. Install Git and add it to PATH to show the history.
set "LAB2_EXIT_CODE=2"

:done
if /i "%~1"=="--no-pause" exit /b %LAB2_EXIT_CODE%
pause
exit /b %LAB2_EXIT_CODE%
