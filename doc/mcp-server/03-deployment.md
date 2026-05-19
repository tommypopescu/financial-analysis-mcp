# MCP Server Deployment Guide

Complete guide for deploying the Financial Analysis MCP Server on OMV server or other environments.

## Prerequisites

### Hardware Requirements
- **CPU**: 1+ cores
- **RAM**: 512MB minimum, 1GB recommended
- **Storage**: 500MB for Docker image + data
- **Network**: Local network access (192.168.1.x)

### Software Requirements
- **Docker**: 20.10+
- **Docker Compose**: 1.29+
- **Git**: For cloning repository
- **SSH**: For remote deployment (optional)

### OMV Server Specifications
- **OS**: Debian-based (OpenMediaVault)
- **IP**: 192.168.1.7
- **User**: tommy
- **Docker**: Installed and running

## Deployment Methods

### Method 1: Docker Compose (Recommended)

#### Step 1: Clone Repository
```bash
ssh tommy@192.168.1.7
cd ~
git clone https://github.com/TommyPopescu/financial-analysis-mcp.git
cd financial-analysis-mcp
```

#### Step 2: Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit if needed (optional)
nano .env
```

**Default .env**:
```env
# Server Configuration
PORT=8000
HOST=0.0.0.0

# Data Directory
DATA_DIR=./data

# Logging
LOG_LEVEL=INFO
```

#### Step 3: Start Server
```bash
docker-compose up -d
```

#### Step 4: Verify Deployment
```bash
# Check container status
docker-compose ps

# Check logs
docker-compose logs -f

# Test endpoint
curl http://localhost:8000/tools/list
```

#### Step 5: Configure Auto-Start
```bash
# Enable Docker service
sudo systemctl enable docker

# Container will auto-restart on reboot (restart: unless-stopped)
```

---

### Method 2: Docker Run

#### Step 1: Pull Image
```bash
docker pull ghcr.io/tommypopescu/financial-analysis-mcp:latest
```

#### Step 2: Create Data Directory
```bash
mkdir -p ~/financial-analysis-mcp/data
```

#### Step 3: Run Container
```bash
docker run -d \
  --name financial-analysis-mcp \
  --restart unless-stopped \
  -p 8000:8000 \
  -v ~/financial-analysis-mcp/data:/app/data \
  ghcr.io/tommypopescu/financial-analysis-mcp:latest
