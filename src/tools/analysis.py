"""
Investment analysis tools
"""
import pandas as pd
from typing import Dict, Any, List
import logging

from ..utils.calculations import (
    compute_rsi, compute_macd, max_drawdown, proximity_52w
)
from ..utils.helpers import (
    get_close_series, last_n_months, format_percentage,
    get_signal_emoji, dict_to_markdown_table
)
from ..config import config

logger = logging.getLogger(__name__)


def generate_investment_summary(df: pd.DataFrame, ticker: str) -> Dict[str, Any]:
    """Generate comprehensive investment analysis summary"""
    try:
        close = get_close_series(df)
        
        # Calculate indicators
        rsi = compute_rsi(close)
        macd_line, signal_line, hist = compute_macd(close)
        ema50 = close.ewm(span=50, adjust=False).mean()
        ema200 = close.ewm(span=200, adjust=False).mean()
        
        # Get latest values
        current_price = close.iloc[-1]
        rsi_current = rsi.iloc[-1]
        macd_current = macd_line.iloc[-1]
        signal_current = signal_line.iloc[-1]
        
        # Calculate metrics
        months = config.ANALYSIS_MONTHS
        end = close.index.max()
        start = last_n_months(end, months)
        period_close = close[close.index >= start]
        
        price_change = ((current_price - period_close.iloc[0]) / period_close.iloc[0] * 100)
        drawdown = max_drawdown(period_close)
        dist_high, dist_low = proximity_52w(close)
        
        # Generate signals
        signals = []
        if rsi_current < 30:
            signals.append(f"{get_signal_emoji('buy')} RSI oversold ({rsi_current:.1f})")
        elif rsi_current > 70:
            signals.append(f"{get_signal_emoji('sell')} RSI overbought ({rsi_current:.1f})")
        
        if macd_current > signal_current:
            signals.append(f"{get_signal_emoji('buy')} MACD bullish crossover")
        else:
            signals.append(f"{get_signal_emoji('sell')} MACD bearish")
        
        if current_price > ema50.iloc[-1] and current_price > ema200.iloc[-1]:
            signals.append(f"{get_signal_emoji('buy')} Price above EMA50 & EMA200")
        
        # Overall recommendation
        buy_signals = sum(1 for s in signals if '🟢' in s)
        sell_signals = sum(1 for s in signals if '🔴' in s)
        
        if buy_signals > sell_signals:
            recommendation = "BUY"
            rec_emoji = "🟢"
        elif sell_signals > buy_signals:
            recommendation = "SELL"
            rec_emoji = "🔴"
        else:
            recommendation = "HOLD"
            rec_emoji = "🟡"
        
        summary = {
            'success': True,
            'ticker': ticker,
            'analysis_period': f'{months} months',
            'current_price': f'${current_price:.2f}',
            'price_change': format_percentage(price_change),
            'max_drawdown': format_percentage(drawdown),
            'distance_from_52w_high': format_percentage(dist_high),
            'distance_from_52w_low': format_percentage(dist_low),
            'rsi': f'{rsi_current:.1f}',
            'macd': f'{macd_current:.2f}',
            'signals': signals,
            'recommendation': f'{rec_emoji} {recommendation}',
            'confidence': 'High' if abs(buy_signals - sell_signals) >= 2 else 'Medium'
        }
        
        return summary
        
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        return {'success': False, 'error': str(e)}


def screen_tickers(tickers: List[str], criteria: Dict[str, Any]) -> Dict[str, Any]:
    """Screen multiple tickers based on criteria"""
    try:
        from .data_extraction import fetch_ticker_data
        
        results = []
        for ticker in tickers:
            data = fetch_ticker_data(ticker)
            if not data.get('success'):
                continue
            
            df = data['dataframe']
            close = get_close_series(df)
            rsi = compute_rsi(close)
            
            # Apply criteria
            matches = True
            if 'rsi_below' in criteria and rsi.iloc[-1] >= criteria['rsi_below']:
                matches = False
            if 'rsi_above' in criteria and rsi.iloc[-1] <= criteria['rsi_above']:
                matches = False
            
            if matches:
                results.append({
                    'ticker': ticker,
                    'price': close.iloc[-1],
                    'rsi': rsi.iloc[-1]
                })
        
        return {
            'success': True,
            'matches': results,
            'count': len(results)
        }
    except Exception as e:
        logger.error(f"Error screening tickers: {str(e)}")
        return {'success': False, 'error': str(e)}

# Made with Bob
