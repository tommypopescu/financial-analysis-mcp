# Modification Guide

## Overview

This guide provides step-by-step instructions for making common modifications to the Financial Analysis MCP Server project. Follow these procedures to ensure changes are safe, tested, and properly deployed.

## Table of Contents

1. [Adding New MCP Tools](#adding-new-mcp-tools)
2. [Modifying Technical Indicators](#modifying-technical-indicators)
3. [Updating Analysis Workflow](#updating-analysis-workflow)
4. [Changing Bob Mode Behavior](#changing-bob-mode-behavior)
5. [Adding New Tickers to Watchlist](#adding-new-tickers-to-watchlist)
6. [Updating Dependencies](#updating-dependencies)
7. [Modifying Docker Configuration](#modifying-docker-configuration)
8. [Testing Changes](#testing-changes)
9. [Deployment Procedures](#deployment-procedures)
10. [Rollback Procedures](#rollback-procedures)

---

## Adding New MCP Tools

### When to Add a New Tool

Add a new MCP tool when you need to:
- Fetch new types of data (e.g., news, fundamentals)
- Perform new calculations (e.g., new indicators)
- Provide new analysis capabilities (e.g., portfolio optimization)

### Step-by-Step Procedure

#### 1. Design the Tool

**Define Tool Specification**:
```python
# Tool name: fetch_company_news
# Description: Fetch recent news articles for a company
# Input: ticker (string), days (integer, optional, default=7)
# Output: list of news articles with title, date, summary, url
```

**Consider**:
- What data does it need? (inputs)
- What will it return? (outputs)
- What errors can occur? (error handling)
- How long will it take? (performance)

#### 2. Create Tool Function

**Location**: `fin/financial-analysis-mcp/src/tools/` (choose appropriate file or create new)

**Example** (`src/tools/news.py`):
```python
"""News fetching tools for MCP server."""
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, List, Any

async def fetch_company_news(ticker: str, days: int = 7) -> Dict[str, Any]:
    """
    Fetch recent news articles for a company.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL')
        days: Number of days to look back (default: 7)
    
    Returns:
        Dictionary with:
        - ticker: str
        - news: List of news articles
        - count: int
    
    Raises:
        ValueError: If ticker is invalid
        Exception: If news fetch fails
    """
    try:
        # Validate ticker
        if not ticker or not isinstance(ticker, str):
            raise ValueError("Invalid ticker symbol")
        
        # Fetch news
        stock = yf.Ticker(ticker)
        news = stock.news
        
        # Filter by date
        cutoff_date = datetime.now() - timedelta(days=days)
        filtered_news = []
        
        for article in news:
            article_date = datetime.fromtimestamp(article.get('providerPublishTime', 0))
            if article_date >= cutoff_date:
                filtered_news.append({
                    'title': article.get('title', ''),
                    'publisher': article.get('publisher', ''),
                    'date': article_date.isoformat(),
                    'summary': article.get('summary', ''),
                    'url': article.get('link', '')
                })
        
        return {
            'ticker': ticker.upper(),
            'news': filtered_news,
            'count': len(filtered_news),
            'days': days
        }
        
    except ValueError as e:
        raise ValueError(f"Invalid input: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to fetch news for {ticker}: {str(e)}")
```

#### 3. Register Tool in Server

**Location**: `fin/financial-analysis-mcp/src/server.py`

**Add Import**:
```python
from src.tools.news import fetch_company_news
```

**Add Tool Definition**:
```python
TOOLS = [
    # ... existing tools ...
    {
        "name": "fetch_company_news",
        "description": "Fetch recent news articles for a company",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Stock ticker symbol (e.g., 'AAPL')"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days to look back (default: 7)",
                    "default": 7
                }
            },
            "required": ["ticker"]
        }
    }
]
```

**Add Tool Handler**:
```python
async def execute_tool(tool_name: str, arguments: dict) -> dict:
    """Execute MCP tool by name."""
    try:
        # ... existing tool handlers ...
        
        elif tool_name == "fetch_company_news":
            ticker = arguments.get("ticker")
            days = arguments.get("days", 7)
            return await fetch_company_news(ticker, days)
        
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
            
    except Exception as e:
        logger.error(f"Tool execution error: {e}")
        raise
```

#### 4. Add Tests

**Location**: `fin/financial-analysis-mcp/tests/test_news.py` (create if needed)

```python
import pytest
from src.tools.news import fetch_company_news

@pytest.mark.asyncio
async def test_fetch_company_news_valid():
    """Test fetching news for valid ticker."""
    result = await fetch_company_news("AAPL", days=7)
    
    assert result['ticker'] == "AAPL"
    assert 'news' in result
    assert isinstance(result['news'], list)
    assert result['count'] >= 0

@pytest.mark.asyncio
async def test_fetch_company_news_invalid_ticker():
    """Test error handling for invalid ticker."""
    with pytest.raises(ValueError):
        await fetch_company_news("", days=7)

@pytest.mark.asyncio
async def test_fetch_company_news_default_days():
    """Test default days parameter."""
    result = await fetch_company_news("MSFT")
    assert result['days'] == 7
```

#### 5. Update Documentation

**Add to** `doc/mcp-server/02-api-reference.md`:

```markdown
### fetch_company_news

Fetch recent news articles for a company.

**Input Parameters**:
- `ticker` (string, required): Stock ticker symbol
- `days` (integer, optional): Number of days to look back (default: 7)

**Output**:
```json
{
  "ticker": "AAPL",
  "news": [
    {
      "title": "Apple announces new product",
      "publisher": "Reuters",
      "date": "2026-05-19T10:30:00",
      "summary": "Apple Inc. announced...",
      "url": "https://..."
    }
  ],
  "count": 1,
  "days": 7
}
```

**Example Usage**:
```python
# Fetch last 7 days of news
result = await fetch_company_news("AAPL")

# Fetch last 30 days of news
result = await fetch_company_news("AAPL", days=30)
```

**Error Handling**:
- `ValueError`: Invalid ticker symbol
- `Exception`: News fetch failed
```

#### 6. Test Locally

```bash
# Navigate to project directory
cd fin/financial-analysis-mcp

# Run tests
pytest tests/test_news.py -v

# Test with docker-compose
docker-compose up --build

# Test tool via wrapper
python C:/Users/O82652826/test-mcp-tool.py fetch_company_news '{"ticker": "AAPL"}'
```

#### 7. Commit and Push

```bash
git add src/tools/news.py
git add src/server.py
git add tests/test_news.py
git add doc/mcp-server/02-api-reference.md
git commit -m "feat: Add fetch_company_news MCP tool"
git push origin master
```

#### 8. Deploy

GitHub Actions will automatically:
1. Build new Docker image
2. Push to GitHub Container Registry

Then manually deploy:
```bash
# SSH to OMV server
ssh user@192.168.1.7

# Pull latest image
docker pull ghcr.io/user/financial-analysis-mcp:latest

# Restart container
docker stop financial-analysis-mcp
docker rm financial-analysis-mcp
docker run -d \
  --name financial-analysis-mcp \
  --restart unless-stopped \
  -p 8000:8000 \
  -v /srv/dev-disk-by-uuid-xxx/financial-data:/app/data \
  ghcr.io/user/financial-analysis-mcp:latest
```

#### 9. Verify

```bash
# Test from Windows
python C:/Users/O82652826/test-mcp-tool.py fetch_company_news '{"ticker": "AAPL"}'

# Test with Bob
# Switch to Financial Analyst mode
# Ask: "Fetch news for AAPL"
```

### Common Pitfalls

1. **Pydantic Serialization**: Don't return pandas DataFrames or other non-serializable objects
   - ❌ `return {'data': df}`
   - ✅ `return {'data': df.to_dict('records')}`

2. **Error Handling**: Always handle errors gracefully
   - ❌ Let exceptions bubble up
   - ✅ Catch, log, and return meaningful error messages

3. **Type Hints**: Use proper type hints for better IDE support
   - ❌ `def tool(ticker):`
   - ✅ `async def tool(ticker: str) -> Dict[str, Any]:`

4. **Async/Await**: Use async for I/O-bound operations
   - ❌ `def fetch_data():`
   - ✅ `async def fetch_data():`

---

## Modifying Technical Indicators

### When to Modify Indicators

Modify indicators when you need to:
- Change calculation parameters (e.g., RSI period)
- Add new indicators
- Fix calculation bugs
- Optimize performance

### Step-by-Step Procedure

#### 1. Locate Indicator Code

**File**: `fin/financial-analysis-mcp/src/utils/calculations.py`

**Example - Modify RSI Period**:

**Current Code**:
```python
def calculate_rsi(close_prices, period=14):
    """Calculate RSI with 14-period."""
    return talib.RSI(close_prices, timeperiod=period)
```

**Modified Code**:
```python
def calculate_rsi(close_prices, period=21):
    """Calculate RSI with 21-period (more conservative)."""
    return talib.RSI(close_prices, timeperiod=period)
```

#### 2. Update Tool Function

**File**: `fin/financial-analysis-mcp/src/tools/data_extraction.py`

**Update `calculate_all_indicators`**:
```python
async def calculate_all_indicators(ticker: str, period: str = "6mo") -> Dict[str, Any]:
    """Calculate all technical indicators."""
    # ... fetch data ...
    
    # Calculate indicators with new parameters
    indicators = {
        'rsi': float(calculate_rsi(close_prices, period=21)),  # Changed from 14
        # ... other indicators ...
    }
    
    return indicators
```

#### 3. Update Documentation

**Update** `doc/mcp-server/02-api-reference.md`:

```markdown
### Technical Indicators

**RSI (Relative Strength Index)**:
- Period: 21 (changed from 14 for more conservative signals)
- Overbought: > 70
- Oversold: < 30
```

**Update** `doc/financial-analyst-mode/03-workflow.md`:

```xml
<indicator>
    <name>RSI</name>
    <period>21</period>
    <interpretation>
        RSI > 70: Overbought (consider selling)
        RSI < 30: Oversold (consider buying)
        RSI 40-60: Neutral
    </interpretation>
</indicator>
```

#### 4. Test Changes

```bash
# Run tests
pytest tests/test_calculations.py -v

# Test with real data
python -c "
from src.tools.data_extraction import calculate_all_indicators
import asyncio
result = asyncio.run(calculate_all_indicators('AAPL'))
print(f'RSI: {result[\"rsi\"]}')
"
```

#### 5. Update Analysis Examples

**Update** `.bob/rules-financial-analyst/2_analysis_examples.xml`:

```xml
<example>
    <indicators>
        <rsi>65.2</rsi>  <!-- Update example values -->
        <!-- Note: RSI now uses 21-period -->
    </indicators>
</example>
```

#### 6. Commit, Push, Deploy

```bash
git add src/utils/calculations.py
git add src/tools/data_extraction.py
git add doc/
git add .bob/rules-financial-analyst/
git commit -m "feat: Change RSI period from 14 to 21 for more conservative signals"
git push origin master

# Deploy (see deployment section)
```

### Adding New Indicator

**Example: Add Ichimoku Cloud**

#### 1. Add Calculation Function

**File**: `src/utils/calculations.py`

```python
def calculate_ichimoku(high_prices, low_prices, close_prices):
    """
    Calculate Ichimoku Cloud components.
    
    Returns:
        dict with tenkan, kijun, senkou_a, senkou_b, chikou
    """
    # Tenkan-sen (Conversion Line): 9-period
    tenkan = (high_prices.rolling(9).max() + low_prices.rolling(9).min()) / 2
    
    # Kijun-sen (Base Line): 26-period
    kijun = (high_prices.rolling(26).max() + low_prices.rolling(26).min()) / 2
    
    # Senkou Span A (Leading Span A)
    senkou_a = ((tenkan + kijun) / 2).shift(26)
    
    # Senkou Span B (Leading Span B): 52-period
    senkou_b = ((high_prices.rolling(52).max() + low_prices.rolling(52).min()) / 2).shift(26)
    
    # Chikou Span (Lagging Span)
    chikou = close_prices.shift(-26)
    
    return {
        'tenkan': float(tenkan.iloc[-1]),
        'kijun': float(kijun.iloc[-1]),
        'senkou_a': float(senkou_a.iloc[-1]),
        'senkou_b': float(senkou_b.iloc[-1]),
        'chikou': float(chikou.iloc[-1])
    }
```

#### 2. Add to `calculate_all_indicators`

```python
async def calculate_all_indicators(ticker: str, period: str = "6mo") -> Dict[str, Any]:
    """Calculate all technical indicators."""
    # ... existing code ...
    
    # Add Ichimoku
    ichimoku = calculate_ichimoku(high_prices, low_prices, close_prices)
    
    indicators = {
        # ... existing indicators ...
        'ichimoku': ichimoku
    }
    
    return indicators
```

#### 3. Update Workflow

**File**: `.bob/rules-financial-analyst/1_analysis_workflow.xml`

```xml
<phase id="2" name="Technical Analysis">
    <indicators>
        <!-- Existing indicators -->
        
        <indicator name="Ichimoku Cloud">
            <purpose>Identify support/resistance and trend</purpose>
            <interpretation>
                Price above cloud: Bullish
                Price below cloud: Bearish
                Price in cloud: Neutral/Consolidation
            </interpretation>
        </indicator>
    </indicators>
</phase>
```

#### 4. Document and Deploy

Follow steps 3-6 from "Modifying Technical Indicators" section.

---

## Updating Analysis Workflow

### When to Update Workflow

Update workflow when you need to:
- Add new analysis phases
- Modify decision logic
- Change quality checks
- Update examples

### Step-by-Step Procedure

#### 1. Identify Change Type

**Types of Changes**:
- **Phase Addition**: Add new phase (e.g., Phase 6: Fundamental Analysis)
- **Phase Modification**: Change existing phase logic
- **Decision Tree Update**: Modify decision logic
- **Quality Check Update**: Add/modify validation rules
- **Example Addition**: Add new analysis examples

#### 2. Update Workflow XML

**File**: `.bob/rules-financial-analyst/1_analysis_workflow.xml`

**Example: Add Phase 6 - Fundamental Analysis**

```xml
<phase id="6" name="Fundamental Analysis">
    <objective>
        Analyze company fundamentals to complement technical analysis
    </objective>
    
    <tools>
        <tool>fetch_company_fundamentals</tool>
    </tools>
    
    <steps>
        <step order="1">
            <action>Fetch P/E ratio</action>
            <interpretation>
                P/E < 15: Undervalued
                P/E 15-25: Fair value
                P/E > 25: Overvalued
            </interpretation>
        </step>
        
        <step order="2">
            <action>Analyze revenue growth</action>
            <interpretation>
                Growth > 20%: Strong
                Growth 10-20%: Moderate
                Growth < 10%: Weak
            </interpretation>
        </step>
        
        <step order="3">
            <action>Check debt-to-equity ratio</action>
            <interpretation>
                D/E < 0.5: Low debt
                D/E 0.5-1.0: Moderate debt
                D/E > 1.0: High debt
            </interpretation>
        </step>
    </steps>
    
    <output>
        <item>P/E ratio</item>
        <item>Revenue growth rate</item>
        <item>Debt-to-equity ratio</item>
        <item>Fundamental score (0-10)</item>
    </output>
    
    <quality_checks>
        <check>All fundamental metrics fetched</check>
        <check>Metrics are recent (< 3 months old)</check>
        <check>Fundamental score calculated</check>
    </quality_checks>
</phase>
```

#### 3. Update Mode Configuration

**File**: `.bob/custom_modes.yaml`

```yaml
financial-analyst:
  roleDefinition: |
    Your analysis follows a rigorous 6-phase framework:
    1. Data Collection
    2. Technical Analysis
    3. Scenario Planning
    4. Risk Assessment
    5. Investment Decision
    6. Fundamental Analysis  # Added
```

#### 4. Add Examples

**File**: `.bob/rules-financial-analyst/2_analysis_examples.xml`

```xml
<example id="8" type="fundamental_analysis">
    <ticker>AAPL</ticker>
    <scenario>Combining technical and fundamental analysis</scenario>
    
    <!-- Phases 1-5 as usual -->
    
    <phase6_fundamentals>
        <pe_ratio>28.5</pe_ratio>
        <interpretation>Slightly overvalued (> 25)</interpretation>
        
        <revenue_growth>15.2%</revenue_growth>
        <interpretation>Moderate growth (10-20%)</interpretation>
        
        <debt_to_equity>0.35</debt_to_equity>
        <interpretation>Low debt (< 0.5)</interpretation>
        
        <fundamental_score>7.5</fundamental_score>
        <interpretation>Good fundamentals despite high P/E</interpretation>
    </phase6_fundamentals>
    
    <combined_verdict>
        <technical_score>8.5</technical_score>
        <fundamental_score>7.5</fundamental_score>
        <combined_score>8.0</combined_score>
        <decision>BUY</decision>
        <rationale>
            Strong technical signals (8.5/10) supported by solid 
            fundamentals (7.5/10). High P/E is justified by strong 
            brand and low debt.
        </rationale>
    </combined_verdict>
</example>
```

#### 5. Update Documentation

**File**: `doc/financial-analyst-mode/03-workflow.md`

Add section for Phase 6:
```markdown
## Phase 6: Fundamental Analysis

### Objective
Analyze company fundamentals to complement technical analysis.

### Tools Used
- `fetch_company_fundamentals`

### Process
1. Fetch P/E ratio
2. Analyze revenue growth
3. Check debt-to-equity ratio
4. Calculate fundamental score

### Output
- P/E ratio with interpretation
- Revenue growth rate
- Debt-to-equity ratio
- Fundamental score (0-10)

### Quality Checks
- All metrics fetched successfully
- Metrics are recent (< 3 months)
- Fundamental score calculated
```

#### 6. Test Workflow

```bash
# Restart VS Code to reload Bob configuration

# Switch to Financial Analyst mode

# Test with real analysis
# Ask: "Analizează AAPL cu analiza fundamentală"

# Verify Bob follows all 6 phases
```

#### 7. Commit and Deploy

```bash
git add .bob/
git add doc/financial-analyst-mode/
git commit -m "feat: Add Phase 6 - Fundamental Analysis to workflow"
git push origin master
```

### Modifying Decision Logic

**Example: Update Trend Assessment Logic**

**File**: `.bob/rules-financial-analyst/1_analysis_workflow.xml`

**Current Logic**:
```xml
<decision_tree id="trend_assessment">
    <question>Is EMA50 > EMA200?</question>
    <yes>
        <result>Uptrend</result>
    </yes>
    <no>
        <result>Downtrend</result>
    </no>
</decision_tree>
```

**Updated Logic** (more nuanced):
```xml
<decision_tree id="trend_assessment">
    <question>Is EMA50 > EMA200?</question>
    <yes>
        <question>Is Price > EMA50?</question>
        <yes>
            <question>Is ADX > 25?</question>
            <yes>
                <result>Strong Uptrend</result>
                <confidence>High</confidence>
            </yes>
            <no>
                <result>Weak Uptrend</result>
                <confidence>Medium</confidence>
            </no>
        </yes>
        <no>
            <result>Uptrend but Price Below EMA50</result>
            <confidence>Low</confidence>
            <action>Wait for confirmation</action>
        </no>
    </yes>
    <no>
        <question>Is Price < EMA50?</question>
        <yes>
            <result>Downtrend</result>
            <confidence>High</confidence>
        </yes>
        <no>
            <result>Neutral/Consolidation</result>
            <confidence>Medium</confidence>
        </no>
    </no>
</decision_tree>
```

---

## Changing Bob Mode Behavior

### When to Change Mode Behavior

Change mode behavior when you need to:
- Modify analysis approach
- Add new capabilities
- Change tool permissions
- Update activation triggers

### Step-by-Step Procedure

#### 1. Update Mode Definition

**File**: `.bob/custom_modes.yaml`

**Example: Add Tool Permission**

```yaml
financial-analyst:
  slug: financial-analyst
  name: "📊 Financial Analyst"
  roleDefinition: |
    # ... existing role definition ...
  
  whenToUse: |
    # ... existing when to use ...
  
  groups:
    - slug: read
      allowed: true
    - slug: write      # Added: Allow file writing
      allowed: true
    - slug: mcp
      allowed: true
    - slug: command
      allowed: true
    - slug: browser    # Added: Allow browser actions
      allowed: true
```

#### 2. Update Workflow Instructions

**File**: `.bob/rules-financial-analyst/1_analysis_workflow.xml`

**Example: Add Browser Research Step**

```xml
<phase id="7" name="Market Research">
    <objective>
        Research market conditions and competitor analysis
    </objective>
    
    <tools>
        <tool>browser_action</tool>
    </tools>
    
    <steps>
        <step order="1">
            <action>Launch browser and navigate to Yahoo Finance</action>
            <tool>browser_action</tool>
            <parameters>
                <action>launch</action>
                <url>https://finance.yahoo.com</url>
            </parameters>
        </step>
        
        <step order="2">
            <action>Search for ticker and capture screenshot</action>
            <tool>browser_action</tool>
        </step>
    </steps>
</phase>
```

#### 3. Test Mode Changes

```bash
# Restart VS Code

# Switch to Financial Analyst mode

# Verify new permissions work
# Try: "Write analysis to file report.md"
# Try: "Open Yahoo Finance for AAPL"
```

#### 4. Document Changes

**File**: `doc/bob-configuration/custom-modes.md`

Update permissions section:
```markdown
### Tool Permissions

Financial Analyst mode has access to:
- ✅ **read**: Read files and directories
- ✅ **write**: Write files (NEW)
- ✅ **mcp**: Use MCP tools
- ✅ **command**: Execute commands
- ✅ **browser**: Browser actions (NEW)
```

---

## Adding New Tickers to Watchlist

### When to Add Tickers

Add tickers when you want to:
- Track new stocks
- Expand to new markets
- Monitor specific sectors

### Step-by-Step Procedure

#### 1. Locate Watchlist File

**File**: `fin/financial-analysis-mcp/data/watchlist.json`

#### 2. Add Ticker

**Current Watchlist**:
```json
{
  "tickers": [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA",
    "TLV", "SNG", "BRD",
    "SAP", "SIE", "ALV"
  ]
}
```

**Updated Watchlist**:
```json
{
  "tickers": [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META",
    "TLV", "SNG", "BRD", "FP",
    "SAP", "SIE", "ALV", "BMW"
  ]
}
```

#### 3. Validate Ticker Format

**US Stocks**: Simple ticker (e.g., "AAPL")
**Romanian Stocks**: Ticker (e.g., "TLV", "SNG")
**German Stocks**: Ticker (e.g., "SAP", "SIE")
**Special Cases**: 
- Berkshire Hathaway: "BRK-A" or "BRK-B"
- Class shares: Use hyphen (e.g., "GOOGL" for Class A)

#### 4. Test New Tickers

```bash
# Test locally
python -c "
from src.tools.watchlist import list_tickers
import asyncio
result = asyncio.run(list_tickers())
print(result)
"

# Test with MCP server
curl -X POST http://192.168.1.7:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "list_tickers"
    },
    "id": 1
  }'
```

#### 5. Commit and Deploy

```bash
git add fin/financial-analysis-mcp/data/watchlist.json
git commit -m "feat: Add TSLA, META, FP, BMW to watchlist"
git push origin master

# Deploy (watchlist is mounted as volume, so just restart container)
ssh user@192.168.1.7
docker restart financial-analysis-mcp
```

---

## Updating Dependencies

### When to Update Dependencies

Update dependencies when:
- Security vulnerabilities discovered
- New features needed
- Bug fixes available
- Performance improvements

### Step-by-Step Procedure

#### 1. Check Current Versions

**File**: `fin/financial-analysis-mcp/requirements.txt`

```txt
fastapi==0.104.1
uvicorn==0.24.0
yfinance==0.2.32
pandas==2.1.3
ta-lib==0.4.28
requests==2.31.0
```

#### 2. Update Requirements

**Option A: Update Specific Package**
```txt
fastapi==0.105.0  # Updated from 0.104.1
```

**Option B: Update All (use with caution)**
```bash
pip list --outdated
pip install --upgrade fastapi uvicorn yfinance pandas
pip freeze > requirements.txt
```

#### 3. Test Locally

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install updated dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Test server
uvicorn src.server:app --reload

# Test tools
python -c "
from src.tools.data_extraction import fetch_ticker_data
import asyncio
result = asyncio.run(fetch_ticker_data('AAPL'))
print(result)
"
```

#### 4. Update Docker

**File**: `fin/financial-analysis-mcp/Dockerfile`

No changes needed if using `requirements.txt`, but verify build:

```bash
docker build -t financial-analysis-mcp:test .
docker run -p 8000:8000 financial-analysis-mcp:test
```

#### 5. Commit and Deploy

```bash
git add requirements.txt
git commit -m "chore: Update dependencies (fastapi 0.104.1 -> 0.105.0)"
git push origin master

# GitHub Actions will build new image
# Then deploy manually (see deployment section)
```

### Handling Breaking Changes

If dependency update breaks code:

#### 1. Identify Breaking Changes

Check changelog:
```bash
# Example for FastAPI
https://github.com/tiangolo/fastapi/releases
```

#### 2. Update Code

**Example: FastAPI 0.104 → 0.105 Breaking Change**

**Old Code**:
```python
from fastapi import FastAPI
app = FastAPI()
```

**New Code** (if API changed):
```python
from fastapi import FastAPI
app = FastAPI(title="MCP Server", version="1.0")
```

#### 3. Test Thoroughly

```bash
pytest tests/ -v
docker-compose up --build
```

#### 4. Update Documentation

Document breaking changes in:
- `doc/ai-context/04-troubleshooting-history.md`
- `doc/mcp-server/05-development.md`

---

## Modifying Docker Configuration

### When to Modify Docker

Modify Docker when you need to:
- Change exposed ports
- Add volume mounts
- Update environment variables
- Optimize image size

### Step-by-Step Procedure

#### 1. Update Dockerfile

**File**: `fin/financial-analysis-mcp/Dockerfile`

**Example: Add Environment Variable**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Add environment variable
ENV LOG_LEVEL=INFO
ENV MAX_WORKERS=4

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY data/ ./data/

EXPOSE 8000

CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

#### 2. Update docker-compose.yml

**File**: `fin/financial-analysis-mcp/docker-compose.yml`

```yaml
version: '3.8'

services:
  mcp-server:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs  # Added
    environment:
      - LOG_LEVEL=DEBUG  # Added
      - MAX_WORKERS=4    # Added
    restart: unless-stopped
```

#### 3. Test Locally

```bash
docker-compose down
docker-compose up --build

# Verify changes
docker logs financial-analysis-mcp
```

#### 4. Update Deployment Script

**File**: `fin/financial-analysis-mcp/deploy.sh` (create if needed)

```bash
#!/bin/bash

# Pull latest image
docker pull ghcr.io/user/financial-analysis-mcp:latest

# Stop and remove old container
docker stop financial-analysis-mcp
docker rm financial-analysis-mcp

# Run new container with updated configuration
docker run -d \
  --name financial-analysis-mcp \
  --restart unless-stopped \
  -p 8000:8000 \
  -v /srv/dev-disk-by-uuid-xxx/financial-data:/app/data \
  -v /srv/dev-disk-by-uuid-xxx/financial-logs:/app/logs \
  -e LOG_LEVEL=INFO \
  -e MAX_WORKERS=4 \
  ghcr.io/user/financial-analysis-mcp:latest

echo "Deployment complete"
```

#### 5. Deploy

```bash
git add Dockerfile docker-compose.yml deploy.sh
git commit -m "feat: Add logging volume and environment variables"
git push origin master

# SSH to server
ssh user@192.168.1.7

# Run deployment script
bash deploy.sh
```

---

## Testing Changes

### Testing Levels

1. **Unit Tests**: Test individual functions
2. **Integration Tests**: Test tool interactions
3. **End-to-End Tests**: Test complete workflows
4. **Manual Tests**: Test with Bob

### Unit Testing

**File**: `fin/financial-analysis-mcp/tests/test_calculations.py`

```python
import pytest
from src.utils.calculations import calculate_rsi, calculate_macd

def test_calculate_rsi():
    """Test RSI calculation."""
    prices = [100, 102, 101, 103, 105, 104, 106, 108, 107, 109, 
              111, 110, 112, 114, 113]
    rsi = calculate_rsi(prices)
    
    assert 0 <= rsi <= 100
    assert isinstance(rsi, float)

def test_calculate_macd():
    """Test MACD calculation."""
    prices = [100] * 50  # 50 prices for MACD
    macd, signal, hist = calculate_macd(prices)
    
    assert isinstance(macd, float)
    assert isinstance(signal, float)
    assert isinstance(hist, float)
```

**Run Tests**:
```bash
pytest tests/test_calculations.py -v
```

### Integration Testing

**File**: `fin/financial-analysis-mcp/tests/test_integration.py`

```python
import pytest
from src.tools.data_extraction import fetch_ticker_data, calculate_all_indicators

@pytest.mark.asyncio
async def test_full_analysis_workflow():
    """Test complete analysis workflow."""
    ticker = "AAPL"
    
    # Step 1: Fetch data
    data = await fetch_ticker_data(ticker, period="6mo")
    assert data['ticker'] == ticker
    assert 'current_price' in data
    
    # Step 2: Calculate indicators
    indicators = await calculate_all_indicators(ticker)
    assert 'rsi' in indicators
    assert 'macd' in indicators
    assert 'ema50' in indicators
```

**Run Tests**:
```bash
pytest tests/test_integration.py -v
```

### End-to-End Testing

**File**: `C:/Users/O82652826/test-e2e.py`

```python
import requests
import json

def test_complete_analysis():
    """Test complete analysis via MCP server."""
    
    # Test 1: Fetch ticker data
    response = requests.post(
        "http://192.168.1.7:8000/mcp",
        json={
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "fetch_ticker_data",
                "arguments": {"ticker": "AAPL", "period": "6mo"}
            },
            "id": 1
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert 'result' in data
    
    # Test 2: Calculate indicators
    response = requests.post(
        "http://192.168.1.7:8000/mcp",
        json={
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "calculate_all_indicators",
                "arguments": {"ticker": "AAPL"}
            },
            "id": 2
        }
    )
    assert response.status_code == 200
    indicators = response.json()
    assert 'result' in indicators
    
    print("✅ All E2E tests passed")

if __name__ == "__main__":
    test_complete_analysis()
```

**Run Test**:
```bash
python C:/Users/O82652826/test-e2e.py
```

### Manual Testing with Bob

1. **Restart VS Code** to reload configuration
2. **Switch to Financial Analyst mode**
3. **Test analysis**: "Analizează AAPL"
4. **Verify**:
   - All 5 phases executed
   - All indicators calculated
   - Scenarios developed
   - Risk assessed
   - Clear verdict provided

---

## Deployment Procedures

### Standard Deployment

#### 1. Commit Changes

```bash
git add .
git commit -m "feat: Description of changes"
git push origin master
```

#### 2. Wait for GitHub Actions

Monitor build at: `https://github.com/user/repo/actions`

Verify:
- ✅ Build successful
- ✅ Tests passed
- ✅ Image pushed to GHCR

#### 3. Deploy to OMV Server

```bash
# SSH to server
ssh user@192.168.1.7

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

# Verify
docker ps
docker logs financial-analysis-mcp
```

#### 4. Test Deployment

```bash
# From Windows
curl http://192.168.1.7:8000/health

# Test with wrapper
python C:/Users/O82652826/test-mcp-tool.py list_tickers '{}'

# Test with Bob
# Ask: "List all tickers in watchlist"
```

### Emergency Deployment

For critical fixes:

```bash
# Build and push manually
docker build -t ghcr.io/user/financial-analysis-mcp:hotfix .
docker push ghcr.io/user/financial-analysis-mcp:hotfix

# Deploy hotfix
ssh user@192.168.1.7
docker pull ghcr.io/user/financial-analysis-mcp:hotfix
docker stop financial-analysis-mcp
docker rm financial-analysis-mcp
docker run -d \
  --name financial-analysis-mcp \
  --restart unless-stopped \
  -p 8000:8000 \
  -v /srv/dev-disk-by-uuid-xxx/financial-data:/app/data \
  ghcr.io/user/financial-analysis-mcp:hotfix
```

---

## Rollback Procedures

### When to Rollback

Rollback when:
- New deployment breaks functionality
- Critical bugs discovered
- Performance degradation
- Data corruption

### Step-by-Step Rollback

#### 1. Identify Last Good Version

```bash
# Check GitHub releases
https://github.com/user/repo/releases

# Or check GHCR tags
docker pull ghcr.io/user/financial-analysis-mcp:v1.0.0
```

#### 2. Deploy Previous Version

```bash
# SSH to server
ssh user@192.168.1.7

# Stop current container
docker stop financial-analysis-mcp
docker rm financial-analysis-mcp

# Run previous version
docker run -d \
  --name financial-analysis-mcp \
  --restart unless-stopped \
  -p 8000:8000 \
  -v /srv/dev-disk-by-uuid-xxx/financial-data:/app/data \
  ghcr.io/user/financial-analysis-mcp:v1.0.0  # Previous version

# Verify
docker logs financial-analysis-mcp
```

#### 3. Test Rollback

```bash
# Test basic functionality
curl http://192.168.1.7:8000/health

# Test tools
python C:/Users/O82652826/test-mcp-tool.py list_tickers '{}'

# Test with Bob
# Ask: "Analizează AAPL"
```

#### 4. Investigate Issue

```bash
# Check logs
docker logs financial-analysis-mcp --tail 100

# Check GitHub Actions
https://github.com/user/repo/actions

# Review recent commits
git log --oneline -10
```

#### 5. Fix and Redeploy

```bash
# Fix issue
git revert <bad-commit-hash>
# or
git commit -m "fix: Description of fix"

# Push fix
git push origin master

# Wait for GitHub Actions
# Deploy fixed version (see deployment section)
```

---

## Best Practices

### General Guidelines

1. **Test Locally First**: Always test changes locally before deploying
2. **Small Changes**: Make small, incremental changes
3. **Document Everything**: Update docs with every change
4. **Version Control**: Commit frequently with clear messages
5. **Backup Data**: Backup watchlist and logs before major changes

### Code Quality

1. **Type Hints**: Use type hints for all functions
2. **Error Handling**: Handle errors gracefully
3. **Logging**: Add logging for debugging
4. **Comments**: Comment complex logic
5. **Tests**: Write tests for new features

### Deployment Safety

1. **Check GitHub Actions**: Verify build success
2. **Test in Staging**: Test with docker-compose first
3. **Monitor Logs**: Watch logs after deployment
4. **Have Rollback Plan**: Know how to rollback
5. **Communicate**: Inform users of downtime

---

## Related Documentation

- [Project Overview](01-project-overview.md)
- [Technical Decisions](02-technical-decisions.md)
- [Troubleshooting History](04-troubleshooting-history.md)
- [MCP Server Development](../mcp-server/05-development.md)
- [Financial Analyst Mode Configuration](../financial-analyst-mode/02-configuration.md)

---

## Summary

This guide provides procedures for:
- ✅ Adding new MCP tools
- ✅ Modifying technical indicators
- ✅ Updating analysis workflow
- ✅ Changing Bob mode behavior
- ✅ Managing watchlist
- ✅ Updating dependencies
- ✅ Modifying Docker configuration
- ✅ Testing changes
- ✅ Deploying safely
- ✅ Rolling back when needed

**Key Principles**:
1. Test locally before deploying
2. Make small, incremental changes
3. Document everything
4. Have rollback plan
5. Monitor after deployment

**Remember**: Safety first, speed second. Better to deploy slowly and correctly than quickly and break things.