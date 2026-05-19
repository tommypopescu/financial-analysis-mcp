# Financial Analysis MCP Server - Complete Implementation Guide

This document contains all the remaining code files needed to complete the MCP server implementation.

## 📁 File Structure

```
financial-analysis-mcp/
├── src/
│   ├── server.py              # Main MCP server (see below)
│   ├── config.py              # ✅ Created
│   ├── tools/
│   │   ├── __init__.py        # See below
│   │   ├── data_extraction.py # ✅ Created
│   │   ├── indicators.py      # ✅ Created
│   │   ├── analysis.py        # See below
│   │   └── ticker_mgmt.py     # See below
│   └── utils/
│       ├── __init__.py        # ✅ Created
│       ├── calculations.py    # ✅ Created
│       └── helpers.py         # ✅ Created
├── data/
│   └── tickers.csv            # Auto-created
├── tests/                     # See below
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # See below
├── Dockerfile                 # See below
├── docker-compose.yml         # See below
├── .env.example               # See below
├── .gitignore                 # See below
├── requirements.txt           # ✅ Created
└── README.md                  # ✅ Created
```

## 🔧 Remaining Implementation Files

### 1. src/tools/ticker_mgmt.py

```python
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
```

### 2. src/tools/analysis.py

```python
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
```

### 3. src/tools/__init__.py

```python
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
    'remove_ticker'
]
```

### 4. src/server.py (Main MCP Server)

```python
"""
Financial Analysis MCP Server
Main server implementation using Model Context Protocol
"""
import asyncio
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .tools import (
    fetch_ticker_data, get_current_price, get_ticker_info,
    calculate_rsi, calculate_macd, calculate_all_indicators,
    generate_investment_summary, screen_tickers,
    list_tickers, add_ticker, remove_ticker
)
from .config import config

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create MCP server
app = Server("financial-analysis-mcp")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools"""
    return [
        Tool(
            name="fetch_ticker_data",
            description="Fetch historical price and volume data for a stock ticker",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"},
                    "period": {"type": "string", "description": "Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)"},
                    "interval": {"type": "string", "description": "Data interval (1m, 5m, 1h, 1d, 1wk, 1mo)"}
                },
                "required": ["ticker"]
            }
        ),
        Tool(
            name="get_current_price",
            description="Get current/latest price for a ticker",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"}
                },
                "required": ["ticker"]
            }
        ),
        Tool(
            name="calculate_all_indicators",
            description="Calculate all technical indicators (RSI, MACD, ADX, etc.) for a ticker",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"},
                    "period": {"type": "string", "description": "Data period"}
                },
                "required": ["ticker"]
            }
        ),
        Tool(
            name="generate_investment_summary",
            description="Generate comprehensive investment analysis with buy/sell/hold recommendation",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"}
                },
                "required": ["ticker"]
            }
        ),
        Tool(
            name="list_tickers",
            description="List all tickers in watchlist",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="add_ticker",
            description="Add ticker to watchlist",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Ticker to add"}
                },
                "required": ["ticker"]
            }
        ),
        Tool(
            name="screen_tickers",
            description="Screen watchlist for investment opportunities",
            inputSchema={
                "type": "object",
                "properties": {
                    "criteria": {"type": "object", "description": "Screening criteria (e.g., rsi_below: 30)"}
                }
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""
    try:
        logger.info(f"Tool called: {name} with args: {arguments}")
        
        if name == "fetch_ticker_data":
            result = fetch_ticker_data(**arguments)
        elif name == "get_current_price":
            result = get_current_price(**arguments)
        elif name == "calculate_all_indicators":
            ticker = arguments['ticker']
            data = fetch_ticker_data(ticker, arguments.get('period', '1y'))
            if data['success']:
                result = calculate_all_indicators(data['dataframe'])
            else:
                result = data
        elif name == "generate_investment_summary":
            ticker = arguments['ticker']
            data = fetch_ticker_data(ticker, '1y')
            if data['success']:
                result = generate_investment_summary(data['dataframe'], ticker)
            else:
                result = data
        elif name == "list_tickers":
            result = list_tickers()
        elif name == "add_ticker":
            result = add_ticker(**arguments)
        elif name == "screen_tickers":
            tickers_data = list_tickers()
            if tickers_data['success']:
                result = screen_tickers(tickers_data['tickers'], arguments.get('criteria', {}))
            else:
                result = tickers_data
        else:
            result = {"success": False, "error": f"Unknown tool: {name}"}
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error in tool {name}: {str(e)}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Main server entry point"""
    logger.info("Starting Financial Analysis MCP Server...")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
```

### 5. Dockerfile

```dockerfile
# Multi-stage build for optimized image
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY src/ ./src/
COPY data/ ./data/

# Make sure scripts are in PATH
ENV PATH=/root/.local/bin:$PATH

# Create data directory
RUN mkdir -p /app/data

# Expose port
EXPOSE 3000

# Run server
CMD ["python", "-m", "src.server"]
```

### 6. docker-compose.yml

```yaml
version: '3.8'

services:
  financial-mcp:
    build: .
    container_name: financial-analysis-mcp
    ports:
      - "3000:3000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - MCP_SERVER_PORT=3000
      - LOG_LEVEL=INFO
      - CACHE_ENABLED=true
      - CACHE_TTL=300
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import socket; s=socket.socket(); s.connect(('localhost', 3000)); s.close()"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 7. .env.example

```env
# Server Configuration
MCP_SERVER_PORT=3000
LOG_LEVEL=INFO

# Data Configuration
TICKER_CSV_PATH=/app/data/tickers.csv
CACHE_ENABLED=true
CACHE_TTL=300

# Market Data Defaults
DEFAULT_PERIOD=1y
DEFAULT_INTERVAL=1d

# Technical Indicators
RSI_WINDOW=14
MACD_FAST=12
MACD_SLOW=26
MACD_SIGNAL=9
ADX_PERIOD=14

# Analysis
ANALYSIS_MONTHS=6
```

### 8. .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
*.log
logs/

# Data
data/*.csv
!data/.gitkeep

# Environment
.env

# Docker
.dockerignore

# OS
.DS_Store
Thumbs.db
```

### 9. .github/workflows/ci-cd.yml

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: |
          pytest tests/ --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/financial-mcp:latest
            ${{ secrets.DOCKER_USERNAME }}/financial-mcp:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Deploy to OMV Server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.OMV_HOST }}
          username: ${{ secrets.OMV_USER }}
          key: ${{ secrets.OMV_SSH_KEY }}
          script: |
            cd /path/to/deployment
            docker-compose pull
            docker-compose up -d
            docker-compose logs -f --tail=50
```

### 10. Bob MCP Configuration (.bob/mcp.json addition)

```json
{
  "mcpServers": {
    "financial-analysis": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v",
        "${workspaceFolder}/fin/financial-analysis-mcp/data:/app/data",
        "financial-mcp:latest"
      ],
      "env": {
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## 🚀 Quick Start Commands

```bash
# Build Docker image
docker build -t financial-mcp:latest .

# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Run tests
pytest tests/

# Install locally for development
pip install -r requirements.txt
python -m src.server
```

## 📝 Next Steps

1. Create remaining files from this guide
2. Test locally with Docker
3. Configure GitHub secrets for CI/CD
4. Push to GitHub repository
5. Deploy to OMV server
6. Configure Bob to use the MCP server

## 🔗 Integration with Bob

Once deployed, Bob can use commands like:
- "Analyze AAPL stock"
- "Show me my watchlist"
- "Screen for oversold stocks"
- "Compare MSFT and GOOGL"