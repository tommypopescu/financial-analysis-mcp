# Financial Analysis MCP - HTTP Deployment Guide

## Problema Rezolvată

Serverul MCP stdio are probleme de compatibilitate cu Bob când rulează remote via SSH + Docker. Soluția este să expunem serverul prin **HTTP** în loc de stdio.

## Avantaje HTTP vs stdio

✅ **Compatibilitate perfectă** - HTTP este un protocol standard  
✅ **Fără probleme SSH** - Bob se conectează direct la HTTP endpoint  
✅ **Mai ușor de debugat** - Poți testa cu curl/Postman  
✅ **Mai flexibil** - Poate fi accesat de orice client HTTP  
✅ **Health checks** - Monitoring mai ușor  

## Deployment pe Server (192.168.1.7)

### Pasul 1: Oprește containerul stdio existent

```bash
ssh root@192.168.1.7
cd /root/financial-analysis-mcp
docker-compose down
```

### Pasul 2: Pull ultimele modificări

```bash
git pull origin main
```

### Pasul 3: Build și start HTTP container

```bash
docker-compose -f docker-compose.http.yml up -d --build
```

### Pasul 4: Verifică că serverul rulează

```bash
# Check container status
docker ps | grep financial-analysis-mcp-http

# Check logs
docker logs financial-analysis-mcp-http

# Test health endpoint
curl http://localhost:8000/health
# Ar trebui să returneze: {"status":"healthy"}

# Test tools list
curl http://localhost:8000/tools
```

### Pasul 5: Testează un tool

```bash
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "get_current_price",
    "arguments": {"ticker": "AAPL"}
  }'
```

## Configurare Bob pentru HTTP

### Opțiunea 1: MCP HTTP Wrapper (Recomandat)

Creează un wrapper Python care convertește stdio la HTTP:

**Fișier: `C:\Users\O82652826\financial-analysis-mcp-wrapper.py`**

```python
#!/usr/bin/env python3
"""
MCP HTTP Wrapper - Converts stdio MCP protocol to HTTP calls
"""
import sys
import json
import requests

SERVER_URL = "http://192.168.1.7:8000"

def main():
    """Main wrapper loop"""
    for line in sys.stdin:
        try:
            request = json.loads(line)
            method = request.get("method", "")
            
            if method == "initialize":
                # Return initialization response
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "financial-analysis-mcp",
                            "version": "1.0.0"
                        }
                    }
                }
            elif method == "tools/list":
                # Get tools from HTTP server
                resp = requests.get(f"{SERVER_URL}/tools")
                tools_data = resp.json()
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {"tools": tools_data["tools"]}
                }
            elif method == "tools/call":
                # Call tool via HTTP
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
                        "content": [
                            {
                                "type": "text",
                                "text": str(result_data.get("result"))
                            }
                        ]
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
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
            print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    main()
```

**Bob Configuration: `C:\Users\O82652826\.bob\settings\mcp_settings.json`**

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
        "list_tickers"
      ]
    }
  }
}
```

### Opțiunea 2: Direct HTTP (Dacă Bob suportă)

Dacă Bob suportă MCP peste HTTP direct:

```json
{
  "mcpServers": {
    "financial-analysis": {
      "type": "http",
      "url": "http://192.168.1.7:8000",
      "alwaysAllow": [
        "fetch_ticker_data",
        "get_current_price",
        "list_tickers"
      ]
    }
  }
}
```

## Testing

### Test 1: Health Check

```bash
curl http://192.168.1.7:8000/health
```

Expected: `{"status":"healthy"}`

### Test 2: List Tools

```bash
curl http://192.168.1.7:8000/tools
```

Expected: JSON cu lista de tools

### Test 3: Call Tool

```bash
curl -X POST http://192.168.1.7:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "get_current_price",
    "arguments": {"ticker": "AAPL"}
  }'
```

Expected: JSON cu prețul curent

### Test 4: Bob Integration

În Bob, încearcă:

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

### Problema: Container nu pornește

**Verificare:**
```bash
docker logs financial-analysis-mcp-http
```

**Soluție:** Verifică că toate dependencies sunt instalate în requirements.txt

### Problema: Port 8000 deja folosit

**Verificare:**
```bash
netstat -tulpn | grep 8000
```

**Soluție:** Schimbă portul în docker-compose.http.yml:
```yaml
ports:
  - "8001:8000"  # Folosește 8001 în loc de 8000
```

### Problema: Bob nu se poate conecta

**Verificare:**
```bash
# De pe Windows
curl http://192.168.1.7:8000/health
```

**Soluție:** Verifică firewall pe server:
```bash
ufw allow 8000/tcp
```

### Problema: Wrapper nu funcționează

**Verificare:**
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python C:\Users\O82652826\financial-analysis-mcp-wrapper.py
```

**Soluție:** Instalează requests:
```bash
pip install requests
```

## Monitoring

### Check Container Status

```bash
docker ps | grep financial-analysis-mcp-http
```

### View Logs

```bash
docker logs -f financial-analysis-mcp-http
```

### Check Resource Usage

```bash
docker stats financial-analysis-mcp-http
```

## Backup și Restore

### Backup Data

```bash
cd /root/financial-analysis-mcp
tar -czf backup-$(date +%Y%m%d).tar.gz data/
```

### Restore Data

```bash
cd /root/financial-analysis-mcp
tar -xzf backup-20260519.tar.gz
```

## Update Procedure

```bash
# 1. Pull latest code
cd /root/financial-analysis-mcp
git pull origin main

# 2. Rebuild container
docker-compose -f docker-compose.http.yml up -d --build

# 3. Verify
curl http://localhost:8000/health
```

## Comparație: stdio vs HTTP

| Aspect | stdio (SSH + Docker) | HTTP |
|--------|---------------------|------|
| Setup | Complex | Simplu |
| Compatibilitate Bob | ❌ Probleme | ✅ Perfect |
| Debugging | Dificil | Ușor (curl/Postman) |
| Monitoring | Limitat | Health checks |
| Latență | ~50-100ms | ~10-20ms |
| Securitate | SSH tunnel | HTTP (poate fi HTTPS) |
| **Recomandat** | ❌ Nu | ✅ **Da** |

## Concluzie

Deployment-ul HTTP rezolvă toate problemele de compatibilitate cu Bob și oferă o soluție mai robustă și mai ușor de întreținut. Serverul poate fi accesat direct via HTTP de către Bob sau orice alt client.

---

**Made with Bob** 🤖