# Troubleshooting History

## Overview

This document records all significant issues encountered during the project, their solutions, and lessons learned. Use this as a reference when encountering similar problems.

## Table of Contents

1. [MCP stdio Compatibility Issues](#mcp-stdio-compatibility-issues)
2. [DataFrame Serialization Errors](#dataframe-serialization-errors)
3. [GitHub Actions Workflow Problems](#github-actions-workflow-problems)
4. [DataFrame MultiIndex Handling](#dataframe-multiindex-handling)
5. [Bob Configuration Conflicts](#bob-configuration-conflicts)
6. [Docker Build Failures](#docker-build-failures)
7. [yfinance Data Issues](#yfinance-data-issues)
8. [Performance Problems](#performance-problems)

---

## MCP stdio Compatibility Issues

### Issue #1: Bob Cannot Connect via SSH + Docker exec

**Date**: 2026-05-17  
**Severity**: Critical  
**Status**: ✅ Resolved

#### Problem Description

Bob (VS Code) could not connect to MCP server running in Docker container on remote server (192.168.1.7) using stdio transport.

**Error Message**:
```
MCP error -32000: Connection closed
Server process exited with code null
```

**Configuration Attempted**:
```json
{
  "mcpServers": {
    "financial-analysis": {
      "command": "ssh",
      "args": [
        "user@192.168.1.7",
        "docker",
        "exec",
        "-i",
        "financial-analysis-mcp",
        "python",
        "-m",
        "src.server"
      ]
    }
  }
}
```

#### Root Cause

1. **stdio Stream Forwarding**: SSH doesn't properly forward stdio streams through Docker exec
2. **Docker exec Limitations**: Docker exec with `-i` flag has issues with bidirectional stdio
3. **MCP Protocol Requirements**: MCP requires reliable bidirectional communication

#### Investigation Steps

1. **Tested SSH Connection**:
   ```bash
   ssh user@192.168.1.7 echo "test"
   # ✅ Works
   ```

2. **Tested Docker exec**:
   ```bash
   ssh user@192.168.1.7 docker exec -i financial-analysis-mcp echo "test"
   # ✅ Works
   ```

3. **Tested MCP Server Directly**:
   ```bash
   ssh user@192.168.1.7 docker exec -i financial-analysis-mcp python -m src.server
   # ❌ Hangs, no response
   ```

4. **Checked Docker Logs**:
   ```bash
   docker logs financial-analysis-mcp
   # No errors, server running fine
   ```

#### Solution

**Implemented HTTP Transport with stdio Wrapper**:

1. **Changed MCP Server to HTTP**:
   - Implemented FastAPI HTTP server
   - Exposed port 8000
   - Kept MCP protocol (JSON-RPC 2.0)

2. **Created stdio-to-HTTP Wrapper**:
   - Python script on Windows
   - Reads stdio from Bob
   - Forwards to HTTP server
   - Returns responses to Bob

**Architecture**:
```
Bob (stdio) → Wrapper (stdio→HTTP) → MCP Server (HTTP)
```

**Wrapper Code** (`C:/Users/O82652826/financial-analysis-mcp-wrapper.py`):
```python
import sys
import json
import requests

MCP_SERVER_URL = "http://192.168.1.7:8000/mcp"

def main():
    for line in sys.stdin:
        request = json.loads(line.strip())
        response = requests.post(MCP_SERVER_URL, json=request, timeout=30)
        print(json.dumps(response.json()))
        sys.stdout.flush()

if __name__ == "__main__":
    main()
```

**Bob Configuration**:
```json
{
  "mcpServers": {
    "financial-analysis": {
      "command": "python",
      "args": ["C:/Users/O82652826/financial-analysis-mcp-wrapper.py"]
    }
  }
}
```

#### Lessons Learned

1. **stdio Limitations**: stdio transport not suitable for remote/containerized services
2. **HTTP Reliability**: HTTP is more reliable for network communication
3. **Wrapper Pattern**: Effective for protocol bridging
4. **Test Early**: Test with actual clients early in development

#### Prevention

- Use HTTP transport for remote services
- Use stdio only for local processes
- Document transport limitations
- Provide wrapper for stdio clients

---

## DataFrame Serialization Errors

### Issue #2: Pydantic Cannot Serialize pandas DataFrame

**Date**: 2026-05-19  
**Severity**: High  
**Status**: ✅ Resolved

#### Problem Description

When calling `fetch_ticker_data` tool, FastAPI/Pydantic threw serialization error.

**Error Message**:
```
pydantic_core._pydantic_core.PydanticSerializationError: 
Unable to serialize unknown type: <class 'pandas.core.frame.DataFrame'>
```

**Stack Trace**:
```python
File "src/tools/data_extraction.py", line 105
    return {
        'ticker': ticker.upper(),
        'period': period,
        'current_price': current_price,
        'dataframe': df  # ❌ This causes error
    }
```

#### Root Cause

FastAPI uses Pydantic for JSON serialization. Pydantic cannot serialize pandas DataFrame objects directly because:
1. DataFrame is a complex Python object
2. Not a standard JSON type
3. Contains numpy arrays internally

#### Investigation Steps

1. **Reproduced Error**:
   ```bash
   # Test with Bob
   "Analizează TLV"
   # Error occurred
   ```

2. **Checked Logs**:
   ```bash
   docker logs financial-analysis-mcp
   # Showed Pydantic serialization error
   ```

3. **Identified Problem Line**:
   ```python
   # Line 105 in data_extraction.py
   'dataframe': df  # This is the problem
   ```

#### Solution

**Removed DataFrame from Return Dictionary**:

**Before**:
```python
return {
    'ticker': ticker.upper(),
    'period': period,
    'current_price': current_price,
    'dataframe': df,  # ❌ Cannot serialize
    'data_points': len(df)
}
```

**After**:
```python
return {
    'ticker': ticker.upper(),
    'period': period,
    'current_price': current_price,
    # 'dataframe': df,  # ❌ Removed
    'data_points': len(df)
}
```

**Commit**: `a2713e4 - DataFrame ce nu poate fi serializat în JSON de către FastAPI/Pydantic`

#### Alternative Solutions Considered

1. **Convert to Dict**:
   ```python
   'dataframe': df.to_dict('records')  # ✅ Works but large
   ```

2. **Convert to JSON String**:
   ```python
   'dataframe': df.to_json()  # ✅ Works but needs parsing
   ```

3. **Return Only Needed Data**:
   ```python
   'prices': df['Close'].tolist()  # ✅ Best for specific needs
   ```

#### Lessons Learned

1. **Pydantic Limitations**: Cannot serialize complex Python objects
2. **Return Only Needed Data**: Don't return entire DataFrames
3. **Test Serialization**: Test JSON serialization early
4. **Use Simple Types**: Stick to dict, list, str, int, float, bool

#### Prevention

- Never return pandas DataFrames in MCP tools
- Convert to dict/list before returning
- Test serialization with FastAPI
- Document serialization requirements

---

## GitHub Actions Workflow Problems

### Issue #3: Workflow Not Triggering on Push to master

**Date**: 2026-05-19  
**Severity**: Medium  
**Status**: ✅ Resolved

#### Problem Description

GitHub Actions workflow not triggering when pushing to `master` branch.

**Workflow Configuration**:
```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [main]  # ❌ Only triggers on 'main'
```

**Repository Branch**: `master` (not `main`)

#### Root Cause

Workflow configured to trigger only on `main` branch, but repository uses `master` branch.

#### Investigation Steps

1. **Checked GitHub Actions**:
   ```
   No workflows triggered after push
   ```

2. **Checked Workflow File**:
   ```yaml
   on:
     push:
       branches: [main]  # Problem found
   ```

3. **Checked Repository Branch**:
   ```bash
   git branch
   # * master
   ```

#### Solution

**Updated Workflow to Include Both Branches**:

**Before**:
```yaml
on:
  push:
    branches: [main]
```

**After**:
```yaml
on:
  push:
    branches: [main, master]  # ✅ Supports both
```

**Commit**: `85864ba - Fix: Add master branch to CI/CD workflow triggers`

#### Lessons Learned

1. **Branch Names Matter**: Verify actual branch name
2. **Support Both**: Support both `main` and `master` for compatibility
3. **Test CI/CD**: Test workflow after setup
4. **Check Logs**: GitHub Actions logs show trigger conditions

#### Prevention

- Always check repository branch name
- Support both `main` and `master` in workflows
- Test CI/CD pipeline after setup
- Document branch naming conventions

---

## DataFrame MultiIndex Handling

### Issue #4: AttributeError on MultiIndex DataFrame

**Date**: 2026-05-17  
**Severity**: High  
**Status**: ✅ Resolved

#### Problem Description

Some tickers (e.g., Romanian stocks) returned DataFrames with MultiIndex columns, causing `.tolist()` AttributeError.

**Error Message**:
```python
AttributeError: 'MultiIndex' object has no attribute 'tolist'
```

**Affected Tickers**: TLV, SNG, BRD (Romanian stocks)

#### Root Cause

yfinance sometimes returns DataFrames with MultiIndex columns:
```python
# Normal columns
['Open', 'High', 'Low', 'Close', 'Volume']

# MultiIndex columns
[('Open', 'TLV'), ('High', 'TLV'), ('Low', 'TLV'), ...]
```

Code assumed simple column names:
```python
columns = df.columns.tolist()  # ❌ Fails for MultiIndex
```

#### Investigation Steps

1. **Reproduced Error**:
   ```python
   df = yf.Ticker("TLV").history(period="6mo")
   print(df.columns)
   # MultiIndex([('Open', 'TLV'), ('High', 'TLV'), ...])
   ```

2. **Tested Fix**:
   ```python
   if isinstance(df.columns, pd.MultiIndex):
       df.columns = ['_'.join(col).strip() for col in df.columns.values]
   ```

#### Solution

**Added MultiIndex Detection and Flattening**:

```python
def fetch_ticker_data(ticker: str, period: str = "6mo") -> Dict[str, Any]:
    """Fetch historical data with MultiIndex handling."""
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    
    # Handle MultiIndex columns
    if isinstance(df.columns, pd.MultiIndex):
        # Flatten MultiIndex: ('Open', 'TLV') -> 'Open_TLV'
        df.columns = ['_'.join(col).strip() for col in df.columns.values]
    
    # Now safe to use .tolist()
    columns = df.columns.tolist()
    
    return {
        'ticker': ticker.upper(),
        'columns': columns,
        'data': df.to_dict('records')
    }
```

#### Lessons Learned

1. **Check Column Type**: Always check if columns are MultiIndex
2. **Flatten MultiIndex**: Flatten before processing
3. **Test International Stocks**: Different markets may have different formats
4. **Defensive Programming**: Handle edge cases

#### Prevention

- Always check for MultiIndex before using `.tolist()`
- Test with international tickers
- Add type checks for DataFrame columns
- Document known edge cases

---

## Bob Configuration Conflicts

### Issue #5: mcp.json vs mcp_settings.json Conflict

**Date**: 2026-05-17  
**Severity**: Medium  
**Status**: ✅ Resolved

#### Problem Description

Bob showed "MCP server not configured" despite having configuration in `mcp.json`.

**Files**:
- `.bob/mcp.json`: SSH-based configuration
- `mcp_settings.json`: Local wrapper configuration

#### Root Cause

Bob reads `mcp_settings.json` first, which had old SSH configuration. The `.bob/mcp.json` was ignored.

#### Investigation Steps

1. **Checked Both Files**:
   ```bash
   cat .bob/mcp.json
   # SSH configuration
   
   cat mcp_settings.json
   # Old SSH configuration
   ```

2. **Tested Priority**:
   ```
   mcp_settings.json takes precedence over .bob/mcp.json
   ```

#### Solution

**Updated mcp_settings.json with Wrapper Configuration**:

```json
{
  "mcpServers": {
    "financial-analysis": {
      "command": "python",
      "args": ["C:/Users/O82652826/financial-analysis-mcp-wrapper.py"]
    }
  }
}
```

**Removed SSH Configuration from .bob/mcp.json**

#### Lessons Learned

1. **Configuration Priority**: `mcp_settings.json` > `.bob/mcp.json`
2. **Single Source of Truth**: Keep configuration in one place
3. **Document Priority**: Document which file takes precedence
4. **Clean Up Old Config**: Remove obsolete configurations

#### Prevention

- Use only one configuration file
- Document configuration file priority
- Remove old configurations
- Test configuration changes

---

## Docker Build Failures

### Issue #6: Missing Dependencies in requirements.txt

**Date**: 2026-05-16  
**Severity**: High  
**Status**: ✅ Resolved

#### Problem Description

Docker build failed due to missing dependencies.

**Error Message**:
```
ERROR: Could not find a version that satisfies the requirement ta-lib
```

#### Root Cause

`requirements.txt` had incorrect package name for TA-Lib.

**Incorrect**:
```txt
ta-lib==0.4.28
```

**Correct**:
```txt
TA-Lib==0.4.28
```

#### Solution

**Fixed Package Names**:
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
yfinance==0.2.32
pandas==2.1.3
TA-Lib==0.4.28  # ✅ Correct capitalization
requests==2.31.0
python-multipart==0.0.6
```

**Added System Dependencies to Dockerfile**:
```dockerfile
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install TA-Lib C library
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib ta-lib-0.4.0-src.tar.gz
```

#### Lessons Learned

1. **Package Names**: Case-sensitive package names
2. **System Dependencies**: Some Python packages need system libraries
3. **Test Builds**: Test Docker builds locally
4. **Document Dependencies**: Document system dependencies

#### Prevention

- Verify package names on PyPI
- Test Docker builds locally
- Document system dependencies
- Use multi-stage builds to reduce image size

---

## yfinance Data Issues

### Issue #7: Missing Data for Some Dates

**Date**: Ongoing  
**Severity**: Low  
**Status**: ⚠️ Known Limitation

#### Problem Description

Some dates missing from historical data (holidays, trading halts).

**Example**:
```python
df = yf.Ticker("AAPL").history(period="1mo")
# Missing: 2026-05-18 (holiday)
```

#### Root Cause

Yahoo Finance doesn't provide data for:
- Market holidays
- Trading halts
- Weekends
- Pre-market/after-hours (unless specifically requested)

#### Current Handling

**Forward Fill Missing Values**:
```python
df = df.fillna(method='ffill')
```

#### Impact

Minimal for medium-term analysis (3-12 months). Missing 1-2 days doesn't significantly affect:
- EMA calculations
- RSI calculations
- MACD calculations

#### Lessons Learned

1. **Data Gaps Normal**: Missing data is expected
2. **Forward Fill**: Acceptable solution for technical analysis
3. **Document Limitations**: Inform users of data limitations
4. **Check Data Quality**: Always validate data before analysis

#### Prevention

- Document data limitations
- Use forward fill for missing values
- Validate data quality
- Consider paid data sources for real-time needs

---

## Performance Problems

### Issue #8: Slow Analysis for Multiple Tickers

**Date**: 2026-05-18  
**Severity**: Low  
**Status**: ⚠️ Optimization Opportunity

#### Problem Description

Analyzing multiple tickers sequentially is slow.

**Current Performance**:
- Single ticker: 2-3 seconds
- 5 tickers: 10-15 seconds
- 10 tickers: 20-30 seconds

#### Root Cause

Sequential processing:
```python
for ticker in tickers:
    result = await analyze_ticker(ticker)  # One at a time
```

#### Potential Solutions

**1. Parallel Processing**:
```python
import asyncio

async def analyze_multiple(tickers):
    tasks = [analyze_ticker(t) for t in tickers]
    results = await asyncio.gather(*tasks)
    return results
```

**2. Caching**:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_ticker_data(ticker, period):
    return yf.Ticker(ticker).history(period=period)
```

**3. Batch API Calls**:
```python
# yfinance supports multiple tickers
data = yf.download(tickers, period="6mo", group_by='ticker')
```

#### Current Status

Not implemented yet. Performance acceptable for current use case (1-2 tickers at a time).

#### Lessons Learned

1. **Optimize When Needed**: Don't optimize prematurely
2. **Measure First**: Measure performance before optimizing
3. **Consider Trade-offs**: Parallel processing adds complexity
4. **Cache Wisely**: Cache can help but needs invalidation strategy

#### Future Work

- Implement parallel processing for multiple tickers
- Add caching layer
- Optimize indicator calculations
- Consider batch API calls

---

## Summary

### Issues by Category

**Critical (Resolved)**:
- ✅ MCP stdio compatibility
- ✅ DataFrame serialization

**High (Resolved)**:
- ✅ DataFrame MultiIndex handling
- ✅ Docker build failures

**Medium (Resolved)**:
- ✅ GitHub Actions workflow
- ✅ Bob configuration conflicts

**Low (Known Limitations)**:
- ⚠️ yfinance data gaps
- ⚠️ Performance optimization

### Key Lessons

1. **Test Early**: Test with actual clients and data early
2. **Handle Edge Cases**: International stocks, MultiIndex, etc.
3. **Document Limitations**: Be clear about what doesn't work
4. **Simple Solutions**: HTTP wrapper simpler than fixing stdio
5. **Defensive Programming**: Check types, handle errors
6. **Configuration Management**: Single source of truth
7. **Performance**: Optimize when needed, not prematurely

### Prevention Checklist

Before deploying changes:
- [ ] Test with multiple tickers (US, Romanian, German)
- [ ] Test serialization (no DataFrames in returns)
- [ ] Test Docker build locally
- [ ] Verify GitHub Actions triggers
- [ ] Check configuration files
- [ ] Test with Bob
- [ ] Monitor logs after deployment
- [ ] Have rollback plan ready

### Related Documentation

- [Project Overview](01-project-overview.md)
- [Technical Decisions](02-technical-decisions.md)
- [Modification Guide](03-modification-guide.md)
- [MCP Server Troubleshooting](../mcp-server/04-troubleshooting.md)

---

## Reporting New Issues

When encountering new issues:

1. **Document the Problem**:
   - Error message
   - Steps to reproduce
   - Expected vs actual behavior

2. **Investigate**:
   - Check logs
   - Test in isolation
   - Identify root cause

3. **Implement Solution**:
   - Fix the issue
   - Test thoroughly
   - Document the fix

4. **Update This Document**:
   - Add new issue section
   - Include solution
   - Document lessons learned

5. **Prevent Recurrence**:
   - Add tests
   - Update documentation
   - Improve error handling

**Template for New Issues**:
```markdown
### Issue #X: Brief Description

**Date**: YYYY-MM-DD
**Severity**: Critical/High/Medium/Low
**Status**: ✅ Resolved / ⚠️ Known Limitation / 🔄 In Progress

#### Problem Description
[Detailed description]

#### Root Cause
[Why it happened]

#### Solution
[How it was fixed]

#### Lessons Learned
[What we learned]

#### Prevention
[How to avoid in future]
```

---

**Remember**: Every issue is a learning opportunity. Document thoroughly so others (including future AI assistants) can learn from your experience.