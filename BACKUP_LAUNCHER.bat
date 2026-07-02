@echo off
cls
title House Price Predictor - Backup Web Server
color 0A

echo.
echo ===============================================
echo 🏠 HOUSE PRICE PREDICTOR - BACKUP LAUNCHER
echo ===============================================
echo.
echo This launcher uses Python's built-in web server
echo if Streamlit connection issues persist.
echo.

REM Check required files
if not exist "Housing.csv" (
    echo ❌ Housing.csv not found!
    echo Please ensure the dataset is in this folder.
    pause
    exit /b 1
)

if not exist "simple_web_app.py" (
    echo ❌ simple_web_app.py not found!
    pause
    exit /b 1
)

echo ✅ Required files found!
echo.

echo 🚀 Starting backup web server...
echo 🌐 This will open at: http://localhost:8080
echo ⏳ Please wait for "Server running at" message...
echo.
echo 💡 This is a simplified version that works without Streamlit
echo 🛑 To stop: Press Ctrl+C in this window
echo.

python simple_web_app.py

echo.
echo 👋 Server stopped.
pause