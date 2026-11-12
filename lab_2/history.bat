@echo off
setlocal
where git >nul 2>nul
if errorlevel 1 goto bundled_git
git -C "%~dp0.." log --oneline --reverse
goto done

:bundled_git
if not exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe" goto missing
"%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe" -C "%~dp0.." log --oneline --reverse
goto done

:missing
echo Git was not found. Install Git to show the repository history.

:done
if /i "%~1"=="--no-pause" exit /b 0
pause
