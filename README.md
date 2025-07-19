

# StockTrendAI - Advanced Indian Stock Market Predictor

🚀 **AI-Powered Stock Market Prediction Platform with 7 Advanced Machine Learning Models**

## 🌟 Features

- **🤖 7 Advanced AI Models**: XGBoost, LSTM, Prophet, Ensemble, Transformer, GRU, and Stacking
- **📊 Real-time Data**: Live Indian stock market data from Yahoo Finance
- **📈 Interactive Charts**: Beautiful Plotly visualizations with technical indicators
- **💼 Portfolio Management**: Track holdings, watchlist, and price alerts
- **📰 News Sentiment**: AI-powered news analysis and sentiment scoring
- **📊 Advanced Analytics**: Risk analysis, Monte Carlo simulation, correlation analysis
- **🎯 Multi-Model Consensus**: Combined predictions with confidence scoring

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/pratham5188/StockTrendAI1.git
   cd StockTrendAI1
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

### Streamlit Cloud Deployment

This application is configured for easy deployment on Streamlit Cloud:

1. **Fork this repository** to your GitHub account
2. **Connect to Streamlit Cloud** at [share.streamlit.io](https://share.streamlit.io)
3. **Deploy** by selecting your forked repository
4. **Access** your live application

## 📋 Requirements

### Python Dependencies
- Python 3.11+
- Streamlit 1.47.0+
- Pandas 2.0.0+
- Plotly 5.15.0+
- Scikit-learn 1.3.0+
- YFinance 0.2.18+
- XGBoost 2.0.0+
- TensorFlow 2.13.0+
- Prophet 1.1.4+

### System Dependencies
- Internet connection for real-time data
- 4GB+ RAM recommended for optimal performance

## 🏗️ Project Structure

```
StockTrendAI1/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── packages.txt          # System dependencies
├── .streamlit/           # Streamlit configuration
│   └── config.toml      # Server and theme settings
├── models/              # AI model implementations
├── utils/               # Utility functions and components
├── config/              # Configuration files
├── styles/              # CSS styling
└── README.md           # This file
```

## 🔧 Configuration

### Streamlit Configuration
The application uses a custom Streamlit configuration in `.streamlit/config.toml`:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#00ff88"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#262730"
textColor = "#ffffff"
```

## 📊 Supported Stocks

The application supports all major Indian stocks and indices:

- **NIFTY 50** stocks (RELIANCE, TCS, HDFC, etc.)
- **SENSEX** components
- **Bank NIFTY** stocks
- **Custom stocks** can be added via the interface

## 🤖 AI Models

1. **XGBoost**: Gradient boosting for fast predictions
2. **LSTM**: Deep learning for sequence modeling
3. **Prophet**: Facebook's time series forecasting
4. **Ensemble**: Multi-model combination
5. **Transformer**: Attention-based neural networks
6. **GRU**: Gated Recurrent Units
7. **Stacking**: Meta-learning ensemble

## 🎯 Usage

1. **Select a Stock**: Choose from the dropdown in the sidebar
2. **Choose Models**: Select which AI models to use for predictions
3. **View Predictions**: See individual model predictions and consensus
4. **Analyze Data**: Use the various tabs for comprehensive analysis
5. **Manage Portfolio**: Track your investments and set alerts

## 🔍 Troubleshooting

### Common Issues

1. **Data Loading Errors**
   - Check internet connection
   - Try refreshing the page
   - Select a different stock

2. **Model Prediction Failures**
   - Ensure sufficient historical data (30+ days recommended)
   - Try different time periods
   - Check model selection in sidebar

3. **Deployment Issues**
   - Verify all dependencies are in `requirements.txt`
   - Check Streamlit Cloud logs for errors
   - Ensure proper file structure

### Health Check

The application includes a health check endpoint for deployment monitoring:
```python
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
```

## 📈 Performance Tips

- Use multiple models for better consensus
- Check confidence levels before making decisions
- Consider market conditions and news sentiment
- Use longer time periods for more accurate predictions
- Monitor technical indicators for additional insights

## ⚠️ Disclaimer

This application is for educational and research purposes only. Stock market predictions are inherently uncertain and should not be used as the sole basis for investment decisions. Always consult with financial advisors and conduct your own research before making investment decisions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Check the troubleshooting section above
- Review Streamlit Cloud logs
- Open an issue on GitHub

---

**Made with ❤️ for the Indian Stock Market Community**

