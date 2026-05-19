# MCP Server API Reference

Complete reference for all tools and resources provided by the Financial Analysis MCP Server.

## Base URL

```
http://192.168.1.7:8000
```

## Endpoints

### List Tools
```http
POST /tools/list
Content-Type: application/json

{}
```

**Response**:
```json
{
  "tools": [
    {
      "name": "fetch_ticker_data",
      "description": "Fetch historical price and volume data for a stock ticker",
      "inputSchema": {...}
    },
    ...
  ]
}
```

### Call Tool
```http
POST /tools/call
Content-Type: application/json

{
  "name": "tool_name",
  "arguments": {...}
}
```

## Tools

### 1. fetch_ticker_data

Fetch historical OHLCV (Open, High, Low, Close, Volume) data for a stock ticker.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "ticker": {
      "type": "string",
      "description": "Stock ticker symbol (e.g., 'AAPL', 'TLV.RO', 'SAP.DE')"
    },
    "period": {
      "type": "string",
      "description": "Data period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max",
      "default": "1mo"
    },
    "interval": {
      "type": "string",
      "description": "Data interval: 1m, 5m, 1h, 1d, 1wk, 1mo",
      "default": "1d"
    }
  },
  "required": ["ticker"]
}
```

**Example Request**:
```json
{
  "name": "fetch_ticker_data",
  "arguments": {
    "ticker": "TLV.RO",
    "period": "1mo",
    "interval": "1d"
  }
}
```

**Example Response**:
```json
{
  "success": true,
  "result": {
    "success": true,
    "ticker": "TLV.RO",
    "period": "1mo",
    "interval": "1d",
    "data_points": 21,
    "start_date": "2026-04-20",
    "end_date": "2026-05-16",
    "data": {
      "dates": ["2026-04-20", "2026-04-21", ...],
      "open": [32.10, 32.25, ...],
      "high": [32.50, 32.60, ...],
      "low": [31.90, 32.00, ...],
      "close": [32.30, 32.45, ...],
      "volume": [1500000, 1600000, ...]
    }
  }
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Ticker TLV not found. Try adding market suffix (e.g., TLV.RO)"
}
```

**Notes**:
- Use market suffixes for non-US stocks: `.RO` (Romania), `.DE` (Germany)
- Maximum data points depend on period and interval
- Volume is in number of shares traded

---

### 2. get_current_price

Get the current/latest price for a stock ticker.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "ticker": {
      "type": "string",
      "description": "Stock ticker symbol"
    }
  },
  "required": ["ticker"]
}
```

**Example Request**:
```json
{
  "name": "get_current_price",
  "arguments": {
    "ticker": "AAPL"
  }
}
```

**Example Response**:
```json
{
  "success": true,
  "result": {
    "success": true,
    "ticker": "AAPL",
    "current_price": 178.45,
    "currency": "USD",
    "timestamp": "2026-05-19T14:30:00Z",
    "market_state": "REGULAR"
  }
}
```

**Market States**:
- `REGULAR` - Market is open
- `PRE` - Pre-market trading
- `POST` - After-hours trading
- `CLOSED` - Market is closed

---

### 3. calculate_all_indicators

