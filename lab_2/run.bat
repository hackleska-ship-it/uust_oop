@echo off
setlocal
cd /d "%~dp0"
if not exist build mkdir build
where g++ >nul 2>nul
if errorlevel 1 goto try_cl
g++ -std=c++11 -Wall -Wextra -pedantic objects.cpp main.cpp -o build\lab2.exe
if errorlevel 1 goto build_failed
goto run

:try_cl
where cl >nul 2>nul
if errorlevel 1 goto no_compiler
cl /nologo /EHsc /W4 /utf-8 objects.cpp main.cpp /Fe:build\lab2.exe
if errorlevel 1 goto build_failed
goto run

:run
build\lab2.exe
if errorlevel 1 goto run_failed
echo.
echo Program finished successfully.
pause
exit /b 0

:no_compiler
echo No C++ compiler found in PATH.
echo Read START_HERE.md. VS Code alone is not a compiler.
echo For Visual Studio, use Developer Command Prompt or create a C++ project.
pause
exit /b 1

:build_failed
echo Compilation failed. Read the compiler messages above.
pause
exit /b 1

:run_failed
echo Program returned a non-zero exit code.
pause
exit /b 1
