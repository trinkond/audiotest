@echo off
setlocal EnableExtensions EnableDelayedExpansion

echo Installing Audiotest dependencies, written by Ondrej Trinkewitz in 2026 at CTU Prague
echo Checking Python version

where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not available in the PATH. Make sure, it is installed correctly.
	pause
    exit /b 1
)

for /f "tokens=2 delims= " %%V in ('python --version 2^>^&1') do (
    set PY_VER=%%V
)

for /f "tokens=1,2 delims=." %%A in ("!PY_VER!") do (
    set PY_MAJOR=%%A
    set PY_MINOR=%%B
)

echo Detected Python version: !PY_VER!
if not "!PY_MAJOR!.!PY_MINOR!"=="3.12" (
    echo [WARNING] The app was developed with Python version 3.12, but !PY_MAJOR!.!PY_MINOR! is installed.
    echo [WARNING] Some features might not work properly.
)

echo.
echo Installing required packages...
python -m pip install requests audiomath PyQt6
if errorlevel 1 (
	echo.
    echo [ERROR] Package installation failed.
	echo Dependencies weren't installed.
	pause
    exit /b 1
)

echo.
echo The app dependencies were installed successfully.
pause
exit /b 0