Calculate all technical indicators for a stock ticker.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "ticker": {
      "type": "string",
      "description": "Stock ticker symbol"
    },
    "period": {
      "type": "string",
      "description": "Data period for calculations",
      "default": "6mo"
    }
  },
  "required": ["ticker"]
}
```

**Example Request**:
```json
{
  "name": "calculate_all_indicators",
  "arguments": {
    "ticker": "TLV.RO",
    "period": "6mo"
  }
}
```

**Example Response**:
```json
{
  "success": true,
  "result": {
    "success": true,
    "ticker": "TLV.RO",
    "current_price": 32.50,
    "indicators": {
      "ema": {
        "ema_50": 31.85,
        "ema_200": 30.20,
        "trend": "bullish",
        "signal": "Golden Cross forming"
      },
      "rsi": {
        "value": 58.3,
        "signal": "neutral",
        "interpretation": "Neither overbought nor oversold"
      },
      "macd": {
        "macd_line": 0.45,
        "signal_line": 0.32,
        "histogram": 0.13,
        "signal": "bullish",
        "interpretation": "MACD above signal line"
      },
      "adx": {
        "value": 28.5,
        "plus_di": 25.3,
        "minus_di": 18.7,
        "trend_strength": "moderate",
        "direction": "bullish"
      },
      "stochastic": {
        "k": 65.2,
        "d": 62.8,
        "signal": "neutral",
        "interpretation": "Mid-range momentum"
      },
      "bollinger": {
        "upper": 33.50,
        "middle": 32.00,
        "lower": 30.50,
        "position": "above_middle",
        "signal": "bullish"
      },
      "mfi": {
        "value": 62.5,
        "signal": "neutral",
        "interpretation": "Moderate buying pressure"
      }
    },
    "summary": {
      "bullish_signals": 4,
      "bearish_signals": 0,
      "neutral_signals": 3,
      "overall_sentiment": "bullish"
    }
  }
}
```

**Indicator Details**:

#### EMA (Exponential Moving Average)
- **ema_50**: 50-period EMA
- **ema_200**: 200-period EMA
- **trend**: "bullish" (price > EMA50 > EMA200), "bearish", "neutral"
- **signal**: Golden Cross, Death Cross, or trend description

#### RSI (Relative Strength Index)
- **value**: 0-100 scale
- **signal**: "overbought" (>70), "oversold" (<30), "neutral"
- **interpretation**: Text description

#### MACD (Moving Average Convergence Divergence)
- **macd_line**: MACD line value
- **signal_line**: Signal line value
- **histogram**: Difference between MACD and signal
- **signal**: "bullish" (MACD > signal), "bearish", "neutral"

#### ADX (Average Directional Index)
- **value**: 0-100 scale (trend strength)
- **plus_di**: +DI (bullish pressure)
- **minus_di**: -DI (bearish pressure)
- **trend_strength**: "weak" (<20), "moderate" (20-40), "strong" (>40)
- **direction**: "bullish" (+DI > -DI), "bearish"

#### Stochastic Oscillator
- **k**: %K line (fast)
- **d**: %D line (slow)
- **signal**: "overbought" (>80), "oversold" (<20), "neutral"

#### Bollinger Bands
- **upper**: Upper band (middle + 2*std)
- **middle**: Middle band (20-period SMA)
- **lower**: Lower band (middle - 2*std)
- **position**: Price position relative to bands
- **signal**: "bullish", "bearish", "neutral"

#### MFI (Money Flow Index)
- **value**: 0-100 scale (volume-weighted RSI)
- **signal**: "overbought" (>80), "oversold" (<20), "neutral"

---

### 4. generate_investment_summary

Generate a comprehensive investment analysis report with buy/sell/hold recommendation.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "ticker": {
      "type": "string",
      "description": "Stock ticker symbol"
    }
  },
  "required": ["ticker"]
}
```

**Example Request**:
```json
{
  "name": "generate_investment_summary",
  "arguments": {
    "ticker": "TLV.RO"
  }
}
```

**Example Response**:
```json
{
  "success": true,
  "result": {
    "success": true,
    "ticker": "TLV.RO",
    "analysis_date": "2026-05-19",
    "current_price": 32.50,
    "price_change_1m": 5.2,
    "price_change_3m": 12.8,
    "price_change_6m": 18.5,
    "indicators": {
      "ema": {...},
      "rsi": {...},
      "macd": {...},
      "adx": {...},
      "stochastic": {...},
      "bollinger": {...},
      "mfi": {...}
    },
    "technical_analysis": {
      "trend": "bullish",
      "momentum": "positive",
      "volatility": "moderate",
      "volume_trend": "increasing"
    },
    "recommendation": {
      "action": "BUY",
      "confidence": "high",
      "reasoning": [
        "Strong bullish trend with Golden Cross forming",
        "RSI in healthy range (58.3) - room for upside",
        "MACD showing positive momentum",
        "Price above both EMA50 and EMA200",
        "Increasing volume confirms trend"
      ],
      "entry_strategy": {
        "ideal_entry": 32.00,
        "stop_loss": 30.50,
        "target_1": 34.50,
        "target_2": 36.00,
        "risk_reward_ratio": 2.5
      },
      "risks": [
        "Market volatility could trigger stop-loss",
        "Overbought conditions may develop if RSI exceeds 70",
        "Watch for MACD bearish crossover"
      ]
    },
    "summary": "Strong BUY recommendation based on bullish technical indicators..."
  }
}
```

**Recommendation Actions**:
- **BUY**: Strong bullish signals, good entry opportunity
- **HOLD**: Mixed signals, maintain current position
- **SELL**: Bearish signals, consider exiting position

**Confidence Levels**:
- **high**: 5+ bullish indicators aligned
- **medium**: 3-4 indicators aligned
- **low**: Mixed or weak signals

---

### 5. list_tickers

List all tickers in the watchlist.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {}
}
```

**Example Request**:
```json
{
  "name": "list_tickers",
  "arguments": {}
}
```

**Example Response**:
```json
{
  "success": true,
  "result": {
    "success": true,
    "count": 27,
    "tickers": [
      {
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "market": "US"
      },
      {
        "ticker": "TLV.RO",
        "name": "Banca Transilvania",
        "market": "Romania"
      },
      {
        "ticker": "SAP.DE",
        "name": "SAP SE",
        "market": "Germany"
      }
    ],
    "by_market": {
      "US": 5,
      "Romania": 17,
      "Germany": 4,
      "Other": 1
    }
  }
}
```

---

### 6. add_ticker

Add a new ticker to the watchlist.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "ticker": {
      "type": "string",
      "description": "Ticker symbol to add"
    }
  },
  "required": ["ticker"]
}
```