```

#### Step 4: Verify
```bash
docker logs financial-analysis-mcp
curl http://localhost:8000/tools/list
```

---

### Method 3: Local Development

#### Step 1: Clone Repository
```bash
git clone https://github.com/TommyPopescu/financial-analysis-mcp.git
cd financial-analysis-mcp
```

#### Step 2: Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Run Server
```bash
python src/server_http.py
```

Server will start on http://localhost:8000

---

## Bob Configuration

### Step 1: Install MCP Wrapper

**Location**: `C:\Users\O82652826\financial-analysis-mcp-wrapper.py`

**Content**: See [bob-configuration/mcp-wrapper.py](../bob-configuration/mcp-wrapper.py)

### Step 2: Configure Bob MCP Settings

**File**: `C:\Users\O82652826\AppData\Local\Programs\IBM Bob\mcp_settings.json`

```json
{
  "mcpServers": {
    "financial-analysis": {
      "command": "python",
      "args": [
        "C:\\Users\\O82652826\\financial-analysis-mcp-wrapper.py"
      ],
      "env": {}
    }
  }
}
```

### Step 3: Add Financial Analyst Mode

**File**: `C:\Users\O82652826\.git\.bob\custom_modes.yaml`

See [bob-configuration/custom_modes.yaml](../bob-configuration/custom_modes.yaml)

### Step 4: Add Mode Instructions

**Files**:
- `C:\Users\O82652826\.git\.bob\rules-financial-analyst\1_analysis_workflow.xml`
- `C:\Users\O82652826\.git\.bob\rules-financial-analyst\2_analysis_examples.xml`

See [bob-configuration/rules-financial-analyst/](../bob-configuration/rules-financial-analyst/)

### Step 5: Restart Bob

Restart Bob to load new configuration.

### Step 6: Verify Connection

```
/mode financial-analyst
list tickers
```

Should show green status indicator for financial-analysis MCP server.

---

## Network Configuration

### Port Forwarding (Optional)

If accessing from different network:

```bash
# On OMV server
sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
sudo iptables-save > /etc/iptables/rules.v4
```

### Firewall Rules

```bash
# Allow port 8000
sudo ufw allow 8000/tcp
sudo ufw reload
```

### DNS/Hosts Configuration

**Windows** (`C:\Windows\System32\drivers\etc\hosts`):
```
192.168.1.7  omv-server financial-mcp
```

**Linux/Mac** (`/etc/hosts`):
```
192.168.1.7  omv-server financial-mcp
```

---

## SSL/HTTPS Setup (Optional)

### Using Nginx Reverse Proxy

#### Step 1: Install Nginx
```bash
sudo apt update
sudo apt install nginx certbot python3-certbot-nginx
```

#### Step 2: Configure Nginx
```nginx
# /etc/nginx/sites-available/financial-mcp
server {
    listen 443 ssl;
    server_name financial-mcp.local;

    ssl_certificate /etc/ssl/certs/financial-mcp.crt;
    ssl_certificate_key /etc/ssl/private/financial-mcp.key;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Step 3: Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/financial-mcp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### Step 4: Update Wrapper
Change URL in wrapper from `http://192.168.1.7:8000` to `https://financial-mcp.local`

---

## Updating Deployment

### Method 1: Automatic (GitHub Actions)

1. Push changes to GitHub
2. GitHub Actions builds new image
3. Pull and restart on server:

```bash
ssh tommy@192.168.1.7
cd ~/financial-analysis-mcp
docker-compose pull
docker-compose up -d
```

### Method 2: Manual Build

```bash
# On OMV server
cd ~/financial-analysis-mcp
git pull
docker-compose build
docker-compose up -d
```

### Method 3: Quick Script

**File**: `UPDATE_AND_DEPLOY.ps1` (Windows)
```powershell
# Pull latest image
ssh tommy@192.168.1.7 "cd ~/financial-analysis-mcp && docker-compose pull"

# Restart container
ssh tommy@192.168.1.7 "cd ~/financial-analysis-mcp && docker-compose up -d"

# Check status
ssh tommy@192.168.1.7 "docker-compose -f ~/financial-analysis-mcp/docker-compose.yml ps"
```

---

## Monitoring

### Container Status
```bash
docker-compose ps
```

### Logs
```bash
# Follow logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Specific service
docker-compose logs financial-analysis-mcp
```

### Resource Usage
```bash
# Container stats
docker stats financial-analysis-mcp

# Disk usage
docker system df
```

### Health Check
```bash
# Test endpoint
curl http://192.168.1.7:8000/tools/list

# Full test
curl -X POST http://192.168.1.7:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"get_current_price","arguments":{"ticker":"AAPL"}}'
```

---

## Backup and Restore

### Backup Data
```bash
# Backup tickers.csv
scp tommy@192.168.1.7:~/financial-analysis-mcp/data/tickers.csv \
    ./backup/tickers-$(date +%Y%m%d).csv

# Backup entire data directory
ssh tommy@192.168.1.7 "tar -czf /tmp/financial-mcp-data.tar.gz -C ~/financial-analysis-mcp/data ."
scp tommy@192.168.1.7:/tmp/financial-mcp-data.tar.gz ./backup/
```

### Restore Data
```bash
# Restore tickers.csv
scp ./backup/tickers-20260519.csv \
    tommy@192.168.1.7:~/financial-analysis-mcp/data/tickers.csv

# Restore entire data directory
scp ./backup/financial-mcp-data.tar.gz tommy@192.168.1.7:/tmp/
ssh tommy@192.168.1.7 "tar -xzf /tmp/financial-mcp-data.tar.gz -C ~/financial-analysis-mcp/data"
```

### Docker Image Backup
```bash
# Save image
docker save ghcr.io/tommypopescu/financial-analysis-mcp:latest | gzip > financial-mcp-image.tar.gz

# Load image
docker load < financial-mcp-image.tar.gz
```

---

## Troubleshooting Deployment

### Container Won't Start

**Check logs**:
```bash
docker-compose logs
```

**Common issues**:
- Port 8000 already in use
- Insufficient permissions
- Missing data directory

**Solutions**:
```bash
# Check port usage
sudo netstat -tulpn | grep 8000

# Fix permissions
sudo chown -R tommy:tommy ~/financial-analysis-mcp

# Create data directory
mkdir -p ~/financial-analysis-mcp/data
```

### Cannot Connect from Bob

**Check network**:
```bash
# From Windows
ping 192.168.1.7
curl http://192.168.1.7:8000/tools/list
```

**Check firewall**:
```bash
# On OMV server
sudo ufw status
sudo ufw allow 8000/tcp
```

**Check wrapper**:
```powershell
# Test wrapper directly
python C:\Users\O82652826\financial-analysis-mcp-wrapper.py
# Then type: {"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}
```

### Slow Performance

**Check resources**:
```bash
docker stats financial-analysis-mcp
```

**Increase resources** (docker-compose.yml):
```yaml
services:
  financial-analysis-mcp:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

### Data Not Persisting

**Check volume mount**:
```bash
docker inspect financial-analysis-mcp | grep -A 10 Mounts
```

**Fix volume**:
```bash
docker-compose down
docker volume rm financial-analysis-mcp_data
docker-compose up -d
```

---

## Security Best Practices

### 1. Network Security
- Keep server on local network only
- Use firewall rules to restrict access
- Consider VPN for remote access

### 2. Container Security
- Run as non-root user (already configured)
- Keep Docker updated
- Scan images for vulnerabilities

### 3. Data Security
- Regular backups of tickers.csv
- Secure SSH keys
- Use environment variables for secrets

### 4. Access Control
- Limit SSH access to OMV server
- Use strong passwords
- Enable 2FA where possible

---

## Performance Optimization

### 1. Docker Configuration
```yaml
# docker-compose.yml
services:
  financial-analysis-mcp:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### 2. Caching Strategy
Future enhancement: Add Redis for caching
```yaml
services:
  redis:
    image: redis:alpine
    volumes:
      - redis-data:/data
```

### 3. Log Rotation
```yaml
services:
  financial-analysis-mcp:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## Multi-Environment Setup

### Development
```bash
# Use local Python
python src/server_http.py
```

### Staging
```bash
# Use Docker with test data
docker-compose -f docker-compose.staging.yml up -d
```

### Production
```bash
# Use Docker with production data
docker-compose up -d
```

---

## Related Documentation

- [Architecture](01-architecture.md) - System design
- [API Reference](02-api-reference.md) - Tool documentation
- [Troubleshooting](04-troubleshooting.md) - Common issues
- [Development](05-development.md) - Making changes