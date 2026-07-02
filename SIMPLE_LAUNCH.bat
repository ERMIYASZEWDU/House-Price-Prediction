@echo off
cls
echo 🏠 House Price Predictor - Simple Launcher
echo ==========================================
echo.

REM Check files
if not exist "Housing.csv" (
    echo ❌ Housing.csv not found!
    pause
    exit
)

if not exist "app.py" (
    echo ❌ app.py not found!
    pause  
    exit
)

echo ✅ Files found!
echo.
echo 🚀 Starting web application...
echo 🌐 Opening at: http://localhost:8501
echo.
echo ⏳ Please wait 10-15 seconds for the app to load...
echo 🌐 Your browser should open automatically
echo 💡 If not, manually go to: http://localhost:8501
echo.
echo 🛑 To stop: Press Ctrl+C in this window
echo.

REM Launch the app
python -m streamlit run app.py --server.port 8501 --server.address localhost

pause