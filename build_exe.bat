@echo off
setlocal

cd /d "%~dp0"
title Build Secret Scroll Caesar Cipher

echo =====================================================
echo   Secret Scroll Caesar Cipher - Windows EXE Builder
echo =====================================================
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python was not found in PATH.
    echo Install Python 3.8 or newer and select "Add Python to PATH".
    pause
    exit /b 1
)

echo [1/3] Checking pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not available for this Python installation.
    pause
    exit /b 1
)

echo [2/3] Installing or updating PyInstaller...
python -m pip install --upgrade pyinstaller
if errorlevel 1 (
    echo [ERROR] PyInstaller installation failed.
    pause
    exit /b 1
)

echo [3/3] Building the executable...
python -m PyInstaller --noconfirm --clean --onefile --windowed --name "SecretScrollCaesarCipher" secret_scroll.py
if errorlevel 1 (
    echo [ERROR] The build failed. Review the messages above.
    pause
    exit /b 1
)

echo.
echo =====================================================
echo   Build completed successfully.
echo   Output: dist\SecretScrollCaesarCipher.exe
echo =====================================================
echo.
pause
endlocal
