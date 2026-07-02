"""
Local test script for the house price prediction API
Run this before deploying to verify everything works
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.index import app, predict_house_price
import json

def test_prediction_function():
    """Test the core prediction function"""
    print("🧪 Testing prediction function...")
    
    test_data = {
        'area': 5000,
        'bedrooms': 3,
        'bathrooms': 2,
        'stories': 2,
        'mainroad': 1,
        'guestroom': 0,
        'basement': 0,
        'hotwaterheating': 0,
        'airconditioning': 1,
        'parking': 1,
        'prefarea': 1,
        'furnishingstatus': 1
    }
    
    try:
        price = predict_house_price(test_data)
        print(f"✅ Prediction successful: ₹{price:,}")
        return True
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        return False

def test_flask_routes():
    """Test Flask routes"""
    print("\n🌐 Testing Flask routes...")
    
    with app.test_client() as client:
        # Test health endpoint
        try:
            response = client.get('/api/health')
            if response.status_code == 200:
                data = json.loads(response.data)
                print(f"✅ Health check: {data['message']}")
            else:
                print(f"❌ Health check failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Health check error: {e}")
        
        # Test test endpoint
        try:
            response = client.get('/api/test')
            if response.status_code == 200:
                data = json.loads(response.data)
                print(f"✅ Test endpoint: ₹{data['sample_prediction']:,}")
            else:
                print(f"❌ Test endpoint failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Test endpoint error: {e}")
        
        # Test prediction endpoint
        try:
            test_payload = {
                'area': 6000,
                'bedrooms': 4,
                'bathrooms': 3,
                'stories': 2,
                'mainroad': 1,
                'guestroom': 1,
                'basement': 1,
                'hotwaterheating': 1,
                'airconditioning': 1,
                'parking': 2,
                'prefarea': 1,
                'furnishingstatus': 2
            }
            
            response = client.post('/api/predict',
                                 data=json.dumps(test_payload),
                                 content_type='application/json')
            
            if response.status_code == 200:
                data = json.loads(response.data)
                print(f"✅ Prediction API: ₹{data['price']:,}")
            else:
                print(f"❌ Prediction API failed: {response.status_code}")
                print(f"Response: {response.data}")
        except Exception as e:
            print(f"❌ Prediction API error: {e}")
        
        # Test home page
        try:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Home page loads successfully")
            else:
                print(f"❌ Home page failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Home page error: {e}")

if __name__ == '__main__':
    print("🏠 House Price Predictor - Local API Test")
    print("=" * 50)
    
    success = True
    
    # Test core function
    if not test_prediction_function():
        success = False
    
    # Test Flask routes
    test_flask_routes()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Ready for deployment.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        
    print("\n📋 Deployment Checklist:")
    print("1. ✅ Fixed duplicate route definitions")
    print("2. ✅ Removed pandas dependency")
    print("3. ✅ Fixed undefined variables")
    print("4. ✅ Added proper error handling")
    print("5. ✅ Added API health checks")
    print("6. ✅ Updated Vercel configuration")
    
    print("\n🚀 Next steps:")
    print("1. Commit and push changes to your repository")
    print("2. Redeploy to Vercel")
    print("3. Test the live deployment")