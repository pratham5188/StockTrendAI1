import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="StockTrendAI - Simple Version",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #00ff88;
        box-shadow: 0 0 20px rgba(0,255,136,0.3);
        text-align: center;
        margin-bottom: 2rem;
    }
    .main-title {
        color: #00ff88;
        font-size: 3rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 0 0 10px rgba(0,255,136,0.5);
    }
    .subtitle {
        color: #ffffff;
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
    }
    .metric-card {
        background: linear-gradient(135deg, rgba(0,255,136,0.1), rgba(0,136,255,0.1));
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid rgba(0,255,136,0.3);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def fetch_stock_data(symbol, period="1y"):
    """Fetch stock data from Yahoo Finance"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period)
        return data
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {str(e)}")
        return None

def calculate_simple_prediction(data):
    """Calculate simple prediction using moving averages"""
    if data is None or len(data) < 20:
        return None
    
    current_price = data['Close'].iloc[-1]
    ma_5 = data['Close'].rolling(window=5).mean().iloc[-1]
    ma_20 = data['Close'].rolling(window=20).mean().iloc[-1]
    
    # Simple trend analysis
    if ma_5 > ma_20 and current_price > ma_5:
        direction = "UP"
        confidence = 75
        predicted_price = current_price * 1.02
    elif ma_5 < ma_20 and current_price < ma_5:
        direction = "DOWN"
        confidence = 75
        predicted_price = current_price * 0.98
    else:
        direction = "HOLD"
        confidence = 60
        predicted_price = current_price
    
    return {
        'direction': direction,
        'confidence': confidence,
        'predicted_price': predicted_price,
        'current_price': current_price
    }

def create_stock_chart(data, symbol):
    """Create interactive stock chart"""
    if data is None or data.empty:
        return None
    
    fig = go.Figure()
    
    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Price',
        increasing_line_color='#00ff88',
        decreasing_line_color='#ff4444'
    ))
    
    # Moving averages
    if len(data) >= 20:
        ma_20 = data['Close'].rolling(window=20).mean()
        fig.add_trace(go.Scatter(
            x=data.index,
            y=ma_20,
            mode='lines',
            name='MA 20',
            line=dict(color='#ffaa00', width=2)
        ))
    
    if len(data) >= 50:
        ma_50 = data['Close'].rolling(window=50).mean()
        fig.add_trace(go.Scatter(
            x=data.index,
            y=ma_50,
            mode='lines',
            name='MA 50',
            line=dict(color='#00aaff', width=2)
        ))
    
    fig.update_layout(
        title=f'{symbol} Stock Price Chart',
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_dark',
        height=600,
        showlegend=True
    )
    
    return fig

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🚀 StockTrendAI</h1>
        <p class="subtitle">Simple Stock Market Analysis & Prediction</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("📊 Settings")
    
    # Stock selection
    stock_symbol = st.sidebar.text_input(
        "Enter Stock Symbol",
        value="AAPL",
        help="Enter stock symbol (e.g., AAPL, MSFT, GOOGL)"
    ).upper()
    
    # Time period
    period = st.sidebar.selectbox(
        "Select Time Period",
        ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=3
    )
    
    # Fetch data
    if st.sidebar.button("📈 Load Data", type="primary"):
        with st.spinner("Loading stock data..."):
            data = fetch_stock_data(stock_symbol, period)
            
            if data is not None and not data.empty:
                st.session_state['stock_data'] = data
                st.session_state['symbol'] = stock_symbol
                st.success(f"✅ Data loaded successfully for {stock_symbol}")
            else:
                st.error("❌ Failed to load data. Please check the stock symbol.")
    
    # Main content
    if 'stock_data' in st.session_state and st.session_state['stock_data'] is not None:
        data = st.session_state['stock_data']
        symbol = st.session_state['symbol']
        
        # Current price and metrics
        current_price = data['Close'].iloc[-1]
        price_change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
        price_change_pct = (price_change / data['Close'].iloc[-2]) * 100
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>Current Price</h3>
                <h2 style="color: #00ff88;">${:.2f}</h2>
            </div>
            """.format(current_price), unsafe_allow_html=True)
        
        with col2:
            color = "#00ff88" if price_change >= 0 else "#ff4444"
            st.markdown("""
            <div class="metric-card">
                <h3>Change</h3>
                <h2 style="color: {};">${:.2f}</h2>
            </div>
            """.format(color, price_change), unsafe_allow_html=True)
        
        with col3:
            color = "#00ff88" if price_change_pct >= 0 else "#ff4444"
            st.markdown("""
            <div class="metric-card">
                <h3>Change %</h3>
                <h2 style="color: {};">{:.2f}%</h2>
            </div>
            """.format(color, price_change_pct), unsafe_allow_html=True)
        
        with col4:
            volume = data['Volume'].iloc[-1]
            st.markdown("""
            <div class="metric-card">
                <h3>Volume</h3>
                <h2 style="color: #00aaff;">{:,}</h2>
            </div>
            """.format(volume), unsafe_allow_html=True)
        
        # Chart
        st.subheader("📈 Stock Price Chart")
        chart = create_stock_chart(data, symbol)
        if chart:
            st.plotly_chart(chart, use_container_width=True)
        
        # Prediction
        st.subheader("🔮 Simple Prediction")
        prediction = calculate_simple_prediction(data)
        
        if prediction:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                direction_color = "#00ff88" if prediction['direction'] == "UP" else "#ff4444" if prediction['direction'] == "DOWN" else "#ffaa00"
                st.markdown("""
                <div class="metric-card">
                    <h3>Prediction</h3>
                    <h2 style="color: {};">{}</h2>
                </div>
                """.format(direction_color, prediction['direction']), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="metric-card">
                    <h3>Confidence</h3>
                    <h2 style="color: #00aaff;">{}%</h2>
                </div>
                """.format(prediction['confidence']), unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="metric-card">
                    <h3>Predicted Price</h3>
                    <h2 style="color: #00ff88;">${:.2f}</h2>
                </div>
                """.format(prediction['predicted_price']), unsafe_allow_html=True)
        
        # Data table
        st.subheader("📊 Recent Data")
        st.dataframe(data.tail(10), use_container_width=True)
        
    else:
        st.info("👈 Please enter a stock symbol and click 'Load Data' to get started.")
        st.markdown("""
        ### 📋 Popular Stock Symbols:
        - **AAPL** - Apple Inc.
        - **MSFT** - Microsoft Corporation
        - **GOOGL** - Alphabet Inc.
        - **AMZN** - Amazon.com Inc.
        - **TSLA** - Tesla Inc.
        - **META** - Meta Platforms Inc.
        - **NVDA** - NVIDIA Corporation
        - **NFLX** - Netflix Inc.
        """)

if __name__ == "__main__":
    main()