"""
MCP Tools for Financial Analysis
"""
from .data_extraction import (
    fetch_ticker_data,
    get_current_price,
    get_ticker_info,
    get_multiple_tickers
)

from .indicators import (
    calculate_rsi,
    calculate_macd,
    calculate_all_indicators
)

from .analysis import (
    generate_investment_summary,
    screen_tickers
)

from .ticker_mgmt import (
    list_tickers,
    add_ticker,
    remove_ticker
)

from .portfolio import (
    list_portfolios,
    get_portfolio,
    add_holding,
    remove_holding,
    set_target_allocation,
    analyze_portfolio_allocation,
    get_portfolio_performance,
    get_investment_recommendation
)

__all__ = [
    # Data extraction
    'fetch_ticker_data',
    'get_current_price',
    'get_ticker_info',
    'get_multiple_tickers',
    # Indicators
    'calculate_rsi',
    'calculate_macd',
    'calculate_all_indicators',
    # Analysis
    'generate_investment_summary',
    'screen_tickers',
    # Ticker management
    'list_tickers',
    'add_ticker',
    'remove_ticker',
    # Portfolio management
    'list_portfolios',
    'get_portfolio',
    'add_holding',
    'remove_holding',
    'set_target_allocation',
    'analyze_portfolio_allocation',
    'get_portfolio_performance',
    'get_investment_recommendation'
]

# Made with Bob
