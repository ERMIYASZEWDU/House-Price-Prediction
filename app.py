import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from ml_pipeline import (
    encode_categoricals,
    engineer_features,
    train_all_models,
    build_feature_row,
)
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="🏠 House Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
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
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .prediction-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 1.8rem;
        font-weight: bold;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .success-box {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        font-weight: bold;
        margin: 10px 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 15px;
        border-radius: 10px;
        color: #333;
        font-weight: bold;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Load and prepare data
@st.cache_data
def load_and_prepare_data():
    """Load and prepare the housing data"""
    try:
        df = pd.read_csv('Housing.csv')
        st.success(f"✅ Dataset loaded: {len(df)} houses with {len(df.columns)} features")

        df_processed = encode_categoricals(df)
        df_processed = engineer_features(df_processed)
        return df, df_processed
    except FileNotFoundError:
        st.error("❌ Housing.csv file not found. Please ensure the dataset is in the same directory.")
        return None, None
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None, None

# Train models
@st.cache_data
def train_models(_df_processed):
    """Train enhanced models and return the best performer."""
    if _df_processed is None:
        return None, None, None

    pipeline = train_all_models()
    results = {}
    for name, metrics in pipeline['results'].items():
        results[name] = {
            'model': metrics['model'],
            'r2': metrics['r2'],
            'mae': metrics['mae'],
            'rmse': metrics['rmse'],
            'predictions': metrics['predictions'],
            'actual': metrics['actual'],
        }

    best_name = pipeline['best_name']
    best_score = pipeline['best_score']
    st.success(
        f"🤖 Best Model: **{best_name}** with R² = **{best_score:.3f}** ({best_score * 100:.1f}% accuracy)"
    )
    return pipeline['best_model'], results, best_name

# Main app
def main():
    # Header with animation
    st.markdown('<h1 class="main-header">🏠 AI House Price Predictor</h1>', unsafe_allow_html=True)
    st.markdown("### *Powered by Advanced Machine Learning & Beautiful UI*")
    
    # Load data and train models
    with st.spinner("🤖 Loading data and training AI models..."):
        df_original, df_processed = load_and_prepare_data()
        
        if df_original is None or df_processed is None:
            st.error("❌ Could not load data. Please check if Housing.csv exists.")
            return
        
        model, results, best_name = train_models(df_processed)
        
        if model is None:
            st.error("❌ Could not train models.")
            return
    
    # Sidebar navigation
    st.sidebar.markdown("## 🎛️ Navigation Panel")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Choose a page:",
        ["🏠 Price Prediction", "📊 Market Analytics", "🔬 Model Performance", "ℹ️ About"],
        key="navigation"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### 🌟 **App Features:**
    - 🤖 **AI Predictions** with 67%+ accuracy
    - 📊 **Real-time Analytics** 
    - 🎨 **Beautiful Modern UI**
    - 📱 **Mobile Friendly**
    """)
    
    # Route to selected page
    if page == "🏠 Price Prediction":
        prediction_page(model, df_original, results)
    elif page == "📊 Market Analytics":
        analytics_page(df_original)
    elif page == "🔬 Model Performance":
        model_performance_page(results)
    elif page == "ℹ️ About":
        about_page()

def about_page():
    st.title("ℹ️ About This Application")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## 🏠 AI House Price Predictor
        
        This is a **production-ready web application** that uses advanced machine learning 
        to predict house prices in real-time. Built with modern web technologies and 
        professional UI/UX design.
        
        ### ✨ **Key Features**
        - 🤖 **Three AI Models**: Enhanced Linear, Random Forest, Gradient Boosting
        - 🎯 **High Accuracy**: Up to 67%+ prediction accuracy (Gradient Boosting)
        - 🎨 **Modern Design**: Beautiful gradients and animations
        - 📱 **Responsive**: Works on desktop, tablet, and mobile
        - ⚡ **Real-time**: Instant price predictions
        - 📊 **Analytics**: Comprehensive market insights
        
        ### 🛠️ **Technology Stack**
        - **Frontend**: Streamlit with Custom CSS
        - **Backend**: Python, Pandas, NumPy  
        - **ML Models**: Scikit-learn (Enhanced Linear, Random Forest, Gradient Boosting)
        - **Visualization**: Plotly Interactive Charts
        - **Data**: 545 house records, 16 engineered features
        
        ### 📊 **Model Performance**
        - **Enhanced Linear**: ~66% accuracy
        - **Random Forest**: ~66% accuracy
        - **Gradient Boosting**: ~67% accuracy (best)
        - **Features Used**: Area, rooms, amenities, engineered ratios
        - **Prediction Speed**: < 100ms per prediction
        """)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 Project Stats</h3>
            <p><strong>Dataset Size:</strong> 545 houses</p>
            <p><strong>Features:</strong> 16 attributes</p>
            <p><strong>Model Accuracy:</strong> 67%+</p>
            <p><strong>Prediction Speed:</strong> Real-time</p>
            <p><strong>UI Framework:</strong> Streamlit</p>
            <p><strong>Responsive:</strong> ✅ Yes</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
        ### 👨‍💻 **Developer**
        **ERMIYASZEWDU**
        
        - 🐙 **GitHub**: [@ERMIYASZEWDU](https://github.com/ERMIYASZEWDU)
        - 🏠 **Project**: [House-Price-Prediction](https://github.com/ERMIYASZEWDU/House-Price-Prediction)
        - ⭐ **Please star the repo if helpful!**
        """)
    
    st.markdown("---")
    
    # Usage instructions
    st.subheader("🚀 How to Use This App")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 🏠 **Prediction Page**
        1. Enter house specifications
        2. Select features and amenities  
        3. Click "Predict Price"
        4. Get instant AI prediction
        5. View market analysis
        """)
    
    with col2:
        st.markdown("""
        #### 📊 **Analytics Page**
        1. View market overview
        2. Explore price distributions
        3. Analyze trends by features
        4. Interactive charts and graphs
        5. Market insights
        """)
    
    with col3:
        st.markdown("""
        #### 🔬 **Performance Page**
        1. Compare AI model accuracy
        2. View prediction quality
        3. Understand error rates
        4. Feature importance analysis
        5. Model interpretability
        """)
    
    st.success("🌟 **Built with ❤️ for the real estate and AI community!**")

def prediction_page(model, df, results):
    st.title("🎯 AI House Price Prediction")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🏡 Enter House Details")
        
        # Input fields with better styling
        area = st.slider("🏠 **Area (Square Feet)**", min_value=1000, max_value=20000, value=5000, step=100)
        bedrooms = st.selectbox("🛏️ **Number of Bedrooms**", [1, 2, 3, 4, 5, 6], index=2)
        bathrooms = st.selectbox("🚿 **Number of Bathrooms**", [1, 2, 3, 4], index=1)
        stories = st.selectbox("🏢 **Number of Stories**", [1, 2, 3, 4], index=1)
        
        st.markdown("---")
        st.subheader("🏠 House Features")
        
        col_a, col_b = st.columns(2)
        with col_a:
            mainroad = st.checkbox("🛣️ Main Road Access", value=True)
            guestroom = st.checkbox("👥 Guest Room", value=False)
            basement = st.checkbox("🏠 Basement", value=False)
            hotwaterheating = st.checkbox("🔥 Hot Water Heating", value=False)
        
        with col_b:
            airconditioning = st.checkbox("❄️ Air Conditioning", value=True)
            parking = st.selectbox("🚗 Parking Spaces", [0, 1, 2, 3], index=1)
            prefarea = st.checkbox("⭐ Preferred Area", value=True)
            furnishingstatus = st.selectbox("🪑 Furnishing Status", 
                                          ["unfurnished", "semi-furnished", "furnished"], 
                                          index=1)
    
    with col2:
        st.subheader("💰 Price Prediction Result")
        
        # Show model info
        best_model_name = max(results.items(), key=lambda x: x[1]['r2'])[0]
        best_r2 = max(results.items(), key=lambda x: x[1]['r2'])[1]['r2']
        
        st.info(f"🤖 **Using Model:** {best_model_name} (Accuracy: {best_r2*100:.1f}%)")
        
        if st.button("🔮 **PREDICT HOUSE PRICE**", type="primary", use_container_width=True):
            furnish_code = (
                2 if furnishingstatus == 'furnished'
                else 1 if furnishingstatus == 'semi-furnished' else 0
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
            
            try:
                # Make prediction
                prediction = model.predict(input_data)[0]
                
                # Display prediction with beautiful styling
                st.markdown(f"""
                <div class="prediction-box">
                    🏠 PREDICTED PRICE<br>
                    ₹{prediction:,.0f}<br>
                    <small style="font-size: 0.7em;">≈ ${prediction/83:,.0f} USD</small>
                </div>
                """, unsafe_allow_html=True)
                
                # Price analysis
                avg_price = df['price'].mean()
                margin = prediction * 0.15
                
                if prediction > avg_price * 1.3:
                    st.markdown(f"""
                    <div class="warning-box">
                        📈 <strong>PREMIUM PROPERTY</strong><br>
                        This house is priced significantly above market average
                    </div>
                    """, unsafe_allow_html=True)
                elif prediction > avg_price * 1.1:
                    st.warning("📊 **Above Average**: This house is priced above market average")
                elif prediction < avg_price * 0.8:
                    st.markdown(f"""
                    <div class="success-box">
                        💰 <strong>GREAT DEAL!</strong><br>
                        This house is priced below market rate
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("📊 **Market Rate**: This house is fairly priced")
                
                # Show detailed analysis
                st.markdown("---")
                
                col_x, col_y = st.columns(2)
                with col_x:
                    st.metric("💰 **Price Range**", 
                             f"₹{prediction-margin:,.0f}", 
                             f"to ₹{prediction+margin:,.0f}")
                with col_y:
                    price_per_sqft = prediction / area
                    st.metric("📊 **Price per Sq Ft**", f"₹{price_per_sqft:,.0f}")
                
                # Comparison metrics
                st.markdown("**📈 Market Comparison:**")
                market_avg_per_sqft = (df['price'] / df['area']).mean()
                
                if price_per_sqft > market_avg_per_sqft * 1.1:
                    st.error(f"Above market avg (₹{market_avg_per_sqft:,.0f}/sqft)")
                elif price_per_sqft < market_avg_per_sqft * 0.9:
                    st.success(f"Below market avg (₹{market_avg_per_sqft:,.0f}/sqft)")
                else:
                    st.info(f"Near market avg (₹{market_avg_per_sqft:,.0f}/sqft)")
                
            except Exception as e:
                st.error(f"❌ Prediction error: {str(e)}")
        
        # Quick prediction examples
        st.markdown("---")
        st.subheader("🚀 Quick Examples")
        
        if st.button("🏠 **Basic 2BHK**", use_container_width=True):
            st.success("**Typical Range:** ₹35,00,000 - ₹50,00,000")
            
        if st.button("🏘️ **Premium 3BHK**", use_container_width=True):
            st.success("**Typical Range:** ₹60,00,000 - ₹90,00,000")
            
        if st.button("🏰 **Luxury 4BHK**", use_container_width=True):
            st.success("**Typical Range:** ₹1,00,00,000 - ₹1,50,00,000")

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
        try:
            import statsmodels  # noqa: F401
            trendline = "ols"
        except ImportError:
            trendline = None
        fig = px.scatter(df, x='area', y='price',
                        title="Price vs Area Relationship",
                        trendline=trendline,
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

def model_performance_page(results):
    st.title("🔬 AI Model Performance Analysis")
    
    if results is None:
        st.error("❌ No model results available")
        return
    
    # Create comparison dataframe
    comparison_data = []
    for name, metrics in results.items():
        comparison_data.append({
            'Model': name,
            'R² Score': metrics['r2'],
            'MAE (₹)': metrics['mae'],
            'RMSE (₹)': metrics['rmse'],
            'Accuracy (%)': metrics['r2'] * 100
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    # Display model comparison
    st.subheader("🏆 Model Comparison Dashboard")
    
    # Metrics cards
    col1, col2, col3 = st.columns(3)
    
    best_model_idx = comparison_df['R² Score'].idxmax()
    best_model = comparison_df.loc[best_model_idx]
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🥇 Best Model</h3>
            <h2>{best_model['Model']}</h2>
            <p>Top Performer</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 Accuracy</h3>
            <h2>{best_model['Accuracy (%)']:.1f}%</h2>
            <p>R² Score: {best_model['R² Score']:.3f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 Error Rate</h3>
            <h2>₹{best_model['MAE (₹)']/1000:.0f}K</h2>
            <p>Mean Absolute Error</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed comparison table
    st.subheader("📋 Detailed Performance Metrics")
    st.dataframe(comparison_df, use_container_width=True)
    
    # Performance visualizations
    st.subheader("📊 Performance Visualizations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # R² Score comparison
        fig1 = px.bar(comparison_df, x='Model', y='Accuracy (%)',
                     title="🎯 Model Accuracy Comparison",
                     color='Accuracy (%)',
                     color_continuous_scale='viridis',
                     text='Accuracy (%)')
        fig1.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig1.update_layout(showlegend=False, yaxis_title="Accuracy (%)")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Error comparison
        fig2 = px.bar(comparison_df, x='Model', y='MAE (₹)',
                     title="📉 Mean Absolute Error (Lower is Better)",
                     color='MAE (₹)',
                     color_continuous_scale='reds_r',
                     text='MAE (₹)')
        fig2.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
        fig2.update_layout(showlegend=False, yaxis_title="MAE (₹)")
        st.plotly_chart(fig2, use_container_width=True)
    
    # Prediction accuracy visualization
    st.subheader("🎯 Prediction Accuracy Analysis")
    
    # Get best model results
    best_model_name = comparison_df.loc[best_model_idx, 'Model']
    best_results = results[best_model_name]
    
    if 'predictions' in best_results and 'actual' in best_results:
        # Predictions vs Actual scatter plot
        fig3 = px.scatter(
            x=best_results['actual'], 
            y=best_results['predictions'],
            title=f"🔍 {best_model_name}: Predicted vs Actual Prices",
            labels={'x': 'Actual Price (₹)', 'y': 'Predicted Price (₹)'},
            opacity=0.7,
            color_discrete_sequence=['#667eea']
        )
        
        # Add perfect prediction line
        min_val = min(best_results['actual'].min(), best_results['predictions'].min())
        max_val = max(best_results['actual'].max(), best_results['predictions'].max())
        fig3.add_trace(go.Scatter(
            x=[min_val, max_val], 
            y=[min_val, max_val],
            mode='lines', 
            name='Perfect Prediction',
            line=dict(dash='dash', color='red', width=2)
        ))
        
        fig3.update_layout(
            xaxis_title="Actual Price (₹)",
            yaxis_title="Predicted Price (₹)",
            showlegend=True
        )
        st.plotly_chart(fig3, use_container_width=True)
        
        # Model insights
        st.subheader("🧠 Model Insights & Interpretation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"""
            **✅ Model Performance Summary:**
            - **Best Model:** {best_model_name}
            - **Accuracy:** {best_model['Accuracy (%)']:.1f}% (R² = {best_model['R² Score']:.3f})
            - **Average Error:** ₹{best_model['MAE (₹)']/1000:.0f}K per prediction
            - **Error Range:** ±15-20% is normal for real estate
            """)
        
        with col2:
            st.warning(f"""
            **💡 Understanding the Results:**
            - Points near the red line = accurate predictions
            - Scattered points = prediction uncertainty 
            - Model explains {best_model['Accuracy (%)']:.0f}% of price variance
            - Remaining {100-best_model['Accuracy (%)']:.0f}% depends on unmeasured factors
            """)
        
        # Feature importance (tree-based models)
        tree_model_name = next(
            (name for name in ('Gradient Boosting', 'Random Forest') if name in results),
            None,
        )
        if tree_model_name and best_model_name == tree_model_name:
            st.subheader(f"🎯 Feature Importance ({tree_model_name})")

            from ml_pipeline import FEATURE_COLUMNS
            tree_model = results[tree_model_name]['model']
            importance_df = pd.DataFrame({
                'Feature': FEATURE_COLUMNS,
                'Importance': tree_model.feature_importances_
            }).sort_values('Importance', ascending=True)
            
            fig4 = px.bar(importance_df, x='Importance', y='Feature', orientation='h',
                         title="📊 Which Features Matter Most?",
                         color='Importance',
                         color_continuous_scale='viridis')
            fig4.update_layout(yaxis_title="Features", xaxis_title="Importance Score")
            st.plotly_chart(fig4, use_container_width=True)
            
            st.info("💡 **Feature Importance** shows which house characteristics have the biggest impact on price predictions.")
    else:
        st.warning("🔍 Prediction accuracy analysis requires model training data.")

if __name__ == "__main__":
    main()