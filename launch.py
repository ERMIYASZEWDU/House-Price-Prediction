#!/usr/bin/env python3
"""
🚀 Simple House Price Predictor Launcher
========================================
"""

import subprocess
import sys
import os
import time

def main():
    print("🏠 House Price Predictor - Starting Web App")
    print("=" * 50)
    
    # Check files
    if not os.path.exists("Housing.csv"):
        print("❌ Error: Housing.csv not found!")
        print("Please make sure Housing.csv is in the same directory.")
        input("Press Enter to exit...")
        return
    
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found!")
        input("Press Enter to exit...")
        return
    
    print("✅ Required files found!")
    print()
    
    # Install streamlit if needed
    try:
        import streamlit
        print("✅ Streamlit is installed")
    except ImportError:
        print("📦 Installing Streamlit...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit", "plotly"])
    
    print()
    print("🚀 Starting House Price Predictor Web App...")
    print("🌐 URL: http://localhost:8501")
    print("⏳ Please wait 10-15 seconds for the app to load...")
    print("🌐 Your browser should open automatically")
    print()
    print("💡 If browser doesn't open, manually go to: http://localhost:8501")
    print("🛑 To stop the app: Press Ctrl+C")
    print("=" * 50)
    print()
    
    try:
        # Launch streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure Python is installed")
        print("2. Run: pip install streamlit pandas numpy scikit-learn plotly")
        print("3. Check if another app is using port 8501")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()