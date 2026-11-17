@echo off
setlocal
cd /d "%~dp0"
if not exist build mkdir build
if defined ZIG_EXE goto check_zig
if exist "..\tools\zig\zig.exe" (
    set "ZIG_EXE=%~dp0..\tools\zig\zig.exe"
    goto use_zig
)
where g++ >nul 2>nul
if errorlevel 1 goto try_cl
g++ -std=c++11 -Wall -Wextra -pedantic -Werror objects.cpp main.cpp -o build\lab2.exe
if errorlevel 1 goto failed
goto done

:check_zig
if exist "%ZIG_EXE%" goto use_zig
echo ZIG_EXE does not point to an existing zig.exe.
exit /b 2

:use_zig
set "ZIG_GLOBAL_CACHE_DIR=%~dp0build\zig-global-cache"
set "ZIG_LOCAL_CACHE_DIR=%~dp0build\zig-cache"
"%ZIG_EXE%" c++ -std=c++11 -Wall -Wextra -pedantic -Werror objects.cpp main.cpp -o build\lab2.exe
if errorlevel 1 goto failed
goto done

:try_cl
where cl >nul 2>nul
if errorlevel 1 goto no_compiler
cl /nologo /EHsc /W4 /WX /utf-8 objects.cpp main.cpp /Fe:build\lab2.exe /Fo:build\
if errorlevel 1 goto failed
goto done

:done
echo Build finished successfully.
exit /b 0

:no_compiler
echo No C++ compiler found. Read START_HERE.md.
echo Use g++, a Visual Studio Developer Command Prompt, or set ZIG_EXE.
exit /b 2

:failed
echo Compilation failed. Read the compiler messages above.
exit /b 1
