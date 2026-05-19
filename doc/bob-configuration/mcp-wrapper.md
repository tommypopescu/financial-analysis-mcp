# MCP Wrapper Configuration

## Overview

The `financial-analysis-mcp-wrapper.py` is a Python script that bridges Bob's stdio-based MCP protocol to the HTTP-based Financial Analysis MCP Server. This wrapper is necessary because Bob uses stdio transport while the MCP server uses HTTP transport.

## Why a Wrapper is Needed

### The Problem

**Bob's MCP Client**:
- Uses stdio transport (standard input/output)
- Expects to communicate via stdin/stdout
- Cannot directly connect to HTTP servers

**Financial Analysis MCP Server**:
- Uses HTTP transport (FastAPI)
- Listens on http://192.168.1.7:8000
- Cannot directly communicate via stdio

### The Solution

The wrapper acts as a translator:
```
Bob (stdio) ←→ Wrapper (stdio ↔ HTTP) ←→ MCP Server (HTTP)
```

## File Location

```
C:/Users/O82652826/financial-analysis-mcp-wrapper.py
```

**Note**: This file is in the user's home directory, not in the project repository.

## Complete Wrapper Code

```python
#!/usr/bin/env python3
"""
MCP Wrapper for Financial Analysis Server
Bridges stdio (Bob) to HTTP (MCP server)
"""

import sys
import json
import requests
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('C:/Users/O82652826/mcp-wrapper.log'),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)

# MCP Server configuration
MCP_SERVER_URL = "http://192.168.1.7:8000"
TIMEOUT = 30  # seconds

def send_to_mcp_server(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send JSON-RPC request to MCP server via HTTP
    
    Args:
        request: JSON-RPC 2.0 request object
        
    Returns:
        JSON-RPC 2.0 response object
    """
    try:
        logger.debug(f"Sending request to MCP server: {json.dumps(request, indent=2)}")
        
        # Send POST request to MCP server
        response = requests.post(
            f"{MCP_SERVER_URL}/mcp",
            json=request,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        
        # Check HTTP status
        response.raise_for_status()
        
        # Parse JSON response
        result = response.json()
        logger.debug(f"Received response from MCP server: {json.dumps(result, indent=2)}")
        
        return result
        
    except requests.exceptions.Timeout:
        logger.error(f"Request timeout after {TIMEOUT} seconds")
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "error": {
                "code": -32000,
                "message": f"Request timeout after {TIMEOUT} seconds"
            }
        }
        
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error: {e}")
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "error": {
                "code": -32000,
                "message": f"Cannot connect to MCP server at {MCP_SERVER_URL}"
            }
        }
        
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error: {e}")
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "error": {
                "code": -32000,
                "message": f"HTTP error: {e}"
            }
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "error": {
                "code": -32700,
                "message": "Invalid JSON response from server"
            }
        }
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }
        }

def main():
    """
    Main loop: Read from stdin, forward to MCP server, write to stdout
    """
    logger.info("MCP Wrapper started")
    logger.info(f"Connecting to MCP server at {MCP_SERVER_URL}")
    
    try:
        # Read from stdin line by line
        for line in sys.stdin:
            line = line.strip()
            
            if not line:
                continue
                
            try:
                # Parse JSON-RPC request from Bob
                request = json.loads(line)
                logger.debug(f"Received from Bob: {json.dumps(request, indent=2)}")
                
                # Forward to MCP server
                response = send_to_mcp_server(request)
                
                # Send response back to Bob via stdout
                response_str = json.dumps(response)
                print(response_str, flush=True)
                logger.debug(f"Sent to Bob: {response_str}")
                
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON from Bob: {e}")
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": "Parse error: Invalid JSON"
                    }
                }
                print(json.dumps(error_response), flush=True)
                
    except KeyboardInterrupt:
        logger.info("MCP Wrapper stopped by user")
    except Exception as e:
        logger.error(f"Fatal error in main loop: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## How It Works

### 1. Initialization

```python
MCP_SERVER_URL = "http://192.168.1.7:8000"
TIMEOUT = 30  # seconds
```

- Sets MCP server URL
- Configures request timeout
- Sets up logging to file and stderr

### 2. Main Loop

```python
for line in sys.stdin:
    request = json.loads(line)      # Read from Bob
    response = send_to_mcp_server(request)  # Forward to server
    print(json.dumps(response))     # Send back to Bob
