# MCP Server Troubleshooting Guide

Common issues and solutions for the Financial Analysis MCP Server.

## Quick Diagnostics

### Health Check Script
```bash
#!/bin/bash
echo "=== Financial Analysis MCP Server Health Check ==="

# 1. Check if container is running
echo -e "\n1. Container Status:"
docker ps | grep financial-analysis-mcp

# 2. Check port
echo -e "\n2. Port 8000 Status:"
sudo netstat -tulpn | grep 8000

# 3. Test endpoint
echo -e "\n3. API Endpoint Test:"
curl -s http://192.168.1.7:8000/tools/list | jq '.tools | length'

# 4. Check logs for errors
echo -e "\n4. Recent Errors:"
docker logs financial-analysis-mcp 2>&1 | grep -i error | tail -5

# 5. Resource usage
echo -e "\n5. Resource Usage:"
docker stats financial-analysis-mcp --no-stream
```

---

## Connection Issues

### Problem: Bob Cannot Connect to MCP Server

**Symptoms**:
- Red status indicator in Bob
- "Connection closed" errors
- "MCP error -32000" messages

**Diagnosis**:
```powershell
# Test from Windows
ping 192.168.1.7
curl http://192.168.1.7:8000/tools/list

# Test wrapper
python C:\Users\O82652826\financial-analysis-mcp-wrapper.py
# Input: {"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}
```

**Solutions**:

1. **Check server is running**:
```bash
ssh tommy@192.168.1.7
docker ps | grep financial-analysis-mcp
```

2. **Check firewall**:
```bash
sudo ufw status
sudo ufw allow 8000/tcp
```

3. **Verify wrapper configuration**:
```python
# In financial-analysis-mcp-wrapper.py
MCP_SERVER_URL = "http://192.168.1.7:8000"  # Correct URL
```

4. **Check Bob configuration**:
```json
// mcp_settings.json
{
  "mcpServers": {
    "financial-analysis": {
      "command": "python",
      "args": ["C:\\Users\\O82652826\\financial-analysis-mcp-wrapper.py"]
    }
  }
}
```

5. **Restart everything**:
```bash
# Restart server
ssh tommy@192.168.1.7 "docker-compose -f ~/financial-analysis-mcp/docker-compose.yml restart"

# Restart Bob
# Close and reopen Bob application
```

---

### Problem: Wrapper Not Working

**Symptoms**:
- Python errors when starting wrapper
- "Module not found" errors
- Timeout errors

**Diagnosis**:
```powershell
# Check Python version
python --version  # Should be 3.8+

# Check requests module
python -c "import requests; print(requests.__version__)"

# Test wrapper manually
python C:\Users\O82652826\financial-analysis-mcp-wrapper.py
```

**Solutions**:

1. **Install missing dependencies**:
```powershell
pip install requests
```

2. **Check Python path in Bob config**:
```json
{
  "mcpServers": {
    "financial-analysis": {
      "command": "python",  // or "python3" or full path
      "args": ["C:\\Users\\O82652826\\financial-analysis-mcp-wrapper.py"]
    }
  }
}
```

3. **Use full Python path**:
```json
{
  "command": "C:\\Python311\\python.exe",
  "args": ["C:\\Users\\O82652826\\financial-analysis-mcp-wrapper.py"]
}
```

---

## Data Issues

### Problem: Ticker Not Found

**Symptoms**:
- "Ticker XXX not found" error
- Empty data returned
- yfinance errors

**Diagnosis**:
```python
import yfinance as yf

# Test ticker directly
ticker = yf.Ticker("TLV")
print(ticker.info)  # Check if data exists

# Try with market suffix
ticker = yf.Ticker("TLV.RO")
print(ticker.info)
```

**Solutions**:

1. **Add market suffix**:
```
TLV → TLV.RO (Romania)
SAP → SAP.DE (Germany)
AAPL → AAPL (US - no suffix needed)
```

