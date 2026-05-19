"""
Helper utility functions
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


def get_close_series(df: pd.DataFrame) -> pd.Series:
    """
    Extract close price series from DataFrame
    
    Args:
        df: DataFrame with price data
        
    Returns:
        Series of closing prices
    """
    if 'Close' in df.columns:
        return df['Close']
    elif 'close' in df.columns:
        return df['close']
    else:
        raise ValueError("DataFrame must contain 'Close' or 'close' column")


def last_n_months(end_date: datetime, months: int = 6) -> datetime:
    """
    Calculate date N months before end_date
    
    Args:
        end_date: End date
        months: Number of months to go back
        
    Returns:
        Start date
    """
    return end_date - pd.DateOffset(months=months)


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format value as percentage string
    
    Args:
        value: Numeric value
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    return f"{value:.{decimals}f}%"


def format_currency(value: float, symbol: str = "$", decimals: int = 2) -> str:
    """
    Format value as currency string
    
    Args:
        value: Numeric value
        symbol: Currency symbol
        decimals: Number of decimal places
        
    Returns:
        Formatted currency string
    """
    return f"{symbol}{value:,.{decimals}f}"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if denominator is zero
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if division by zero
        
    Returns:
        Result of division or default
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ZeroDivisionError):
        return default


def validate_ticker(ticker: str) -> bool:
    """
    Validate ticker symbol format
    
    Args:
        ticker: Ticker symbol
        
    Returns:
        True if valid, False otherwise
    """
    if not ticker or not isinstance(ticker, str):
        return False
    
    # Remove whitespace
    ticker = ticker.strip().upper()
    
    # Basic validation: alphanumeric, dots, hyphens
    if not ticker.replace('.', '').replace('-', '').isalnum():
        return False
    
    # Length check (most tickers are 1-5 characters)
    if len(ticker) < 1 or len(ticker) > 10:
        return False
    
    return True


def parse_period(period_str: str) -> Optional[str]:
    """
    Parse and validate period string for yfinance
    
    Args:
        period_str: Period string (e.g., '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max')
        
    Returns:
        Validated period string or None if invalid
    """
    valid_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    
    if period_str in valid_periods:
        return period_str
    
    logger.warning(f"Invalid period: {period_str}. Using default '1y'")
    return '1y'


def parse_interval(interval_str: str) -> Optional[str]:
    """
    Parse and validate interval string for yfinance
    
    Args:
        interval_str: Interval string (e.g., '1m', '5m', '1h', '1d', '1wk', '1mo')
        
    Returns:
        Validated interval string or None if invalid
    """
    valid_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
    
    if interval_str in valid_intervals:
        return interval_str
    
    logger.warning(f"Invalid interval: {interval_str}. Using default '1d'")
    return '1d'


def get_signal_emoji(signal: str) -> str:
    """
    Get emoji for signal type
    
    Args:
        signal: Signal type ('buy', 'sell', 'hold', 'neutral')
        
    Returns:
        Emoji string
    """
    signal_map = {
        'buy': '🟢',
        'strong_buy': '🟢🟢',
        'sell': '🔴',
        'strong_sell': '🔴🔴',
        'hold': '🟡',
        'neutral': '⚪'
    }
    return signal_map.get(signal.lower(), '⚪')


def truncate_string(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """
    Truncate string to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def dict_to_markdown_table(data: Dict[str, Any], headers: tuple = ('Key', 'Value')) -> str:
    """
    Convert dictionary to markdown table
    
    Args:
        data: Dictionary to convert
        headers: Table headers
        
    Returns:
        Markdown table string
    """
    lines = [
        f"| {headers[0]} | {headers[1]} |",
        "|---|---|"
    ]
    
    for key, value in data.items():
        # Format value based on type
        if isinstance(value, float):
            value_str = f"{value:.2f}"
        elif isinstance(value, (list, tuple)):
            value_str = ', '.join(str(v) for v in value)
        else:
            value_str = str(value)
        
        lines.append(f"| {key} | {value_str} |")
    
    return '\n'.join(lines)


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    Calculate percentage change between two values
    
    Args:
        old_value: Original value
        new_value: New value
        
    Returns:
        Percentage change
    """
    if old_value == 0:
        return 0.0
    return ((new_value - old_value) / old_value) * 100


def is_market_hours() -> bool:
    """
    Check if current time is during market hours (US Eastern Time)
    Simplified check - assumes weekdays 9:30 AM - 4:00 PM ET
    
    Returns:
        True if market is open, False otherwise
    """
    now = datetime.now()
    
    # Check if weekend
    if now.weekday() >= 5:  # Saturday = 5, Sunday = 6
        return False
    
    # Simplified check - would need proper timezone handling for production
    hour = now.hour
    return 9 <= hour < 16


def clean_ticker_symbol(ticker: str) -> str:
    """
    Clean and normalize ticker symbol
    
    Args:
        ticker: Raw ticker symbol
        
    Returns:
        Cleaned ticker symbol
    """
    return ticker.strip().upper().replace(' ', '')

# Made with Bob