```

**Flow**:
1. Read JSON-RPC request from stdin (Bob)
2. Parse JSON
3. Forward to MCP server via HTTP POST
4. Receive HTTP response
5. Write JSON-RPC response to stdout (Bob)

### 3. Error Handling

The wrapper handles multiple error types:

**Timeout Errors**:
```python
except requests.exceptions.Timeout:
    return {"error": {"code": -32000, "message": "Request timeout"}}
```

**Connection Errors**:
```python
except requests.exceptions.ConnectionError:
    return {"error": {"code": -32000, "message": "Cannot connect"}}
```

**HTTP Errors**:
```python
except requests.exceptions.HTTPError:
    return {"error": {"code": -32000, "message": "HTTP error"}}
```

**JSON Errors**:
```python
except json.JSONDecodeError:
    return {"error": {"code": -32700, "message": "Invalid JSON"}}
```

### 4. Logging

All activity is logged to:
- **File**: `C:/Users/O82652826/mcp-wrapper.log`
- **Console**: stderr (visible in Bob's output)

**Log Levels**:
- `DEBUG`: Request/response details
- `INFO`: Startup/shutdown messages
- `ERROR`: Error conditions

## Installation

### Step 1: Create Wrapper File

Create `C:/Users/O82652826/financial-analysis-mcp-wrapper.py` with the code above.

### Step 2: Install Dependencies

```powershell
pip install requests
```

### Step 3: Test Wrapper

```powershell
# Test manually
python C:/Users/O82652826/financial-analysis-mcp-wrapper.py
```

Then send a test request via stdin:
```json
{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}
```

Press Ctrl+Z then Enter (Windows) to send EOF.

### Step 4: Configure Bob

Add to Bob's MCP settings (location varies by Bob version):

```json
{
  "mcpServers": {
    "financial-analysis": {
      "command": "python",
      "args": [
        "C:/Users/O82652826/financial-analysis-mcp-wrapper.py"
      ],
      "env": {}
    }
  }
}
```

### Step 5: Restart VS Code

Bob loads MCP configuration on startup.

## Configuration Options

### Change MCP Server URL

```python
MCP_SERVER_URL = "http://192.168.1.7:8000"  # Default
# MCP_SERVER_URL = "http://localhost:8000"  # Local testing
# MCP_SERVER_URL = "https://mcp.example.com"  # Remote server
```

### Adjust Timeout

```python
TIMEOUT = 30  # Default: 30 seconds
# TIMEOUT = 60  # For slow operations
# TIMEOUT = 10  # For fast operations
```

### Change Log Location

```python
logging.FileHandler('C:/Users/O82652826/mcp-wrapper.log')
# logging.FileHandler('D:/logs/mcp-wrapper.log')
# logging.FileHandler('/var/log/mcp-wrapper.log')
```

### Adjust Log Level

```python
logging.basicConfig(level=logging.DEBUG)  # Verbose
# logging.basicConfig(level=logging.INFO)   # Normal
# logging.basicConfig(level=logging.WARNING)  # Quiet
# logging.basicConfig(level=logging.ERROR)  # Errors only
```

## Troubleshooting

### Wrapper Not Starting

**Symptoms**:
- Bob shows "MCP server failed to start"
- No log file created

**Solutions**:
1. Check Python is installed: `python --version`
2. Check file path is correct
3. Check file permissions
4. Run manually to see errors:
   ```powershell
   python C:/Users/O82652826/financial-analysis-mcp-wrapper.py
   ```

### Connection Refused

**Symptoms**:
```
ERROR - Connection error: Cannot connect to MCP server
```

**Solutions**:
1. Check MCP server is running:
   ```bash
   docker ps | grep financial-analysis
   ```
2. Test server directly:
   ```powershell
   curl http://192.168.1.7:8000/health
   ```
3. Check firewall settings
4. Verify URL in wrapper matches server

### Timeout Errors

**Symptoms**:
```
ERROR - Request timeout after 30 seconds
```

**Solutions**:
1. Increase timeout in wrapper:
   ```python
   TIMEOUT = 60  # Increase to 60 seconds
   ```
2. Check server performance:
   ```bash
   docker stats financial-analysis-mcp
   ```
3. Check network latency:
   ```powershell
   Test-NetConnection 192.168.1.7 -Port 8000
   ```

### JSON Parse Errors

**Symptoms**:
```
ERROR - JSON decode error: Expecting value
```

**Solutions**:
1. Check server is returning valid JSON
2. Test server endpoint directly:
   ```powershell
   curl -X POST http://192.168.1.7:8000/mcp `
     -H "Content-Type: application/json" `
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
   ```
3. Check wrapper log for full response
4. Verify server is not returning HTML error pages

### Wrapper Crashes

**Symptoms**:
- Wrapper stops responding
- Bob shows "MCP connection closed"

**Solutions**:
1. Check wrapper log for errors
2. Check Python version compatibility
3. Update requests library:
   ```powershell
   pip install --upgrade requests
   ```
4. Add more error handling if needed

## Monitoring

### Check Wrapper Status

```powershell
# Check if wrapper process is running
Get-Process python | Where-Object {$_.CommandLine -like "*mcp-wrapper*"}
```

### View Logs

```powershell
# View last 50 lines
Get-Content C:/Users/O82652826/mcp-wrapper.log -Tail 50

# Follow log in real-time
Get-Content C:/Users/O82652826/mcp-wrapper.log -Wait
```

### Test Connection

```powershell
# Test MCP server is reachable
Test-NetConnection 192.168.1.7 -Port 8000

# Test HTTP endpoint
curl http://192.168.1.7:8000/health
```

## Performance Optimization

### Reduce Logging

For production, reduce log verbosity:
```python
logging.basicConfig(level=logging.WARNING)  # Only warnings and errors
```

### Connection Pooling

For better performance, use session:
```python
session = requests.Session()

def send_to_mcp_server(request: Dict[str, Any]) -> Dict[str, Any]:
    response = session.post(...)  # Reuses connection
```

### Async Processing

For concurrent requests (advanced):
```python
import asyncio
import aiohttp

async def send_to_mcp_server(request):
    async with aiohttp.ClientSession() as session:
        async with session.post(...) as response:
            return await response.json()
```

## Security Considerations

### 1. Network Security

- MCP server is on local network (192.168.1.7)
- No authentication required (trusted network)
- Consider VPN if accessing remotely

### 2. Input Validation

Wrapper validates:
- JSON structure
- Request format
- Response format

### 3. Error Information

Logs may contain sensitive data:
- Ticker symbols
- Analysis results
- User queries

**Recommendation**: Restrict log file permissions:
```powershell
icacls C:/Users/O82652826/mcp-wrapper.log /grant:r "$env:USERNAME:(R,W)"
```

## Alternative Approaches

### 1. Direct HTTP Connection

If Bob supported HTTP transport directly:
```json
{
  "mcpServers": {
    "financial-analysis": {
      "url": "http://192.168.1.7:8000/mcp",
      "transport": "http"
    }
  }
}
```

**Status**: Not currently supported by Bob

### 2. SSH Tunnel

Use SSH tunnel instead of wrapper:
```bash
ssh -L 8000:localhost:8000 user@192.168.1.7
```

**Status**: Tested but had compatibility issues

### 3. WebSocket Transport

Use WebSocket instead of HTTP:
```python
# Server side
import websockets

# Client side (wrapper)
import websockets
```

**Status**: Not implemented (HTTP is sufficient)

## Related Documentation

- [Custom Modes Configuration](custom-modes.md)
- [Workflow Instructions](workflow-instructions.md)
- [MCP Server Deployment](../mcp-server/03-deployment.md)
- [MCP Server Troubleshooting](../mcp-server/04-troubleshooting.md)

## Summary

The MCP wrapper:
- ✅ Bridges stdio (Bob) to HTTP (MCP server)
- ✅ Handles JSON-RPC 2.0 protocol
- ✅ Provides error handling and logging
- ✅ Enables Bob to use HTTP-based MCP servers
- ✅ Simple Python script, easy to modify

**Key Points**:
1. Located at `C:/Users/O82652826/financial-analysis-mcp-wrapper.py`
2. Requires `requests` library
3. Logs to `mcp-wrapper.log`
4. Configured in Bob's MCP settings
5. Forwards requests to http://192.168.1.7:8000

**Next Steps**:
- Configure [Workflow Instructions](workflow-instructions.md)
- Test wrapper with Bob
- Monitor logs for issues
- Optimize as needed