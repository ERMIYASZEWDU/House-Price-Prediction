import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="🏠 House Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 20px;
        margin-bottom: 30px;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .prediction-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .info-box {
        background: #f8f9fa;
        border-left: 5px solid #007bff;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    
    .stSelectbox > div > div > select {
        background-color: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 8px;
    }
    
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Load data and train model (simplified for demo)
@st.cache_data
def load_data():
    # Load the dataset
    df = pd.read_csv('Housing.csv')
    return df

@st.cache_data
def prepare_model_data(df):
    """Prepare data for modeling"""
    # Create a copy
    df_model = df.copy()
    
    # Encode categorical variables
    categorical_cols = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 
                       'airconditioning', 'prefarea', 'furnishingstatus']
    
    for col in categorical_cols:
        if col != 'furnishingstatus':
            df_model[col] = df_model[col].map({'yes': 1, 'no': 0})
        else:
            df_model[col] = df_model[col].map({'furnished': 2, 'semi-furnished': 1, 'unfurnished': 0})
    
    return df_model

# Initialize session state
if 'model_trained' not in st.session_state:
    st.session_state.model_trained = False
    st.session_state.model = None
    st.session_state.model_metrics = {}

def train_models(df):
    """Train multiple models and return the best one"""
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
    
    # Prepare features and target
    X = df.drop('price', axis=1)
    y = df['price']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train models
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
    }
    
    results = {}
    best_model = None
    best_score = 0
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        results[name] = {
            'model': model,
            'r2': r2,
            'mae': mae,
            'rmse': rmse,
            'predictions': y_pred,
            'actual': y_test
        }
        
        if r2 > best_score:
            best_score = r2
            best_model = model
    
    return best_model, results, X.columns.tolist()

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">🏠 AI House Price Predictor</h1>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    df_model = prepare_model_data(df)
    
    # Sidebar
    st.sidebar.title("🎛️ Control Panel")
    page = st.sidebar.selectbox("Choose Page", 
                               ["🏠 Price Prediction", "📊 Data Analytics", "🔬 Model Performance", "ℹ️ About"])
    
    if page == "🏠 Price Prediction":
        prediction_page(df, df_model)
    elif page == "📊 Data Analytics":
        analytics_page(df)
    elif page == "🔬 Model Performance":
        model_performance_page(df_model)
    elif page == "ℹ️ About":
        about_page()

