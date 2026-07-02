"""
🚀 Simple House Price Predictor Launcher
========================================

This script launches the web UI for house price prediction.
"""

import subprocess
import sys
import os

def main():
    print("🏠 House Price Predictor - Starting Web App...")
    print("="*50)
    
    # Check if Housing.csv exists
    if not os.path.exists("Housing.csv"):
        print("❌ Error: Housing.csv not found!")
        print("Please make sure Housing.csv is in the same directory.")
        input("Press Enter to exit...")
        return
    
    # Check if app.py exists
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found!")
        input("Press Enter to exit...")
        return
    
    print("🚀 Starting Streamlit application...")
    print("🌐 This will open in your browser at: http://localhost:8501")
    print("💡 Press Ctrl+C in this window to stop the app")
    print("="*50)
    
    try:
        # Run streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped!")
    except FileNotFoundError:
        print("❌ Streamlit not installed. Installing now...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit", "plotly"])
        print("✅ Installation complete. Please run this script again.")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()