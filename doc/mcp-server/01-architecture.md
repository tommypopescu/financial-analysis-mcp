# 🏗️ Arhitectura Financial Analysis MCP Server

## 📋 Cuprins
- [Overview](#overview)
- [Arhitectura de Nivel Înalt](#arhitectura-de-nivel-înalt)
- [Componente Principale](#componente-principale)
- [Fluxul de Date](#fluxul-de-date)
- [Integrarea cu Bob](#integrarea-cu-bob)
- [Decizii de Design](#decizii-de-design)

## Overview

Financial Analysis MCP Server este un server MCP (Model Context Protocol) specializat pentru analiza financiară automată. Serverul oferă tool-uri pentru extragerea datelor financiare, calculul indicatorilor tehnici și generarea de recomandări de investiții.

### Caracteristici Principale
- **Transport HTTP**: FastAPI pentru compatibilitate maximă
- **Wrapper Stdio**: Bridge pentru integrarea cu Bob
- **9 Tool-uri MCP**: Funcționalități complete de analiză
- **7 Indicatori Tehnici**: EMA, RSI, MACD, ADX, Stochastic, Bollinger, MFI
- **Deployment Docker**: Containerizat pentru portabilitate

## Arhitectura de Nivel Înalt

```
┌─────────────────────────────────────────────────────────────┐
│                         Bob AI Assistant                     │
│                    (Windows, stdio protocol)                 │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ stdio (JSON-RPC 2.0)
                         │
┌────────────────────────▼────────────────────────────────────┐
│              financial-analysis-mcp-wrapper.py               │
│                   (Python Stdio-to-HTTP Bridge)              │
│                                                              │
│  • Convertește stdio → HTTP requests                        │
│  • Gestionează JSON-RPC 2.0 protocol                        │
│  • Buffering și error handling                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP (POST /mcp)
                         │
┌────────────────────────▼────────────────────────────────────┐
│           Financial Analysis MCP Server (FastAPI)            │
│                    (192.168.1.7:8000)                        │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              HTTP Transport Layer                     │  │
│  │  • FastAPI application                                │  │
│  │  • POST /mcp endpoint                                 │  │
│  │  • JSON-RPC 2.0 handling                              │  │
│  │  • CORS enabled                                       │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                    │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │              MCP Protocol Handler                     │  │
│  │  • tools/list - List available tools                  │  │
│  │  • tools/call - Execute tool                          │  │
│  │  • resources/list - List resources                    │  │
│  │  • Error handling & validation                        │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                    │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │                  Tool Layer                           │  │
│  │                                                        │  │
│  │  Data Extraction Tools:                               │  │
│  │  • fetch_ticker_data - Historical data                │  │
│  │  • get_current_price - Current price                  │  │
│  │                                                        │  │
│  │  Analysis Tools:                                      │  │
│  │  • calculate_all_indicators - Technical indicators    │  │
│  │  • generate_investment_summary - AI summary           │  │
│  │                                                        │  │
│  │  Watchlist Tools:                                     │  │
│  │  • list_tickers - List watchlist                      │  │
│  │  • add_ticker - Add to watchlist                      │  │
│  │  • screen_tickers - Screen opportunities              │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                    │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │              Calculation Layer                        │  │
│  │  • calculate_ema() - Exponential Moving Average       │  │
│  │  • calculate_rsi() - Relative Strength Index          │  │
│  │  • calculate_macd() - MACD indicator                  │  │
│  │  • calculate_adx() - Average Directional Index        │  │
│  │  • calculate_stochastic() - Stochastic Oscillator     │  │
│  │  • calculate_bollinger_bands() - Bollinger Bands      │  │
│  │  • calculate_mfi() - Money Flow Index                 │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                    │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │                Data Layer                             │  │
│  │  • yfinance integration                               │  │
│  │  • Data caching                                       │  │
│  │  • Error handling                                     │  │
│  │  • MultiIndex handling                                │  │
│  └──────────────────────┬───────────────────────────────┘  │
└─────────────────────────┼───────────────────────────────────┘
                          │
                          │ API Calls
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    Yahoo Finance API                         │
│  • Historical price data                                     │
│  • Current market data                                       │
│  • Volume and market cap                                     │
└──────────────────────────────────────────────────────────────┘
```

## Componente Principale

### 1. Stdio-to-HTTP Wrapper (`financial-analysis-mcp-wrapper.py`)

**Responsabilități**:
- Convertește comunicarea stdio (Bob) în HTTP requests
- Gestionează protocolul JSON-RPC 2.0
- Buffering pentru mesaje mari
- Error handling și retry logic

**Implementare**:
```python
class StdioToHttpBridge:
    def __init__(self, http_url: str):
        self.http_url = http_url
        self.session = requests.Session()
    
    def forward_request(self, json_rpc_request: dict) -> dict:
        """Forward JSON-RPC request to HTTP server"""
        response = self.session.post(
            self.http_url,
            json=json_rpc_request,
            headers={"Content-Type": "application/json"}
        )
        return response.json()
```

**Avantaje**:
- Bob poate folosi stdio (standard pentru MCP)
- Serverul poate rula remote (192.168.1.7)
- Separare clară între transport și logică

### 2. HTTP Transport Layer (FastAPI)

**Responsabilități**:
- Expune endpoint `/mcp` pentru JSON-RPC 2.0
- Validare requests și responses
- CORS handling pentru cross-origin requests
- Logging și monitoring

**Implementare**:
```python
@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """Handle MCP JSON-RPC 2.0 requests"""
    body = await request.json()
    
    # Validate JSON-RPC 2.0 format
    if "jsonrpc" not in body or body["jsonrpc"] != "2.0":
        return error_response(-32600, "Invalid Request")
    
    # Route to appropriate handler
    method = body.get("method")
    if method == "tools/list":
        return handle_tools_list()
    elif method == "tools/call":
        return handle_tools_call(body.get("params"))
    # ...
```

**Configurare**:
- Port: 8000
- Host: 0.0.0.0 (accessible din exterior)
- CORS: Enabled pentru toate originile
- Timeout: 30 secunde per request

### 3. MCP Protocol Handler

**Responsabilități**:
- Implementează specificația MCP
- Gestionează tool discovery și execution
- Resource management
- Error handling conform JSON-RPC 2.0

**Metode Suportate**:
```json
{
  "tools/list": "List all available tools",
  "tools/call": "Execute a specific tool",
  "resources/list": "List available resources",
  "resources/read": "Read a specific resource"
}
```

**Format Request**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "fetch_ticker_data",
    "arguments": {
      "ticker": "AAPL",
      "period": "1mo"
    }
  }
}
```

**Format Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Historical data for AAPL..."
      }
    ]
  }
}
```

### 4. Tool Layer

**9 Tool-uri Disponibile**:

#### Data Extraction Tools
1. **fetch_ticker_data**: Extrage date istorice
   - Input: ticker, period, interval
   - Output: DataFrame cu prețuri și volume

2. **get_current_price**: Obține prețul curent
   - Input: ticker
   - Output: Preț curent și informații de bază

#### Analysis Tools
3. **calculate_all_indicators**: Calculează toți indicatorii
   - Input: ticker, period
   - Output: Dicționar cu 7 indicatori tehnici

4. **generate_investment_summary**: Generează recomandare
   - Input: ticker
   - Output: Analiză completă cu verdict BUY/HOLD/SELL

#### Watchlist Tools
5. **list_tickers**: Listează watchlist-ul
   - Input: none
   - Output: Listă de tickere

6. **add_ticker**: Adaugă ticker în watchlist
   - Input: ticker
   - Output: Confirmare

7. **screen_tickers**: Screening pentru oportunități
   - Input: criteria (dict)
   - Output: Tickere care îndeplinesc criteriile

**Structura Tool**:
```python
{
    "name": "fetch_ticker_data",
    "description": "Fetch historical price and volume data",
    "inputSchema": {
        "type": "object",
        "properties": {
            "ticker": {
                "type": "string",
                "description": "Stock ticker symbol"
            },
            "period": {
                "type": "string",
                "description": "Data period (1d, 5d, 1mo, etc.)"
            }
        },
        "required": ["ticker"]
    }
}
```

### 5. Calculation Layer

**7 Indicatori Tehnici Implementați**:

#### 1. EMA (Exponential Moving Average)
```python
def calculate_ema(data: pd.Series, period: int) -> pd.Series:
    """Calculate EMA with specified period"""
    return data.ewm(span=period, adjust=False).mean()
```
- **Utilizare**: Identificare trend
- **Perioade**: EMA50, EMA200
- **Interpretare**: Preț > EMA = bullish, Preț < EMA = bearish

#### 2. RSI (Relative Strength Index)
```python
def calculate_rsi(data: pd.Series, period: int = 14) -> pd.Series:
    """Calculate RSI indicator"""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
```
- **Range**: 0-100
- **Overbought**: > 70
- **Oversold**: < 30

#### 3. MACD (Moving Average Convergence Divergence)
```python
def calculate_macd(data: pd.Series) -> dict:
    """Calculate MACD indicator"""
    ema12 = data.ewm(span=12, adjust=False).mean()
    ema26 = data.ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    histogram = macd_line - signal_line
    
    return {
        "macd": macd_line,
        "signal": signal_line,
        "histogram": histogram
    }
```
- **Componente**: MACD line, Signal line, Histogram
- **Semnale**: Crossover pentru buy/sell

#### 4. ADX (Average Directional Index)
```python
def calculate_adx(high: pd.Series, low: pd.Series, 
                  close: pd.Series, period: int = 14) -> pd.Series:
    """Calculate ADX indicator"""
    # Complex calculation involving +DI, -DI, and smoothing
    # ...
    return adx
```
- **Range**: 0-100
- **Trend Puternic**: > 25
- **Trend Slab**: < 20

#### 5. Stochastic Oscillator
```python
def calculate_stochastic(high: pd.Series, low: pd.Series,
                         close: pd.Series, period: int = 14) -> dict:
    """Calculate Stochastic Oscillator"""
    lowest_low = low.rolling(window=period).min()
    highest_high = high.rolling(window=period).max()
    
    k = 100 * (close - lowest_low) / (highest_high - lowest_low)
    d = k.rolling(window=3).mean()
    
    return {"k": k, "d": d}
```
- **Range**: 0-100
- **Overbought**: > 80
- **Oversold**: < 20

#### 6. Bollinger Bands
```python
def calculate_bollinger_bands(data: pd.Series, 
                               period: int = 20) -> dict:
    """Calculate Bollinger Bands"""
    sma = data.rolling(window=period).mean()
    std = data.rolling(window=period).std()
    
    return {
        "upper": sma + (2 * std),
        "middle": sma,
        "lower": sma - (2 * std)
    }
```
- **Componente**: Upper, Middle, Lower band
- **Utilizare**: Volatilitate și nivele de suport/rezistență

#### 7. MFI (Money Flow Index)
```python
def calculate_mfi(high: pd.Series, low: pd.Series,
                  close: pd.Series, volume: pd.Series,
                  period: int = 14) -> pd.Series:
    """Calculate Money Flow Index"""
    typical_price = (high + low + close) / 3
    money_flow = typical_price * volume
    
    # Positive and negative money flow calculation
    # ...
    
    return mfi
```
- **Range**: 0-100
- **Overbought**: > 80
- **Oversold**: < 20

### 6. Data Layer

**Responsabilități**:
- Integrare cu yfinance
- Caching pentru performanță
- Error handling pentru date lipsă
- MultiIndex handling pentru DataFrames

**Implementare**:
```python
def fetch_ticker_data(ticker: str, period: str = "1mo",
                      interval: str = "1d") -> pd.DataFrame:
    """Fetch data from Yahoo Finance"""
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        
        # Handle MultiIndex if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        return df
    except Exception as e:
        logger.error(f"Error fetching data for {ticker}: {e}")
        raise
```

**Caching Strategy**:
- Cache în memorie pentru date recente (< 1 oră)
- Invalidare automată după expirare
- Cache per ticker și period

## Fluxul de Date

### 1. Request Flow (Bob → Server)

```
Bob AI
  │
  │ 1. User request: "Analizează AAPL"
  │
  ▼
Stdio Wrapper
  │
  │ 2. Convert to JSON-RPC 2.0
  │    {
  │      "jsonrpc": "2.0",
  │      "method": "tools/call",
  │      "params": {
  │        "name": "generate_investment_summary",
  │        "arguments": {"ticker": "AAPL"}
  │      }
  │    }
  │
  │ 3. HTTP POST to 192.168.1.7:8000/mcp
  │
  ▼
FastAPI Server
  │
  │ 4. Validate JSON-RPC format
  │ 5. Route to tool handler
  │
  ▼
Tool Layer
  │
  │ 6. Execute generate_investment_summary
  │ 7. Call fetch_ticker_data
  │
  ▼
Data Layer
  │
  │ 8. Fetch from Yahoo Finance
  │ 9. Process MultiIndex
  │
  ▼
Calculation Layer
  │
  │ 10. Calculate all 7 indicators
  │ 11. Analyze trends
  │
  ▼
Tool Layer
  │
  │ 12. Generate summary with verdict
  │ 13. Format response
  │
  ▼
FastAPI Server
  │
  │ 14. Wrap in JSON-RPC response
  │
  ▼
Stdio Wrapper
  │
  │ 15. Forward to Bob via stdio
  │
  ▼
Bob AI
  │
  │ 16. Present analysis to user
  │
  ▼
User
```

### 2. Data Processing Pipeline

```
Raw Data (Yahoo Finance)
  │
  │ • OHLCV data
  │ • MultiIndex columns
  │
  ▼
Data Cleaning
  │
  │ • Flatten MultiIndex
  │ • Handle missing values
  │ • Validate data types
  │
  ▼
Indicator Calculation
  │
  │ • EMA50, EMA200
  │ • RSI (14)
  │ • MACD (12, 26, 9)
  │ • ADX (14)
  │ • Stochastic (14, 3)
  │ • Bollinger Bands (20, 2)
  │ • MFI (14)
  │
  ▼
Trend Analysis
  │
  │ • Price vs EMA
  │ • RSI levels
  │ • MACD crossovers
  │ • ADX strength
  │
  ▼
Signal Generation
  │
  │ • Buy signals
  │ • Sell signals
  │ • Hold conditions
  │
  ▼
Risk Assessment
  │
  │ • Volatility (Bollinger width)
  │ • Momentum (RSI, Stochastic)
  │ • Trend strength (ADX)
  │
  ▼
Investment Summary
  │
  │ • Verdict: BUY/HOLD/SELL
  │ • Confidence level
  │ • Risk factors
  │ • Entry/exit points
  │
  ▼
Formatted Response
```

## Integrarea cu Bob

### 1. Configurare Bob

**Fișier**: `.bob/mcp.json`
```json
{
  "mcpServers": {
    "financial-analysis": {
      "command": "python",
      "args": [
        "C:/Users/O82652826/financial-analysis-mcp-wrapper.py"
      ],
      "env": {
        "MCP_SERVER_URL": "http://192.168.1.7:8000/mcp"
      }
    }
  }
}
```

### 2. Financial Analyst Mode

**Fișier**: `.bob/custom_modes.yaml`
```yaml
financial-analyst:
  name: "📊 Financial Analyst"
  roleDefinition: |
    You are a professional financial analyst specializing in 
    medium-term stock market investments...
  
  tools:
    - fetch_ticker_data
    - calculate_all_indicators
    - generate_investment_summary
    - list_tickers
    - add_ticker
    - screen_tickers
```

### 3. Workflow Instructions

**Fișier**: `.bob/rules-financial-analyst/1_analysis_workflow.xml`
- Definește framework-ul de analiză în 5 faze
- Instrucțiuni detaliate pentru fiecare fază
- Template-uri pentru rapoarte

## Decizii de Design

### 1. De ce HTTP în loc de Stdio Direct?

**Problema**: Bob + SSH + Docker exec = stdio incompatibil

**Soluții Evaluate**:
1. ❌ **Stdio direct**: Nu funcționează prin SSH + Docker
2. ❌ **WebSocket**: Prea complex pentru JSON-RPC 2.0
3. ✅ **HTTP + Wrapper**: Simplu, robust, testabil

**Avantaje HTTP**:
- Funcționează remote (192.168.1.7)
- Ușor de testat (curl, Postman)
- Logging și monitoring simplu
- Scalabil (load balancer, multiple instances)

### 2. De ce FastAPI?

**Alternative Evaluate**:
1. Flask: Mai simplu dar mai puțin performant
2. Django: Prea complex pentru un API simplu
3. ✅ FastAPI: Perfect balance

**Avantaje FastAPI**:
- Async support pentru performanță
- Automatic OpenAPI documentation
- Type hints și validation
- Modern și bine documentat

### 3. De ce yfinance?

**Alternative Evaluate**:
1. Alpha Vantage: API key necesar, rate limits
2. IEX Cloud: Paid service
3. ✅ yfinance: Free, simplu, reliable

**Avantaje yfinance**:
- Gratuit și fără API key
- Date comprehensive
- Comunitate activă
- Bine documentat

### 4. De ce Docker?

**Avantaje**:
- Deployment consistent
- Izolare de sistem
- Ușor de actualizat
- Portabil între servere

**Configurare**:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 5. Structura Modulară

**Organizare**:
```
src/
├── main.py              # FastAPI app
├── tools/
│   ├── data_extraction.py
│   ├── analysis.py
│   └── watchlist.py
└── utils/
    ├── calculations.py
    └── helpers.py
```

**Avantaje**:
- Separare clară a responsabilităților
- Ușor de testat individual
- Extensibil pentru noi tool-uri
- Reutilizare cod

## Performance și Scalabilitate

### Optimizări Implementate

1. **Caching**:
   - Date în memorie pentru 1 oră
   - Reduce API calls la Yahoo Finance

2. **Async Processing**:
   - FastAPI async pentru multiple requests
   - Non-blocking I/O

3. **Connection Pooling**:
   - Requests session pentru HTTP wrapper
   - Reduce overhead de conexiune

### Limitări Curente

1. **Single Instance**: Un singur container Docker
2. **No Persistence**: Cache doar în memorie
3. **Rate Limits**: Yahoo Finance poate limita requests

### Planuri Viitoare

1. **Redis Cache**: Pentru persistență între restarts
2. **Load Balancer**: Multiple instances pentru scalabilitate
3. **Database**: Stocare istorică pentru analize complexe
4. **Monitoring**: Prometheus + Grafana pentru metrics

## Securitate

### Măsuri Implementate

1. **No Authentication**: Server intern (192.168.1.7)
2. **CORS**: Enabled pentru development
3. **Input Validation**: Pydantic models
4. **Error Handling**: Nu expune stack traces

### Recomandări pentru Producție

1. **API Key**: Autentificare pentru requests
2. **Rate Limiting**: Prevent abuse
3. **HTTPS**: TLS pentru comunicare
4. **Firewall**: Restrict access la IP-uri cunoscute

## Concluzie

Arhitectura Financial Analysis MCP Server este:
- **Modulară**: Componente independente și reutilizabile
- **Scalabilă**: Poate fi extinsă cu noi tool-uri
- **Robustă**: Error handling la toate nivelurile
- **Performantă**: Caching și async processing
- **Maintainabilă**: Cod clar și bine documentat

Pentru detalii despre implementare, vezi:
- [API Reference](./02-api-reference.md)
- [Deployment Guide](./03-deployment.md)
- [Development Guide](./05-development.md)