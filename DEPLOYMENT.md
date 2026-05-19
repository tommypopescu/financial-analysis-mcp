port 300# 🚀 Deployment Guide - Financial Analysis MCP Server

Ghid complet pentru deployment pe server OMV cu Git CI/CD pipeline.

## 📋 Prerequisite

### Pe Serverul OMV
- Docker și Docker Compose instalate
- Git instalat
- Acces SSH configurat
- Port 3000 disponibil (sau alt port configurat)

### Pe GitHub
- Repository creat: `https://github.com/tommypopescu/fin.git`
- Secrets configurate (vezi mai jos)

## 🔐 Configurare GitHub Secrets

În repository-ul GitHub, mergi la **Settings → Secrets and variables → Actions** și adaugă:

```
OMV_HOST=<IP sau hostname server OMV>
OMV_USER=<username SSH>
OMV_SSH_KEY=<private SSH key pentru autentificare>
DOCKER_USERNAME=<Docker Hub username> (opțional)
DOCKER_PASSWORD=<Docker Hub password/token> (opțional)
```

## 📁 Structura Repository

```
fin/
├── financial-analysis-mcp/     # MCP Server
│   ├── src/
│   ├── data/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── ...
├── fin/                        # Script-ul original
│   └── rsi_macd_gui_enhanced_v7.7.5_with_dropdown_fixed.py
└── .github/
    └── workflows/
        └── ci-cd.yml
```

## 🔧 Setup Inițial

### 1. Pregătire Locală

```bash
# Clonează repository-ul (dacă nu l-ai făcut deja)
git clone https://github.com/tommypopescu/fin.git
cd fin

# Verifică structura
ls -la financial-analysis-mcp/

# Creează fișierul .env din template
cd financial-analysis-mcp
cp .env.example .env

# Editează .env cu setările tale (opțional)
nano .env
```

### 2. Test Local cu Docker

```bash
# Build imagine Docker
docker build -t financial-mcp:latest .

# Rulează cu docker-compose
docker-compose up -d

# Verifică logs
docker-compose logs -f

# Test funcționalitate (în alt terminal)
# Serverul ar trebui să răspundă pe port 3000

# Oprește pentru deployment
docker-compose down
```

### 3. Commit și Push

```bash
# Adaugă toate fișierele
git add .

# Commit
git commit -m "Add Financial Analysis MCP Server with Docker and CI/CD"

# Push la GitHub
git push origin main
```

## 🔄 CI/CD Pipeline Automată

### Workflow-ul Automată

Când faci push pe branch `main`, GitHub Actions va:

1. **Test** - Rulează teste (dacă există)
2. **Build** - Construiește imaginea Docker
3. **Push** - Împinge imaginea în Docker Hub (opțional)
4. **Deploy** - Deployează automat pe serverul OMV

### Monitorizare Pipeline

1. Mergi la repository pe GitHub
2. Click pe tab-ul **Actions**
3. Vezi status-ul workflow-ului
4. Click pe run pentru detalii și logs

## 🖥️ Setup pe Serverul OMV

### Pregătire Inițială (O singură dată)

```bash
# Conectează-te la server OMV
ssh user@omv-server

# Creează director pentru deployment
mkdir -p ~/deployments/financial-mcp
cd ~/deployments/financial-mcp

# Clonează repository-ul
git clone https://github.com/tommypopescu/fin.git .

# Navighează la directorul MCP
cd financial-analysis-mcp

# Creează directoare necesare
mkdir -p data logs

# Creează fișier .env
cp .env.example .env
nano .env  # Editează cu setările pentru producție
```

### Deployment Manual (Prima dată sau pentru debug)

```bash
# Pe serverul OMV
cd ~/deployments/financial-mcp/financial-analysis-mcp

# Pull ultimele schimbări
git pull origin main

# Build și start
docker-compose up -d --build

# Verifică status
docker-compose ps

# Vezi logs
docker-compose logs -f

# Test funcționalitate
docker-compose exec financial-mcp python -c "import yfinance; print('OK')"
```

## 🔄 Deployment Automat via CI/CD

După configurarea inițială, deployment-ul este automat:

