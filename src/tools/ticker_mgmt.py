"""
Ticker management tools for CSV watchlist
"""
import csv
from pathlib import Path
from typing import List, Dict, Any
import logging

from ..config import config
from ..utils.helpers import validate_ticker, clean_ticker_symbol

logger = logging.getLogger(__name__)


def list_tickers() -> Dict[str, Any]:
    """Get all tickers from CSV watchlist"""
    try:
        ticker_path = config.get_ticker_csv_path()
        
        if not ticker_path.exists():
            return {
                'success': True,
                'tickers': [],
                'count': 0
            }
        
        with open(ticker_path, 'r') as f:
            reader = csv.DictReader(f)
            tickers = [row['ticker'] for row in reader if row.get('ticker')]
        
        return {
            'success': True,
            'tickers': tickers,
            'count': len(tickers)
        }
    except Exception as e:
        logger.error(f"Error listing tickers: {str(e)}")
        return {'success': False, 'error': str(e)}


def add_ticker(ticker: str) -> Dict[str, Any]:
    """Add ticker to watchlist"""
    try:
        ticker = clean_ticker_symbol(ticker)
        
        if not validate_ticker(ticker):
            return {
                'success': False,
                'error': f'Invalid ticker: {ticker}'
            }
        
        # Check if already exists
        current = list_tickers()
        if ticker in current.get('tickers', []):
            return {
                'success': False,
                'error': f'Ticker {ticker} already in watchlist'
            }
        
        # Add to CSV
        ticker_path = config.get_ticker_csv_path()
        with open(ticker_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([ticker])
        
        return {
            'success': True,
            'ticker': ticker,
            'message': f'Added {ticker} to watchlist'
        }
    except Exception as e:
        logger.error(f"Error adding ticker: {str(e)}")
        return {'success': False, 'error': str(e)}


def remove_ticker(ticker: str) -> Dict[str, Any]:
    """Remove ticker from watchlist"""
    try:
        ticker = clean_ticker_symbol(ticker)
        ticker_path = config.get_ticker_csv_path()
        
        # Read all tickers
        with open(ticker_path, 'r') as f:
            reader = csv.DictReader(f)
            tickers = [row for row in reader if row.get('ticker') != ticker]
        
        # Write back
        with open(ticker_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['ticker'])
            writer.writeheader()
            writer.writerows(tickers)
        
        return {
            'success': True,
            'ticker': ticker,
            'message': f'Removed {ticker} from watchlist'
        }
    except Exception as e:
        logger.error(f"Error removing ticker: {str(e)}")
        return {'success': False, 'error': str(e)}

# Made with Bob
