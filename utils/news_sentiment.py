import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import streamlit as st
from textblob import TextBlob
import re

class NewsSentimentAnalyzer:
    """News sentiment analysis and market intelligence system"""
    
    def __init__(self):
        self.cache = {}
        self.cache_duration = 300  # 5 minutes
        
    def clean_text(self, text):
        """Clean and preprocess text for sentiment analysis"""
        if not text:
            return ""
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of given text using TextBlob"""
        if not text:
            return {'polarity': 0, 'subjectivity': 0, 'sentiment': 'neutral'}
        
        try:
            cleaned_text = self.clean_text(text)
            blob = TextBlob(cleaned_text)
            
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Classify sentiment
            if polarity > 0.1:
                sentiment = 'positive'
            elif polarity < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            return {
                'polarity': polarity,
                'subjectivity': subjectivity,
                'sentiment': sentiment
            }
            
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return {'polarity': 0, 'subjectivity': 0, 'sentiment': 'neutral'}
    
    def get_stock_news_mock(self, symbol, company_name):
        """Mock news data for demonstration (replace with real API)"""
        
        # Generate realistic mock news data
        mock_news = [
            {
                'headline': f'{company_name} Reports Strong Q4 Earnings, Beats Estimates',
                'summary': f'{company_name} announced strong quarterly results with revenue growth of 15% year-over-year, exceeding analyst expectations.',
                'published_date': (datetime.now() - timedelta(hours=2)).isoformat(),
                'source': 'Business Standard',
                'url': 'https://example.com/news1',
                'relevance_score': 0.95
            },
            {
                'headline': f'Analysts Upgrade {company_name} Stock to Buy Rating',
                'summary': f'Leading investment firm upgrades {company_name} citing strong fundamentals and growth prospects in the sector.',
                'published_date': (datetime.now() - timedelta(hours=6)).isoformat(),
                'source': 'Economic Times',
                'url': 'https://example.com/news2',
                'relevance_score': 0.87
            },
            {
                'headline': f'{company_name} Announces Strategic Partnership for Digital Transformation',
                'summary': f'{company_name} partners with technology leader to accelerate digital initiatives and improve operational efficiency.',
                'published_date': (datetime.now() - timedelta(hours=12)).isoformat(),
                'source': 'Financial Express',
                'url': 'https://example.com/news3',
                'relevance_score': 0.78
            },
            {
                'headline': f'Market Volatility Affects {company_name} Stock Price',
                'summary': f'{company_name} shares fluctuate amid broader market uncertainty and sector-specific challenges.',
                'published_date': (datetime.now() - timedelta(days=1)).isoformat(),
                'source': 'Mint',
                'url': 'https://example.com/news4',
                'relevance_score': 0.65
            },
            {
                'headline': f'{company_name} Expands Operations in Emerging Markets',
                'summary': f'{company_name} announces expansion plans in key emerging markets to drive future growth and market share.',
                'published_date': (datetime.now() - timedelta(days=2)).isoformat(),
                'source': 'Bloomberg',
                'url': 'https://example.com/news5',
                'relevance_score': 0.82
            }
        ]
        
        return mock_news
    
    def get_news_sentiment(self, symbol, company_name):
        """Get news sentiment analysis for a stock"""
        cache_key = f"news_sentiment_{symbol}"
        current_time = time.time()
        
        # Check cache
        if (cache_key in self.cache and 
            current_time - self.cache[cache_key]['timestamp'] < self.cache_duration):
            return self.cache[cache_key]['data']
        
        try:
            # Get news data (using mock data for now)
            news_data = self.get_stock_news_mock(symbol, company_name)
            
            # Analyze sentiment for each news item
            analyzed_news = []
            sentiment_scores = []
            
            for news in news_data:
                # Analyze headline and summary
                headline_sentiment = self.analyze_sentiment(news['headline'])
                summary_sentiment = self.analyze_sentiment(news['summary'])
                
                # Combine sentiment scores (weighted average)
                combined_polarity = (headline_sentiment['polarity'] * 0.7 + 
                                   summary_sentiment['polarity'] * 0.3)
                combined_subjectivity = (headline_sentiment['subjectivity'] * 0.7 + 
                                       summary_sentiment['subjectivity'] * 0.3)
                
                # Apply relevance score weighting
                weighted_polarity = combined_polarity * news['relevance_score']
                
                news_with_sentiment = {
                    **news,
                    'sentiment': {
                        'polarity': combined_polarity,
                        'subjectivity': combined_subjectivity,
                        'weighted_polarity': weighted_polarity,
                        'classification': 'positive' if combined_polarity > 0.1 else 'negative' if combined_polarity < -0.1 else 'neutral'
                    }
                }
                
                analyzed_news.append(news_with_sentiment)
                sentiment_scores.append(weighted_polarity)
            
            # Calculate overall sentiment
            if sentiment_scores:
                overall_sentiment = np.mean(sentiment_scores)
                sentiment_distribution = {
                    'positive': len([s for s in sentiment_scores if s > 0.1]),
                    'negative': len([s for s in sentiment_scores if s < -0.1]),
                    'neutral': len([s for s in sentiment_scores if -0.1 <= s <= 0.1])
                }
            else:
                overall_sentiment = 0
                sentiment_distribution = {'positive': 0, 'negative': 0, 'neutral': 0}
            
            # Determine sentiment signal
            if overall_sentiment > 0.2:
                sentiment_signal = 'Very Positive'
            elif overall_sentiment > 0.1:
                sentiment_signal = 'Positive'
            elif overall_sentiment < -0.2:
                sentiment_signal = 'Very Negative'
            elif overall_sentiment < -0.1:
                sentiment_signal = 'Negative'
            else:
                sentiment_signal = 'Neutral'
            
            result = {
                'symbol': symbol,
                'company_name': company_name,
                'overall_sentiment': overall_sentiment,
                'sentiment_signal': sentiment_signal,
                'sentiment_distribution': sentiment_distribution,
                'news_count': len(analyzed_news),
                'news_items': analyzed_news,
                'last_updated': datetime.now().isoformat()
            }
            
            # Cache the result
            self.cache[cache_key] = {
                'data': result,
                'timestamp': current_time
            }
            
            return result
            
        except Exception as e:
            print(f"Error getting news sentiment for {symbol}: {e}")
            return {
                'symbol': symbol,
                'company_name': company_name,
                'overall_sentiment': 0,
                'sentiment_signal': 'Neutral',
                'sentiment_distribution': {'positive': 0, 'negative': 0, 'neutral': 0},
                'news_count': 0,
                'news_items': [],
                'last_updated': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def get_market_sentiment(self, symbols_list):
        """Get overall market sentiment from multiple stocks"""
        market_sentiments = []
        
        for symbol in symbols_list:
            sentiment_data = self.get_news_sentiment(symbol, symbol)
            if sentiment_data and 'overall_sentiment' in sentiment_data:
                market_sentiments.append(sentiment_data['overall_sentiment'])
        
        if not market_sentiments:
            return {
                'market_sentiment': 0,
                'sentiment_signal': 'Neutral',
                'analyzed_stocks': 0
            }
        
        overall_market_sentiment = np.mean(market_sentiments)
        
        # Determine market sentiment signal
        if overall_market_sentiment > 0.15:
            market_signal = 'Very Bullish'
        elif overall_market_sentiment > 0.05:
            market_signal = 'Bullish'
        elif overall_market_sentiment < -0.15:
            market_signal = 'Very Bearish'
        elif overall_market_sentiment < -0.05:
            market_signal = 'Bearish'
        else:
            market_signal = 'Neutral'
        
        return {
            'market_sentiment': overall_market_sentiment,
            'sentiment_signal': market_signal,
            'analyzed_stocks': len(market_sentiments),
            'sentiment_distribution': {
                'positive': len([s for s in market_sentiments if s > 0.1]),
                'negative': len([s for s in market_sentiments if s < -0.1]),
                'neutral': len([s for s in market_sentiments if -0.1 <= s <= 0.1])
            }
        }
    
    def get_trending_topics(self, news_items):
        """Extract trending topics from news headlines"""
        if not news_items:
            return []
        
        # Simple keyword extraction from headlines
        keywords = {}
        
        for item in news_items:
            headline = item.get('headline', '')
            words = self.clean_text(headline).lower().split()
            
            for word in words:
                if len(word) > 3:  # Filter out short words
                    keywords[word] = keywords.get(word, 0) + 1
        
        # Sort by frequency and return top keywords
        sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
        return sorted_keywords[:10]  # Top 10 trending topics
    
    def sentiment_impact_score(self, sentiment_data, stock_data):
        """Calculate potential impact of sentiment on stock price"""
        if not sentiment_data or not stock_data:
            return 0
        
        overall_sentiment = sentiment_data.get('overall_sentiment', 0)
        news_count = sentiment_data.get('news_count', 0)
        
        # Calculate recent volatility
        if len(stock_data) >= 20:
            recent_volatility = stock_data['Close'].tail(20).pct_change().std()
        else:
            recent_volatility = 0.02  # Default volatility
        
        # Impact score calculation
        # Higher sentiment + more news + higher volatility = higher impact
        base_impact = abs(overall_sentiment) * 100
        news_multiplier = min(news_count / 10, 1.0)  # Cap at 10 news items
        volatility_multiplier = min(recent_volatility * 50, 2.0)  # Cap multiplier
        
        impact_score = base_impact * news_multiplier * volatility_multiplier
        
        return min(impact_score, 100)  # Cap at 100
    
    def get_sentiment_signals(self, sentiment_data):
        """Generate trading signals based on sentiment"""
        try:
            signals = []
            
            avg_sentiment = sentiment_data.get('average_sentiment', 0)
            confidence = sentiment_data.get('confidence', 0)
            
            if avg_sentiment > 0.3 and confidence > 0.7:
                signals.append({
                    'signal': 'BUY',
                    'strength': 'Strong',
                    'reason': 'Very positive sentiment with high confidence'
                })
            elif avg_sentiment > 0.1 and confidence > 0.5:
                signals.append({
                    'signal': 'BUY',
                    'strength': 'Moderate',
                    'reason': 'Positive sentiment detected'
                })
            elif avg_sentiment < -0.3 and confidence > 0.7:
                signals.append({
                    'signal': 'SELL',
                    'strength': 'Strong',
                    'reason': 'Very negative sentiment with high confidence'
                })
            elif avg_sentiment < -0.1 and confidence > 0.5:
                signals.append({
                    'signal': 'SELL',
                    'strength': 'Moderate',
                    'reason': 'Negative sentiment detected'
                })
            else:
                signals.append({
                    'signal': 'HOLD',
                    'strength': 'Neutral',
                    'reason': 'Mixed or neutral sentiment'
                })
            
            return signals
            
        except Exception as e:
            print(f"Error generating sentiment signals: {str(e)}")
            return []
    
    def render_news_tab(self, symbol):
        """Render the complete news and sentiment analysis interface"""
        st.markdown("# 📰 News & Sentiment Analysis")
        
        # Validate input
        if not symbol or symbol.strip() == "":
            st.warning("Please select a stock symbol to analyze news sentiment.")
            st.info("💡 Use the sidebar to select a stock for news analysis.")
            return
        
        # Validate symbol format
        if not isinstance(symbol, str) or len(symbol) < 2:
            st.error("❌ Invalid stock symbol format.")
            return
        
        # Get company name for better news results
        from config.settings import INDIAN_STOCKS
        company_name = INDIAN_STOCKS.get(symbol, symbol)
        
        try:
            # News and sentiment analysis
            st.markdown(f"### 📰 Latest News for {company_name} ({symbol})")
            
            with st.spinner("🔍 Fetching latest news and analyzing sentiment..."):
                # Get news and sentiment
                news_sentiment = self.get_news_sentiment(symbol, company_name)
                
                if news_sentiment and news_sentiment.get('news_items'):
                    # Display sentiment overview
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        avg_sentiment = news_sentiment.get('average_sentiment', 0)
                        sentiment_label = self._get_sentiment_label(avg_sentiment)
                        sentiment_color = self._get_sentiment_color(avg_sentiment)
                        st.metric("📊 Overall Sentiment", sentiment_label, delta=f"{avg_sentiment:.3f}")
                    
                    with col2:
                        confidence = news_sentiment.get('confidence', 0)
                        st.metric("🎯 Confidence", f"{confidence:.1%}")
                    
                    with col3:
                        news_count = len(news_sentiment.get('news_items', []))
                        st.metric("📄 News Articles", news_count)
                    
                    # Sentiment signals
                    st.markdown("### 🚦 Trading Signals Based on Sentiment")
                    signals = self.get_sentiment_signals(news_sentiment)
                    
                    for signal in signals:
                        signal_color = {
                            'BUY': '🟢',
                            'SELL': '🔴', 
                            'HOLD': '🟡'
                        }.get(signal['signal'], '⚪')
                        
                        st.info(f"{signal_color} **{signal['signal']}** ({signal['strength']}) - {signal['reason']}")
                    
                    # News articles display
                    st.markdown("### 📰 Recent News Articles")
                    
                    for i, article in enumerate(news_sentiment['news_items'][:10], 1):
                        with st.expander(f"📄 Article {i}: {article['title'][:80]}..."):
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                st.markdown(f"**Title:** {article['title']}")
                                st.markdown(f"**Summary:** {article['content'][:300]}...")
                                st.markdown(f"**Source:** {article['source']}")
                                st.markdown(f"**Published:** {article['published_date']}")
                            
                            with col2:
                                sentiment_score = article.get('sentiment_score', 0)
                                sentiment_label = self._get_sentiment_label(sentiment_score)
                                sentiment_emoji = self._get_sentiment_emoji(sentiment_score)
                                
                                st.markdown(f"**Sentiment:** {sentiment_emoji}")
                                st.markdown(f"**Score:** {sentiment_score:.3f}")
                                st.markdown(f"**Label:** {sentiment_label}")
                    
                    # Sentiment distribution chart
                    st.markdown("### 📊 Sentiment Distribution")
                    self._render_sentiment_chart(news_sentiment)
                    
                else:
                    st.warning("⚠️ No recent news found for this stock.")
                    st.info("💡 Try checking back later or verify the stock symbol is correct.")
            
            # Market sentiment analysis
            st.markdown("---")
            st.markdown("### 🌍 Market Sentiment Overview")
            
            with st.spinner("🔍 Analyzing broader market sentiment..."):
                # Get market sentiment for related stocks
                try:
                    related_symbols = [symbol]  # Could expand this to include sector stocks
                    market_sentiment = self.get_market_sentiment(related_symbols)
                    
                    if market_sentiment:
                        st.markdown("#### 📈 Market Sentiment Summary")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            market_score = market_sentiment.get('overall_sentiment', 0)
                            market_label = self._get_sentiment_label(market_score)
                            st.metric("🌍 Market Sentiment", market_label, delta=f"{market_score:.3f}")
                        
                        with col2:
                            trend = market_sentiment.get('trend', 'Neutral')
                            trend_emoji = "📈" if trend == "Positive" else "📉" if trend == "Negative" else "➡️"
                            st.metric("📊 Trend Direction", f"{trend_emoji} {trend}")
                        
                        # Trending topics
                        trending = self.get_trending_topics(news_sentiment.get('news_items', []))
                        if trending:
                            st.markdown("#### 🔥 Trending Topics")
                            for topic, frequency in trending.items():
                                st.info(f"🏷️ **{topic}**: Mentioned {frequency} times")
                
                except Exception as e:
                    st.warning(f"⚠️ Could not fetch market sentiment: {str(e)}")
            
        except Exception as e:
            st.error(f"❌ Error in news analysis: {str(e)}")
            st.info("Please try refreshing or check your internet connection.")
    
    def _get_sentiment_label(self, score):
        """Convert sentiment score to label"""
        if score > 0.3:
            return "Very Positive"
        elif score > 0.1:
            return "Positive"
        elif score > -0.1:
            return "Neutral"
        elif score > -0.3:
            return "Negative"
        else:
            return "Very Negative"
    
    def _get_sentiment_color(self, score):
        """Get color for sentiment score"""
        if score > 0.1:
            return "green"
        elif score < -0.1:
            return "red"
        else:
            return "gray"
    
    def _get_sentiment_emoji(self, score):
        """Get emoji for sentiment score"""
        if score > 0.3:
            return "😄 Very Positive"
        elif score > 0.1:
            return "🙂 Positive"
        elif score > -0.1:
            return "😐 Neutral"
        elif score > -0.3:
            return "🙁 Negative"
        else:
            return "😞 Very Negative"
    
    def _render_sentiment_chart(self, news_sentiment):
        """Render sentiment distribution chart"""
        try:
            import plotly.graph_objects as go
            
            news_items = news_sentiment.get('news_items', [])
            if not news_items:
                return
            
            # Count sentiment categories
            sentiment_counts = {
                'Very Positive': 0,
                'Positive': 0,
                'Neutral': 0,
                'Negative': 0,
                'Very Negative': 0
            }
            
            for article in news_items:
                score = article.get('sentiment_score', 0)
                label = self._get_sentiment_label(score)
                sentiment_counts[label] += 1
            
            # Create pie chart
            fig = go.Figure(data=[go.Pie(
                labels=list(sentiment_counts.keys()),
                values=list(sentiment_counts.values()),
                hole=0.3,
                marker_colors=['#00ff88', '#90EE90', '#FFD700', '#FFA500', '#ff0044']
            )])
            
            fig.update_layout(
                title=dict(
                    text="News Sentiment Distribution",
                    font=dict(color='white', size=16)
                ),
                template="plotly_dark",
                paper_bgcolor='black',
                plot_bgcolor='black',
                font=dict(color='white'),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.warning(f"⚠️ Could not render sentiment chart: {str(e)}")