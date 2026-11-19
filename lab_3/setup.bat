@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" goto install
if defined PYTHON_EXE (
    "%PYTHON_EXE%" -m venv .venv
    goto check
)
where py >nul 2>nul
if errorlevel 1 goto use_python
py -3 -m venv .venv
goto check
:use_python
python -m venv .venv
:check
if not exist ".venv\Scripts\python.exe" (
    echo Python 3.10 or newer is required. Install Python and run setup.bat again.
    exit /b 1
)
:install
".venv\Scripts\python.exe" -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)"
if errorlevel 1 (
    echo Python 3.10 or newer is required.
    exit /b 1
)
".venv\Scripts\python.exe" -m pip install -r requirements.txt
exit /b %errorlevel%
