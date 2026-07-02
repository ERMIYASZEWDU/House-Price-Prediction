# 🏠 INTERACTIVE HOUSE PRICE PREDICTOR
# Copy this code and paste it as a NEW CELL in your Jupyter notebook
# Run it after training your models!

# ============================================================================
# METHOD 5: INTERACTIVE TESTING
# ============================================================================

def predict_house_price_interactive():
    """
    Interactive function to predict house price based on user input.
    This is the simplest version - just asks for each feature one by one.
    """
    
    print("\n" + "="*80)
    print("🏠 INTERACTIVE HOUSE PRICE PREDICTOR")
    print("="*80)
    print("\nEnter house details (press Enter to use default values):\n")
    
    try:
        # Get user inputs with default values
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
        
        # Create DataFrame with the inputs
        house = pd.DataFrame({
            'area': [area], 
            'bedrooms': [bedrooms], 
            'bathrooms': [bathrooms],
            'stories': [stories], 
            'mainroad': [mainroad], 
            'guestroom': [guestroom],
            'basement': [basement], 
            'hotwaterheating': [hotwater], 
            'airconditioning': [aircon], 
            'parking': [parking],
            'prefarea': [prefarea], 
            'furnishingstatus': [furnish]
        })
        
        # Predict using the best model (Multi-variate)
        predicted_price = model_multi.predict(house)[0]
        
        # Display results
        print("\n" + "="*80)
        print("💰 PREDICTION RESULT")
        print("="*80)
        print(f"\nHouse Specifications:")
        print(f"  Area: {area} sqft")
        print(f"  Bedrooms: {bedrooms}")
        print(f"  Bathrooms: {bathrooms}")
        print(f"  Stories: {stories}")
        print(f"  On main road: {'Yes' if mainroad == 1 else 'No'}")
        print(f"  Guest room: {'Yes' if guestroom == 1 else 'No'}")
        print(f"  Basement: {'Yes' if basement == 1 else 'No'}")
        print(f"  Hot water heating: {'Yes' if hotwater == 1 else 'No'}")
        print(f"  Air conditioning: {'Yes' if aircon == 1 else 'No'}")
        print(f"  Parking spaces: {parking}")
        print(f"  Preferred area: {'Yes' if prefarea == 1 else 'No'}")
        
        furnish_status = {0: 'Furnished', 1: 'Semi-furnished', 2: 'Unfurnished'}
        print(f"  Furnishing: {furnish_status.get(furnish, 'Unknown')}")
        
        print(f"\n💰 Estimated Price: ₹{predicted_price:,.2f}")
        print(f"💰 Estimated Price: ${predicted_price/80:,.2f} USD (approx)")
        
        # Comparison with average
        avg_price = y.mean()
        difference = predicted_price - avg_price
        percentage = (difference / avg_price) * 100
        
        print(f"\n📊 Comparison with Average:")
        print(f"   Dataset average price: ₹{avg_price:,.2f}")
        print(f"   Your house difference: ₹{difference:,.2f} ({percentage:+.1f}%)")
        
        if percentage > 20:
            print(f"   💎 This house is above average!")
        elif percentage < -20:
            print(f"   💵 This house is below average price")
        else:
            print(f"   📍 This house is around average price")
            
        print("\n" + "="*80)
        
        # Ask if user wants to try again
        again = input("\nWould you like to predict another house? (yes/no): ")
        if again.lower() in ['yes', 'y']:
            predict_house_price_interactive()
            
    except ValueError:
        print("\n❌ Error: Please enter valid numbers!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Make sure you have trained the model_multi first!")


# ============================================================================
# SIMPLE VERSION - NO USER INPUT (FOR QUICK TESTING)
# ============================================================================

def quick_test():
    """Quick test with predefined values - no user input needed"""
    
    print("\n" + "="*80)
    print("🏠 QUICK TEST - SAMPLE HOUSE PREDICTION")
    print("="*80)
    
    # Sample house specifications
    sample_house = pd.DataFrame({
        'area': [5000], 
        'bedrooms': [3], 
        'bathrooms': [2],
        'stories': [2], 
        'mainroad': [1], 
        'guestroom': [0],
        'basement': [1], 
        'hotwaterheating': [0], 
        'airconditioning': [1], 
        'parking': [2],
        'prefarea': [1], 
        'furnishingstatus': [0]
    })
    
    print("\nSample House:")
    print("  - 5000 sqft")
    print("  - 3 bedrooms, 2 bathrooms")
    print("  - 2 stories")
    print("  - Main road: Yes")
    print("  - Basement: Yes")
    print("  - Air conditioning: Yes")
    print("  - 2 parking spaces")
    print("  - Furnished")
    
    predicted_price = model_multi.predict(sample_house)[0]
    
    print(f"\n💰 Predicted Price: ₹{predicted_price:,.2f}")
    print(f"💰 Predicted Price: ${predicted_price/80:,.2f} USD (approx)")
    print("\n" + "="*80)


# ============================================================================
# INSTRUCTIONS
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                  🏠 INTERACTIVE HOUSE PRICE TESTER                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

Two functions are now available:

1. quick_test()
   - Fast test with pre-defined sample house
   - No user input required
   - Good for checking if model works

2. predict_house_price_interactive()
   - Full interactive experience
   - Enter your own house specifications
   - Get detailed predictions

USAGE:
------
Just type the function name and press Enter:

>>> quick_test()              # Quick sample
>>> predict_house_price_interactive()  # Full interactive

NOTE: Make sure you've run all previous cells and trained model_multi first!
""")
