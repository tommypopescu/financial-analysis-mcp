# Financial Analysis MCP Server - Quick Start Guide

## 🚀 Deployment pe OMV Server

### Prerequisite
- OMV server cu Docker și Docker Compose instalat ✅
- Git instalat pe server
- Acces SSH la server

### Pași de Deployment

#### 1. Clonează Repository-ul pe OMV Server

```bash
# Conectează-te la OMV server
ssh user@omv-server-ip

# Clonează repository-ul
cd /path/to/deployment
git clone https://github.com/tommypopescu/fin.git
cd fin/financial-analysis-mcp
```

#### 2. Configurează Environment Variables

```bash
# Copiază fișierul .env.example
cp .env.example .env

# Editează .env cu setările tale
nano .env
```

Setări importante în `.env`:
```env
MCP_SERVER_PORT=3000
LOG_LEVEL=INFO
TICKER_CSV_PATH=/app/data/tickers.csv
CACHE_ENABLED=true
CACHE_TTL=300
```

#### 3. Pull Docker Image de pe GHCR

```bash
# Pull imaginea de pe GitHub Container Registry
docker pull ghcr.io/tommypopescu/financial-analysis-mcp:latest

# SAU build local
docker build -t ghcr.io/tommypopescu/financial-analysis-mcp:latest .
```

#### 4. Actualizează docker-compose.yml pentru GHCR

```yaml
version: '3.8'

services:
  financial-mcp:
    image: ghcr.io/tommypopescu/financial-analysis-mcp:latest
    container_name: financial-analysis-mcp
    ports:
      - "3000:3000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - MCP_SERVER_PORT=3000
      - LOG_LEVEL=INFO
      - CACHE_ENABLED=true
      - CACHE_TTL=300
    restart: unless-stopped
```

#### 5. Start Container

```bash
# Start cu docker-compose
docker-compose up -d

# Verifică că containerul rulează
docker-compose ps

# Vezi logs
docker-compose logs -f
```

#### 6. Testează MCP Server-ul

```bash
# Verifică health check
docker-compose exec financial-mcp python -c "import socket; s=socket.socket(); s.connect(('localhost', 3000)); s.close(); print('OK')"

# Testează un tool
docker-compose exec financial-mcp python -c "from src.tools import get_current_price; print(get_current_price('AAPL'))"
```

### 7. Configurează Bob pentru a folosi MCP Server-ul

Adaugă în `.bob/mcp.json`:

```json
{
  "mcpServers": {
    "financial-analysis": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "financial-analysis-mcp",
        "python",
        "-m",
        "src.server"
      ],
      "env": {
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## 📊 Utilizare cu Bob

După configurare, Bob poate folosi comenzi precum:

```
"Analizează acțiunea AAPL"
"Arată-mi lista de tickers din watchlist"
"Caută acțiuni cu RSI sub 30"
"Compară MSFT și GOOGL"
"Adaugă TSLA în watchlist"
```

## 🔄 Update și Maintenance

### Update la versiune nouă (cu GHCR)

```bash
cd /path/to/deployment/fin/financial-analysis-mcp

# Pull ultima versiune de pe GHCR
docker pull ghcr.io/tommypopescu/financial-analysis-mcp:latest

# Restart container
docker-compose down
docker-compose up -d

# Verifică logs
docker-compose logs -f
```

### Backup date

```bash
# Backup watchlist
cp data/tickers.csv data/tickers.csv.backup

# Backup logs
tar -czf logs-backup-$(date +%Y%m%d).tar.gz logs/
```

### Monitorizare

```bash
# Vezi logs în timp real
docker-compose logs -f

# Verifică status
docker-compose ps

# Verifică resurse folosite
docker stats financial-analysis-mcp
```

## 🐛 Troubleshooting

### Container nu pornește

```bash
# Verifică logs
docker-compose logs

# Verifică configurația
docker-compose config

# Pull forțat ultima versiune
docker pull ghcr.io/tommypopescu/financial-analysis-mcp:latest
docker-compose down
docker-compose up -d
```

### Erori de import

```bash
# Reinstalează dependencies
docker-compose exec financial-mcp pip install -r requirements.txt
docker-compose restart
```

### Port deja folosit

```bash
# Schimbă portul în docker-compose.yml
ports:
  - "3001:3000"  # folosește 3001 în loc de 3000
```

## 📝 Comenzi Utile

```bash
# Pull ultima versiune
docker pull ghcr.io/tommypopescu/financial-analysis-mcp:latest

# Start
docker-compose up -d

# Stop
docker-compose down

# Restart
docker-compose restart

# Vezi logs
docker-compose logs -f

# Execută comandă în container
docker-compose exec financial-mcp bash

# Curăță tot (ATENȚIE: șterge și datele!)
docker-compose down -v
```

## 🔄 GitHub Actions Workflow

Workflow-ul automat va:
1. Build imaginea Docker la fiecare push pe `main`
2. Push imaginea la GitHub Container Registry (GHCR)
3. Tag-uri automate: `latest` și SHA commit

**Nu sunt necesare secrets** - workflow-ul folosește `GITHUB_TOKEN` automat!

### Verifică imaginea pe GHCR

```bash
# Vezi imaginile disponibile
https://github.com/tommypopescu?tab=packages

# Pull o versiune specifică
docker pull ghcr.io/tommypopescu/financial-analysis-mcp:SHA_COMMIT
```

## 💡 Tips

1. **Folosește GHCR** pentru imagini Docker (nu Docker Hub)
2. **Monitorizează logs** regulat pentru erori
3. **Backup watchlist-ul** înainte de update-uri
4. **Pull automat** la fiecare update din GitHub
5. **Workflow simplu** - fără configurare secrets complexă

## 🆘 Suport

Pentru probleme sau întrebări:
- Verifică logs: `docker-compose logs -f`
- Verifică GitHub Actions pentru build status
- Verifică GitHub Packages pentru imagini disponibile
- Consultă documentația completă în README.md

## 🔗 Link-uri Utile

- Repository: https://github.com/tommypopescu/fin
- Packages (GHCR): https://github.com/tommypopescu?tab=packages
- Actions: https://github.com/tommypopescu/fin/actions