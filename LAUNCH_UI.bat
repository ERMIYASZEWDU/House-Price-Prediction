@echo off
title House Price Predictor - Reliable Launcher
color 0A
cls

echo.
echo ===============================================
echo 🏠 HOUSE PRICE PREDICTOR - WEB APPLICATION
echo ===============================================
echo.

REM Check if we're in the right directory
if not exist "Housing.csv" (
    echo ❌ Error: Housing.csv not found!
    echo.
    echo Please make sure you are running this from the project directory
    echo that contains Housing.csv and app.py files.
    echo.
    echo Current directory: %CD%
    echo.
    pause
    exit /b 1
)

if not exist "app.py" (
    echo ❌ Error: app.py not found!
    echo Please make sure app.py is in the same folder.
    pause
    exit /b 1
)

echo ✅ Required files found!
echo.

REM Kill any existing streamlit processes
echo 🔄 Cleaning up any running processes...
taskkill /f /im "streamlit.exe" 2>nul
taskkill /f /im "python.exe" /fi "WINDOWTITLE eq Streamlit*" 2>nul

echo.
echo 📦 Checking Streamlit installation...

REM Check if streamlit is installed
python -c "import streamlit" 2>nul
if %errorlevel% neq 0 (
    echo 📦 Installing Streamlit and dependencies...
    pip install streamlit pandas numpy scikit-learn plotly
    if %errorlevel% neq 0 (
        echo ❌ Installation failed! Please install manually:
        echo pip install streamlit pandas numpy scikit-learn plotly
        pause
        exit /b 1
    )
)

echo ✅ Streamlit is ready!
echo.

REM Test with simple app first
echo 🧪 Running connection test...
echo.
echo Starting test server on port 8502...
echo If this works, we'll launch the main app.
echo.

start /min python -m streamlit run test_app.py --server.port 8502 --server.headless true

REM Wait a moment for test server to start
timeout /t 3 >nul

echo.
echo 🌐 Test server should be running at: http://localhost:8502
echo.
echo Please check if the test page opens in your browser.
echo If it works, press any key to launch the main app.
echo If not, press Ctrl+C to troubleshoot.
echo.
pause

REM Launch main app
echo.
echo 🚀 Launching main House Price Predictor app...
echo.
echo 🌐 Main app will be available at: http://localhost:8501
echo 💡 Press Ctrl+C in this window to stop the app
echo.

python -m streamlit run app.py --server.port 8501

echo.
echo 👋 Application stopped.
pause