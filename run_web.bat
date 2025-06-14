@echo off
title Object Detection Web Interface
color 0A

echo.
echo ============================================
echo   🚀 Object Detection Web Interface
echo ============================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo ❌ Virtual environment not found!
    echo Please run setup.ps1 first to create the environment.
    echo.
    pause
    exit /b 1
)

echo 🔧 Activating virtual environment...
call "venv\Scripts\activate.bat"

if errorlevel 1 (
    echo ❌ Failed to activate virtual environment!
    pause
    exit /b 1
)

echo ✅ Virtual environment activated
echo.

echo 🌐 Starting optimized web server...
echo 📱 Access at: http://127.0.0.1:5000
echo 📷 Camera page: http://127.0.0.1:5000/camera
echo.
echo ⚡ Performance optimizations active:
echo   - Model caching
echo   - Frame skipping for live detection
echo   - GPU acceleration (if available)
echo   - Optimized image processing
echo.
echo 💡 Press Ctrl+C to stop the server
echo.

REM Start the web interface
python web_interface.py

if errorlevel 1 (
    echo.
    echo ❌ Failed to start web interface!
    echo Check if all dependencies are installed.
    pause
    exit /b 1
)

echo.
echo ✅ Web interface stopped.
pause
