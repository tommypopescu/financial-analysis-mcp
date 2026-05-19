"""
Data extraction tools for fetching market data via yfinance
"""
import yfinance as yf
import pandas as pd
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

from ..config import config
from ..utils.helpers import validate_ticker, parse_period, parse_interval, clean_ticker_symbol

logger = logging.getLogger(__name__)


def fetch_ticker_data(
    ticker: str,
    period: str = None,
    interval: str = None,
    start: Optional[str] = None,
    end: Optional[str] = None
) -> Dict[str, Any]:
    """
    Fetch historical price and volume data for a ticker
    
    Args:
        ticker: Stock ticker symbol
        period: Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
        start: Start date (YYYY-MM-DD format)
        end: End date (YYYY-MM-DD format)
        
    Returns:
        Dictionary with ticker data and metadata
    """
    try:
        # Clean and validate ticker
        ticker = clean_ticker_symbol(ticker)
        if not validate_ticker(ticker):
            return {
                'success': False,
                'error': f'Invalid ticker symbol: {ticker}',
                'ticker': ticker
            }
        
        # Use defaults if not provided
        period = parse_period(period) if period else config.DEFAULT_PERIOD
        interval = parse_interval(interval) if interval else config.DEFAULT_INTERVAL
        
        logger.info(f"Fetching data for {ticker} (period={period}, interval={interval})")
        
        # Fetch data
        if start and end:
            df = yf.download(
                ticker,
                start=start,
                end=end,
                interval=interval,
                auto_adjust=True,
                progress=False,
                threads=False
            )
        else:
            df = yf.download(
                ticker,
                period=period,
                interval=interval,
                auto_adjust=True,
                progress=False,
                threads=False
            )
        
        if df is None or df.empty:
            return {
                'success': False,
                'error': f'No data available for {ticker}',
                'ticker': ticker
            }
        
        # Handle MultiIndex columns (yfinance sometimes returns this format)
        if isinstance(df.columns, pd.MultiIndex):
            # Flatten MultiIndex to single level - take the first level (field names)
            df.columns = df.columns.get_level_values(0)
        
        # Convert DataFrame to dict format
        # Use .values.tolist() to ensure we get a list even if column is a Series
        data_dict = {
            'dates': df.index.strftime('%Y-%m-%d').tolist(),
            'open': df['Open'].values.tolist() if 'Open' in df.columns else [],
            'high': df['High'].values.tolist() if 'High' in df.columns else [],
            'low': df['Low'].values.tolist() if 'Low' in df.columns else [],
            'close': df['Close'].values.tolist() if 'Close' in df.columns else [],
            'volume': df['Volume'].values.tolist() if 'Volume' in df.columns else []
        }
        
        return {
            'success': True,
            'ticker': ticker,
            'period': period,
            'interval': interval,
            'data_points': len(df),
            'start_date': df.index[0].strftime('%Y-%m-%d'),
            'end_date': df.index[-1].strftime('%Y-%m-%d'),
            'data': data_dict
        }
        
    except Exception as e:
        logger.error(f"Error fetching data for {ticker}: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'ticker': ticker
        }


def get_current_price(ticker: str) -> Dict[str, Any]:
    """
    Get current/latest price information for a ticker
    
    Args:
        ticker: Stock ticker symbol
        
    Returns:
        Dictionary with current price data
    """
    try:
        ticker = clean_ticker_symbol(ticker)
        if not validate_ticker(ticker):
            return {
                'success': False,
                'error': f'Invalid ticker symbol: {ticker}'
            }
        
        logger.info(f"Fetching current price for {ticker}")
        
        # Get ticker object
        stock = yf.Ticker(ticker)
        
        # Get latest data
        hist = stock.history(period='1d')
        if hist.empty:
            return {
                'success': False,
                'error': f'No price data available for {ticker}',
                'ticker': ticker
            }
        
        latest = hist.iloc[-1]
        
        # Get additional info
        info = stock.info
        
        return {
            'success': True,
            'ticker': ticker,
            'price': float(latest['Close']),
            'open': float(latest['Open']),
            'high': float(latest['High']),
            'low': float(latest['Low']),
            'volume': int(latest['Volume']),
            'timestamp': hist.index[-1].strftime('%Y-%m-%d %H:%M:%S'),
            'currency': info.get('currency', 'USD'),
            'market_cap': info.get('marketCap'),
            'previous_close': info.get('previousClose')
        }
        
    except Exception as e:
        logger.error(f"Error fetching current price for {ticker}: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'ticker': ticker
        }


def get_ticker_info(ticker: str) -> Dict[str, Any]:
    """
    Get company information and fundamentals for a ticker
    
    Args:
        ticker: Stock ticker symbol
        
    Returns:
        Dictionary with company information
    """
    try:
        ticker = clean_ticker_symbol(ticker)
        if not validate_ticker(ticker):
            return {
                'success': False,
                'error': f'Invalid ticker symbol: {ticker}'
            }
        
        logger.info(f"Fetching info for {ticker}")
        
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Extract key information
        result = {
            'success': True,
            'ticker': ticker,
            'company_name': info.get('longName', info.get('shortName', ticker)),
            'sector': info.get('sector'),
            'industry': info.get('industry'),
            'country': info.get('country'),
            'website': info.get('website'),
            'description': info.get('longBusinessSummary'),
            'market_cap': info.get('marketCap'),
            'enterprise_value': info.get('enterpriseValue'),
            'trailing_pe': info.get('trailingPE'),
            'forward_pe': info.get('forwardPE'),
            'peg_ratio': info.get('pegRatio'),
            'price_to_book': info.get('priceToBook'),
            'dividend_yield': info.get('dividendYield'),
            'beta': info.get('beta'),
            '52_week_high': info.get('fiftyTwoWeekHigh'),
            '52_week_low': info.get('fiftyTwoWeekLow'),
            'avg_volume': info.get('averageVolume'),
            'shares_outstanding': info.get('sharesOutstanding'),
            'float_shares': info.get('floatShares'),
            'employees': info.get('fullTimeEmployees')
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Error fetching info for {ticker}: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'ticker': ticker
        }


def get_multiple_tickers(
    tickers: List[str],
    period: str = None,
    interval: str = None
) -> Dict[str, Any]:
    """
    Fetch data for multiple tickers at once
    
    Args:
        tickers: List of ticker symbols
        period: Data period
        interval: Data interval
        
    Returns:
        Dictionary with data for all tickers
    """
    try:
        # Clean and validate tickers
        tickers = [clean_ticker_symbol(t) for t in tickers]
        valid_tickers = [t for t in tickers if validate_ticker(t)]
        
        if not valid_tickers:
            return {
                'success': False,
                'error': 'No valid tickers provided'
            }
        
        period = parse_period(period) if period else config.DEFAULT_PERIOD
        interval = parse_interval(interval) if interval else config.DEFAULT_INTERVAL
        
        logger.info(f"Fetching data for {len(valid_tickers)} tickers")
        
        results = {}
        for ticker in valid_tickers:
            result = fetch_ticker_data(ticker, period, interval)
            results[ticker] = result
        
        successful = sum(1 for r in results.values() if r.get('success'))
        
        return {
            'success': True,
            'total_tickers': len(valid_tickers),
            'successful': successful,
            'failed': len(valid_tickers) - successful,
            'results': results
        }
        
    except Exception as e:
        logger.error(f"Error fetching multiple tickers: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

# Made with Bob