2. **Verify ticker exists**:
- Check Yahoo Finance website
- Search for correct ticker symbol
- Verify market is supported

3. **Add to watchlist**:
```json
{
  "name": "add_ticker",
  "arguments": {"ticker": "TLV.RO"}
}
```

---

### Problem: Insufficient Data for Indicators

**Symptoms**:
- "Not enough data" errors
- NaN values in indicators
- Calculation errors

**Diagnosis**:
```python
# Check data availability
import yfinance as yf
ticker = yf.Ticker("TLV.RO")
hist = ticker.history(period="6mo")
print(f"Data points: {len(hist)}")  # Should be 120+ for 6mo daily
```

**Solutions**:

1. **Use longer period**:
```json
{
  "name": "calculate_all_indicators",
  "arguments": {
    "ticker": "TLV.RO",
    "period": "1y"  // Instead of "1mo"
  }
}
```

2. **Check trading days**:
- New IPOs may have limited history
- Delisted stocks have no recent data
- Market holidays reduce data points

3. **Minimum requirements**:
- RSI: 14+ days
- MACD: 26+ days
- EMA200: 200+ days
- Recommended: 6mo (120+ trading days)

---

### Problem: Pydantic Serialization Error

**Symptoms**:
- "Unable to serialize unknown type" error
- HTTP 500 errors
- DataFrame serialization errors

**Diagnosis**:
```bash
# Check server logs
docker logs financial-analysis-mcp | grep -i "pydantic"
```

**Solution**:
This was fixed in commit a2713e4. If you see this error:

1. **Update to latest version**:
```bash
ssh tommy@192.168.1.7
cd ~/financial-analysis-mcp
docker-compose pull
docker-compose up -d
```

2. **Verify fix in code** (`src/tools/data_extraction.py`):
```python
# ❌ WRONG - Don't return DataFrame
return {
    'data': data_dict,
    'dataframe': df  # This causes error!
}

# ✅ CORRECT - Only JSON-serializable data
return {
    'data': data_dict
}
```

---

## Performance Issues

### Problem: Slow Response Times

**Symptoms**:
- Requests take >10 seconds
- Timeouts
- Bob shows "thinking" for long time

**Diagnosis**:
```bash
# Check server resources
docker stats financial-analysis-mcp

# Check network latency
ping 192.168.1.7

# Test API directly
time curl http://192.168.1.7:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"get_current_price","arguments":{"ticker":"AAPL"}}'
```

**Solutions**:

1. **Increase Docker resources**:
```yaml
# docker-compose.yml
services:
  financial-analysis-mcp:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

2. **Check Yahoo Finance API**:
- May be rate limited
- Network issues
- API downtime

3. **Optimize requests**:
- Use shorter periods when possible
- Avoid parallel requests for same ticker
- Cache results in Bob conversation

---

### Problem: High Memory Usage

**Symptoms**:
- Container using >1GB RAM
- OOM (Out of Memory) errors
- Server crashes

**Diagnosis**:
```bash
docker stats financial-analysis-mcp
```

**Solutions**:

1. **Set memory limits**:
```yaml
# docker-compose.yml
services:
  financial-analysis-mcp:
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
```

2. **Restart container periodically**:
```bash
# Add to crontab
0 3 * * * docker-compose -f ~/financial-analysis-mcp/docker-compose.yml restart
```

3. **Check for memory leaks**:
```bash
# Monitor over time
watch -n 5 'docker stats financial-analysis-mcp --no-stream'
```

---

## Docker Issues

### Problem: Container Won't Start

**Symptoms**:
- Container exits immediately
- "Error starting userland proxy" messages
- Port binding errors

**Diagnosis**:
```bash
# Check logs
docker logs financial-analysis-mcp

# Check port usage
sudo netstat -tulpn | grep 8000

# Check Docker status
sudo systemctl status docker
```

**Solutions**:

1. **Port already in use**:
```bash
# Find process using port 8000
sudo lsof -i :8000

