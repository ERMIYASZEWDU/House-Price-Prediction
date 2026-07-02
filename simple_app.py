import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import plotly.express as px

st.set_page_config(
    page_title="🏠 House Price Predictor",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 House Price Predictor")
st.write("A simple and functional web app for predicting house prices!")

# Try to load data
try:
    df = pd.read_csv('Housing.csv')
    st.success(f"✅ Data loaded successfully! {len(df)} houses in dataset.")
    
    # Encode categorical data
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
    
    # Train model
    X = df_processed.drop('price', axis=1)
    y = df_processed['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    
    st.success(f"✅ Model trained! Accuracy (R²): {score:.3f}")
    
    # Sidebar for input
    st.sidebar.header("🏡 Enter House Details")
    
    area = st.sidebar.slider("Area (sq ft)", 1000, 20000, 5000)
    bedrooms = st.sidebar.selectbox("Bedrooms", [1,2,3,4,5,6], index=2)
    bathrooms = st.sidebar.selectbox("Bathrooms", [1,2,3,4], index=1)
    stories = st.sidebar.selectbox("Stories", [1,2,3,4], index=1)
    mainroad = st.sidebar.checkbox("Main Road", value=True)
    guestroom = st.sidebar.checkbox("Guest Room")
    basement = st.sidebar.checkbox("Basement")
    hotwaterheating = st.sidebar.checkbox("Hot Water Heating")
    airconditioning = st.sidebar.checkbox("Air Conditioning", value=True)
    parking = st.sidebar.selectbox("Parking Spaces", [0,1,2,3], index=1)
    prefarea = st.sidebar.checkbox("Preferred Area", value=True)
    furnishing = st.sidebar.selectbox("Furnishing", 
                                    ["unfurnished", "semi-furnished", "furnished"], 
                                    index=1)
    
    # Predict button
    if st.sidebar.button("🔮 Predict Price", type="primary"):
        # Prepare input
        input_data = [[
            area, bedrooms, bathrooms, stories,
            1 if mainroad else 0,
            1 if guestroom else 0, 
            1 if basement else 0,
            1 if hotwaterheating else 0,
            1 if airconditioning else 0,
            parking,
            1 if prefarea else 0,
            2 if furnishing == 'furnished' else 1 if furnishing == 'semi-furnished' else 0
        ]]
        
        prediction = model.predict(input_data)[0]
        
        # Display result
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("💰 Predicted Price", f"₹{prediction:,.0f}", f"${prediction/83:,.0f} USD")
            
            # Price analysis
            avg_price = df['price'].mean()
            if prediction > avg_price * 1.2:
                st.warning("📈 Above market average")
            elif prediction < avg_price * 0.8:
                st.success("📉 Below market - Good deal!")
            else:
                st.info("📊 Market rate pricing")
        
        with col2:
            # Show price range
            margin = prediction * 0.15
            st.info(f"**Price Range:** ₹{prediction-margin:,.0f} - ₹{prediction+margin:,.0f}")
    
    # Show some analytics
    st.subheader("📊 Market Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🏠 Total Houses", len(df))
    with col2:
        st.metric("💰 Average Price", f"₹{df['price'].mean()/1000000:.1f}M")
    with col3:
        st.metric("📏 Average Area", f"{df['area'].mean():.0f} sqft")
    
    # Price distribution chart
    fig = px.histogram(df, x='price', title='House Price Distribution', nbins=30)
    fig.update_xaxis(title="Price (₹)")
    fig.update_yaxis(title="Number of Houses")
    st.plotly_chart(fig, use_container_width=True)
    
    # Price vs Area scatter
    fig2 = px.scatter(df, x='area', y='price', title='Price vs Area', 
                     trendline="ols", opacity=0.7)
    fig2.update_xaxis(title="Area (sq ft)")
    fig2.update_yaxis(title="Price (₹)")
    st.plotly_chart(fig2, use_container_width=True)

except FileNotFoundError:
    st.error("❌ Housing.csv file not found!")
    st.info("Please make sure the Housing.csv file is in the same directory as this app.")
except Exception as e:
    st.error(f"❌ Error: {str(e)}")

st.markdown("---")
st.markdown("**🚀 Made by ERMIYASZEWDU** | [GitHub Repository](https://github.com/ERMIYASZEWDU/House-Price-Prediction)")