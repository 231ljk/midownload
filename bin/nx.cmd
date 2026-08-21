@echo off
REM Nx Programming Language - CLI Wrapper (Windows)
REM Version: 0.1.0 (Developer Preview)
setlocal

set "SCRIPT_DIR=%~dp0"
set "INTERPRETER=%SCRIPT_DIR%nx_interpreter.py"

where python >nul 2>nul
if %errorlevel%==0 (
    python "%INTERPRETER%" %*
    goto :eof
)

where py >nul 2>nul
if %errorlevel%==0 (
    py "%INTERPRETER%" %*
    goto :eof
)

echo Error: Python 3 is required to run Nx.
echo Please install Python 3 from https://python.org
echo.
echo During installation, make sure to check "Add Python to PATH".
exit /b 1
