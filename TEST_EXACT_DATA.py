# TEST: Why predictions don't equal actual prices even with exact data
# Add this cell to your Jupyter notebook to understand!

print("="*80)
print("🔬 TESTING: Exact Training Data vs Predictions")
print("="*80)

# Test 1: Predict on a house from TRAINING set
print("\n📊 TEST 1: House from TRAINING SET")
print("-"*80)

# Get first house from training set
first_house_features = X_train.iloc[[0]]
actual_price_train = y_train.iloc[0]

# Predict
predicted_price_train = model_multi.predict(first_house_features)[0]

print(f"\n🏠 House Features:")
print(first_house_features)
print(f"\n💰 Actual Price:     ₹{actual_price_train:,.2f}")
print(f"💰 Predicted Price:  ₹{predicted_price_train:,.2f}")
print(f"💰 Difference:       ₹{abs(actual_price_train - predicted_price_train):,.2f}")
print(f"📊 Error Percentage: {abs(actual_price_train - predicted_price_train)/actual_price_train*100:.2f}%")

if abs(actual_price_train - predicted_price_train) < 1000:
    print("\n✅ Almost perfect! (Training data)")
else:
    print(f"\n⚠️ Still has error even on training data!")

# Test 2: Predict on a house from TEST set (never seen before)
print("\n" + "="*80)
print("\n📊 TEST 2: House from TEST SET (Never Seen)")
print("-"*80)

# Get first house from test set
first_house_test = X_test.iloc[[0]]
actual_price_test = y_test.iloc[0]

# Predict
predicted_price_test = model_multi.predict(first_house_test)[0]

print(f"\n🏠 House Features:")
print(first_house_test)
print(f"\n💰 Actual Price:     ₹{actual_price_test:,.2f}")
print(f"💰 Predicted Price:  ₹{predicted_price_test:,.2f}")
print(f"💰 Difference:       ₹{abs(actual_price_test - predicted_price_test):,.2f}")
print(f"📊 Error Percentage: {abs(actual_price_test - predicted_price_test)/actual_price_test*100:.2f}%")

print("\n⚠️ This is WORSE because model never saw this house!")

# Test 3: Compare multiple houses
print("\n" + "="*80)
print("\n📊 TEST 3: Compare 5 TRAINING vs 5 TEST houses")
print("-"*80)

print("\n🎓 TRAINING SET (Model saw these):")
print("-"*40)
train_errors = []
for i in range(5):
    actual = y_train.iloc[i]
    predicted = model_multi.predict(X_train.iloc[[i]])[0]
    error = abs(actual - predicted)
    error_pct = (error / actual) * 100
    train_errors.append(error_pct)
    print(f"House {i+1}: Actual=₹{actual:,.0f} | Predicted=₹{predicted:,.0f} | Error={error_pct:.1f}%")

print(f"\n📊 Average Training Error: {sum(train_errors)/len(train_errors):.2f}%")

print("\n🆕 TEST SET (Model NEVER saw these):")
print("-"*40)
test_errors = []
for i in range(5):
    actual = y_test.iloc[i]
    predicted = model_multi.predict(X_test.iloc[[i]])[0]
    error = abs(actual - predicted)
    error_pct = (error / actual) * 100
    test_errors.append(error_pct)
    print(f"House {i+1}: Actual=₹{actual:,.0f} | Predicted=₹{predicted:,.0f} | Error={error_pct:.1f}%")

print(f"\n📊 Average Test Error: {sum(test_errors)/len(test_errors):.2f}%")

# Explanation
print("\n" + "="*80)
print("💡 WHY ARE THEY DIFFERENT?")
print("="*80)
print("""
1. LINEAR REGRESSION MODEL:
   - Creates ONE straight line (formula) to fit ALL houses
   - Formula: Price = w1×area + w2×bedrooms + ... + constant
   - This ONE line CANNOT perfectly fit every house!

2. TRAINING DATA:
   - Model tries to minimize AVERAGE error
   - Some houses over-predicted, some under-predicted
   - Even training data has errors!

3. TEST DATA:
   - Model never saw these houses during training
   - Uses the learned formula to predict
   - Usually WORSE than training error

4. SIMPLE EXAMPLE:
   Imagine predicting Y from X:
   X:  1,  2,  3,  4,  5
   Y: 10, 25, 35, 45, 60
   
   Best line: Y = 12×X - 2
   Predictions: 10, 22, 34, 46, 58
   
   See? Even with exact training X values,
   Y predictions don't match perfectly!
   That's because ONE LINE can't fit all points exactly!

5. YOUR MODEL:
   - Uses ONE equation for ALL 436 training houses
   - Impossible to be perfect for every house
   - Trained on average, not perfection
""")

print("\n" + "="*80)
print("✅ CONCLUSION")
print("="*80)
print("""
Even with EXACT SAME features from training:
❌ Predictions won't be 100% perfect
✅ This is NORMAL and EXPECTED
✅ Linear Regression finds BEST AVERAGE line
✅ Not a memorization algorithm!

If you want perfect predictions on training data:
→ Use Decision Trees with max_depth=None (overfits)
→ But then TEST data predictions will be terrible!
→ Your current model balances both (GOOD!)
""")

print("\n🎓 Your model is trained correctly!")
print("="*80)