# Kill process or change port
# In docker-compose.yml: "8001:8000"
```

2. **Permission issues**:
```bash
sudo chown -R tommy:tommy ~/financial-analysis-mcp
sudo chmod -R 755 ~/financial-analysis-mcp
```

3. **Docker daemon not running**:
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

4. **Image pull failed**:
```bash
# Manual pull
docker pull ghcr.io/tommypopescu/financial-analysis-mcp:latest

# Check credentials if private
docker login ghcr.io
```

---

### Problem: Container Keeps Restarting

**Symptoms**:
- Container status shows "Restarting"
- Logs show repeated startup attempts
- Application crashes

**Diagnosis**:
```bash
# Check restart count
docker ps -a | grep financial-analysis-mcp

# Check logs for errors
docker logs financial-analysis-mcp --tail 100
```

**Solutions**:

1. **Check application errors**:
```bash
# Look for Python tracebacks
docker logs financial-analysis-mcp 2>&1 | grep -A 10 "Traceback"
```

2. **Verify dependencies**:
```bash
# Rebuild image
docker-compose build --no-cache
docker-compose up -d
```

3. **Check environment variables**:
```bash
# Verify .env file
cat ~/financial-analysis-mcp/.env
```

4. **Disable auto-restart temporarily**:
```yaml
# docker-compose.yml
services:
  financial-analysis-mcp:
    restart: "no"  # For debugging
```

---

## API Errors

### Problem: HTTP 500 Internal Server Error

**Symptoms**:
- API returns 500 status code
- "Internal Server Error" message
- Server logs show exceptions

**Diagnosis**:
```bash
# Check recent errors
docker logs financial-analysis-mcp | grep -i "error" | tail -20

# Test specific endpoint
curl -v http://192.168.1.7:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"get_current_price","arguments":{"ticker":"AAPL"}}'
```

**Solutions**:

1. **Check server logs**:
```bash
docker logs financial-analysis-mcp -f
```

2. **Verify request format**:
```json
// Correct format
{
  "name": "tool_name",
  "arguments": {...}
}

// Wrong format
{
  "tool": "tool_name",  // Should be "name"
  "params": {...}       // Should be "arguments"
}
```

3. **Update to latest version**:
```bash
docker-compose pull
docker-compose up -d
```

---

### Problem: HTTP 404 Not Found

**Symptoms**:
- API returns 404 status code
- "Not Found" message
- Wrong endpoint

**Solutions**:

1. **Verify endpoint**:
```bash
# Correct endpoints
POST /tools/list
POST /tools/call
POST /resources/list
POST /resources/read

# Wrong endpoints
GET /tools/list  # Should be POST
POST /tool/call  # Should be /tools/call
```

2. **Check server is running**:
```bash
curl http://192.168.1.7:8000/
# Should return FastAPI welcome message
```

---

## Yahoo Finance API Issues

### Problem: Rate Limit Exceeded

**Symptoms**:
- "Too many requests" errors
- 429 status codes
- Temporary data unavailability

**Solutions**:

1. **Wait and retry**:
```python
# Exponential backoff
import time
for i in range(3):
    try:
        data = fetch_ticker_data(ticker)
        break
    except RateLimitError:
        time.sleep(2 ** i)
```

2. **Reduce request frequency**:
- Cache results in Bob conversation
- Use longer periods (less frequent updates)
- Batch ticker analysis

3. **Use different IP** (if persistent):
- VPN
- Different network
- Wait 1 hour for reset

---

### Problem: Market Data Delayed

**Symptoms**:
- Prices seem outdated
- Volume data missing
- Timestamp in past

**Solutions**:

1. **Check market hours**:
- US: 9:30 AM - 4:00 PM ET
- Romania: 10:00 AM - 6:00 PM EET
- Germany: 9:00 AM - 5:30 PM CET

2. **Understand data delays**:
- Real-time data requires subscription
- Free data has 15-20 minute delay
- After-hours data may be limited

3. **Use appropriate period**:
```json
{
  "period": "1d",      // For intraday
  "interval": "1m"     // 1-minute bars
}
```

---

## Bob Integration Issues

### Problem: Financial Analyst Mode Not Available

**Symptoms**:
- Mode not in mode list
- `/mode financial-analyst` doesn't work
- Mode configuration not loaded

**Solutions**:

1. **Verify configuration file**:
```yaml
# .bob/custom_modes.yaml
- slug: financial-analyst
  name: 📊 Financial Analyst
  roleDefinition: |
    ...
```

2. **Check file location**:
```
C:\Users\O82652826\.git\.bob\custom_modes.yaml
```

3. **Restart Bob**:
- Close Bob completely
- Reopen Bob
- Check mode list

4. **Verify rules directory**:
```
C:\Users\O82652826\.git\.bob\rules-financial-analyst\
  ├── 1_analysis_workflow.xml
  └── 2_analysis_examples.xml
```

---

### Problem: MCP Tools Not Working in Mode

**Symptoms**:
- Mode loads but tools fail
- "Tool not found" errors
- MCP server disconnected

**Solutions**:

1. **Check MCP server status**:
- Green indicator = connected
- Red indicator = disconnected

2. **Verify mode has MCP access**:
```yaml
# custom_modes.yaml
groups:
  - read
  - mcp      # Required for MCP tools
  - command
```

3. **Test tools manually**:
```
/mode financial-analyst
list tickers
```

4. **Check wrapper logs**:
```powershell
# Run wrapper with logging
python C:\Users\O82652826\financial-analysis-mcp-wrapper.py > wrapper.log 2>&1
```

---

## Data Persistence Issues

### Problem: Tickers Not Saving

**Symptoms**:
- Added tickers disappear after restart
- tickers.csv not updating
- Changes not persisting

**Solutions**:

1. **Check volume mount**:
```bash
docker inspect financial-analysis-mcp | grep -A 5 Mounts
```

2. **Verify file permissions**:
```bash
ls -la ~/financial-analysis-mcp/data/tickers.csv
chmod 644 ~/financial-analysis-mcp/data/tickers.csv
```

3. **Check Docker volume**:
```bash
docker volume ls
docker volume inspect financial-analysis-mcp_data
```

4. **Manual backup**:
```bash
# Backup before changes
cp ~/financial-analysis-mcp/data/tickers.csv ~/tickers.backup.csv
```

---

## Getting Help

### Collect Diagnostic Information

```bash
#!/bin/bash
# diagnostic-report.sh

echo "=== Financial Analysis MCP Diagnostic Report ===" > report.txt
echo "Date: $(date)" >> report.txt

echo -e "\n=== Container Status ===" >> report.txt
docker ps -a | grep financial >> report.txt

echo -e "\n=== Recent Logs ===" >> report.txt
docker logs financial-analysis-mcp --tail 50 >> report.txt 2>&1

echo -e "\n=== Resource Usage ===" >> report.txt
docker stats financial-analysis-mcp --no-stream >> report.txt

echo -e "\n=== Network Test ===" >> report.txt
curl -s http://192.168.1.7:8000/tools/list >> report.txt

echo -e "\n=== Docker Version ===" >> report.txt
docker --version >> report.txt

echo "Report saved to report.txt"
```

### Contact Information

- **GitHub Issues**: https://github.com/TommyPopescu/financial-analysis-mcp/issues
- **Documentation**: See other files in `doc/` directory
- **Logs**: Always include Docker logs when reporting issues

---

## Related Documentation

- [Architecture](01-architecture.md) - System design
- [API Reference](02-api-reference.md) - Tool documentation
- [Deployment](03-deployment.md) - Deployment guide
- [Development](05-development.md) - Making changes