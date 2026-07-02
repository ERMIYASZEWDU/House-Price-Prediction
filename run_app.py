"""
🚀 House Price Predictor - Web Application Launcher
==================================================

This script launches the beautiful web UI for the house price prediction project.
Run this file to start the interactive web application.

Author: ERMIYASZEWDU
Project: House Price Prediction ML
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages. Please install manually:")
        print("pip install streamlit pandas numpy scikit-learn plotly")
        return False

def run_streamlit_app():
    """Launch the Streamlit web application"""
    print("🚀 Launching House Price Predictor Web App...")
    print("🌐 Opening in your default web browser...")
    print("📍 URL: http://localhost:8501")
    print("\n" + "="*60)
    print("🏠 HOUSE PRICE PREDICTOR - WEB APPLICATION")
    print("="*60)
    print("✨ Features:")
    print("   🎯 Interactive Price Prediction")
    print("   📊 Market Analytics Dashboard")
    print("   🔬 AI Model Performance")
    print("   💡 Beautiful Modern UI")
    print("="*60)
    print("\n💡 Tip: Press Ctrl+C to stop the application")
    
    try:
        # Run streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError:
        print("❌ Failed to run Streamlit. Please run manually:")
        print("streamlit run app.py")

def main():
    """Main function to run the application"""
    print("🏠 House Price Predictor - Web UI Launcher")
    print("="*50)
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return
    
    # Check if app.py exists
    if not os.path.exists("app.py"):
        print("❌ app.py not found!")
        return
    
    # Install requirements and run app
    if install_requirements():
        print("\n🚀 Starting web application...")
        run_streamlit_app()

if __name__ == "__main__":
    main()