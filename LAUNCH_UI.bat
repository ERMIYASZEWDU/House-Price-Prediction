@echo off
title House Price Predictor - Web UI Launcher
color 0A

echo.
echo ===============================================
echo 🏠 HOUSE PRICE PREDICTOR - WEB UI LAUNCHER
echo ===============================================
echo.
echo 🚀 Starting Beautiful Web Application...
echo 💻 This will open in your browser automatically
echo 🌐 URL: http://localhost:8501
echo.
echo ⏳ Please wait while we prepare everything...
echo.

REM Install requirements
echo 📦 Installing packages...
pip install streamlit pandas numpy scikit-learn plotly

echo.
echo ✅ Packages installed successfully!
echo.
echo 🚀 Launching web application...
echo 💡 Press Ctrl+C to stop the application
echo.

REM Run the Streamlit app
streamlit run app.py

pause