"""
Core calculation functions for technical indicators
Extracted and adapted from the original RSI & MACD GUI script
"""
import pandas as pd
import numpy as np
from typing import Tuple, Optional


def compute_rsi(close: pd.Series, window: int = 14) -> pd.Series:
    """
    Calculate Relative Strength Index (RSI)
    
    Args:
        close: Series of closing prices
        window: RSI period (default: 14)
        
    Returns:
        Series of RSI values
    """
    if isinstance(close, pd.DataFrame):
        close = close.squeeze()
    delta = close.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def compute_macd(
    close: pd.Series, 
    fast: int = 12, 
    slow: int = 26, 
    signal: int = 9
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    Calculate MACD (Moving Average Convergence Divergence)
    
    Args:
        close: Series of closing prices
        fast: Fast EMA period (default: 12)
        slow: Slow EMA period (default: 26)
        signal: Signal line period (default: 9)
        
    Returns:
        Tuple of (macd_line, signal_line, histogram)
    """
    if isinstance(close, pd.DataFrame):
        close = close.squeeze()
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def compute_adx(df: pd.DataFrame, period: int = 14) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    """
    Calculate ADX (Average Directional Index) with +DI, -DI, and ATR
    
    Args:
        df: DataFrame with High, Low, Close columns
        period: ADX period (default: 14)
        
    Returns:
        Tuple of (adx, plus_di, minus_di, atr)
    """
    high, low, close = df['High'], df['Low'], df['Close']
    
    # True Range
    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    
    # Directional Movement
    up_move = high - high.shift()
    down_move = low.shift() - low
    plus_dm = up_move.where((up_move > down_move) & (up_move > 0), 0.0)
    minus_dm = down_move.where((down_move > up_move) & (down_move > 0), 0.0)
    
    # Directional Indicators
    plus_di = 100 * (plus_dm.rolling(window=period).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(window=period).mean() / atr)
    
    # ADX
    dx = 100 * ((plus_di - minus_di).abs() / (plus_di + minus_di))
    adx = dx.rolling(window=period).mean()
    
    return adx, plus_di, minus_di, atr


def compute_supertrend(
    df: pd.DataFrame, 
    period: int = 10, 
    multiplier: float = 3.0
) -> pd.Series:
    """
    Calculate Supertrend indicator
    
    Args:
        df: DataFrame with High, Low, Close columns
        period: ATR period (default: 10)
        multiplier: ATR multiplier (default: 3.0)
        
    Returns:
        Series of Supertrend values
    """
    high, low, close = df['High'], df['Low'], df['Close']
    
    # ATR calculation
    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    
    # Basic bands
    hl_avg = (high + low) / 2
    upper_band = hl_avg + (multiplier * atr)
    lower_band = hl_avg - (multiplier * atr)
    
    # Supertrend calculation
    supertrend = pd.Series(index=df.index, dtype=float)
    direction = pd.Series(index=df.index, dtype=int)
    
    for i in range(period, len(df)):
        if i == period:
            supertrend.iloc[i] = lower_band.iloc[i]
            direction.iloc[i] = 1
        else:
            if close.iloc[i] > supertrend.iloc[i-1]:
                supertrend.iloc[i] = lower_band.iloc[i]
                direction.iloc[i] = 1
            else:
                supertrend.iloc[i] = upper_band.iloc[i]
                direction.iloc[i] = -1
                
    return supertrend


def compute_stochastic(
    df: pd.DataFrame, 
    k_period: int = 14, 
    d_period: int = 3
) -> Tuple[pd.Series, pd.Series]:
    """
    Calculate Stochastic Oscillator
    
    Args:
        df: DataFrame with High, Low, Close columns
        k_period: %K period (default: 14)
        d_period: %D period (default: 3)
        
    Returns:
        Tuple of (%K, %D)
    """
    high, low, close = df['High'], df['Low'], df['Close']
    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()
    k = 100 * ((close - lowest_low) / (highest_high - lowest_low))
    d = k.rolling(window=d_period).mean()
    return k, d


def compute_bbands(
    close: pd.Series, 
    period: int = 20, 
    std_dev: float = 2.0
) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    """
    Calculate Bollinger Bands
    
    Args:
        close: Series of closing prices
        period: Moving average period (default: 20)
        std_dev: Standard deviation multiplier (default: 2.0)
        
    Returns:
        Tuple of (middle_band, upper_band, lower_band, bandwidth)
    """
    if isinstance(close, pd.DataFrame):
        close = close.squeeze()
    middle = close.rolling(window=period).mean()
    std = close.rolling(window=period).std()
    upper = middle + (std_dev * std)
    lower = middle - (std_dev * std)
    bandwidth = (upper - lower) / middle
    return middle, upper, lower, bandwidth


def compute_obv(df: pd.DataFrame) -> pd.Series:
    """
    Calculate On-Balance Volume (OBV)
    
    Args:
        df: DataFrame with Close and Volume columns
        
    Returns:
        Series of OBV values
    """
    close, volume = df['Close'], df['Volume']
    obv = (volume * ((close.diff() > 0).astype(int) - (close.diff() < 0).astype(int))).cumsum()
    return obv


def compute_mfi(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculate Money Flow Index (MFI)
    
    Args:
        df: DataFrame with High, Low, Close, Volume columns
        period: MFI period (default: 14)
        
    Returns:
        Series of MFI values
    """
    high, low, close, volume = df['High'], df['Low'], df['Close'], df['Volume']
    typical_price = (high + low + close) / 3
    money_flow = typical_price * volume
    
    positive_flow = money_flow.where(typical_price > typical_price.shift(), 0.0).rolling(window=period).sum()
    negative_flow = money_flow.where(typical_price < typical_price.shift(), 0.0).rolling(window=period).sum()
    
    mfi = 100 - (100 / (1 + positive_flow / negative_flow.replace(0, np.nan)))
    return mfi


def compute_breadth_over_ma(close: pd.Series, ma_period: int = 200) -> float:
    """
    Calculate percentage of price above moving average
    
    Args:
        close: Series of closing prices
        ma_period: Moving average period (default: 200)
        
    Returns:
        Percentage above MA
    """
    ma = close.rolling(window=ma_period).mean()
    return float((close > ma).sum() / len(close) * 100)


def proximity_52w(close: pd.Series) -> Tuple[float, float]:
    """
    Calculate distance from 52-week high and low
    
    Args:
        close: Series of closing prices
        
    Returns:
        Tuple of (distance_from_high_pct, distance_from_low_pct)
    """
    last_price = close.iloc[-1]
    high_52w = close.rolling(window=252).max().iloc[-1]
    low_52w = close.rolling(window=252).min().iloc[-1]
    
    dist_high = ((last_price - high_52w) / high_52w * 100) if high_52w > 0 else 0.0
    dist_low = ((last_price - low_52w) / low_52w * 100) if low_52w > 0 else 0.0
    
    return dist_high, dist_low


def max_drawdown(close: pd.Series) -> float:
    """
    Calculate maximum drawdown
    
    Args:
        close: Series of closing prices
        
    Returns:
        Maximum drawdown percentage
    """
    cummax = close.cummax()
    drawdown = (close - cummax) / cummax
    return float(drawdown.min() * 100)


def cross_counts(series1: pd.Series, series2: pd.Series) -> int:
    """
    Count number of crossovers between two series
    
    Args:
        series1: First series
        series2: Second series
        
    Returns:
        Number of crossovers
    """
    diff = series1 - series2
    return int((diff * diff.shift() < 0).sum())

# Made with Bob
