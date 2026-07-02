@echo off
title House Price Predictor Web App
color 0A

echo.
echo ===============================================
echo 🏠 HOUSE PRICE PREDICTOR - WEB APPLICATION
echo ===============================================
echo.

REM Check if files exist
if not exist "Housing.csv" (
    echo ❌ Error: Housing.csv not found!
    echo Please make sure the dataset file is in this folder.
    pause
    exit /b 1
)

if not exist "app.py" (
    echo ❌ Error: app.py not found!
    pause
    exit /b 1
)

echo ✅ Files found successfully!
echo.
echo 🚀 Starting web application...
echo 🌐 This will open in your browser at: http://localhost:8501
echo 💡 Press Ctrl+C to stop the application
echo.

REM Try to run streamlit directly first
streamlit run app.py 2>nul
if %errorlevel%==0 goto :end

echo.
echo 📦 Installing Streamlit (first time only)...
pip install streamlit pandas numpy scikit-learn plotly

echo.
echo 🚀 Launching application...
streamlit run app.py

:end
echo.
echo 👋 Application stopped.
pause