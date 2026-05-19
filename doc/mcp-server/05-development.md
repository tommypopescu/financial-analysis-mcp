# MCP Server Development Guide

Guide for developers who want to modify or extend the Financial Analysis MCP Server.

## Development Setup

### Prerequisites
- Python 3.11+
- Git
- Docker (optional, for testing)
- Code editor (VS Code recommended)

### Local Development Environment

#### 1. Clone Repository
```bash
git clone https://github.com/TommyPopescu/financial-analysis-mcp.git
cd financial-analysis-mcp
```

#### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

#### 4. Run Server Locally
```bash
python src/server_http.py
```

Server will start on http://localhost:8000

---

## Project Structure

```
financial-analysis-mcp/
├── src/
│   ├── server_http.py          # FastAPI HTTP server
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── data_extraction.py  # Data fetching tools
│   │   ├── analysis.py         # Analysis tools
│   │   └── ticker_mgmt.py      # Ticker management
│   └── utils/
│       └── calculations.py     # Technical indicators
├── data/
│   └── tickers.csv            # Watchlist
├── tests/                     # Unit tests (future)
├── Dockerfile                 # Docker image
├── docker-compose.yml         # Docker Compose config
├── requirements.txt           # Python dependencies
└── README.md                  # Project README
```

---

## Adding a New Tool

### Step 1: Define Tool Function

Create function in appropriate file (`src/tools/`):

```python
# src/tools/analysis.py

def calculate_fibonacci_levels(ticker: str, period: str = "1y") -> dict:
    """
    Calculate Fibonacci retracement levels for a ticker.
    
    Args:
        ticker: Stock ticker symbol
        period: Data period (default: 1y)
        
    Returns:
        dict: Fibonacci levels and analysis
    """
    try:
        # Fetch data
        import yfinance as yf
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        
        if hist.empty:
            return {
                'success': False,
                'error': f'No data available for {ticker}'
            }
        
        # Calculate levels
        high = hist['High'].max()
        low = hist['Low'].min()
        diff = high - low
        
        levels = {
            '0.0': low,
            '23.6': low + (diff * 0.236),
            '38.2': low + (diff * 0.382),
            '50.0': low + (diff * 0.500),
            '61.8': low + (diff * 0.618),
            '78.6': low + (diff * 0.786),
            '100.0': high
        }
        
        current_price = hist['Close'].iloc[-1]
        
        return {
            'success': True,
            'ticker': ticker,
            'period': period,
            'high': float(high),
            'low': float(low),
            'current_price': float(current_price),
            'levels': {k: float(v) for k, v in levels.items()},
            'analysis': _analyze_fib_position(current_price, levels)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def _analyze_fib_position(price: float, levels: dict) -> str:
    """Analyze price position relative to Fibonacci levels."""
    # Implementation...
    pass
```

### Step 2: Register Tool in Server

Add to `src/server_http.py`:

```python
# In TOOLS list
TOOLS = [
    # ... existing tools ...
    {
        "name": "calculate_fibonacci_levels",
        "description": "Calculate Fibonacci retracement levels for technical analysis",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Stock ticker symbol"
                },
                "period": {
                    "type": "string",
                    "description": "Data period (1mo, 3mo, 6mo, 1y, 2y, 5y)",
                    "default": "1y"
                }
            },
            "required": ["ticker"]
        }
    }
]

# In call_tool function
@app.post("/tools/call")
async def call_tool(request: ToolCallRequest):
    tool_name = request.name
    args = request.arguments
    
    # ... existing tool handlers ...
    
    elif tool_name == "calculate_fibonacci_levels":
        from tools.analysis import calculate_fibonacci_levels
        result = calculate_fibonacci_levels(
            ticker=args.get("ticker"),
            period=args.get("period", "1y")
        )
        return {"success": True, "result": result}
```

### Step 3: Test Tool

```python
# test_fibonacci.py
import requests

response = requests.post(
    "http://localhost:8000/tools/call",
    json={
        "name": "calculate_fibonacci_levels",
        "arguments": {
            "ticker": "AAPL",
            "period": "1y"
        }
    }
)

print(response.json())
```

### Step 4: Update Documentation

Add to `doc/mcp-server/02-api-reference.md`:

```markdown
### 8. calculate_fibonacci_levels

Calculate Fibonacci retracement levels for technical analysis.

**Input Schema**:
...

**Example Request**:
...

**Example Response**:
...
```

---

## Adding a New Technical Indicator

### Step 1: Implement Calculation

Add to `src/utils/calculations.py`:

```python
def calculate_ichimoku(df: pd.DataFrame) -> dict:
    """
    Calculate Ichimoku Cloud indicator.
    
    Args:
        df: DataFrame with OHLC data
        
    Returns:
        dict: Ichimoku components and signals
    """
    # Tenkan-sen (Conversion Line): 9-period
    period9_high = df['High'].rolling(window=9).max()
    period9_low = df['Low'].rolling(window=9).min()
    tenkan_sen = (period9_high + period9_low) / 2
    
    # Kijun-sen (Base Line): 26-period
    period26_high = df['High'].rolling(window=26).max()
    period26_low = df['Low'].rolling(window=26).min()
    kijun_sen = (period26_high + period26_low) / 2
    
    # Senkou Span A (Leading Span A): (Tenkan + Kijun) / 2, shifted 26 periods
    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)
    
    # Senkou Span B (Leading Span B): 52-period, shifted 26 periods
    period52_high = df['High'].rolling(window=52).max()
    period52_low = df['Low'].rolling(window=52).min()
    senkou_span_b = ((period52_high + period52_low) / 2).shift(26)
    
    # Chikou Span (Lagging Span): Close shifted -26 periods
    chikou_span = df['Close'].shift(-26)
    
    # Current values
    current_price = df['Close'].iloc[-1]
    current_tenkan = tenkan_sen.iloc[-1]
    current_kijun = kijun_sen.iloc[-1]
    current_span_a = senkou_span_a.iloc[-1]
    current_span_b = senkou_span_b.iloc[-1]
    
    # Determine signal
    signal = "neutral"
    if current_price > current_span_a and current_price > current_span_b:
        if current_tenkan > current_kijun:
            signal = "strong_bullish"
        else:
            signal = "bullish"
    elif current_price < current_span_a and current_price < current_span_b:
        if current_tenkan < current_kijun:
            signal = "strong_bearish"
        else:
            signal = "bearish"
    
    return {
        'tenkan_sen': float(current_tenkan),
        'kijun_sen': float(current_kijun),
        'senkou_span_a': float(current_span_a),
        'senkou_span_b': float(current_span_b),
        'signal': signal,
        'interpretation': _interpret_ichimoku(signal, current_price, current_span_a, current_span_b)
    }

def _interpret_ichimoku(signal: str, price: float, span_a: float, span_b: float) -> str:
    """Generate interpretation text for Ichimoku signal."""
    # Implementation...
    pass
```

### Step 2: Add to calculate_all_indicators

Update `src/tools/analysis.py`:

```python
def calculate_all_indicators(ticker: str, period: str = "6mo") -> dict:
    # ... existing code ...
    
    # Add Ichimoku
    ichimoku = calculate_ichimoku(df)
    indicators['ichimoku'] = ichimoku
    
    # Update summary
    if ichimoku['signal'] in ['strong_bullish', 'bullish']:
        summary['bullish_signals'] += 1
    elif ichimoku['signal'] in ['strong_bearish', 'bearish']:
        summary['bearish_signals'] += 1
    else:
        summary['neutral_signals'] += 1
    
    return result
```

---

## Modifying Existing Tools

### Example: Change RSI Period

**Current**: RSI uses 14-period
**Goal**: Make RSI period configurable

#### Step 1: Update Function Signature

```python
# src/utils/calculations.py

def calculate_rsi(df: pd.DataFrame, period: int = 14) -> dict:
    """
    Calculate RSI with configurable period.
    
    Args:
        df: DataFrame with Close prices
        period: RSI period (default: 14)
    """
    # ... implementation with period parameter ...
```

#### Step 2: Update Tool Interface

```python
# src/tools/analysis.py

def calculate_all_indicators(ticker: str, period: str = "6mo", rsi_period: int = 14) -> dict:
    # ...
    rsi = calculate_rsi(df, period=rsi_period)
    # ...
```

#### Step 3: Update API Schema

```python
# src/server_http.py

{
    "name": "calculate_all_indicators",
    "inputSchema": {
        "properties": {
            "ticker": {...},
            "period": {...},
            "rsi_period": {
                "type": "integer",
                "description": "RSI calculation period",
                "default": 14,
                "minimum": 2,
                "maximum": 50
            }
        }
    }
}
```

---

## Testing

### Manual Testing

```python
# test_manual.py
import requests

def test_tool(tool_name, arguments):
    response = requests.post(
        "http://localhost:8000/tools/call",
        json={
            "name": tool_name,
            "arguments": arguments
        }
    )
    print(f"\n=== {tool_name} ===")
    print(response.json())

# Test cases
test_tool("get_current_price", {"ticker": "AAPL"})
test_tool("calculate_all_indicators", {"ticker": "TLV.RO", "period": "6mo"})
test_tool("generate_investment_summary", {"ticker": "MSFT"})
```

### Unit Tests (Future)

```python
# tests/test_calculations.py
import pytest
import pandas as pd
from src.utils.calculations import calculate_rsi, calculate_macd

def test_rsi_calculation():
    # Create test data
    data = {
        'Close': [100, 102, 101, 103, 105, 104, 106, 108, 107, 109,
                  111, 110, 112, 114, 113, 115, 117, 116, 118, 120]
    }
    df = pd.DataFrame(data)
    
    # Calculate RSI
    result = calculate_rsi(df, period=14)
    
    # Assertions
    assert 'value' in result
    assert 0 <= result['value'] <= 100
    assert result['signal'] in ['overbought', 'oversold', 'neutral']

def test_macd_calculation():
    # Implementation...
    pass
```

