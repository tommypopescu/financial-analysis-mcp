# 📚 Documentație Financial Analysis MCP Server

Bine ai venit la documentația completă pentru Financial Analysis MCP Server - un server MCP (Model Context Protocol) pentru analiza financiară automată folosind AI.

## 📖 Cuprins

### 1. [MCP Server](./mcp-server/)
Documentație tehnică completă despre serverul MCP:
- **[01-architecture.md](./mcp-server/01-architecture.md)** - Arhitectura și design-ul sistemului
- **[02-api-reference.md](./mcp-server/02-api-reference.md)** - Referință completă API pentru toate tool-urile
- **[03-deployment.md](./mcp-server/03-deployment.md)** - Ghid deployment Docker și OMV
- **[04-troubleshooting.md](./mcp-server/04-troubleshooting.md)** - Rezolvarea problemelor comune
- **[05-development.md](./mcp-server/05-development.md)** - Ghid pentru dezvoltare și extindere

### 2. [Financial Analyst Mode](./financial-analyst-mode/)
Documentație despre modul specializat de analiză financiară pentru Bob:
- **[01-overview.md](./financial-analyst-mode/01-overview.md)** - Prezentare generală și capabilități
- **[02-configuration.md](./financial-analyst-mode/02-configuration.md)** - Configurare completă
- **[03-workflow.md](./financial-analyst-mode/03-workflow.md)** - Framework de analiză în 5 faze
- **[04-usage-guide.md](./financial-analyst-mode/04-usage-guide.md)** - Ghid de utilizare pas cu pas
- **[05-examples.md](./financial-analyst-mode/05-examples.md)** - Exemple reale de analiză

### 3. [Bob Configuration](./bob-configuration/)
Documentație despre configurarea Bob AI Assistant:
- **[README.md](./bob-configuration/README.md)** - Index configurații Bob
- **[custom-modes.md](./bob-configuration/custom-modes.md)** - Documentație custom_modes.yaml
- **[mcp-wrapper.md](./bob-configuration/mcp-wrapper.md)** - Wrapper stdio-to-HTTP
- **[workflow-instructions.md](./bob-configuration/workflow-instructions.md)** - Instrucțiuni workflow XML

### 4. [AI Context](./ai-context/)
Context pentru AI assistants (Bob, Claude, etc.) pentru modificări viitoare:
- **[README.md](./ai-context/README.md)** - Ghid pentru AI assistants
- **[01-project-overview.md](./ai-context/01-project-overview.md)** - Overview complet proiect
- **[02-technical-decisions.md](./ai-context/02-technical-decisions.md)** - Decizii tehnice și rațiuni
- **[03-modification-guide.md](./ai-context/03-modification-guide.md)** - Ghid pentru modificări
- **[04-troubleshooting-history.md](./ai-context/04-troubleshooting-history.md)** - Istoric probleme rezolvate

## 🚀 Quick Start

### Pentru Utilizatori
1. Citește [Financial Analyst Mode - Usage Guide](./financial-analyst-mode/04-usage-guide.md)
2. Vezi [Exemple de Analiză](./financial-analyst-mode/05-examples.md)
3. Consultă [Troubleshooting](./mcp-server/04-troubleshooting.md) dacă întâmpini probleme

### Pentru Dezvoltatori
1. Citește [Architecture](./mcp-server/01-architecture.md) pentru înțelegerea sistemului
2. Consultă [API Reference](./mcp-server/02-api-reference.md) pentru detalii tehnice
3. Urmează [Development Guide](./mcp-server/05-development.md) pentru extindere

### Pentru AI Assistants
1. Începe cu [AI Context - README](./ai-context/README.md)
2. Citește [Project Overview](./ai-context/01-project-overview.md)
3. Consultă [Modification Guide](./ai-context/03-modification-guide.md) înainte de modificări

## 🎯 Capabilități Principale

### Analiza Tehnică
- **7 Indicatori Tehnici**: EMA50/200, RSI, MACD, ADX, Stochastic, Bollinger Bands, MFI
- **Analiza Trend-urilor**: Identificare automată trend bullish/bearish/neutral
- **Suport/Rezistență**: Detectare nivele cheie de preț

### Analiza Fundamentală
- **Date Financiare**: Preț curent, volum, capitalizare de piață
- **Istoric Prețuri**: Date istorice pentru orice perioadă
- **Comparații**: Analiza relativă între multiple acțiuni

### Recomandări Investiții
- **Framework 5 Faze**: Colectare Date → Analiză Tehnică → Planificare Scenarii → Evaluare Risc → Decizie
- **Verdicts Clare**: BUY/HOLD/SELL cu justificare detaliată
- **Managementul Riscului**: Recomandări pentru poziționare și diversificare

## 📊 Arhitectură

```
Financial Analysis MCP Server
├── HTTP Transport (FastAPI)
│   ├── Port: 8000
│   └── Endpoint: /mcp
├── Tools (9 tool-uri disponibile)
│   ├── fetch_ticker_data
│   ├── get_current_price
│   ├── calculate_all_indicators
│   ├── generate_investment_summary
│   ├── list_tickers
│   ├── add_ticker
│   └── screen_tickers
├── Data Layer (yfinance)
│   └── Yahoo Finance API
└── Bob Integration
    ├── Stdio Wrapper (Python)
    └── Financial Analyst Mode
```

## 🔧 Deployment

Serverul rulează în Docker pe OMV (192.168.1.7:8000):
```bash
docker run -d \
  --name financial-analysis-mcp \
  -p 8000:8000 \
  --restart unless-stopped \
  tommypopescu/financial-analysis-mcp:latest
```

## 📝 Contribuții

Pentru modificări sau îmbunătățiri:
1. Consultă [Development Guide](./mcp-server/05-development.md)
2. Citește [Technical Decisions](./ai-context/02-technical-decisions.md)
3. Urmează [Modification Guide](./ai-context/03-modification-guide.md)

## 🐛 Probleme Cunoscute

Vezi [Troubleshooting History](./ai-context/04-troubleshooting-history.md) pentru:
- Probleme rezolvate anterior
- Soluții testate
- Lecții învățate

## 📞 Suport

Pentru probleme sau întrebări:
1. Consultă [Troubleshooting Guide](./mcp-server/04-troubleshooting.md)
2. Verifică [Troubleshooting History](./ai-context/04-troubleshooting-history.md)
3. Creează un issue pe GitHub

## 📄 Licență

Acest proiect este open-source și disponibil pentru uz personal și educațional.

---

**Ultima actualizare**: Mai 2026  
**Versiune**: 1.0.0  
**Autor**: Tommy Popescu