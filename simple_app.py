import streamlit as st
import pandas as pd
import plotly.express as px
from ml_pipeline import train_all_models, build_feature_row

st.set_page_config(
    page_title="🏠 House Price Predictor",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 House Price Predictor")
st.write("A simple and functional web app for predicting house prices!")

# Try to load data
try:
    pipeline = train_all_models()
    df = pipeline['df_raw']
    model = pipeline['best_model']
    model_name = pipeline['best_name']
    score = pipeline['best_score']

    st.success(f"✅ Data loaded! {len(df)} houses. Best model: **{model_name}** (R² = {score:.3f})")
    
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
        furnish_code = (
            2 if furnishing == 'furnished'
            else 1 if furnishing == 'semi-furnished' else 0
        )
        input_data = build_feature_row(
            area=area,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            stories=stories,
            mainroad=1 if mainroad else 0,
            guestroom=1 if guestroom else 0,
            basement=1 if basement else 0,
            hotwaterheating=1 if hotwaterheating else 0,
            airconditioning=1 if airconditioning else 0,
            parking=parking,
            prefarea=1 if prefarea else 0,
            furnishingstatus=furnish_code,
        )
        
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
    fig.update_layout(xaxis_title="Price (₹)", yaxis_title="Number of Houses")
    st.plotly_chart(fig, use_container_width=True)
    
    # Price vs Area scatter
    try:
        import statsmodels  # noqa: F401
        trendline = "ols"
    except ImportError:
        trendline = None
    fig2 = px.scatter(df, x='area', y='price', title='Price vs Area',
                     trendline=trendline, opacity=0.7)
    fig2.update_layout(xaxis_title="Area (sq ft)", yaxis_title="Price (₹)")
    st.plotly_chart(fig2, use_container_width=True)

except FileNotFoundError:
    st.error("❌ Housing.csv file not found!")
    st.info("Please make sure the Housing.csv file is in the same directory as this app.")
except Exception as e:
    st.error(f"❌ Error: {str(e)}")

st.markdown("---")
st.markdown("**🚀 Made by ERMIYASZEWDU** | [GitHub Repository](https://github.com/ERMIYASZEWDU/House-Price-Prediction)")