**Example Request**:
```json
{
  "name": "add_ticker",
  "arguments": {
    "ticker": "BRD.RO"
  }
}
```

**Example Response**:
```json
{
  "success": true,
  "result": {
    "success": true,
    "ticker": "BRD.RO",
    "message": "Ticker BRD.RO added to watchlist",
    "total_tickers": 28
  }
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Ticker BRD.RO already exists in watchlist"
}
```

---

### 7. screen_tickers

Screen watchlist for investment opportunities based on criteria.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "criteria": {
      "type": "object",
      "description": "Screening criteria",
      "properties": {
        "rsi_below": {"type": "number"},
        "rsi_above": {"type": "number"},
        "price_above_ema50": {"type": "boolean"},
        "macd_bullish": {"type": "boolean"},
        "adx_above": {"type": "number"}
      }
    }
  }
}
```

**Example Request**:
```json
{
  "name": "screen_tickers",
  "arguments": {
    "criteria": {
      "rsi_below": 40,
      "price_above_ema50": true,
      "macd_bullish": true
    }
  }
}
```

**Example Response**:
```json
{
  "success": true,
  "result": {
    "success": true,
    "criteria": {
      "rsi_below": 40,
      "price_above_ema50": true,
      "macd_bullish": true
    },
    "matches": [
      {
        "ticker": "TLV.RO",
        "current_price": 32.50,
        "rsi": 38.5,
        "ema_50": 31.85,
        "macd_signal": "bullish",
        "score": 3
      },
      {
        "ticker": "SNG.RO",
        "current_price": 0.45,
        "rsi": 35.2,
        "ema_50": 0.42,
        "macd_signal": "bullish",
        "score": 3
      }
    ],
    "total_screened": 27,
    "total_matches": 2
  }
}
```

**Available Criteria**:
- `rsi_below`: RSI below threshold (oversold)
- `rsi_above`: RSI above threshold (overbought)
- `price_above_ema50`: Price above 50-period EMA
- `price_below_ema50`: Price below 50-period EMA
- `macd_bullish`: MACD line above signal line
- `macd_bearish`: MACD line below signal line
- `adx_above`: ADX above threshold (strong trend)
- `adx_below`: ADX below threshold (weak trend)

---

## Error Handling

All tools return a consistent error format:

```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

### Common Error Codes

| Error | Description | Solution |
|-------|-------------|----------|
| Ticker not found | Invalid ticker symbol | Check ticker symbol and add market suffix |
| Insufficient data | Not enough historical data | Use longer period or different ticker |
| API rate limit | Too many Yahoo Finance requests | Wait and retry |
| Network timeout | Connection to Yahoo Finance failed | Check internet connection |
| Invalid period | Unsupported period value | Use valid period (1d, 5d, 1mo, etc.) |
| Invalid interval | Unsupported interval value | Use valid interval (1m, 5m, 1h, 1d, etc.) |

---

## Rate Limits

### Yahoo Finance API
- **Limit**: ~2000 requests/hour per IP
- **Recommendation**: Cache results for 5-15 minutes
- **Retry**: Exponential backoff on rate limit errors

### MCP Server
- **No hard limits** (single user environment)
- **Recommendation**: Avoid parallel requests for same ticker
- **Performance**: ~3-5 seconds per comprehensive analysis

---

## Testing

### Using curl (PowerShell)
```powershell
Invoke-RestMethod -Uri "http://192.168.1.7:8000/tools/call" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"name":"get_current_price","arguments":{"ticker":"AAPL"}}'
```

### Using Python
```python
import requests

response = requests.post(
    "http://192.168.1.7:8000/tools/call",
    json={
        "name": "calculate_all_indicators",
        "arguments": {
            "ticker": "TLV.RO",
            "period": "6mo"
        }
    }
)

result = response.json()
print(result)
```

### Using Bob Financial Analyst Mode
```
/mode financial-analyst
analizeaza AAPL
```

---

## Best Practices

### 1. Ticker Symbols
- Always use market suffixes for non-US stocks
- Verify ticker exists before analysis
- Use `list_tickers` to see available tickers

### 2. Data Periods
- Use 6mo for comprehensive technical analysis
- Use 1mo for short-term momentum analysis
- Use 1y+ for long-term trend analysis

### 3. Error Handling
- Always check `success` field in response
- Handle rate limit errors with retry logic
- Validate ticker symbols before API calls

### 4. Performance
- Cache indicator calculations when possible
- Avoid redundant API calls
- Use `generate_investment_summary` for complete analysis

---

## Related Documentation

- [Architecture](01-architecture.md) - System design and components
- [Deployment](03-deployment.md) - How to deploy the server
- [Troubleshooting](04-troubleshooting.md) - Common issues
- [Development](05-development.md) - How to add new tools