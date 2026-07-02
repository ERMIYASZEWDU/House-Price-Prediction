# 🧪 How to Test Your Housing Price Prediction Model

This guide shows you **5 different ways** to test your trained model.

---

## ✅ Method 1: Test with Existing Test Data (Already Done!)

Your notebook **already tests** the model using the test set (20% of data).

**Location:** After each model training (Uni-variate, Bi-variate, Multi-variate)

**What it shows:**
- R² Score (how well model fits)
- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)
- Scatter plots showing predicted vs actual prices

**This is automatic** - runs when you execute the model cells.

---

## ✅ Method 2: Predict Price for a NEW House (Manual Input)

Add this cell after your conclusions to predict for a house you describe:

```python
## 10. Test Model with New Data

### Predict Price for a Custom House

# Create a new house with your specifications
new_house = pd.DataFrame({
    'area': [5000],              # Square feet
    'bedrooms': [3],             # Number of bedrooms
    'bathrooms': [2],            # Number of bathrooms
    'stories': [2],              # Number of stories
    'mainroad': [1],             # 1=yes, 0=no
    'guestroom': [0],            # 1=yes, 0=no
    'basement': [1],             # 1=yes, 0=no
    'hotwaterheating': [0],      # 1=yes, 0=no
    'airconditioning': [1],      # 1=yes, 0=no
    'parking': [2],              # Number of parking spaces
    'prefarea': [1],             # 1=yes, 0=no
    'furnishingstatus': [0]      # 0=furnished, 1=semi-furnished, 2=unfurnished
})

print("House Specifications:")
print("="*60)
print(f"Area: {new_house['area'][0]} sqft")
print(f"Bedrooms: {new_house['bedrooms'][0]}")
print(f"Bathrooms: {new_house['bathrooms'][0]}")
print(f"Stories: {new_house['stories'][0]}")
print(f"Mainroad: {'Yes' if new_house['mainroad'][0] == 1 else 'No'}")
print(f"Guestroom: {'Yes' if new_house['guestroom'][0] == 1 else 'No'}")
print(f"Basement: {'Yes' if new_house['basement'][0] == 1 else 'No'}")
print(f"Hot Water Heating: {'Yes' if new_house['hotwaterheating'][0] == 1 else 'No'}")
print(f"Air Conditioning: {'Yes' if new_house['airconditioning'][0] == 1 else 'No'}")
print(f"Parking: {new_house['parking'][0]} spaces")
print(f"Preferred Area: {'Yes' if new_house['prefarea'][0] == 1 else 'No'}")
print("="*60)

# Predict using the BEST model (Multi-variate)
predicted_price = model_multi.predict(new_house)[0]

print(f"\n💰 Predicted Price: ₹{predicted_price:,.2f}")
print(f"💰 Predicted Price: ${predicted_price/80:,.2f} USD")  # Approx conversion

# Compare with average price
avg_price = y.mean()
difference = predicted_price - avg_price
percentage = (difference / avg_price) * 100

print(f"\n📊 Comparison:")
print(f"   Average price in dataset: ₹{avg_price:,.2f}")
print(f"   Difference: ₹{difference:,.2f} ({percentage:+.1f}%)")
```

---

## ✅ Method 3: Test with Random Houses from Dataset

Test how well the model predicts for **random houses** from your data:

```python
### Test with 5 Random Houses from Dataset

# Select 5 random houses from test set
import random
random_indices = random.sample(range(len(X_test)), 5)

print("\n" + "="*80)
print("TESTING WITH 5 RANDOM HOUSES FROM DATASET")
print("="*80)

for i, idx in enumerate(random_indices, 1):
    actual_price = y_test.iloc[idx]
    predicted_price = model_multi.predict(X_test.iloc[[idx]])[0]
    error = abs(actual_price - predicted_price)
    error_percentage = (error / actual_price) * 100
    
    print(f"\n🏠 House #{i}:")
    print(f"   Area: {X_test.iloc[idx]['area']} sqft")
    print(f"   Bedrooms: {X_test.iloc[idx]['bedrooms']}")
    print(f"   Bathrooms: {X_test.iloc[idx]['bathrooms']}")
    print(f"   Actual Price:     ₹{actual_price:,.2f}")
    print(f"   Predicted Price:  ₹{predicted_price:,.2f}")
    print(f"   Error:            ₹{error:,.2f} ({error_percentage:.1f}%)")
    
    if error_percentage < 10:
        print(f"   Status: ✅ Excellent prediction!")
    elif error_percentage < 20:
        print(f"   Status: ✓ Good prediction")
    else:
        print(f"   Status: ⚠️ Could be better")

print("\n" + "="*80)
```

---

## ✅ Method 4: Test Model Accuracy (Statistical Test)

Check overall model performance:

```python
### Overall Model Performance

from sklearn.metrics import mean_absolute_percentage_error

# Predict all test prices
y_test_pred = model_multi.predict(X_test)

# Calculate metrics
mape = mean_absolute_percentage_error(y_test, y_test_pred) * 100
r2 = r2_score(y_test, y_test_pred)

# Count predictions within certain error ranges
errors = np.abs(y_test - y_test_pred)
error_percentages = (errors / y_test) * 100

within_10_percent = np.sum(error_percentages < 10)
within_20_percent = np.sum(error_percentages < 20)
within_30_percent = np.sum(error_percentages < 30)

print("\n" + "="*80)
print("MODEL ACCURACY REPORT")
print("="*80)
print(f"\n📈 Overall Metrics:")
print(f"   R² Score: {r2:.4f} (explains {r2*100:.2f}% of variance)")
print(f"   Mean Absolute Percentage Error (MAPE): {mape:.2f}%")
print(f"\n📊 Prediction Accuracy Distribution:")
print(f"   Predictions within ±10% of actual price: {within_10_percent}/{len(y_test)} ({within_10_percent/len(y_test)*100:.1f}%)")
print(f"   Predictions within ±20% of actual price: {within_20_percent}/{len(y_test)} ({within_20_percent/len(y_test)*100:.1f}%)")
print(f"   Predictions within ±30% of actual price: {within_30_percent}/{len(y_test)} ({within_30_percent/len(y_test)*100:.1f}%)")
print("\n" + "="*80)
```

---

## ✅ Method 5: Interactive Testing (User Input)

Let users input house details and get predictions:

```python
### Interactive House Price Predictor

def predict_house_price():
    """Interactive function to predict house price based on user input"""
    
    print("\n" + "="*80)
    print("🏠 INTERACTIVE HOUSE PRICE PREDICTOR")
    print("="*80)
    print("\nEnter house details (press Enter for default values):\n")
    
    # Get user inputs
    area = int(input("Area (sqft) [default: 5000]: ") or 5000)
    bedrooms = int(input("Number of bedrooms [default: 3]: ") or 3)
    bathrooms = int(input("Number of bathrooms [default: 2]: ") or 2)
    stories = int(input("Number of stories [default: 2]: ") or 2)
    mainroad = int(input("On main road? (1=yes, 0=no) [default: 1]: ") or 1)
    guestroom = int(input("Has guestroom? (1=yes, 0=no) [default: 0]: ") or 0)
    basement = int(input("Has basement? (1=yes, 0=no) [default: 1]: ") or 1)
    hotwater = int(input("Hot water heating? (1=yes, 0=no) [default: 0]: ") or 0)
    aircon = int(input("Air conditioning? (1=yes, 0=no) [default: 1]: ") or 1)
    parking = int(input("Parking spaces [default: 2]: ") or 2)
    prefarea = int(input("Preferred area? (1=yes, 0=no) [default: 1]: ") or 1)
    furnish = int(input("Furnishing (0=furnished, 1=semi, 2=unfurnished) [default: 0]: ") or 0)
    
    # Create DataFrame
    house = pd.DataFrame({
        'area': [area], 'bedrooms': [bedrooms], 'bathrooms': [bathrooms],
        'stories': [stories], 'mainroad': [mainroad], 'guestroom': [guestroom],
        'basement': [basement], 'hotwaterheating': [hotwater], 
        'airconditioning': [aircon], 'parking': [parking],
        'prefarea': [prefarea], 'furnishingstatus': [furnish]
    })
    
    # Predict
    predicted_price = model_multi.predict(house)[0]
    
    print("\n" + "="*80)
    print("💰 PREDICTION RESULT")
    print("="*80)
    print(f"\nEstimated Price: ₹{predicted_price:,.2f}")
    print(f"Estimated Price: ${predicted_price/80:,.2f} USD (approx)")
    print("\n" + "="*80)

# Run the interactive predictor
predict_house_price()
```

---

## 📝 Summary

| Method | What It Tests | When to Use |
|--------|---------------|-------------|
| **Method 1** | Overall model performance on test set | Always (automatic) |
| **Method 2** | Specific house with known features | When you have exact house specs |
| **Method 3** | Random samples from dataset | Check model consistency |
| **Method 4** | Statistical accuracy metrics | Understand model reliability |
| **Method 5** | Interactive user input | Demo/presentation mode |

---

## 🎯 Which Method to Use?

- **Just learning?** → Use Method 1 (already done in notebook)
- **Have a specific house?** → Use Method 2
- **Want to impress someone?** → Use Method 5 (interactive)
- **Need detailed stats?** → Use Method 4
- **Testing thoroughly?** → Use ALL methods!

---

## 💡 Tips

1. **Always test with realistic values** (don't test with 100 bedrooms!)
2. **Compare predictions with similar houses** in your dataset
3. **Remember**: Model can only be as accurate as your training data
4. **Your model explains 64.95% of price variance** - this is good but not perfect

---

**Happy Testing! 🚀**
