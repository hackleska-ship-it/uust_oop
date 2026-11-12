@echo off
setlocal
cd /d "%~dp0"
if not exist build mkdir build
if exist "..\tools\zig\zig.exe" goto use_zig
where g++ >nul 2>nul
if errorlevel 1 goto try_cl
g++ -std=c++11 -Wall -Wextra -pedantic objects.cpp main.cpp -o build\lab2.exe
if errorlevel 1 goto failed
goto done

:use_zig
set "ZIG_GLOBAL_CACHE_DIR=%~dp0..\tools\zig-cache"
set "ZIG_LOCAL_CACHE_DIR=%~dp0build\zig-cache"
"..\tools\zig\zig.exe" c++ -std=c++11 -Wall -Wextra -pedantic objects.cpp main.cpp -o build\lab2.exe
if errorlevel 1 goto failed
goto done

:try_cl
where cl >nul 2>nul
if errorlevel 1 goto no_compiler
cl /nologo /EHsc /W4 /utf-8 objects.cpp main.cpp /Fe:build\lab2.exe
if errorlevel 1 goto failed
goto done

:done
echo Build finished successfully.
exit /b 0

:no_compiler
echo No C++ compiler found. Read START_HERE.md.
echo demo.bat can run the bundled program without rebuilding.
exit /b 2

:failed
echo Compilation failed. Read the compiler messages above.
exit /b 1
