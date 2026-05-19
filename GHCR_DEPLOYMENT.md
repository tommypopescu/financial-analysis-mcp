# Deployment cu GitHub Container Registry (GHCR)

## Situația Actuală

Imaginea Docker este construită automat de GitHub Actions și publicată la:
```
ghcr.io/tommypopescu/financial-analysis-mcp:latest
```

## Ce S-a Modificat

1. **Dockerfile** - Actualizat să expună portul 8000 pentru HTTP server
2. **requirements.txt** - Include FastAPI și uvicorn pentru HTTP transport
3. **src/server_http.py** - Nou server HTTP pentru compatibilitate cu Bob
4. **docker-compose.http.yml** - Configurație pentru deployment cu GHCR

## Pași pentru Deployment

### 1. Upload Fișiere pe GitHub

Trebuie să urcăm fișierele noi/modificate pe GitHub:

**Fișiere noi:**
- `src/server_http.py`
- `docker-compose.http.yml`
- `Dockerfile.http` (opțional)
- `HTTP_DEPLOYMENT_GUIDE.md`
- `DEPLOY_HTTP_NOW.md`
- `LOCAL_WINDOWS_SETUP.md`
- `GHCR_DEPLOYMENT.md` (acest fișier)

**Fișiere modificate:**
- `Dockerfile` (adăugat EXPOSE 8000)
- `requirements.txt` (adăugat FastAPI, uvicorn)
- `src/config.py` (adăugat HTTP_PORT)

### 2. Așteaptă Build-ul Automat

După push pe GitHub:
1. GitHub Actions va detecta automat push-ul pe branch `main`
2. Va construi imaginea Docker cu `Dockerfile` actualizat
3. Va publica imaginea la `ghcr.io/tommypopescu/financial-analysis-mcp:latest`
4. Procesul durează ~5-10 minute

Poți urmări progresul aici:
https://github.com/tommypopescu/financial-analysis-mcp/actions

### 3. Deploy pe Server (192.168.1.7)

**Fără Git pe server:**

```bash
# Conectează-te la server
ssh root@192.168.1.7

# Creează directorul dacă nu există
mkdir -p /root/financial-analysis-mcp
cd /root/financial-analysis-mcp

# Creează docker-compose.http.yml manual
cat > docker-compose.http.yml << 'EOF'
version: '3.8'

services:
  financial-analysis-mcp-http:
    image: ghcr.io/tommypopescu/financial-analysis-mcp:latest
    container_name: financial-analysis-mcp-http
    command: ["python", "-m", "src.server_http"]
    ports:
      - "8000:8000"
    environment:
      - LOG_LEVEL=INFO
      - HTTP_PORT=8000
    volumes:
      - ./data:/app/data
    restart: unless-stopped
EOF

# Oprește containerul vechi (dacă există)
docker stop financial-analysis-mcp 2>/dev/null || true
docker rm financial-analysis-mcp 2>/dev/null || true

# Pull imaginea nouă de pe GHCR
docker pull ghcr.io/tommypopescu/financial-analysis-mcp:latest

# Pornește containerul HTTP
docker-compose -f docker-compose.http.yml up -d

# Verifică că rulează
docker ps | grep financial-analysis-mcp-http
curl http://localhost:8000/health
```

### 4. Testează API-ul

```bash
# Health check
curl http://localhost:8000/health

# Lista tools
curl http://localhost:8000/tools

# Test tool call
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "get_ticker_info",
    "arguments": {
      "ticker": "AAPL"
    }
  }'
```

### 5. Configurează Bob (Windows)

Creează wrapper Python la `C:\Users\O82652826\financial-analysis-mcp-wrapper.py`:

```python
import sys
import json
import requests
from typing import Any, Dict

SERVER_URL = "http://192.168.1.7:8000"

def call_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Call MCP tool via HTTP"""
    response = requests.post(
        f"{SERVER_URL}/tools/call",
        json={"name": name, "arguments": arguments},
        timeout=30
    )
    response.raise_for_status()
    return response.json()

def main():
    """Main stdio loop for MCP protocol"""
    for line in sys.stdin:
        try:
            request = json.loads(line)
            method = request.get("method")
            
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
                tools_response = requests.get(f"{SERVER_URL}/tools")
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {"tools": tools_response.json()}
                }
            elif method == "tools/call":
                params = request.get("params", {})
                result = call_tool(params["name"], params.get("arguments", {}))
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": result
                }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                }
            
            print(json.dumps(response), flush=True)
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": request.get("id") if 'request' in locals() else None,
                "error": {"code": -32603, "message": str(e)}
            }
            print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    main()
```

Configurează Bob în `.bob/mcp.json`:

```json
{
  "mcpServers": {
    "financial-analysis": {
      "command": "python",
      "args": ["C:\\Users\\O82652826\\financial-analysis-mcp-wrapper.py"]
    }
  }
}
```

## Verificare Finală

1. **Pe server:**
   ```bash
   docker logs financial-analysis-mcp-http
   curl http://localhost:8000/health
   ```

2. **În Bob:**
   - Restart Bob
   - Test: "Analizează acțiunea AAPL"

## Troubleshooting

### Imaginea nu se găsește
```bash
# Verifică că GitHub Actions a terminat build-ul
# Apoi pull manual:
docker pull ghcr.io/tommypopescu/financial-analysis-mcp:latest
```

### Containerul nu pornește
```bash
docker logs financial-analysis-mcp-http
# Verifică că portul 8000 nu e ocupat:
netstat -tulpn | grep 8000
```

### Bob nu se conectează
- Verifică că wrapper-ul Python există
- Verifică că serverul HTTP răspunde: `curl http://192.168.1.7:8000/health`
- Verifică logs în Bob

## Avantaje GHCR

✅ Build automat la fiecare push pe GitHub  
✅ Nu trebuie Git pe server  
✅ Imagini versionate (latest + SHA)  
✅ Pull simplu cu `docker pull`  
✅ Consistență între dezvoltare și producție