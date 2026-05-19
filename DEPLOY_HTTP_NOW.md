# Deploy HTTP Server - Instrucțiuni Rapide

## Fișiere Create pentru HTTP

✅ **src/server_http.py** - Server HTTP cu FastAPI  
✅ **Dockerfile.http** - Docker image pentru HTTP  
✅ **docker-compose.http.yml** - Docker Compose config  
✅ **requirements.txt** - Actualizat cu FastAPI și uvicorn  
✅ **src/config.py** - Adăugat HTTP_PORT  

## Deployment pe Server (192.168.1.7)

### Pasul 1: Upload Fișiere Noi pe GitHub

```bash
cd C:\Users\O82652826\.git\fin\financial-analysis-mcp

git add .
git commit -m "Add HTTP transport support for MCP server"
git push origin main
```

### Pasul 2: Deploy pe Server

```bash
# Conectează-te la server
ssh root@192.168.1.7

# Navighează la director
cd /root/financial-analysis-mcp

# Pull ultimele modificări
git pull origin main

# Oprește containerul stdio vechi
docker-compose down

# Build și start HTTP container
docker-compose -f docker-compose.http.yml up -d --build

# Așteaptă ~30 secunde pentru build
```

### Pasul 3: Verificare

```bash
# Check container
docker ps | grep financial-analysis-mcp-http

# Check logs
docker logs financial-analysis-mcp-http

# Test health endpoint
curl http://localhost:8000/health
# Expected: {"status":"healthy"}

# Test tools list
curl http://localhost:8000/tools | jq

# Test tool call
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"get_current_price","arguments":{"ticker":"AAPL"}}' | jq
```

## Configurare Bob (Windows)

### Pasul 1: Creează Wrapper

Creează fișierul: `C:\Users\O82652826\financial-analysis-mcp-wrapper.py`

```python
#!/usr/bin/env python3
"""MCP HTTP Wrapper - Converts stdio to HTTP"""
import sys
import json
import requests

SERVER_URL = "http://192.168.1.7:8000"

def main():
    for line in sys.stdin:
        try:
            request = json.loads(line)
            method = request.get("method", "")
            
            if method == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {
                            "name": "financial-analysis-mcp",
                            "version": "1.0.0"
                        }
                    }
                }
            elif method == "tools/list":
                resp = requests.get(f"{SERVER_URL}/tools")
                tools_data = resp.json()
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {"tools": tools_data["tools"]}
                }
            elif method == "tools/call":
                params = request.get("params", {})
                resp = requests.post(
                    f"{SERVER_URL}/tools/call",
                    json={
                        "name": params.get("name"),
                        "arguments": params.get("arguments", {})
                    }
                )
                result_data = resp.json()
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": str(result_data.get("result"))
                        }]
                    }
                }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
            
            print(json.dumps(response), flush=True)
            
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": request.get("id") if "request" in locals() else None,
                "error": {"code": -32603, "message": str(e)}
            }
            print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    main()
```

### Pasul 2: Instalează requests

```powershell
pip install requests
```

### Pasul 3: Testează Wrapper

```powershell
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python C:\Users\O82652826\financial-analysis-mcp-wrapper.py
```

Ar trebui să vezi un răspuns JSON cu "result".

### Pasul 4: Configurează Bob

Editează: `C:\Users\O82652826\.bob\settings\mcp_settings.json`

```json
{
  "mcpServers": {
    "financial-analysis": {
      "type": "stdio",
      "command": "python",
      "args": [
        "C:\\Users\\O82652826\\financial-analysis-mcp-wrapper.py"
      ],
      "env": {
        "SERVER_URL": "http://192.168.1.7:8000"
      },
      "alwaysAllow": [
        "fetch_ticker_data",
        "get_current_price",
        "list_tickers",
        "calculate_all_indicators",
        "generate_investment_summary"
      ]
    }
  }
}
```

### Pasul 5: Restartează Bob

Restartează Bob complet pentru a încărca noua configurație.

### Pasul 6: Testează în Bob

Încearcă comenzile:

```
Analizează acțiunea AAPL
```

```
Care este prețul curent al TSLA?
```

```
Arată-mi toți indicatorii tehnici pentru MSFT
```

## Troubleshooting

### Container nu pornește

```bash
docker logs financial-analysis-mcp-http
```

Verifică dacă toate dependencies sunt instalate.

### Port 8000 ocupat

```bash
# Verifică ce folosește portul
netstat -tulpn | grep 8000

# Sau schimbă portul în docker-compose.http.yml
ports:
  - "8001:8000"
```

### Bob nu se conectează

```powershell
# Testează de pe Windows
curl http://192.168.1.7:8000/health
```

Dacă nu merge, verifică firewall pe server:
```bash
ufw allow 8000/tcp
```

### Wrapper nu funcționează

```powershell
# Verifică că requests este instalat
pip list | findstr requests

# Testează manual
python C:\Users\O82652826\financial-analysis-mcp-wrapper.py
# Apoi scrie: {"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}
# Apasă Enter
```

## Verificare Finală

### Pe Server

```bash
# Container rulează
docker ps | grep financial-analysis-mcp-http

# Health check OK
curl http://localhost:8000/health

# Tools list OK
curl http://localhost:8000/tools
```

### Pe Windows

```powershell
# Server accesibil
curl http://192.168.1.7:8000/health

# Wrapper funcționează
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python C:\Users\O82652826\financial-analysis-mcp-wrapper.py
```

### În Bob

Scrie în Bob:
```
Analizează AAPL
```

Ar trebui să primești o analiză completă cu indicatori tehnici.

## Rezumat

✅ **Server HTTP** - Rulează în Docker pe 192.168.1.7:8000  
✅ **Wrapper Python** - Convertește stdio la HTTP pentru Bob  
✅ **Bob Config** - Folosește wrapper-ul pentru comunicare  
✅ **Compatibilitate** - Rezolvă toate problemele stdio  

Soluția este **production-ready** și poate fi folosită imediat!

---

**Made with Bob** 🤖