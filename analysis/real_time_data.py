import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
from typing import Dict, List, Optional

class RealTimeDataFetcher:
    """Fetch real-time stock data from various APIs"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_yahoo_finance_data(self, symbol: str, period: str = "1mo") -> pd.DataFrame:
        """Fetch data from Yahoo Finance (free, no API key required)"""
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            params = {
                'range': period,
                'interval': '1d',
                'includePrePost': 'true',
                'events': 'div,split'
            }
            
            response = self.session.get(url, params=params)
            data = response.json()
            
            if 'chart' not in data or not data['chart']['result']:
                raise ValueError(f"No data found for symbol: {symbol}")
            
            result = data['chart']['result'][0]
            timestamps = result['timestamp']
            quotes = result['indicators']['quote'][0]
            
            df = pd.DataFrame({
                'datetime': [datetime.fromtimestamp(ts) for ts in timestamps],
                'open': quotes['open'],
                'high': quotes['high'],
                'low': quotes['low'],
                'close': quotes['close'],
                'volume': quotes['volume']
            })
            
            df = df.dropna()
            df['symbol'] = symbol
            return df
            
        except Exception as e:
            print(f"Error fetching Yahoo Finance data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_alpha_vantage_data(self, symbol: str, api_key: str) -> pd.DataFrame:
        """Fetch data from Alpha Vantage API"""
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'TIME_SERIES_DAILY',
                'symbol': symbol,
                'apikey': api_key,
                'outputsize': 'compact'
            }
            
            response = self.session.get(url, params=params)
            data = response.json()
            
            if 'Time Series (Daily)' not in data:
                raise ValueError(f"No data found for symbol: {symbol}")
            
            time_series = data['Time Series (Daily)']
            df_data = []
            
            for date, values in time_series.items():
                df_data.append({
                    'datetime': pd.to_datetime(date),
                    'open': float(values['1. open']),
                    'high': float(values['2. high']),
                    'low': float(values['3. low']),
                    'close': float(values['4. close']),
                    'volume': int(values['5. volume'])
                })
            
            df = pd.DataFrame(df_data)
            df = df.sort_values('datetime')
            df['symbol'] = symbol
            return df
            
        except Exception as e:
            print(f"Error fetching Alpha Vantage data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_market_news(self, symbol: str = None, limit: int = 10) -> List[Dict]:
        """Fetch market news (mock implementation - in real app, use NewsAPI or similar)"""
        # This is a mock implementation
        # In a real application, you would use NewsAPI, Bloomberg API, or similar
        mock_news = [
            {
                'title': f'Market Update: {symbol or "General Market"} Shows Strong Performance',
                'summary': 'Trading volumes increased significantly with positive market sentiment.',
                'published': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'Financial Times'
            },
            {
                'title': 'Technical Analysis: Bullish Patterns Emerging',
                'summary': 'Chart patterns suggest continued upward momentum in the coming weeks.',
                'published': (datetime.now() - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'MarketWatch'
            }
        ]
        return mock_news[:limit]
    
    def calculate_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators for the data"""
        if df.empty:
            return df
        
        # Moving averages
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['sma_50'] = df['close'].rolling(window=50).mean()
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        df['bb_middle'] = df['close'].rolling(window=20).mean()
        bb_std = df['close'].rolling(window=20).std()
        df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
        df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
        
        # MACD
        exp1 = df['close'].ewm(span=12).mean()
        exp2 = df['close'].ewm(span=26).mean()
        df['macd'] = exp1 - exp2
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        df['macd_histogram'] = df['macd'] - df['macd_signal']
        
        return df
    
    def get_portfolio_analysis(self, symbols: List[str], weights: List[float] = None) -> Dict:
        """Analyze a portfolio of stocks"""
        if weights is None:
            weights = [1.0 / len(symbols)] * len(symbols)
        
        portfolio_data = {}
        total_return = 0
        
        for symbol, weight in zip(symbols, weights):
            df = self.get_yahoo_finance_data(symbol)
            if not df.empty:
                df = self.calculate_technical_indicators(df)
                portfolio_data[symbol] = df
                
                # Calculate returns
                if len(df) > 1:
                    returns = df['close'].pct_change().dropna()
                    total_return += returns.mean() * weight
        
        return {
            'portfolio_data': portfolio_data,
            'total_return': total_return,
            'symbols': symbols,
            'weights': weights
        }
    
    def get_market_sentiment(self, symbol: str) -> Dict:
        """Get market sentiment analysis (mock implementation)"""
        # In a real application, this would analyze news, social media, etc.
        sentiment_scores = {
            'positive': np.random.uniform(0.3, 0.7),
            'negative': np.random.uniform(0.1, 0.4),
            'neutral': np.random.uniform(0.2, 0.5)
        }
        
        # Normalize to sum to 1
        total = sum(sentiment_scores.values())
        for key in sentiment_scores:
            sentiment_scores[key] /= total
        
        return {
            'symbol': symbol,
            'sentiment': sentiment_scores,
            'overall_sentiment': 'positive' if sentiment_scores['positive'] > 0.4 else 'negative',
            'confidence': max(sentiment_scores.values())
        }

# Usage examples and utility functions
def fetch_stock_data(symbol: str, source: str = 'yahoo') -> pd.DataFrame:
    """Convenience function to fetch stock data"""
    fetcher = RealTimeDataFetcher()
    
    if source == 'yahoo':
        return fetcher.get_yahoo_finance_data(symbol)
    else:
        # Add other sources as needed
        return pd.DataFrame()

def analyze_stock_performance(symbol: str) -> Dict:
    """Analyze a single stock's performance"""
    fetcher = RealTimeDataFetcher()
    df = fetcher.get_yahoo_finance_data(symbol)
    
    if df.empty:
        return {'error': f'No data found for {symbol}'}
    
    df = fetcher.calculate_technical_indicators(df)
    
    # Calculate performance metrics
    returns = df['close'].pct_change().dropna()
    
    analysis = {
        'symbol': symbol,
        'current_price': df['close'].iloc[-1],
        'price_change': df['close'].iloc[-1] - df['close'].iloc[-2],
        'price_change_pct': (df['close'].iloc[-1] - df['close'].iloc[-2]) / df['close'].iloc[-2] * 100,
        'volatility': returns.std() * np.sqrt(252),  # Annualized
        'sharpe_ratio': returns.mean() / returns.std() * np.sqrt(252),
        'rsi': df['rsi'].iloc[-1] if not pd.isna(df['rsi'].iloc[-1]) else None,
        'sma_20': df['sma_20'].iloc[-1] if not pd.isna(df['sma_20'].iloc[-1]) else None,
        'sma_50': df['sma_50'].iloc[-1] if not pd.isna(df['sma_50'].iloc[-1]) else None,
        'sentiment': fetcher.get_market_sentiment(symbol)
    }
    
    return analysis
