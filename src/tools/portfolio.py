"""
Portfolio Management Tools
Manages family portfolios, holdings, weights, and investment recommendations
Uses CSV files for easy manual editing and Excel compatibility
"""

import csv
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from .data_extraction import fetch_ticker_data, get_current_price
# Note: analysis imports are done locally where needed to avoid circular imports

# Portfolio data directory
PORTFOLIO_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')

# CSV file paths
PORTFOLIO1_FILE = os.path.join(PORTFOLIO_DIR, 'portfolio1_holdings.csv')
PORTFOLIO2_FILE = os.path.join(PORTFOLIO_DIR, 'portfolio2_holdings.csv')
PORTFOLIO1_TARGETS = os.path.join(PORTFOLIO_DIR, 'portfolio1_targets.csv')
PORTFOLIO2_TARGETS = os.path.join(PORTFOLIO_DIR, 'portfolio2_targets.csv')
PORTFOLIO_INFO = os.path.join(PORTFOLIO_DIR, 'portfolio_info.csv')

def _ensure_portfolio_files():
    """Ensure portfolio directory and files exist"""
    os.makedirs(PORTFOLIO_DIR, exist_ok=True)
    
    # Create portfolio info file if not exists
    if not os.path.exists(PORTFOLIO_INFO):
        with open(PORTFOLIO_INFO, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['portfolio_id', 'name', 'description', 'currency', 'last_updated'])
            writer.writerow(['portfolio1', 'Portfolio 1', 'Family Portfolio 1', 'EUR', datetime.now().isoformat()])
            writer.writerow(['portfolio2', 'Portfolio 2', 'Family Portfolio 2', 'EUR', datetime.now().isoformat()])
    
    # Create holdings files if not exist
    for holdings_file in [PORTFOLIO1_FILE, PORTFOLIO2_FILE]:
        if not os.path.exists(holdings_file):
            with open(holdings_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ticker', 'shares', 'avg_price', 'purchase_date', 'notes'])
    
    # Create target allocation files if not exist
    for targets_file in [PORTFOLIO1_TARGETS, PORTFOLIO2_TARGETS]:
        if not os.path.exists(targets_file):
            with open(targets_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ticker', 'target_weight_pct', 'notes'])

def _get_portfolio_file(portfolio_id: str) -> Tuple[str, str]:
    """Get holdings and targets file paths for portfolio"""
    if portfolio_id == 'portfolio1':
        return PORTFOLIO1_FILE, PORTFOLIO1_TARGETS
    elif portfolio_id == 'portfolio2':
        return PORTFOLIO2_FILE, PORTFOLIO2_TARGETS
    else:
        raise ValueError(f"Invalid portfolio_id: {portfolio_id}. Use 'portfolio1' or 'portfolio2'")

def _read_holdings(holdings_file: str) -> Dict:
    """Read holdings from CSV file"""
    holdings = {}
    
    if os.path.exists(holdings_file):
        with open(holdings_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ticker = row['ticker'].strip().upper()
                holdings[ticker] = {
                    'shares': float(row['shares']),
                    'avg_price': float(row['avg_price']),
                    'purchase_date': row['purchase_date'],
                    'notes': row.get('notes', '')
                }
    
    return holdings

def _write_holdings(holdings_file: str, holdings: Dict):
    """Write holdings to CSV file"""
    with open(holdings_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ticker', 'shares', 'avg_price', 'purchase_date', 'notes'])
        
        for ticker, data in sorted(holdings.items()):
            writer.writerow([
                ticker,
                data['shares'],
                data['avg_price'],
                data['purchase_date'],
                data.get('notes', '')
            ])

def _read_targets(targets_file: str) -> Dict:
    """Read target allocations from CSV file"""
    targets = {}
    
    if os.path.exists(targets_file):
        with open(targets_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ticker = row['ticker'].strip().upper()
                targets[ticker] = {
                    'target_weight_pct': float(row['target_weight_pct']),
                    'notes': row.get('notes', '')
                }
    
    return targets

def _write_targets(targets_file: str, targets: Dict):
    """Write target allocations to CSV file"""
    with open(targets_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ticker', 'target_weight_pct', 'notes'])
        
        for ticker, data in sorted(targets.items()):
            writer.writerow([
                ticker,
                data['target_weight_pct'],
                data.get('notes', '')
            ])

def list_portfolios() -> Dict:
    """
    List all portfolios with summary information
    
    Returns:
        Dict with portfolio summaries
    """
    _ensure_portfolio_files()
    
    summary = {}
    
    for portfolio_id in ['portfolio1', 'portfolio2']:
        holdings_file, targets_file = _get_portfolio_file(portfolio_id)
        holdings = _read_holdings(holdings_file)
        
        # Calculate current values
        total_value = 0.0
        
        for ticker, holding in holdings.items():
            shares = holding['shares']
            if shares > 0:
                price_data = get_current_price(ticker)
                if price_data['success']:
                    current_price = price_data['current_price']
                    total_value += shares * current_price
        
        # Read portfolio info
        portfolio_name = f"Portfolio {portfolio_id[-1]}"
        currency = "EUR"
        
        if os.path.exists(PORTFOLIO_INFO):
            with open(PORTFOLIO_INFO, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['portfolio_id'] == portfolio_id:
                        portfolio_name = row['name']
                        currency = row['currency']
                        break
        
        summary[portfolio_id] = {
            'name': portfolio_name,
            'total_value': round(total_value, 2),
            'currency': currency,
            'holdings_count': len(holdings),
            'csv_files': {
                'holdings': os.path.basename(holdings_file),
                'targets': os.path.basename(targets_file)
            }
        }
    
    return {
        'success': True,
        'portfolios': summary,
        'data_directory': PORTFOLIO_DIR
    }

def get_portfolio(portfolio_id: str) -> Dict:
    """
    Get detailed portfolio information
    
    Args:
        portfolio_id: Portfolio identifier (portfolio1 or portfolio2)
        
    Returns:
        Dict with detailed portfolio data
    """
    _ensure_portfolio_files()
    
    try:
        holdings_file, targets_file = _get_portfolio_file(portfolio_id)
    except ValueError as e:
        return {
            'success': False,
            'error': str(e)
        }
    
    holdings = _read_holdings(holdings_file)
    targets = _read_targets(targets_file)
    
    # Calculate current values and weights
    holdings_detail = {}
    total_value = 0.0
    
    for ticker, holding in holdings.items():
        shares = holding['shares']
        avg_price = holding['avg_price']
        
        if shares > 0:
            price_data = get_current_price(ticker)
            if price_data['success']:
                current_price = price_data['current_price']
                current_value = shares * current_price
                total_value += current_value
                
                holdings_detail[ticker] = {
                    'shares': shares,
                    'avg_price': round(avg_price, 2),
                    'current_price': current_price,
                    'current_value': round(current_value, 2),
                    'cost_basis': round(shares * avg_price, 2),
                    'profit_loss': round(current_value - (shares * avg_price), 2),
                    'profit_loss_pct': round(((current_price / avg_price) - 1) * 100, 2) if avg_price > 0 else 0,
                    'purchase_date': holding['purchase_date'],
                    'notes': holding.get('notes', '')
                }
    
    # Calculate actual weights
    for ticker in holdings_detail:
        holdings_detail[ticker]['weight_pct'] = round((holdings_detail[ticker]['current_value'] / total_value) * 100, 2) if total_value > 0 else 0
    
    # Format target allocations
    target_allocation = {ticker: data['target_weight_pct'] for ticker, data in targets.items()}
    
    return {
        'success': True,
        'portfolio_id': portfolio_id,
        'name': f"Portfolio {portfolio_id[-1]}",
        'total_value': round(total_value, 2),
        'currency': 'EUR',
        'holdings': holdings_detail,
        'target_allocation': target_allocation,
        'csv_files': {
            'holdings': holdings_file,
            'targets': targets_file
        }
    }

def add_holding(portfolio_id: str, ticker: str, shares: float, avg_price: float, 
                purchase_date: Optional[str] = None, notes: str = '') -> Dict:
    """
    Add or update a holding in portfolio
    
    Args:
        portfolio_id: Portfolio identifier
        ticker: Stock ticker symbol
        shares: Number of shares
        avg_price: Average purchase price per share
        purchase_date: Purchase date (optional, defaults to today)
        notes: Optional notes about the holding
        
    Returns:
        Dict with operation result
    """
    _ensure_portfolio_files()
    
    try:
        holdings_file, _ = _get_portfolio_file(portfolio_id)
    except ValueError as e:
        return {
            'success': False,
            'error': str(e)
        }
    
    ticker = ticker.strip().upper()
    holdings = _read_holdings(holdings_file)
    
    # If holding exists, update it (average down/up)
    if ticker in holdings:
        existing = holdings[ticker]
        old_shares = existing['shares']
        old_avg_price = existing['avg_price']
        
        # Calculate new average price
        total_cost = (old_shares * old_avg_price) + (shares * avg_price)
        new_shares = old_shares + shares
        new_avg_price = total_cost / new_shares if new_shares > 0 else avg_price
        
        holdings[ticker] = {
            'shares': new_shares,
            'avg_price': new_avg_price,
            'purchase_date': existing['purchase_date'],
            'notes': notes or existing.get('notes', '')
        }
        
        action = 'updated'
    else:
        holdings[ticker] = {
            'shares': shares,
            'avg_price': avg_price,
            'purchase_date': purchase_date or datetime.now().strftime('%Y-%m-%d'),
            'notes': notes
        }
        action = 'added'
    
    _write_holdings(holdings_file, holdings)
    
    return {
        'success': True,
        'action': action,
        'portfolio_id': portfolio_id,
        'ticker': ticker,
        'shares': holdings[ticker]['shares'],
        'avg_price': round(holdings[ticker]['avg_price'], 2),
        'csv_file': holdings_file
    }

def remove_holding(portfolio_id: str, ticker: str, shares: Optional[float] = None) -> Dict:
    """
    Remove or reduce a holding from portfolio
    
    Args:
        portfolio_id: Portfolio identifier
        ticker: Stock ticker symbol
        shares: Number of shares to remove (None = remove all)
        
    Returns:
        Dict with operation result
    """
    _ensure_portfolio_files()
    
    try:
        holdings_file, _ = _get_portfolio_file(portfolio_id)
    except ValueError as e:
        return {
            'success': False,
            'error': str(e)
        }
    
    ticker = ticker.strip().upper()
    holdings = _read_holdings(holdings_file)
    
    if ticker not in holdings:
        return {
            'success': False,
            'error': f'Ticker {ticker} not found in portfolio'
        }
    
    current_shares = holdings[ticker]['shares']
    
    if shares is None or shares >= current_shares:
        # Remove completely
        del holdings[ticker]
        action = 'removed'
        remaining_shares = 0
    else:
        # Reduce shares
        holdings[ticker]['shares'] = current_shares - shares
        action = 'reduced'
        remaining_shares = current_shares - shares
    
    _write_holdings(holdings_file, holdings)
    
    return {
        'success': True,
        'action': action,
        'portfolio_id': portfolio_id,
        'ticker': ticker,
        'remaining_shares': remaining_shares,
        'csv_file': holdings_file
    }

def set_target_allocation(portfolio_id: str, ticker: str, target_weight_pct: float, notes: str = '') -> Dict:
    """
    Set target allocation percentage for a ticker in portfolio
    
    Args:
        portfolio_id: Portfolio identifier
        ticker: Stock ticker symbol
        target_weight_pct: Target weight percentage (0-100)
        notes: Optional notes about the target
        
    Returns:
        Dict with operation result
    """
    _ensure_portfolio_files()
    
    try:
        _, targets_file = _get_portfolio_file(portfolio_id)
    except ValueError as e:
        return {
            'success': False,
            'error': str(e)
        }
    
    ticker = ticker.strip().upper()
    targets = _read_targets(targets_file)
    
    if target_weight_pct < 0 or target_weight_pct > 100:
        return {
            'success': False,
            'error': 'Target weight must be between 0 and 100'
        }
    
    targets[ticker] = {
        'target_weight_pct': target_weight_pct,
        'notes': notes
    }
    
    _write_targets(targets_file, targets)
    
    # Check if total allocation exceeds 100%
    total_allocation = sum(t['target_weight_pct'] for t in targets.values())
    warning = None
    if total_allocation > 100:
        warning = f"⚠️ Total allocation is {round(total_allocation, 1)}% (exceeds 100%)"
    
    return {
        'success': True,
        'portfolio_id': portfolio_id,
        'ticker': ticker,
        'target_weight_pct': target_weight_pct,
        'total_allocation': round(total_allocation, 2),
        'warning': warning,
        'csv_file': targets_file
    }

def analyze_portfolio_allocation(portfolio_id: str) -> Dict:
    """
    Analyze portfolio allocation vs targets and provide rebalancing recommendations
    
    Args:
        portfolio_id: Portfolio identifier
        
    Returns:
        Dict with allocation analysis and recommendations
    """
    portfolio_data = get_portfolio(portfolio_id)
    
    if not portfolio_data['success']:
        return portfolio_data
    
    holdings = portfolio_data['holdings']
    target_allocation = portfolio_data['target_allocation']
    total_value = portfolio_data['total_value']
    
    if not target_allocation:
        return {
            'success': False,
            'error': 'No target allocation set for this portfolio. Use set_target_allocation to add targets.',
            'csv_file': portfolio_data['csv_files']['targets']
        }
    
    # Calculate deviations
    analysis = {}
    rebalancing_needed = []
    
    for ticker, target_pct in target_allocation.items():
        current_pct = holdings.get(ticker, {}).get('weight_pct', 0)
        deviation = current_pct - target_pct
        
        target_value = (target_pct / 100) * total_value
        current_value = holdings.get(ticker, {}).get('current_value', 0)
        value_diff = current_value - target_value
        
        analysis[ticker] = {
            'current_weight': round(current_pct, 2),
            'target_weight': round(target_pct, 2),
            'deviation': round(deviation, 2),
            'current_value': round(current_value, 2),
            'target_value': round(target_value, 2),
            'value_difference': round(value_diff, 2),
            'action': 'HOLD' if abs(deviation) < 2 else ('SELL' if deviation > 0 else 'BUY')
        }
        
        if abs(deviation) >= 2:  # Threshold for rebalancing
            rebalancing_needed.append({
                'ticker': ticker,
                'action': 'SELL' if deviation > 0 else 'BUY',
                'amount': abs(round(value_diff, 2)),
                'deviation': round(deviation, 2)
            })
    
    # Check for holdings not in target allocation
    for ticker in holdings:
        if ticker not in target_allocation:
            analysis[ticker] = {
                'current_weight': holdings[ticker]['weight_pct'],
                'target_weight': 0,
                'deviation': holdings[ticker]['weight_pct'],
                'current_value': holdings[ticker]['current_value'],
                'target_value': 0,
                'value_difference': holdings[ticker]['current_value'],
                'action': 'SELL (not in target allocation)'
            }
            rebalancing_needed.append({
                'ticker': ticker,
                'action': 'SELL',
                'amount': holdings[ticker]['current_value'],
                'deviation': holdings[ticker]['weight_pct']
            })
    
    return {
        'success': True,
        'portfolio_id': portfolio_id,
        'total_value': total_value,
        'currency': portfolio_data['currency'],
        'allocation_analysis': analysis,
        'rebalancing_recommendations': sorted(rebalancing_needed, key=lambda x: abs(x['deviation']), reverse=True),
        'is_balanced': len(rebalancing_needed) == 0
    }

def get_portfolio_performance(portfolio_id: str, period: str = '1y', benchmark_ticker: Optional[str] = None) -> Dict:
    """
    Get portfolio performance and price history based on current holdings.
    
    Args:
        portfolio_id: Portfolio identifier (portfolio1 or portfolio2)
        period: Historical period for portfolio performance
        benchmark_ticker: Optional benchmark ticker for comparison
        
    Returns:
        Dict with portfolio history, return metrics, and optional benchmark comparison
    """
    _ensure_portfolio_files()
    
    try:
        holdings_file, _ = _get_portfolio_file(portfolio_id)
    except ValueError as e:
        return {
            'success': False,
            'error': str(e)
        }
    
    holdings = _read_holdings(holdings_file)
    active_holdings = {
        ticker: holding for ticker, holding in holdings.items()
        if holding.get('shares', 0) > 0
    }
    
    if not active_holdings:
        return {
            'success': False,
            'error': f'Portfolio {portfolio_id} has no active holdings'
        }
    
    portfolio_dates = None
    portfolio_values = None
    holdings_history = {}
    total_cost_basis = 0.0
    
    for ticker, holding in active_holdings.items():
        shares = holding['shares']
        avg_price = holding['avg_price']
        total_cost_basis += shares * avg_price
        
        history = fetch_ticker_data(ticker, period=period, interval='1d')
        if not history.get('success'):
            return {
                'success': False,
                'error': f"Failed to fetch history for {ticker}: {history.get('error', 'Unknown error')}",
                'ticker': ticker
            }
        
        dates = history['data']['dates']
        closes = history['data']['close']
        
        if not dates or not closes:
            return {
                'success': False,
                'error': f'No historical close data available for {ticker}',
                'ticker': ticker
            }
        
        if portfolio_dates is None:
            portfolio_dates = dates
            portfolio_values = [0.0] * len(dates)
        elif dates != portfolio_dates:
            return {
                'success': False,
                'error': f'Historical data alignment mismatch for {ticker}. Try a different period.'
            }
        
        position_values = [round(price * shares, 2) for price in closes]
        holdings_history[ticker] = {
            'shares': shares,
            'avg_price': round(avg_price, 2),
            'cost_basis': round(shares * avg_price, 2),
            'start_price': round(closes[0], 2),
            'end_price': round(closes[-1], 2),
            'start_value': round(position_values[0], 2),
            'end_value': round(position_values[-1], 2),
            'return_pct': round(((closes[-1] / closes[0]) - 1) * 100, 2) if closes[0] else 0,
            'history': position_values
        }
        
        portfolio_values = [
            round(current_total + position_value, 2)
            for current_total, position_value in zip(portfolio_values, position_values)
        ]
    
    start_value = portfolio_values[0]
    end_value = portfolio_values[-1]
    total_return = round(end_value - total_cost_basis, 2)
    total_return_pct = round(((end_value / total_cost_basis) - 1) * 100, 2) if total_cost_basis > 0 else 0
    period_return = round(end_value - start_value, 2)
    period_return_pct = round(((end_value / start_value) - 1) * 100, 2) if start_value > 0 else 0
    
    result = {
        'success': True,
        'portfolio_id': portfolio_id,
        'period': period,
        'currency': 'EUR',
        'holdings_count': len(active_holdings),
        'cost_basis': round(total_cost_basis, 2),
        'start_value': round(start_value, 2),
        'end_value': round(end_value, 2),
        'total_return': total_return,
        'total_return_pct': total_return_pct,
        'period_return': period_return,
        'period_return_pct': period_return_pct,
        'history': {
            'dates': portfolio_dates,
            'portfolio_values': portfolio_values
        },
        'holdings_history': holdings_history
    }
    
    if benchmark_ticker:
        benchmark_data = fetch_ticker_data(benchmark_ticker, period=period, interval='1d')
        if benchmark_data.get('success') and benchmark_data['data']['close']:
            benchmark_closes = benchmark_data['data']['close']
            benchmark_start = benchmark_closes[0]
            benchmark_end = benchmark_closes[-1]
            benchmark_return_pct = round(((benchmark_end / benchmark_start) - 1) * 100, 2) if benchmark_start > 0 else 0
            
            result['benchmark'] = {
                'ticker': benchmark_ticker.strip().upper(),
                'start_price': round(benchmark_start, 2),
                'end_price': round(benchmark_end, 2),
                'return_pct': benchmark_return_pct,
                'relative_performance_pct': round(period_return_pct - benchmark_return_pct, 2),
                'history': {
                    'dates': benchmark_data['data']['dates'],
                    'close': benchmark_closes
                }
            }
        else:
            result['benchmark'] = {
                'ticker': benchmark_ticker.strip().upper(),
                'error': benchmark_data.get('error', 'Failed to fetch benchmark data')
            }
    
    return result

def get_investment_recommendation(portfolio_id: str, ticker: str, investment_amount: float) -> Dict:
    """
    Get personalized investment recommendation for a ticker considering portfolio context
    
    Args:
        portfolio_id: Portfolio identifier
        ticker: Stock ticker to analyze
        investment_amount: Amount to potentially invest
        
    Returns:
        Dict with personalized recommendation
    """
    # Get portfolio data
    portfolio_data = get_portfolio(portfolio_id)
    if not portfolio_data['success']:
        return portfolio_data
    
    # Get technical analysis
    from .analysis import generate_investment_summary
    data = fetch_ticker_data(ticker, '1y')
    
    if not data['success']:
        return data
    
    # Reconstruct DataFrame
    import pandas as pd
    df = pd.DataFrame({
        'Open': data['data']['open'],
        'High': data['data']['high'],
        'Low': data['data']['low'],
        'Close': data['data']['close'],
        'Volume': data['data']['volume']
    }, index=pd.to_datetime(data['data']['dates']))
    
    technical_analysis = generate_investment_summary(df, ticker)
    
    # Portfolio context
    total_value = portfolio_data['total_value']
    current_holding = portfolio_data['holdings'].get(ticker, {})
    current_weight = current_holding.get('weight_pct', 0)
    target_allocation = portfolio_data.get('target_allocation', {})
    target_weight = target_allocation.get(ticker, 0)
    
    # Calculate new weight after investment
    new_total_value = total_value + investment_amount
    new_holding_value = current_holding.get('current_value', 0) + investment_amount
    new_weight = (new_holding_value / new_total_value) * 100 if new_total_value > 0 else 0
    
    # Determine recommendation considering portfolio
    recommendation = technical_analysis['recommendation']
    confidence = technical_analysis['confidence']
    
    # Adjust based on portfolio allocation
    allocation_warning = None
    if target_weight > 0:
        if new_weight > target_weight + 5:
            allocation_warning = f"⚠️ Investment would exceed target allocation ({target_weight}%) by {round(new_weight - target_weight, 1)}%"
            if confidence == "High":
                confidence = "Medium"
        elif new_weight < target_weight - 5:
            allocation_warning = f"✅ Investment aligns with target allocation ({target_weight}%). Still {round(target_weight - new_weight, 1)}% below target."
    
    # Check diversification
    diversification_warning = None
    if new_weight > 15:
        diversification_warning = f"⚠️ Position would be {round(new_weight, 1)}% of portfolio. Consider diversification (max recommended: 10-15%)"
        if confidence == "High":
            confidence = "Medium"
    
    return {
        'success': True,
        'ticker': ticker,
        'portfolio_id': portfolio_id,
        'portfolio_name': portfolio_data['name'],
        'investment_amount': investment_amount,
        'technical_analysis': technical_analysis,
        'portfolio_context': {
            'current_portfolio_value': round(total_value, 2),
            'current_holding_value': round(current_holding.get('current_value', 0), 2),
            'current_weight': round(current_weight, 2),
            'target_weight': round(target_weight, 2),
            'new_portfolio_value': round(new_total_value, 2),
            'new_holding_value': round(new_holding_value, 2),
            'new_weight': round(new_weight, 2),
            'weight_change': round(new_weight - current_weight, 2)
        },
        'recommendation': recommendation,
        'confidence': confidence,
        'allocation_warning': allocation_warning,
        'diversification_warning': diversification_warning,
        'final_verdict': _generate_final_verdict(
            recommendation, 
            confidence, 
            allocation_warning, 
            diversification_warning,
            new_weight,
            target_weight
        )
    }

def _generate_final_verdict(recommendation: str, confidence: str, allocation_warning: Optional[str], 
                           diversification_warning: Optional[str], new_weight: float, target_weight: float) -> str:
    """Generate final investment verdict considering all factors"""
    
    if "🔴" in recommendation:  # SELL or HOLD
        return f"{recommendation} - Technical analysis suggests avoiding this investment"
    
    warnings = []
    if allocation_warning and "⚠️" in allocation_warning:
        warnings.append("allocation concerns")
    if diversification_warning:
        warnings.append("diversification concerns")
    
    if warnings:
        return f"🟡 PROCEED WITH CAUTION - {recommendation} but consider {', '.join(warnings)}"
    
    if target_weight > 0 and new_weight < target_weight:
        return f"🟢 STRONG BUY - {recommendation} and aligns with portfolio targets"
    
    return f"🟢 {recommendation}"

# Made with Bob
