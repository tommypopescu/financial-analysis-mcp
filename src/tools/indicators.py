"""
Technical indicators calculation tools
"""
import pandas as pd
from typing import Dict, Any, Optional
import logging

from ..utils.calculations import (
    compute_rsi, compute_macd, compute_adx, compute_supertrend,
    compute_stochastic, compute_bbands, compute_obv, compute_mfi
)
from ..config import config

logger = logging.getLogger(__name__)


def calculate_rsi(df: pd.DataFrame, window: int = None) -> Dict[str, Any]:
    """Calculate RSI indicator"""
    try:
        window = window or config.RSI_WINDOW
        close = df['Close']
        rsi = compute_rsi(close, window)
        
        return {
            'success': True,
            'indicator': 'RSI',
            'window': window,
            'current_value': float(rsi.iloc[-1]),
            'values': rsi.tolist(),
            'signal': 'oversold' if rsi.iloc[-1] < 30 else 'overbought' if rsi.iloc[-1] > 70 else 'neutral'
        }
    except Exception as e:
        logger.error(f"Error calculating RSI: {str(e)}")
        return {'success': False, 'error': str(e)}


def calculate_macd(df: pd.DataFrame, fast: int = None, slow: int = None, signal: int = None) -> Dict[str, Any]:
    """Calculate MACD indicator"""
    try:
        fast = fast or config.MACD_FAST
        slow = slow or config.MACD_SLOW
        signal_period = signal or config.MACD_SIGNAL
        
        close = df['Close']
        macd_line, signal_line, histogram = compute_macd(close, fast, slow, signal_period)
        
        return {
            'success': True,
            'indicator': 'MACD',
            'parameters': {'fast': fast, 'slow': slow, 'signal': signal_period},
            'macd_line': float(macd_line.iloc[-1]),
            'signal_line': float(signal_line.iloc[-1]),
            'histogram': float(histogram.iloc[-1]),
            'signal': 'bullish' if histogram.iloc[-1] > 0 else 'bearish'
        }
    except Exception as e:
        logger.error(f"Error calculating MACD: {str(e)}")
        return {'success': False, 'error': str(e)}


def calculate_all_indicators(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate all available technical indicators"""
    try:
        close = df['Close']
        
        # Calculate all indicators
        rsi = compute_rsi(close)
        macd_line, signal_line, histogram = compute_macd(close)
        adx, plus_di, minus_di, atr = compute_adx(df)
        supertrend = compute_supertrend(df)
        k, d = compute_stochastic(df)
        bb_mid, bb_upper, bb_lower, bb_width = compute_bbands(close)
        obv = compute_obv(df)
        mfi = compute_mfi(df)
        
        return {
            'success': True,
            'ticker': df.attrs.get('ticker', 'Unknown'),
            'indicators': {
                'rsi': {
                    'value': float(rsi.iloc[-1]),
                    'signal': 'oversold' if rsi.iloc[-1] < 30 else 'overbought' if rsi.iloc[-1] > 70 else 'neutral'
                },
                'macd': {
                    'macd_line': float(macd_line.iloc[-1]),
                    'signal_line': float(signal_line.iloc[-1]),
                    'histogram': float(histogram.iloc[-1]),
                    'signal': 'bullish' if histogram.iloc[-1] > 0 else 'bearish'
                },
                'adx': {
                    'value': float(adx.iloc[-1]),
                    'plus_di': float(plus_di.iloc[-1]),
                    'minus_di': float(minus_di.iloc[-1]),
                    'trend_strength': 'strong' if adx.iloc[-1] > 25 else 'weak'
                },
                'stochastic': {
                    'k': float(k.iloc[-1]),
                    'd': float(d.iloc[-1]),
                    'signal': 'oversold' if k.iloc[-1] < 20 else 'overbought' if k.iloc[-1] > 80 else 'neutral'
                },
                'bollinger_bands': {
                    'upper': float(bb_upper.iloc[-1]),
                    'middle': float(bb_mid.iloc[-1]),
                    'lower': float(bb_lower.iloc[-1]),
                    'width': float(bb_width.iloc[-1])
                },
                'obv': float(obv.iloc[-1]),
                'mfi': {
                    'value': float(mfi.iloc[-1]),
                    'signal': 'oversold' if mfi.iloc[-1] < 20 else 'overbought' if mfi.iloc[-1] > 80 else 'neutral'
                }
            }
        }
    except Exception as e:
        logger.error(f"Error calculating all indicators: {str(e)}")
        return {'success': False, 'error': str(e)}

# Made with Bob
