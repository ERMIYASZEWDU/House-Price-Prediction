#!/usr/bin/env python3
"""
🏠 Simple House Price Predictor - Alternative Web Server
======================================================

This creates a simple HTTP server using Python's built-in modules
if Streamlit connection issues persist.
"""

import http.server
import socketserver
import webbrowser
import threading
import time
import json
import urllib.parse
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import os

# Load and prepare data
def load_data():
    try:
        df = pd.read_csv('Housing.csv')
        # Encode categorical variables
        df_processed = df.copy()
        categorical_mappings = {
            'mainroad': {'yes': 1, 'no': 0},
            'guestroom': {'yes': 1, 'no': 0},
            'basement': {'yes': 1, 'no': 0},
            'hotwaterheating': {'yes': 1, 'no': 0},
            'airconditioning': {'yes': 1, 'no': 0},
            'prefarea': {'yes': 1, 'no': 0},
            'furnishingstatus': {'furnished': 2, 'semi-furnished': 1, 'unfurnished': 0}
        }
        
        for col, mapping in categorical_mappings.items():
            df_processed[col] = df_processed[col].map(mapping)
        
        return df, df_processed
    except Exception as e:
        return None, None

# Train model
def train_model(df_processed):
    if df_processed is None:
        return None
    
    X = df_processed.drop('price', axis=1)
    y = df_processed['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    
    return model, score

# Initialize data and model
df_original, df_processed = load_data()
model, accuracy = train_model(df_processed) if df_processed is not None else (None, 0)

class HousePriceHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏠 House Price Predictor</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.5rem;
            font-weight: bold;
        }}
        
        .content {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            padding: 30px;
        }}
        
        .form-group {{
            margin-bottom: 20px;
        }}
        
        .form-group label {{
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #333;
        }}
        
        .form-group input, .form-group select {{
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }}
        
        .form-group input:focus, .form-group select:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .checkbox-group {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 10px;
        }}
        
        .checkbox-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .predict-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            margin-bottom: 20px;
            transition: transform 0.2s;
        }}
        
        .predict-btn:hover {{
            transform: translateY(-2px);
        }}
        
        .result-box {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 20px;
            display: none;
        }}
        
        .result-box.show {{
            display: block;
            animation: slideIn 0.5s ease-out;
        }}
        
        @keyframes slideIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 2px solid #e1e5e9;
        }}
        
        .stat-card h3 {{
            margin: 0 0 10px 0;
            color: #667eea;
        }}
        
        .stat-card p {{
            margin: 0;
            font-size: 18px;
            font-weight: bold;
        }}
        
        @media (max-width: 768px) {{
            .content {{
                grid-template-columns: 1fr;
            }}
            
            .checkbox-group {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏠 AI House Price Predictor</h1>
            <p>Powered by Machine Learning • Accuracy: {accuracy*100:.1f}% • Dataset: {len(df_original) if df_original is not None else 'N/A'} Houses</p>
        </div>
        
        <div class="content">
            <div class="input-section">
                <h2>🏡 Enter House Details</h2>
                
                <div class="form-group">
                    <label for="area">🏠 Area (Square Feet)</label>
                    <input type="range" id="area" name="area" min="1000" max="20000" value="5000" oninput="updateAreaDisplay(this.value)">
                    <div>Current: <span id="areaDisplay">5000</span> sq ft</div>
                </div>
                
                <div class="form-group">
                    <label for="bedrooms">🛏️ Number of Bedrooms</label>
                    <select id="bedrooms" name="bedrooms">
                        <option value="1">1 Bedroom</option>
                        <option value="2">2 Bedrooms</option>
                        <option value="3" selected>3 Bedrooms</option>
                        <option value="4">4 Bedrooms</option>
                        <option value="5">5 Bedrooms</option>
                        <option value="6">6 Bedrooms</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="bathrooms">🚿 Number of Bathrooms</label>
                    <select id="bathrooms" name="bathrooms">
                        <option value="1">1 Bathroom</option>
                        <option value="2" selected>2 Bathrooms</option>
                        <option value="3">3 Bathrooms</option>
                        <option value="4">4 Bathrooms</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="stories">🏢 Number of Stories</label>
                    <select id="stories" name="stories">
                        <option value="1">1 Story</option>
                        <option value="2" selected>2 Stories</option>
                        <option value="3">3 Stories</option>
                        <option value="4">4 Stories</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="parking">🚗 Parking Spaces</label>
                    <select id="parking" name="parking">
                        <option value="0">No Parking</option>
                        <option value="1" selected>1 Space</option>
                        <option value="2">2 Spaces</option>
                        <option value="3">3 Spaces</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="furnishing">🪑 Furnishing Status</label>
                    <select id="furnishing" name="furnishing">
                        <option value="0">Unfurnished</option>
                        <option value="1" selected>Semi-furnished</option>
                        <option value="2">Fully Furnished</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>🏠 House Features</label>
                    <div class="checkbox-group">
                        <div class="checkbox-item">
                            <input type="checkbox" id="mainroad" name="mainroad" checked>
                            <label for="mainroad">🛣️ Main Road Access</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="guestroom" name="guestroom">
                            <label for="guestroom">👥 Guest Room</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="basement" name="basement">
                            <label for="basement">🏠 Basement</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="hotwaterheating" name="hotwaterheating">
                            <label for="hotwaterheating">🔥 Hot Water Heating</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="airconditioning" name="airconditioning" checked>
                            <label for="airconditioning">❄️ Air Conditioning</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="prefarea" name="prefarea" checked>
                            <label for="prefarea">⭐ Preferred Area</label>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="result-section">
                <h2>💰 Price Prediction</h2>
                
                <button class="predict-btn" onclick="predictPrice()">
                    🔮 PREDICT HOUSE PRICE
                </button>
                
                <div id="resultBox" class="result-box">
                    <h2>🏠 PREDICTED PRICE</h2>
                    <div id="predictedPrice" style="font-size: 2.5rem; margin: 20px 0;"></div>
                    <div id="priceUSD" style="font-size: 1.2rem; opacity: 0.9;"></div>
                    <div id="marketAnalysis" style="margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.2); border-radius: 10px;"></div>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>🏠 Dataset</h3>
                        <p>{len(df_original) if df_original is not None else 'N/A'} Houses</p>
                    </div>
                    <div class="stat-card">
                        <h3>🤖 AI Model</h3>
                        <p>Linear Regression</p>
                    </div>
                    <div class="stat-card">
                        <h3>🎯 Accuracy</h3>
                        <p>{accuracy*100:.1f}%</p>
                    </div>
                    <div class="stat-card">
                        <h3>💰 Avg Price</h3>
                        <p>₹{df_original['price'].mean()/1000000:.1f}M</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function updateAreaDisplay(value) {{
            document.getElementById('areaDisplay').textContent = value;
        }}
        
        function predictPrice() {{
            // Collect form data
            const formData = {{
                area: parseInt(document.getElementById('area').value),
                bedrooms: parseInt(document.getElementById('bedrooms').value),
                bathrooms: parseInt(document.getElementById('bathrooms').value),
                stories: parseInt(document.getElementById('stories').value),
                parking: parseInt(document.getElementById('parking').value),
                furnishing: parseInt(document.getElementById('furnishing').value),
                mainroad: document.getElementById('mainroad').checked ? 1 : 0,
                guestroom: document.getElementById('guestroom').checked ? 1 : 0,
                basement: document.getElementById('basement').checked ? 1 : 0,
                hotwaterheating: document.getElementById('hotwaterheating').checked ? 1 : 0,
                airconditioning: document.getElementById('airconditioning').checked ? 1 : 0,
                prefarea: document.getElementById('prefarea').checked ? 1 : 0
            }};
            
            // Send prediction request
            fetch('/predict', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                }},
                body: JSON.stringify(formData)
            }})
            .then(response => response.json())
            .then(data => {{
                if (data.error) {{
                    alert('Error: ' + data.error);
                    return;
                }}
                
                // Display results
                document.getElementById('predictedPrice').innerHTML = '₹' + data.price.toLocaleString();
                document.getElementById('priceUSD').innerHTML = '≈ $' + Math.round(data.price / 83).toLocaleString() + ' USD';
                document.getElementById('marketAnalysis').innerHTML = data.analysis;
                document.getElementById('resultBox').classList.add('show');
            }})
            .catch(error => {{
                console.error('Error:', error);
                alert('Failed to get prediction. Please try again.');
            }});
        }}
    </script>
