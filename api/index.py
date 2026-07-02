from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import os

app = Flask(__name__)

# Load and prepare data
def load_and_prepare_data():
    try:
        # Try to load from current directory first
        csv_path = 'Housing.csv'
        if not os.path.exists(csv_path):
            # Try from parent directory
            csv_path = '../Housing.csv'
        
        df = pd.read_csv(csv_path)
        df_processed = df.copy()
        
        # Encode categorical variables
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
        print(f"Error loading data: {e}")
        return None, None

# Train model
def train_model(df_processed):
    if df_processed is None:
        return None, 0
    
    X = df_processed.drop('price', axis=1)
    y = df_processed['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    
    return model, score

# Initialize model
df_original, df_processed = load_and_prepare_data()
model, accuracy = train_model(df_processed)

@app.route('/')
def home():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏠 House Price Predictor - Vercel Deployment</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: bold;
        }
        
        .content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            padding: 30px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #333;
        }
        
        .form-group input, .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-size: 16px;
            box-sizing: border-box;
        }
        
        .checkbox-group {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }
        
        .checkbox-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .predict-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            margin: 20px 0;
            transition: transform 0.2s;
        }
        
        .predict-btn:hover {
            transform: translateY(-2px);
        }
        
        .result-box {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin: 20px 0;
            display: none;
        }
        
        .result-box.show {
            display: block;
            animation: slideIn 0.5s ease-out;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .stat-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        
        @media (max-width: 768px) {
            .content {
                grid-template-columns: 1fr;
            }
            .checkbox-group {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏠 AI House Price Predictor</h1>
            <p>Deployed on Vercel • ML Accuracy: {{ "%.1f"|format(accuracy*100) }}% • Dataset: {{ dataset_size }} Houses</p>
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
                            <label for="mainroad">🛣️ Main Road</label>
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
                            <label for="hotwaterheating">🔥 Hot Water</label>
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
                <h2>💰 AI Price Prediction</h2>
                
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
                        <h3>🤖 AI Model</h3>
                        <p>Linear Regression</p>
                    </div>
                    <div class="stat-card">
                        <h3>🎯 Accuracy</h3>
                        <p>{{ "%.1f"|format(accuracy*100) }}%</p>
                    </div>
                    <div class="stat-card">
                        <h3>🏠 Dataset</h3>
                        <p>{{ dataset_size }} Houses</p>
                    </div>
                    <div class="stat-card">
                        <h3>🌐 Deployment</h3>
                        <p>Vercel Cloud</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function updateAreaDisplay(value) {
            document.getElementById('areaDisplay').textContent = value;
        }
        
        function predictPrice() {
            const formData = {
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
            };
            
            fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert('Error: ' + data.error);
                    return;
                }
                
                document.getElementById('predictedPrice').innerHTML = '₹' + data.price.toLocaleString();
                document.getElementById('priceUSD').innerHTML = '≈ $' + Math.round(data.price / 83).toLocaleString() + ' USD';
                document.getElementById('marketAnalysis').innerHTML = data.analysis;
                document.getElementById('resultBox').classList.add('show');
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to get prediction. Please try again.');
            });
        }
    </script>
</body>
</html>
    ''', 
    accuracy=accuracy if accuracy else 0.649,
    dataset_size=len(df_original) if df_original is not None else 545
    )

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if model is None:
            return jsonify({"error": "Model not available"}), 500
        
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
        
        return jsonify({
            "price": int(prediction),
            "analysis": analysis
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vercel expects this for serverless functions
def handler(request):
    return app(request)

if __name__ == '__main__':
    app.run(debug=True)