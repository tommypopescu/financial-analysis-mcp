# Configurare Bob pentru Financial Analysis MCP Server

## Status Container
✅ Container rulează stabil pe `192.168.1.7`
✅ Nu mai există crash loops
✅ Gata pentru integrare cu Bob

## Configurare MCP în Bob

### Pasul 1: Editează fișierul de configurare Bob

Pe mașina unde rulează Bob (probabil Windows), editează fișierul:
```
C:\Users\O82652826\.bob\mcp.json
```

### Pasul 2: Adaugă configurația MCP

Adaugă următoarea configurație în `mcp.json`:

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
      ],
      "env": {
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**Notă**: Înlocuiește `user@192.168.1.7` cu username-ul tău SSH real de pe serverul OMV.

### Alternativă: Dacă Bob rulează pe același server (192.168.1.7)

Dacă Bob rulează direct pe serverul OMV, folosește această configurație mai simplă:

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

## Testare

### 1. Verifică că Bob vede serverul MCP

După ce salvezi configurația, restartează Bob și verifică că serverul MCP este disponibil.

### 2. Testează cu comenzi simple

Încearcă următoarele comenzi în Bob:

**Română:**
```
Analizează acțiunea AAPL
```

```
Arată-mi indicatorii tehnici pentru TSLA
```

```
Care este prețul curent al BTC-USD?
```

**Engleză:**
```
Analyze AAPL stock
```

```
Show me technical indicators for TSLA
```

```
What's the current price of BTC-USD?
```

## Tool-uri Disponibile

Serverul MCP oferă următoarele 10 tool-uri:

1. **fetch_ticker_data** - Extrage date istorice pentru un ticker
2. **get_current_price** - Obține prețul curent
3. **calculate_rsi** - Calculează RSI (Relative Strength Index)
4. **calculate_macd** - Calculează MACD (Moving Average Convergence Divergence)
5. **calculate_adx** - Calculează ADX (Average Directional Index)
6. **calculate_all_indicators** - Calculează toți indicatorii tehnici
7. **generate_investment_summary** - Generează rezumat complet de investiție
8. **list_tickers** - Listează ticker-ele din watchlist
9. **add_ticker** - Adaugă ticker în watchlist
10. **screen_tickers** - Scanează multiple ticker-e

## Indicatori Tehnici Implementați

- **RSI** (Relative Strength Index) - 14 perioade
- **MACD** (12, 26, 9)
- **ADX** (Average Directional Index) - 14 perioade
- **Supertrend** (10, 3.0)
- **Stochastic Oscillator** (14, 3, 3)
- **Bollinger Bands** (20, 2)
- **OBV** (On-Balance Volume)
- **MFI** (Money Flow Index) - 14 perioade

## Exemple de Utilizare

### Analiză Completă
```
Bob, folosește tool-ul generate_investment_summary pentru AAPL cu perioada de 6 luni
```

### Verificare Rapidă
```
Bob, verifică prețul curent pentru MSFT și calculează RSI
```

### Screening Multiple Acțiuni
```
Bob, scanează acțiunile AAPL, MSFT, GOOGL, TSLA și arată-mi care au RSI sub 30
```

## Troubleshooting

### Problema: Bob nu vede serverul MCP
**Soluție**: Verifică că:
- Fișierul `mcp.json` este valid JSON
- Path-ul către container este corect
- Containerul rulează: `docker ps | grep financial-analysis-mcp`

### Problema: Erori de conexiune SSH
**Soluție**: 
- Verifică că poți face SSH manual: `ssh user@192.168.1.7`
- Asigură-te că ai chei SSH configurate (fără parolă)

### Problema: Tool-urile nu funcționează
**Soluție**:
- Verifică logs: `docker logs financial-analysis-mcp`
- Testează manual: `docker exec -i financial-analysis-mcp python -m src.server`

## Arhitectură

```
Bob (Windows) 
    ↓ SSH
OMV Server (192.168.1.7)
    ↓ docker exec -i
Container: financial-analysis-mcp
    ↓ stdio (stdin/stdout)
MCP Server (Python)
    ↓ yfinance API
Yahoo Finance
```

## Note Importante

1. **Portul 3000 NU este folosit** - MCP folosește stdio, nu HTTP
2. **Containerul trebuie să ruleze** înainte ca Bob să se conecteze
3. **SSH trebuie configurat** dacă Bob rulează pe altă mașină
4. **Datele sunt cached** în `/app/data` pentru performanță
5. **Logs sunt în** `/app/logs` pentru debugging

## Next Steps

După ce configurezi Bob:
1. Testează cu o comandă simplă
2. Verifică că tool-urile funcționează
3. Începe să folosești analiza automată de investiții!

---
Made with Bob 🤖
