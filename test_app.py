import streamlit as st
import pandas as pd

# Simple test app to verify Streamlit works
st.title("🚀 Streamlit Test - House Price Predictor")

st.success("✅ Streamlit is working correctly!")

# Test data loading
try:
    df = pd.read_csv('Housing.csv')
    st.success(f"✅ Data loaded successfully! Found {len(df)} houses in dataset.")
    
    # Show first few rows
    st.subheader("📊 Sample Data")
    st.dataframe(df.head())
    
    # Basic statistics
    st.subheader("📈 Basic Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Houses", len(df))
    with col2:
        st.metric("Average Price", f"₹{df['price'].mean()/1000000:.1f}M")
    with col3:
        st.metric("Average Area", f"{df['area'].mean():.0f} sqft")
    
    st.balloons()
    st.success("🎉 Everything is working perfectly! You can now run the main app.")
    
except FileNotFoundError:
    st.error("❌ Housing.csv not found. Make sure the file is in the same directory.")
except Exception as e:
    st.error(f"❌ Error: {e}")

st.markdown("---")
st.info("💡 If you see this page, Streamlit is working. Now try the main app!")