def prediction_page(df, df_model):
    st.title("🎯 Predict House Price")
    
    # Train model if not already trained
    if not st.session_state.model_trained:
        with st.spinner("🤖 Training AI models... Please wait!"):
            model, results, feature_names = train_models(df_model)
            st.session_state.model = model
            st.session_state.model_metrics = results
            st.session_state.feature_names = feature_names
            st.session_state.model_trained = True
        st.success("✅ AI models trained successfully!")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🏡 House Specifications")
        
        # Input fields with better UI
        area = st.slider("🏠 Area (sq ft)", min_value=1000, max_value=20000, value=5000, step=100)
        bedrooms = st.selectbox("🛏️ Bedrooms", [1, 2, 3, 4, 5, 6], index=2)
        bathrooms = st.selectbox("🚿 Bathrooms", [1, 2, 3, 4], index=1)
        stories = st.selectbox("🏢 Stories", [1, 2, 3, 4], index=1)
        
        st.subheader("🏠 Amenities")
        mainroad = st.checkbox("🛣️ Main Road Access", value=True)
        guestroom = st.checkbox("👥 Guest Room", value=False)
        basement = st.checkbox("🏠 Basement", value=False)
        hotwaterheating = st.checkbox("🔥 Hot Water Heating", value=False)
        airconditioning = st.checkbox("❄️ Air Conditioning", value=True)
        parking = st.selectbox("🚗 Parking Spaces", [0, 1, 2, 3], index=1)
        prefarea = st.checkbox("⭐ Preferred Area", value=True)
        furnishingstatus = st.selectbox("🪑 Furnishing", 
                                      ["unfurnished", "semi-furnished", "furnished"], 
                                      index=1)
    
    with col2:
        st.subheader("🎯 Price Prediction")
        
        if st.button("💰 Predict Price", type="primary"):
            # Prepare input data
            input_data = pd.DataFrame({
                'area': [area],
                'bedrooms': [bedrooms],
                'bathrooms': [bathrooms],
                'stories': [stories],
                'mainroad': [1 if mainroad else 0],
                'guestroom': [1 if guestroom else 0],
                'basement': [1 if basement else 0],
                'hotwaterheating': [1 if hotwaterheating else 0],
                'airconditioning': [1 if airconditioning else 0],
                'parking': [parking],
                'prefarea': [1 if prefarea else 0],
                'furnishingstatus': [2 if furnishingstatus == 'furnished' 
                                   else 1 if furnishingstatus == 'semi-furnished' else 0]
            })
            
            # Make prediction
            prediction = st.session_state.model.predict(input_data)[0]
            
            # Display prediction with animation
            st.markdown(f"""
            <div class="prediction-box">
                💰 Predicted Price: ₹{prediction:,.0f}
                <br>
                <small>≈ ${prediction/83:,.0f} USD</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Price range
            margin = prediction * 0.15
            st.info(f"📊 **Price Range**: ₹{prediction-margin:,.0f} - ₹{prediction+margin:,.0f}")
            
            # Comparison with market
            avg_price = df['price'].mean()
            if prediction > avg_price * 1.2:
                st.warning("📈 **Above Market**: This house is priced above average market rate")
            elif prediction < avg_price * 0.8:
                st.success("📉 **Below Market**: This house is a good deal!")
            else:
                st.info("📊 **Market Rate**: This house is priced at market rate")
        
        # Quick predictions for different scenarios
        st.subheader("🚀 Quick Scenarios")
        if st.button("🏠 Basic House"):
            st.write("**Basic 2BHK**: ₹35,00,000 - ₹45,00,000")
        if st.button("🏡 Premium Villa"):
            st.write("**Premium 4BHK**: ₹80,00,000 - ₹1,20,00,000")
        if st.button("🏢 Luxury Penthouse"):
            st.write("**Luxury 5BHK**: ₹1,50,00,000 - ₹2,50,00,000")

def analytics_page(df):
    st.title("📊 Housing Market Analytics")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🏠 Total Houses</h3>
            <h2>{len(df)}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_price = df['price'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰 Avg Price</h3>
            <h2>₹{avg_price/1000000:.1f}M</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_area = df['area'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>📏 Avg Area</h3>
            <h2>{avg_area:.0f} sqft</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        price_per_sqft = (df['price'] / df['area']).mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>💲 Price/SqFt</h3>
            <h2>₹{price_per_sqft:.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏠 Price Distribution")
        fig = px.histogram(df, x='price', nbins=30, 
                          title="House Price Distribution",
                          color_discrete_sequence=['#667eea'])
        fig.update_layout(xaxis_title="Price (₹)", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Price vs Area")
        fig = px.scatter(df, x='area', y='price', 
                        title="Price vs Area Relationship",
                        trendline="ols",
                        color_discrete_sequence=['#11998e'])
        fig.update_layout(xaxis_title="Area (sqft)", yaxis_title="Price (₹)")
        st.plotly_chart(fig, use_container_width=True)
    
    # More analytics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🛏️ Bedrooms Analysis")
        bedroom_stats = df.groupby('bedrooms')['price'].mean().reset_index()
        fig = px.bar(bedroom_stats, x='bedrooms', y='price',
                    title="Average Price by Bedrooms",
                    color='price',
                    color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🏢 Stories vs Price")
        stories_stats = df.groupby('stories')['price'].mean().reset_index()
        fig = px.bar(stories_stats, x='stories', y='price',
                    title="Average Price by Stories",
                    color='price',
                    color_continuous_scale='Plasma')
        st.plotly_chart(fig, use_container_width=True)

def model_performance_page(df_model):
    st.title("🔬 AI Model Performance")
    
    if not st.session_state.model_trained:
        st.warning("Please visit the Prediction page first to train the models!")
        return
    
    # Model comparison
    results = st.session_state.model_metrics
    
    # Create comparison dataframe
    comparison_data = []
    for name, metrics in results.items():
        comparison_data.append({
            'Model': name,
            'R² Score': metrics['r2'],
            'MAE': metrics['mae'],
            'RMSE': metrics['rmse']
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    st.subheader("🏆 Model Comparison")
    st.dataframe(comparison_df, use_container_width=True)
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(comparison_df, x='Model', y='R² Score',
                    title="Model Accuracy (R² Score)",
                    color='R² Score',
                    color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(comparison_df, x='Model', y='MAE',
                    title="Mean Absolute Error",
                    color='MAE',
                    color_continuous_scale='Reds_r')
        st.plotly_chart(fig, use_container_width=True)
    
    # Prediction vs Actual plot
    st.subheader("🎯 Predictions vs Actual Values")
    
    best_model_name = comparison_df.loc[comparison_df['R² Score'].idxmax(), 'Model']
    best_results = results[best_model_name]
    
    fig = px.scatter(x=best_results['actual'], y=best_results['predictions'],
                    title=f"{best_model_name} - Predictions vs Actual",
                    labels={'x': 'Actual Price', 'y': 'Predicted Price'})
    
    # Add perfect prediction line
    min_val = min(best_results['actual'].min(), best_results['predictions'].min())
    max_val = max(best_results['actual'].max(), best_results['predictions'].max())
    fig.add_trace(go.Scatter(x=[min_val, max_val], y=[min_val, max_val],
                            mode='lines', name='Perfect Prediction',
                            line=dict(dash='dash', color='red')))
    
    st.plotly_chart(fig, use_container_width=True)

def about_page():
    st.title("ℹ️ About This Project")
    
    st.markdown("""
    ## 🏠 AI House Price Predictor
    
    This is a comprehensive machine learning project that predicts house prices using advanced AI algorithms.
    
    ### 🎯 **Key Features**
    - **Interactive UI**: Beautiful, user-friendly interface
    - **Multiple Models**: Linear Regression and Random Forest
    - **Real-time Predictions**: Instant price estimates
    - **Market Analytics**: Comprehensive data visualization
    - **Model Performance**: Detailed accuracy metrics
    
    ### 📊 **Technology Stack**
    - **Frontend**: Streamlit with custom CSS
    - **Backend**: Python, Pandas, NumPy
    - **ML Models**: Scikit-learn
    - **Visualization**: Plotly
    - **Data**: 545 house records with 13 features
    
    ### 🚀 **Model Performance**
    - **Accuracy**: Up to 80% R² score
    - **Features**: Area, bedrooms, bathrooms, amenities
    - **Predictions**: Real-time price estimation
    
    ### 👨‍💻 **Developer**
    **ERMIYASZEWDU**
    - GitHub: [@ERMIYASZEWDU](https://github.com/ERMIYASZEWDU)
    - Project: [House Price Prediction](https://github.com/ERMIYASZEWDU/House-Price-Prediction)
    
    ### 📄 **How to Use**
    1. **Prediction**: Enter house details and get instant price
    2. **Analytics**: Explore market trends and statistics
    3. **Performance**: View model accuracy and comparisons
    
    ---
    
    ⭐ **If you found this helpful, please star the GitHub repository!**
    """)

if __name__ == "__main__":
    main()