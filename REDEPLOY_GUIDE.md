# 🚀 Redeploy Guide - Financial Analysis MCP Server

## Ce am făcut

### 1. **Fix DataFrame MultiIndex Bug** ✅
Am rezolvat eroarea `'DataFrame' object has no attribute 'tolist'` care apărea când yfinance returna coloane MultiIndex.

**Fișier modificat:** `src/tools/data_extraction.py` (liniile 73-95)

**Schimbări:**
```python
# Handle MultiIndex columns (yfinance sometimes returns this format)
if isinstance(df.columns, pd.MultiIndex):
    # Flatten MultiIndex to single level - take the first level (field names)
    df.columns = df.columns.get_level_values(0)

# Convert DataFrame to dict format
# Use .values.tolist() to ensure we get a list even if column is a Series
data_dict = {
    'dates': df.index.strftime('%Y-%m-%d').tolist(),
    'open': df['Open'].values.tolist() if 'Open' in df.columns else [],
    'high': df['High'].values.tolist() if 'High' in df.columns else [],
    'low': df['Low'].values.tolist() if 'Low' in df.columns else [],
    'close': df['Close'].values.tolist() if 'Close' in df.columns else [],
    'volume': df['Volume'].values.tolist() if 'Volume' in df.columns else []
}
```

### 2. **Adăugat Tickere Românești și Germane** ✅
Am actualizat `data/tickers.csv` cu tickerele tale:

**Tickere Germane:**
- 4GLD.DE
- SEC0.DE
- SXR8.DE
- QDV5.DE

**Tickere Românești:**
- AQ.RO, AROBS.RO, DIGI.RO, DN.RO, EL.RO
- ONE.RO, SFG.RO, SNG.RO, SNP.RO, TEL.RO
- TGN.RO, TLV.RO, TRP.RO, BIO.RO, PE.RO
- M.RO, SNN.RO

### 3. **Push pe GitHub** ✅
Codul a fost push-at cu succes pe GitHub. GitHub Actions construiește acum imaginea Docker nouă.

---

## 📋 Pași pentru Redeploy

### Pasul 1: Verifică Build-ul GitHub Actions

1. Deschide: https://github.com/tommypopescu/financial-analysis-mcp/actions
2. Verifică că ultimul workflow "Build and Push Docker Image" este **verde** (✓)
3. Durează ~2-3 minute

### Pasul 2: Redeploy pe OMV Server

Rulează aceste comenzi pentru a actualiza containerul:

```powershell
# Conectează-te la OMV și redeploy
ssh tommy@192.168.1.7 "cd /srv/dev-disk-by-uuid-d76a33c0-e0e0-4a8f-9e1e-e0e0e0e0e0e0/docker/financial-analysis-mcp && docker-compose -f docker-compose.http.yml down && docker pull ghcr.io/tommypopescu/financial-analysis-mcp:latest && docker-compose -f docker-compose.http.yml up -d"
```

**SAU** conectează-te manual:

```bash
# 1. Conectează-te la OMV
ssh tommy@192.168.1.7

# 2. Navighează la directorul Docker
cd /srv/dev-disk-by-uuid-d76a33c0-e0e0-4a8f-9e1e-e0e0e0e0e0e0/docker/financial-analysis-mcp

# 3. Oprește containerul vechi
docker-compose -f docker-compose.http.yml down

# 4. Pull imaginea nouă
docker pull ghcr.io/tommypopescu/financial-analysis-mcp:latest

# 5. Pornește containerul nou
docker-compose -f docker-compose.http.yml up -d

# 6. Verifică logs
docker-compose -f docker-compose.http.yml logs --tail=50
```

### Pasul 3: Verifică că Serverul Funcționează

```powershell
# Test health endpoint
curl http://192.168.1.7:8000/health

# Ar trebui să returneze:
# {"status":"healthy"}
```

### Pasul 4: Testează cu Bob

Acum poți testa cu Bob folosind comenzi precum:

```
Analizează acțiunea AAPL
Analizează acțiunea SNG.RO
Analizează acțiunea 4GLD.DE
Listează toate tickerele
```

---

## 🔍 Troubleshooting

### Dacă serverul nu pornește:

```bash
# Verifică logs pentru erori
docker-compose -f docker-compose.http.yml logs

# Verifică status container
docker ps -a | grep financial-analysis
```

### Dacă Bob nu se poate conecta:

1. Verifică că wrapper-ul rulează corect:
   ```powershell
   python C:\Users\O82652826\financial-analysis-mcp-wrapper.py
   ```

2. Verifică configurația Bob în:
   - `C:\Users\O82652826\.bob\settings\mcp_settings.json`

3. Restart Bob (închide și redeschide VS Code)

---

## 📊 Ce Funcționează Acum

✅ **DataFrame MultiIndex handling** - Nu mai apare eroarea `.tolist()`
✅ **Tickere românești** - Poți analiza SNG.RO, DIGI.RO, etc.
✅ **Tickere germane** - Poți analiza 4GLD.DE, SEC0.DE, etc.
✅ **Tickere americane** - AAPL, MSFT, GOOGL, TSLA, AMZN
✅ **Toate tool-urile MCP** - fetch_ticker_data, calculate_all_indicators, generate_investment_summary, etc.

---

## 🎯 Next Steps

După redeploy, testează cu Bob:

1. **Test simplu:**
   ```
   Listează toate tickerele
   ```

2. **Test analiză americană:**
   ```
   Analizează acțiunea AAPL
   ```

3. **Test analiză românească:**
   ```
   Analizează acțiunea SNG.RO
   ```

4. **Test analiză germană:**
   ```
   Analizează acțiunea 4GLD.DE
   ```

---

## 📝 Notițe

- **GitHub Repository:** https://github.com/tommypopescu/financial-analysis-mcp
- **Docker Image:** ghcr.io/tommypopescu/financial-analysis-mcp:latest
- **Server URL:** http://192.168.1.7:8000
- **Wrapper Local:** C:\Users\O82652826\financial-analysis-mcp-wrapper.py

---

**Made with Bob** 🤖