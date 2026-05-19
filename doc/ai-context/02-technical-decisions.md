# Technical Decisions

## Overview

This document explains the key technical decisions made during the project, including the rationale, alternatives considered, and trade-offs. Understanding these decisions is crucial for making informed changes and avoiding past mistakes.

## Table of Contents

1. [MCP Protocol Selection](#mcp-protocol-selection)
2. [HTTP Transport vs Stdio](#http-transport-vs-stdio)
3. [FastAPI Framework Choice](#fastapi-framework-choice)
4. [Docker Deployment Strategy](#docker-deployment-strategy)
5. [Technical Indicators Selection](#technical-indicators-selection)
6. [5-Phase Analysis Framework](#5-phase-analysis-framework)
7. [yfinance for Market Data](#yfinance-for-market-data)
8. [Wrapper Architecture](#wrapper-architecture)
9. [Bob Mode Configuration](#bob-mode-configuration)
10. [Documentation Structure](#documentation-structure)

---

## MCP Protocol Selection

### Decision
Use Model Context Protocol (MCP) for AI tool integration instead of custom API or direct function calls.

### Rationale

**Advantages**:
1. **Standardization**: MCP is an emerging standard for AI tool integration
2. **Multi-AI Support**: Works with Bob, Claude, and other MCP-compatible assistants
3. **Protocol Features**: Built-in error handling, type safety, documentation
4. **Future-Proof**: Growing ecosystem and adoption
5. **Tool Discovery**: AI can discover available tools automatically

**Why Not Alternatives**:
- **Custom REST API**: Would require custom client for each AI
- **Direct Function Calls**: No standardization, hard to integrate
- **OpenAI Function Calling**: Vendor lock-in, not universal

### Trade-offs

**Pros**:
- ✅ Standard protocol
- ✅ Multi-AI compatibility
- ✅ Built-in features
- ✅ Growing ecosystem

**Cons**:
- ❌ Relatively new protocol
- ❌ Limited documentation initially
- ❌ Requires MCP-compatible clients

### Implementation Details

**Protocol Version**: MCP 1.0 (JSON-RPC 2.0 based)

**Tool Definition Example**:
```python
{
    "name": "fetch_ticker_data",
    "description": "Fetch historical price and volume data",
    "inputSchema": {
        "type": "object",
        "properties": {
            "ticker": {"type": "string"},
            "period": {"type": "string"}
        },
        "required": ["ticker"]
    }
}
```

### Lessons Learned

1. **MCP is powerful but requires understanding**: Initial learning curve
2. **Transport matters**: Stdio vs HTTP has significant implications
3. **Error handling is crucial**: MCP errors must be properly formatted
4. **Documentation helps adoption**: Clear tool descriptions essential

---

## HTTP Transport vs Stdio

### Decision
Use HTTP transport for MCP server instead of stdio, with a wrapper for Bob compatibility.

### Background

**Initial Approach**: Stdio transport (standard input/output)
- Bob uses stdio by default
- Simpler protocol
- No network overhead

**Problem Encountered**: Bob couldn't connect via SSH + Docker exec
- Error: "MCP error -32000: Connection closed"
- Stdio streams not properly forwarded through SSH
- Docker exec stdio handling issues

### Solution Evolution

**Attempt 1: Fix Stdio**
- Tried various SSH configurations
- Attempted Docker exec with -i -t flags
- Result: ❌ Failed - fundamental compatibility issue

**Attempt 2: HTTP Transport**
- Implemented FastAPI HTTP server
- Exposed port 8000
- Result: ✅ Success - but Bob still uses stdio

**Attempt 3: Wrapper Bridge**
- Created Python wrapper on Windows
- Wrapper reads stdio from Bob
- Wrapper forwards to HTTP server
- Result: ✅ Complete success

### Architecture

```
Bob (stdio) → Wrapper (stdio→HTTP) → MCP Server (HTTP)
```

**Wrapper Location**: `C:/Users/O82652826/financial-analysis-mcp-wrapper.py`

**Wrapper Function**:
```python
def forward_request(request):
    """Forward stdio request to HTTP server"""
    response = requests.post(
        "http://192.168.1.7:8000/mcp",
        json=request,
        timeout=30
    )
    return response.json()
```

### Rationale

**Why HTTP**:
1. **Reliability**: HTTP is battle-tested for remote communication
2. **Debugging**: Easy to test with curl, Postman, browser
3. **Monitoring**: Standard HTTP logging and metrics
4. **Scalability**: Can add load balancing, caching, etc.
5. **Compatibility**: Works with any HTTP client

**Why Wrapper**:
1. **Bob Compatibility**: Bob requires stdio transport
2. **Transparency**: Bob doesn't know about HTTP backend
3. **Flexibility**: Can switch backends without changing Bob config
4. **Error Handling**: Wrapper can add retry logic, logging

### Trade-offs

**HTTP Pros**:
- ✅ Reliable remote communication
- ✅ Easy debugging and testing
- ✅ Standard tooling
- ✅ Scalable architecture

**HTTP Cons**:
- ❌ Network latency (minimal on LAN)
- ❌ Requires port management
- ❌ More complex than stdio

**Wrapper Pros**:
- ✅ Bob compatibility maintained
- ✅ Transparent to user
- ✅ Can add features (retry, cache)

**Wrapper Cons**:
- ❌ Additional component to maintain
- ❌ Extra process running
- ❌ Potential point of failure

### Alternatives Considered

1. **Pure Stdio**: ❌ Doesn't work with remote Docker
2. **WebSocket**: ⚠️ More complex, no clear benefit
3. **gRPC**: ⚠️ Overkill for this use case
4. **Direct Bob HTTP**: ❌ Bob doesn't support HTTP transport

### Implementation Details

**HTTP Server (FastAPI)**:
```python
@app.post("/mcp")
async def handle_mcp_request(request: dict):
    """Handle MCP JSON-RPC request"""
    method = request.get("method")
    params = request.get("params", {})
    
    if method == "tools/call":
        tool_name = params.get("name")
        tool_args = params.get("arguments", {})
        result = await execute_tool(tool_name, tool_args)
        return {"result": result}
```

**Wrapper (stdio bridge)**:
```python
def main():
    """Main wrapper loop"""
    for line in sys.stdin:
        request = json.loads(line)
        response = forward_to_http(request)
        print(json.dumps(response))
        sys.stdout.flush()
```

### Lessons Learned

1. **Stdio limitations**: Not suitable for remote/containerized services
2. **HTTP reliability**: Better for production deployments
3. **Wrapper pattern**: Effective for protocol bridging
4. **Testing importance**: Test with actual clients early

---

## FastAPI Framework Choice

### Decision
Use FastAPI for HTTP MCP server instead of Flask, Django, or raw ASGI.

### Rationale

**Advantages**:
1. **Performance**: Built on Starlette (async ASGI)
2. **Type Safety**: Pydantic models for validation
3. **Documentation**: Auto-generated OpenAPI docs
4. **Modern**: Async/await support
5. **Developer Experience**: Excellent error messages

**Why Not Alternatives**:
- **Flask**: Synchronous, slower, less type safety
- **Django**: Too heavy, unnecessary features
- **Raw ASGI**: Too low-level, more code to write
- **aiohttp**: Less mature, fewer features

### Trade-offs

**Pros**:
- ✅ Fast and async
- ✅ Type-safe with Pydantic
- ✅ Auto-generated docs
- ✅ Modern Python features
- ✅ Great error handling

**Cons**:
- ❌ Newer framework (less mature than Flask)
- ❌ Async can be complex
- ❌ Pydantic serialization limitations (e.g., DataFrames)

### Implementation Example

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Financial Analysis MCP Server")

class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: dict = {}
    id: int | str | None = None

@app.post("/mcp")
async def handle_mcp(request: MCPRequest):
    """Handle MCP request"""
    try:
        result = await process_request(request)
        return {"jsonrpc": "2.0", "result": result, "id": request.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Lessons Learned

1. **Pydantic serialization**: Cannot serialize pandas DataFrames directly
   - Solution: Convert to dict/list before returning
2. **Async benefits**: Significant for I/O-bound operations (API calls)
3. **Type hints**: Catch errors early, improve IDE support
4. **Documentation**: Auto-docs at `/docs` endpoint very useful

---

## Docker Deployment Strategy

### Decision
Deploy MCP server in Docker container on OMV server instead of bare metal or VM.

### Rationale

**Advantages**:
1. **Isolation**: Dependencies contained, no conflicts
2. **Reproducibility**: Same environment everywhere
3. **Portability**: Easy to move to different servers
4. **Updates**: Simple to rebuild and redeploy
5. **Resource Management**: CPU/memory limits

**Why Not Alternatives**:
- **Bare Metal**: Dependency conflicts, hard to reproduce
- **Virtual Machine**: More overhead, slower
- **Kubernetes**: Overkill for single service
- **Serverless**: Not suitable for stateful service

### Docker Configuration

**Multi-Stage Build**:
```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/
COPY data/ ./data/
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Benefits of Multi-Stage**:
- Smaller final image (no build tools)
- Faster deployment
- Better security (fewer packages)

### Deployment Process

**GitHub Actions CI/CD**:
```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [main, master]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and push
        run: |
          docker build -t ghcr.io/user/financial-analysis-mcp:latest .
          docker push ghcr.io/user/financial-analysis-mcp:latest
```

**Manual Deployment on OMV**:
```bash
# Pull latest image
docker pull ghcr.io/user/financial-analysis-mcp:latest

# Stop old container
docker stop financial-analysis-mcp

# Remove old container
docker rm financial-analysis-mcp

# Run new container
docker run -d \
  --name financial-analysis-mcp \
  --restart unless-stopped \
  -p 8000:8000 \
  -v /srv/dev-disk-by-uuid-xxx/financial-data:/app/data \
  ghcr.io/user/financial-analysis-mcp:latest
```

### Trade-offs

**Pros**:
- ✅ Isolated environment
- ✅ Easy updates
- ✅ Reproducible builds
- ✅ Resource control
- ✅ Portable

**Cons**:
- ❌ Docker overhead (minimal)
- ❌ Learning curve
- ❌ Image size (mitigated by multi-stage)

### Lessons Learned

1. **Multi-stage builds**: Significantly reduce image size
2. **Volume mounts**: Essential for persistent data (watchlist)
3. **Restart policy**: `unless-stopped` prevents manual restarts
4. **Port mapping**: Ensure host port available
5. **GitHub Actions**: Automate builds, reduce manual work

---

## Technical Indicators Selection

### Decision
Use 7 specific technical indicators: EMA50, EMA200, RSI, MACD, ADX, Stochastic, Bollinger Bands, MFI.

### Rationale

**Selection Criteria**:
1. **Proven Track Record**: Widely used by professional traders
2. **Complementary**: Each provides different insights
3. **Medium-Term Focus**: Suitable for 3-12 month holding periods
4. **Reliable**: Well-documented, mathematically sound
5. **Available**: Supported by ta-lib library

### Indicator Breakdown

#### 1. EMA50 & EMA200 (Trend)
**Purpose**: Identify trend direction and strength

**Why These Periods**:
- EMA50: Medium-term trend (2-3 months)
- EMA200: Long-term trend (8-10 months)
- Golden Cross (EMA50 > EMA200): Bullish signal
- Death Cross (EMA50 < EMA200): Bearish signal

**Alternatives Considered**:
- SMA: ❌ Less responsive to recent price changes
- EMA20/EMA100: ⚠️ Too short/long for medium-term

#### 2. RSI (Momentum)
**Purpose**: Measure momentum and overbought/oversold conditions

**Why 14-Period**:
- Standard period, widely accepted
- Good balance between sensitivity and reliability
- Overbought: RSI > 70
- Oversold: RSI < 30

**Alternatives Considered**:
- RSI(7): ❌ Too sensitive, many false signals
- RSI(21): ❌ Too slow, misses opportunities

#### 3. MACD (Trend Confirmation)
**Purpose**: Confirm trend changes and momentum

**Why 12,26,9**:
- Standard parameters
- 12-period fast EMA
- 26-period slow EMA
- 9-period signal line
- Crossovers indicate trend changes

**Alternatives Considered**:
- Custom periods: ⚠️ Less standard, harder to compare

#### 4. ADX (Trend Strength)
**Purpose**: Measure trend strength (not direction)

**Why 14-Period**:
- Standard period
- ADX > 25: Strong trend
- ADX < 20: Weak trend, range-bound

**Alternatives Considered**:
- Aroon: ⚠️ Similar but less widely used
- DMI alone: ❌ Doesn't measure strength as clearly

#### 5. Stochastic Oscillator (Momentum)
**Purpose**: Compare closing price to price range

**Why 14,3,3**:
- 14-period lookback
- 3-period %K smoothing
- 3-period %D smoothing
- Overbought: > 80
- Oversold: < 20

**Alternatives Considered**:
- Fast Stochastic: ❌ Too noisy
- Slow Stochastic (5,3,3): ⚠️ Less responsive

#### 6. Bollinger Bands (Volatility)
**Purpose**: Measure volatility and identify extremes

**Why 20,2**:
- 20-period SMA
- 2 standard deviations
- Price at upper band: Potentially overbought
- Price at lower band: Potentially oversold

**Alternatives Considered**:
- Keltner Channels: ⚠️ Similar but less popular
- ATR bands: ⚠️ More complex

#### 7. MFI (Volume-Weighted Momentum)
**Purpose**: Incorporate volume into momentum analysis

**Why 14-Period**:
- Standard period
- Similar to RSI but includes volume
- MFI > 80: Overbought with volume
- MFI < 20: Oversold with volume

**Alternatives Considered**:
- OBV: ❌ Cumulative, harder to interpret
- Volume RSI: ⚠️ Less standard

### Why Not More Indicators?

**Reasons for Limiting to 7**:
1. **Avoid Paralysis**: Too many indicators = conflicting signals
2. **Computational Cost**: Each indicator requires calculation
3. **Simplicity**: Easier to explain and understand
4. **Proven Combination**: These 7 cover all bases

**Categories Covered**:
- Trend: EMA50, EMA200, MACD
- Momentum: RSI, Stochastic, MFI
- Volatility: Bollinger Bands
- Strength: ADX

### Trade-offs

**Pros**:
- ✅ Comprehensive coverage
- ✅ Proven indicators
- ✅ Complementary insights
- ✅ Standard parameters

**Cons**:
- ❌ No fundamental analysis
- ❌ Lagging indicators (historical data)
- ❌ Can give conflicting signals

### Implementation

**Calculation Library**: ta-lib (Technical Analysis Library)

**Why ta-lib**:
- Industry standard
- Fast (C implementation)
- Comprehensive (150+ indicators)
- Well-tested

**Example Calculation**:
```python
import talib

def calculate_rsi(close_prices, period=14):
    """Calculate RSI using ta-lib"""
    return talib.RSI(close_prices, timeperiod=period)

def calculate_macd(close_prices):
    """Calculate MACD using ta-lib"""
    macd, signal, hist = talib.MACD(
        close_prices,
        fastperiod=12,
        slowperiod=26,
        signalperiod=9
    )
    return macd, signal, hist
```

### Lessons Learned

1. **Standard parameters**: Use widely accepted values for comparability
2. **Complementary indicators**: Choose indicators that provide different insights
3. **Volume matters**: MFI adds important volume dimension
4. **Trend + Momentum**: Both are essential for complete picture
5. **Simplicity wins**: 7 indicators sufficient, more adds confusion

---

## 5-Phase Analysis Framework

### Decision
Structure analysis into 5 distinct phases instead of ad-hoc or single-step analysis.

### Rationale

**Why 5 Phases**:
1. **Systematic**: Ensures nothing is missed
2. **Reproducible**: Same process every time
3. **Educational**: User learns methodology
4. **Quality Control**: Each phase has validation
5. **Comprehensive**: Covers all aspects

### Phase Breakdown

#### Phase 1: Data Collection
**Purpose**: Gather all necessary data

**Activities**:
- Fetch historical OHLCV data (6 months)
- Get current price
- Calculate all 7 technical indicators

**Why First**:
- Foundation for all analysis
- Validates data availability
- Identifies data quality issues early

**Quality Checks**:
- Minimum 60 days of data
- All indicators calculated successfully
- Current price is recent (<1 day old)

#### Phase 2: Technical Analysis
**Purpose**: Interpret indicators and identify patterns

**Activities**:
- Analyze trend (EMA50 vs EMA200)
- Assess momentum (RSI, MACD, Stochastic)
- Evaluate strength (ADX)
- Check volume (MFI)
- Review volatility (Bollinger Bands)

**Why Second**:
- Requires data from Phase 1
- Provides foundation for scenarios
- Identifies current market state

**Quality Checks**:
- Trend direction identified
- Momentum assessed
- All indicators interpreted

#### Phase 3: Scenario Planning
**Purpose**: Develop possible future outcomes

**Activities**:
- Bullish scenario (probability, target, timeframe)
- Bearish scenario (probability, target, timeframe)
- Neutral scenario (probability, range, timeframe)

**Why Third**:
- Requires technical analysis from Phase 2
- Provides context for risk assessment
- Helps set realistic expectations

**Quality Checks**:
- All 3 scenarios developed
- Probabilities sum to 100%
- Targets are realistic
- Timeframes specified

#### Phase 4: Risk Assessment
**Purpose**: Calculate risk parameters

**Activities**:
- Position sizing (% of portfolio)
- Stop loss placement
- Risk/reward ratio calculation
- Maximum loss estimation

**Why Fourth**:
- Requires scenarios from Phase 3
- Essential before making decision
- Protects capital

**Quality Checks**:
- Position size ≤ 5% of portfolio
- Stop loss defined
- Risk/reward ≥ 1:2
- Maximum loss acceptable

#### Phase 5: Investment Decision
**Purpose**: Make final recommendation

**Activities**:
- Calculate signal score (0-10)
- Determine verdict (BUY/HOLD/SELL)
- Assess confidence level
- Provide action plan

**Why Last**:
- Requires all previous phases
- Synthesizes all information
- Provides clear direction

**Quality Checks**:
- Verdict is unequivocal
- Rationale is clear
- Action plan is specific
- Confidence level justified

### Why Not Alternatives?

**Single-Step Analysis**: ❌ Too simplistic, misses nuances

**3-Phase (Data, Analysis, Decision)**: ⚠️ Skips scenarios and risk

**7-Phase (Add Fundamentals, News)**: ⚠️ Too complex for current scope

**Ad-hoc Analysis**: ❌ Inconsistent, unreliable

### Trade-offs

**Pros**:
- ✅ Systematic and thorough
- ✅ Reproducible results
- ✅ Educational value
- ✅ Quality assurance
- ✅ Clear structure

**Cons**:
- ❌ Takes longer (2-3 minutes vs instant)
- ❌ More complex to implement
- ❌ Requires discipline to follow

### Implementation

**Workflow XML**: `.bob/rules-financial-analyst/1_analysis_workflow.xml`

**Example Phase Definition**:
```xml
<phase id="1" name="Data Collection">
    <objective>
        Gather all necessary market data and technical indicators
    </objective>
    
    <tools>
        <tool>fetch_ticker_data</tool>
        <tool>get_current_price</tool>
        <tool>calculate_all_indicators</tool>
    </tools>
    
    <quality_checks>
        <check>Minimum 60 days of data</check>
        <check>All indicators calculated</check>
        <check>Current price is recent</check>
    </quality_checks>
</phase>
```

### Lessons Learned

1. **Structure matters**: Systematic approach produces better results
2. **Quality checks essential**: Catch issues early
3. **Scenarios are valuable**: Help set realistic expectations
4. **Risk first**: Always assess risk before deciding
5. **Clear verdicts**: Users need unequivocal recommendations

---

## yfinance for Market Data

### Decision
Use yfinance library for market data instead of paid APIs or web scraping.

### Rationale

**Advantages**:
1. **Free**: No API costs
2. **Comprehensive**: US, international, crypto
3. **Historical Data**: Years of OHLCV data
4. **Easy to Use**: Simple Python API
5. **Maintained**: Active development

**Why Not Alternatives**:
- **Alpha Vantage**: ❌ Rate limits, API key required
- **IEX Cloud**: ❌ Paid, limited free tier
- **Bloomberg API**: ❌ Expensive, complex
- **Web Scraping**: ❌ Fragile, legal issues
- **Quandl**: ❌ Limited free data

### Trade-offs

**Pros**:
- ✅ Free and unlimited
- ✅ Easy to use
- ✅ Comprehensive coverage
- ✅ No API keys needed
- ✅ Active community

**Cons**:
- ❌ 15-20 minute delay (not real-time)
- ❌ Depends on Yahoo Finance
- ❌ Occasional data gaps
- ❌ No official support
- ❌ Rate limiting possible

### Implementation

**Basic Usage**:
```python
import yfinance as yf

def fetch_ticker_data(ticker, period="6mo"):
    """Fetch historical data"""
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    return df

def get_current_price(ticker):
    """Get latest price"""
    stock = yf.Ticker(ticker)
    return stock.info.get('currentPrice')
```

**MultiIndex Handling**:
```python
def handle_multiindex(df):
    """Handle MultiIndex columns"""
    if isinstance(df.columns, pd.MultiIndex):
        # Flatten MultiIndex
        df.columns = ['_'.join(col).strip() 
                     for col in df.columns.values]
    return df
```

### Known Issues

**Issue 1: MultiIndex Columns**
- **Problem**: Some tickers return MultiIndex columns
- **Solution**: Flatten before processing
- **Commit**: Fixed in data_extraction.py

**Issue 2: Data Gaps**
- **Problem**: Some dates missing (holidays, halts)
- **Solution**: Forward fill missing values
- **Impact**: Minimal for medium-term analysis

**Issue 3: Ticker Symbols**
- **Problem**: Different symbols for same stock (e.g., BRK.A vs BRK-A)
- **Solution**: Document correct format, validate input
- **Impact**: User education needed

### Lessons Learned

1. **Free has trade-offs**: Delay acceptable for medium-term
2. **Data validation**: Always check for gaps and errors
3. **MultiIndex handling**: Common issue, needs robust solution
4. **Ticker formats**: Vary by exchange, document clearly
5. **Backup plan**: Consider paid API for future if needed

---

## Wrapper Architecture

### Decision
Create Python wrapper to bridge Bob's stdio to HTTP MCP server.

### Rationale

**Problem**: Bob uses stdio, MCP server uses HTTP

**Solution Options**:
1. **Modify Bob**: ❌ Not possible, closed source
2. **Modify MCP Server**: ❌ Loses HTTP benefits
3. **Create Wrapper**: ✅ Best of both worlds

**Wrapper Benefits**:
1. **Transparency**: Bob doesn't know about HTTP
2. **Flexibility**: Can change backend without Bob changes
3. **Features**: Can add retry, caching, logging
4. **Simplicity**: Small, focused component

### Architecture

```
┌─────────┐
│   Bob   │
│ (stdio) │
└────┬────┘
     │ stdin/stdout
     │ JSON-RPC 2.0
┌────▼────────────────────────────┐
│  Wrapper (Python)               │
│  - Read from stdin              │
│  - Parse JSON-RPC               │
│  - Forward to HTTP              │
│  - Return response to stdout    │
└────┬────────────────────────────┘
     │ HTTP POST
     │ http://192.168.1.7:8000/mcp
┌────▼────────────────────────────┐
│  MCP Server (FastAPI)           │
│  - Handle HTTP request          │
│  - Execute tool                 │
│  - Return JSON response         │
└─────────────────────────────────┘
```

### Implementation

**Wrapper Code** (`financial-analysis-mcp-wrapper.py`):
```python
import sys
import json
import requests
import logging

MCP_SERVER_URL = "http://192.168.1.7:8000/mcp"
TIMEOUT = 30

def forward_request(request):
    """Forward stdio request to HTTP server"""
    try:
        response = requests.post(
            MCP_SERVER_URL,
            json=request,
            timeout=TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP request failed: {e}")
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": -32000,
                "message": f"HTTP request failed: {str(e)}"
            },
            "id": request.get("id")
        }

def main():
    """Main wrapper loop"""
    logging.basicConfig(
        filename='C:/Users/O82652826/mcp-wrapper.log',
        level=logging.INFO
    )
    
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            logging.info(f"Request: {request}")
            
            response = forward_request(request)
            logging.info(f"Response: {response}")
            
            print(json.dumps(response))
            sys.stdout.flush()
        except Exception as e:
            logging.error(f"Error: {e}")
            error_response = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": str(e)
                },
                "id": None
            }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
```

### Trade-offs

**Pros**:
- ✅ Maintains Bob compatibility
- ✅ Enables HTTP backend
- ✅ Can add features (retry, cache)
- ✅ Simple and focused
- ✅ Easy to debug

**Cons**:
- ❌ Additional component
- ❌ Extra process
- ❌ Potential failure point
- ❌ Adds latency (minimal)

### Lessons Learned

1. **Wrapper pattern works**: Effective for protocol bridging
2. **Logging essential**: Helps debug issues
3. **Error handling**: Must handle both stdio and HTTP errors
4. **Timeout important**: Prevent hanging on slow requests
5. **Flush stdout**: Required for stdio communication

---

## Bob Mode Configuration

### Decision
Create dedicated "Financial Analyst" mode for Bob instead of using generic modes.

### Rationale

**Why Custom Mode**:
1. **Specialized Behavior**: Investment analysis requires specific workflow
2. **Tool Permissions**: Only financial tools needed
3. **Consistent Results**: Enforces 5-phase framework
4. **User Experience**: Clear mode for financial tasks
5. **Extensibility**: Easy to add more financial modes

**Why Not Generic**:
- **Code Mode**: ❌ Too broad, no financial focus
- **Ask Mode**: ❌ No tool execution
- **Advanced Mode**: ⚠️ Works but not specialized

### Configuration

**Mode Definition** (`.bob/custom_modes.yaml`):
```yaml
financial-analyst:
  slug: financial-analyst
  name: "📊 Financial Analyst"
  roleDefinition: |
    You are a professional financial analyst specializing in 
    medium-term stock market investments (3-12 months).
    
    Your analysis follows a rigorous 5-phase framework:
    1. Data Collection
    2. Technical Analysis
    3. Scenario Planning
    4. Risk Assessment
    5. Investment Decision
    
    You provide clear, unequivocal verdicts: BUY, HOLD, or SELL.
  
  whenToUse: |
    Use this mode when performing comprehensive stock market 
    analysis for investment decisions.
  
  groups:
    - slug: read
      allowed: true
    - slug: mcp
      allowed: true
    - slug: command
      allowed: true
```

**Workflow Instructions** (`.bob/rules-financial-analyst/`):
- `1_analysis_workflow.xml`: 5-phase framework (398 lines)
- `2_analysis_examples.xml`: Educational examples (827 lines)

### Trade-offs

**Pros**:
- ✅ Specialized for financial analysis
- ✅ Enforces consistent methodology
- ✅ Clear user experience
- ✅ Easy to extend
- ✅ Separate from other modes

**Cons**:
- ❌ More configuration to maintain
- ❌ Mode switching overhead
- ❌ Requires XML workflow files

### Lessons Learned

1. **Specialized modes better**: More focused than generic modes
2. **XML workflows powerful**: Provide detailed guidance
3. **Examples essential**: Help Bob understand expectations
4. **Mode switching**: Users need clear indication of active mode
5. **Documentation critical**: Mode behavior must be documented

---

## Documentation Structure

### Decision
Organize documentation in `doc/` folder with subdirectories for each component.

### Rationale

**Why Structured Documentation**:
1. **Findability**: Easy to locate relevant docs
2. **Maintainability**: Clear ownership of each doc
3. **Completeness**: Ensures all aspects covered
4. **AI-Friendly**: AI can navigate structure
5. **Scalability**: Easy to add new docs

**Structure**:
```
doc/
├── README.md                    # Index and navigation
├── mcp-server/                  # MCP server docs
│   ├── 01-architecture.md
│   ├── 02-api-reference.md
│   ├── 03-deployment.md
│   ├── 04-troubleshooting.md
│   └── 05-development.md
├── financial-analyst-mode/      # Mode docs
│   ├── 01-overview.md
│   ├── 02-configuration.md
│   ├── 03-workflow.md
│   ├── 04-usage-guide.md
│   └── 05-examples.md
├── bob-configuration/           # Bob config docs
│   ├── README.md
│   ├── custom-modes.md
│   ├── mcp-wrapper.md
│   └── workflow-instructions.md
└── ai-context/                  # AI context docs
    ├── README.md
    ├── 01-project-overview.md
    ├── 02-technical-decisions.md
    ├── 03-modification-guide.md
    └── 04-troubleshooting-history.md
```

### Trade-offs

**Pros**:
- ✅ Well-organized
- ✅ Easy to navigate
- ✅ Clear ownership
- ✅ Scalable
- ✅ AI-friendly

**Cons**:
- ❌ More files to maintain
- ❌ Potential duplication
- ❌ Requires discipline

### Documentation Standards

**File Naming**:
- Use numbered prefixes for ordered docs (01-, 02-, etc.)
- Use descriptive names (architecture.md, not arch.md)
- Use kebab-case (technical-decisions.md)

**Content Structure**:
- Start with overview/summary
- Use clear headings (##, ###)
- Include code examples
- Add cross-references
- Provide context

**Maintenance**:
- Update when code changes
- Add new patterns discovered
- Remove obsolete information
- Keep cross-references current

### Lessons Learned

1. **Structure matters**: Well-organized docs are actually used
2. **AI context essential**: Helps AI understand project
3. **Examples valuable**: Show don't just tell
4. **Cross-references**: Link related docs
5. **Keep updated**: Outdated docs worse than no docs

---

## Summary

This document captures the key technical decisions made during the project. Understanding these decisions helps:
- ✅ Make informed changes
- ✅ Avoid repeating mistakes
- ✅ Maintain architectural consistency
- ✅ Evaluate alternatives properly
- ✅ Preserve institutional knowledge

**Key Takeaways**:
1. **HTTP over stdio**: More reliable for remote services
2. **Wrapper pattern**: Effective for protocol bridging
3. **FastAPI**: Excellent for modern Python APIs
4. **Docker**: Essential for reproducible deployments
5. **7 indicators**: Comprehensive without overwhelming
6. **5-phase framework**: Systematic analysis produces better results
7. **yfinance**: Good enough for medium-term analysis
8. **Custom modes**: Better than generic for specialized tasks
9. **Structured docs**: Essential for maintainability

**Related Documentation**:
- [Project Overview](01-project-overview.md)
- [Modification Guide](03-modification-guide.md)
- [Troubleshooting History](04-troubleshooting-history.md)
- [MCP Server Architecture](../mcp-server/01-architecture.md)