---

## Docker Development

### Build Image Locally

```bash
# Build
docker build -t financial-analysis-mcp:dev .

# Run
docker run -p 8000:8000 financial-analysis-mcp:dev

# Test
curl http://localhost:8000/tools/list
```

### Debug Container

```bash
# Run with shell
docker run -it --entrypoint /bin/bash financial-analysis-mcp:dev

# Inside container
python src/server_http.py
```

### Multi-stage Build Optimization

```dockerfile
# Dockerfile
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/
COPY data/ ./data/

ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000

CMD ["python", "src/server_http.py"]
```

---

## CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD

on:
  push:
    branches: [ "main", "master" ]
  pull_request:
    branches: [ "main", "master" ]

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
          pip install -r requirements.txt
          pip install pytest
      
      - name: Run tests
        run: pytest tests/
  
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t financial-analysis-mcp:${{ github.sha }} .
      
      - name: Push to registry
        run: |
          echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin
          docker tag financial-analysis-mcp:${{ github.sha }} ghcr.io/${{ github.repository }}:latest
          docker push ghcr.io/${{ github.repository }}:latest
```

---

## Code Style and Best Practices

### Python Style Guide

Follow PEP 8:
```python
# Good
def calculate_indicator(df: pd.DataFrame, period: int = 14) -> dict:
    """Calculate technical indicator."""
    result = {}
    return result

# Bad
def CalculateIndicator(df,period=14):
    result={}
    return result
```

### Type Hints

Always use type hints:
```python
from typing import Dict, List, Optional

def fetch_data(ticker: str, period: str = "1mo") -> Dict[str, any]:
    """Fetch ticker data."""
    pass

def process_tickers(tickers: List[str]) -> Optional[Dict]:
    """Process multiple tickers."""
    pass
```

### Error Handling

Always return structured errors:
```python
def my_tool(ticker: str) -> dict:
    try:
        # Tool logic
        return {
            'success': True,
            'result': {...}
        }
    except ValueError as e:
        return {
            'success': False,
            'error': f'Invalid input: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }
```

### Documentation

Use docstrings:
```python
def calculate_indicator(df: pd.DataFrame, period: int = 14) -> dict:
    """
    Calculate technical indicator.
    
    Args:
        df: DataFrame with OHLC data
        period: Calculation period (default: 14)
        
    Returns:
        dict: Indicator values and signals
        
    Raises:
        ValueError: If period is invalid
        
    Example:
        >>> df = fetch_data("AAPL")
        >>> result = calculate_indicator(df, period=20)
        >>> print(result['value'])
    """
    pass
```

---

## Performance Optimization

### Caching Results

```python
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=100)
def fetch_ticker_data_cached(ticker: str, period: str, cache_key: str) -> dict:
    """Cached version of fetch_ticker_data."""
    return fetch_ticker_data(ticker, period)

def get_cache_key() -> str:
    """Generate cache key based on current time (5-minute buckets)."""
    now = datetime.now()
    bucket = now.replace(minute=now.minute // 5 * 5, second=0, microsecond=0)
    return bucket.isoformat()

# Usage
result = fetch_ticker_data_cached("AAPL", "1mo", get_cache_key())
```

### Async Operations

```python
import asyncio
import aiohttp

async def fetch_multiple_tickers(tickers: List[str]) -> List[dict]:
    """Fetch data for multiple tickers concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_ticker_async(session, ticker) for ticker in tickers]
        results = await asyncio.gather(*tasks)
    return results
```

---

## Debugging

### Enable Debug Logging

```python
# src/server_http.py
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@app.post("/tools/call")
async def call_tool(request: ToolCallRequest):
    logger.debug(f"Tool call: {request.name} with args: {request.arguments}")
    # ...
```

### VS Code Debug Configuration

```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "src.server_http:app",
                "--reload",
                "--host", "0.0.0.0",
                "--port", "8000"
            ],
            "jinja": true
        }
    ]
}
```

---

## Contributing

### Pull Request Process

1. Fork repository
2. Create feature branch
3. Make changes
4. Add tests
5. Update documentation
6. Submit PR

### Commit Message Format

```
type(scope): subject

body

footer
```

Example:
```
feat(tools): add Fibonacci retracement calculator

- Implement calculate_fibonacci_levels function
- Add tool registration in server
- Update API documentation

Closes #123
```

---

## Related Documentation

- [Architecture](01-architecture.md) - System design
- [API Reference](02-api-reference.md) - Tool documentation
- [Deployment](03-deployment.md) - Deployment guide
- [Troubleshooting](04-troubleshooting.md) - Common issues