</body>
</html>
            """
            
            self.wfile.write(html_content.encode())
        
        elif self.path == '/predict' and hasattr(self, 'do_POST'):
            self.do_POST()
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/predict':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                
                if model is None:
                    self.send_json_response({"error": "Model not available. Please check Housing.csv file."})
                    return
                
                # Make prediction
                features = [[
                    data['area'], data['bedrooms'], data['bathrooms'], data['stories'],
                    data['mainroad'], data['guestroom'], data['basement'],
                    data['hotwaterheating'], data['airconditioning'], data['parking'],
                    data['prefarea'], data['furnishing']
                ]]
                
                prediction = model.predict(features)[0]
                
                # Market analysis
                if df_original is not None:
                    avg_price = df_original['price'].mean()
                    if prediction > avg_price * 1.2:
                        analysis = "📈 <strong>Above Market</strong> - This house is priced above average"
                    elif prediction < avg_price * 0.8:
                        analysis = "💰 <strong>Great Deal!</strong> - This house is below market rate"
                    else:
                        analysis = "📊 <strong>Market Rate</strong> - This house is fairly priced"
                else:
                    analysis = "📊 Price estimated using AI model"
                
                self.send_json_response({
                    "price": int(prediction),
                    "analysis": analysis
                })
                
            except Exception as e:
                self.send_json_response({"error": str(e)})
    
    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

def start_server():
    PORT = 8080
    try:
        with socketserver.TCPServer(("", PORT), HousePriceHandler) as httpd:
            print(f"🏠 House Price Predictor Server")
            print(f"🌐 Server running at: http://localhost:{PORT}")
            print(f"📊 Dataset: {len(df_original) if df_original is not None else 'Not loaded'} houses")
            print(f"🤖 Model accuracy: {accuracy*100:.1f}%" if accuracy else "🤖 Model: Not available")
            print(f"💡 Press Ctrl+C to stop")
            print("=" * 50)
            
            # Open browser
            def open_browser():
                time.sleep(1)
                webbrowser.open(f'http://localhost:{PORT}')
            
            threading.Thread(target=open_browser).start()
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    if not os.path.exists("Housing.csv"):
        print("❌ Error: Housing.csv not found!")
        print("Please make sure Housing.csv is in the same directory.")
        input("Press Enter to exit...")
    else:
        start_server()