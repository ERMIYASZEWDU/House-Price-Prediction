"""
🔧 House Price Predictor - Troubleshooting Script
================================================

This script diagnoses and fixes common issues with the web application.
"""

import subprocess
import sys
import os
import socket

def check_port(port):
    """Check if a port is available"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result != 0  # True if port is available

def check_files():
    """Check if required files exist"""
    required_files = ['Housing.csv', 'app.py', 'test_app.py']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    return missing_files

def check_python_packages():
    """Check if required packages are installed"""
    required_packages = ['streamlit', 'pandas', 'numpy', 'scikit-learn', 'plotly']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_packages(packages):
    """Install missing packages"""
    for package in packages:
        print(f"📦 Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    return True

def kill_streamlit_processes():
    """Kill any running Streamlit processes"""
    try:
        # Windows
        subprocess.run(["taskkill", "/f", "/im", "streamlit.exe"], 
                      capture_output=True, text=True)
        subprocess.run(["taskkill", "/f", "/im", "python.exe", "/fi", "WINDOWTITLE eq *streamlit*"], 
                      capture_output=True, text=True)
    except:
        pass

def main():
    print("🔧 House Price Predictor - Troubleshooting Tool")
    print("=" * 60)
    
    # Step 1: Check files
    print("\n📁 Step 1: Checking required files...")
    missing_files = check_files()
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        print("Please ensure all required files are in the same directory.")
        return False
    else:
        print("✅ All required files found!")
    
    # Step 2: Check Python packages
    print("\n📦 Step 2: Checking Python packages...")
    missing_packages = check_python_packages()
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        if not install_packages(missing_packages):
            return False
    else:
        print("✅ All required packages installed!")
    
    # Step 3: Check ports
    print("\n🌐 Step 3: Checking network ports...")
    ports_to_check = [8501, 8502, 8503]
    available_port = None
    
    for port in ports_to_check:
        if check_port(port):
            available_port = port
            print(f"✅ Port {port} is available!")
            break
        else:
            print(f"⚠️ Port {port} is busy")
    
    if not available_port:
        print("❌ No available ports found. Cleaning up processes...")
        kill_streamlit_processes()
        available_port = 8501
    
    # Step 4: Test launch
    print(f"\n🚀 Step 4: Testing Streamlit launch on port {available_port}...")
    
    try:
        print("🧪 Starting test application...")
        print(f"🌐 URL: http://localhost:{available_port}")
        print("💡 Check if browser opens. Press Ctrl+C to continue to main app.")
        
        # Launch test app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "test_app.py", 
            f"--server.port={available_port}"
        ])
        
    except KeyboardInterrupt:
        print("\n✅ Test completed!")
    except Exception as e:
        print(f"❌ Error launching test app: {e}")
        return False
    
    # Step 5: Launch main app
    print(f"\n🏠 Step 5: Launching main House Price Predictor...")
    
    try:
        print(f"🌐 Main app URL: http://localhost:8501")
        print("💡 Press Ctrl+C to stop the application")
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py", 
            "--server.port=8501"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped!")
    except Exception as e:
        print(f"❌ Error launching main app: {e}")
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("✅ Troubleshooting completed successfully!")
        else:
            print("❌ Some issues remain. Please check the error messages above.")
    except KeyboardInterrupt:
        print("\n👋 Troubleshooting interrupted by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    input("\nPress Enter to exit...")