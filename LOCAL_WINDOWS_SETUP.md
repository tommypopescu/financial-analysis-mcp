# Financial Analysis MCP - Local Windows Setup

## Problema Actuală

Serverul MCP funcționează corect pe server (192.168.1.7), dar Bob are probleme de compatibilitate când se conectează via SSH + Docker. Serverul primește cereri dar răspunde cu erori de validare.

## Soluție: Rulare Locală pe Windows

În loc să ruleze serverul remote, îl vom rula **local pe Windows** unde Bob rulează.

### Pasul 1: Instalează Python 3.11+

Verifică dacă ai Python instalat:
```powershell
python --version
```

Dacă nu ai Python sau versiunea este < 3.11, descarcă de la: https://www.python.org/downloads/

### Pasul 2: Clonează Repository-ul

```powershell
cd C:\Users\O82652826
git clone https://github.com/tommypopescu/financial-analysis-mcp.git
cd financial-analysis-mcp
```

### Pasul 3: Creează Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Pasul 4: Instalează Dependencies

```powershell
pip install -r requirements.txt
```

### Pasul 5: Testează Serverul Local

```powershell
python -m src.server
```

Ar trebui să vezi:
```
2026-05-19 11:00:00,000 - __main__ - INFO - Starting Financial Analysis MCP Server...
2026-05-19 11:00:00,000 - __main__ - INFO - Server is ready and waiting for connections...
```

Apasă `Ctrl+C` pentru a opri serverul.

### Pasul 6: Configurează Bob pentru Local

Editează `C:\Users\O82652826\.bob\settings\mcp_settings.json`:

```json
{
  "mcpServers": {
    "financial-analysis": {
      "type": "stdio",
      "command": "C:\\Users\\O82652826\\financial-analysis-mcp\\venv\\Scripts\\python.exe",
      "args": [
        "-m",
        "src.server"
      ],
      "cwd": "C:\\Users\\O82652826\\financial-analysis-mcp",
      "env": {
        "LOG_LEVEL": "INFO"
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

**Notă**: Ajustează path-urile dacă ai clonat repository-ul într-o altă locație.

### Pasul 7: Restartează Bob

După modificarea configurației, restartează Bob complet.

### Pasul 8: Testează în Bob

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

## Avantaje Rulare Locală

✅ **Fără probleme SSH** - Nu mai depinde de conexiune SSH  
✅ **Fără probleme Docker** - Rulează direct pe Windows  
✅ **Mai rapid** - Nu mai există latență de rețea  
✅ **Mai ușor de debugat** - Logs direct în terminal  
✅ **Compatibilitate perfectă** - Aceeași versiune MCP SDK ca Bob  

## Troubleshooting

### Problema: "python: command not found"

**Soluție**: Instalează Python 3.11+ de la python.org și asigură-te că este în PATH.

### Problema: "pip install failed"

**Soluție**: 
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Problema: "Module not found: mcp"

**Soluție**: Asigură-te că virtual environment este activat:
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Problema: Bob încă nu vede serverul

**Soluție**:
1. Verifică că path-urile din `mcp_settings.json` sunt corecte
2. Verifică că virtual environment există la path-ul specificat
3. Testează manual: `C:\Users\O82652826\financial-analysis-mcp\venv\Scripts\python.exe -m src.server`
4. Restartează Bob complet

## Verificare Configurație

### Test 1: Python și Virtual Environment
```powershell
cd C:\Users\O82652826\financial-analysis-mcp
.\venv\Scripts\Activate.ps1
python --version  # Ar trebui să fie 3.11+
```

### Test 2: Dependencies
```powershell
python -c "import mcp; import yfinance; import pandas; print('All dependencies OK')"
```

### Test 3: Server Pornește
```powershell
python -m src.server
# Ar trebui să vezi "Starting Financial Analysis MCP Server..."
# Apasă Ctrl+C pentru a opri
```

### Test 4: Bob Config
Verifică că fișierul `mcp_settings.json` conține configurația corectă și path-urile sunt valide.

## Comparație: Remote vs Local

| Aspect | Remote (SSH + Docker) | Local (Windows) |
|--------|----------------------|-----------------|
| Setup | Complex (SSH keys, Docker) | Simplu (Python + pip) |
| Latență | ~50-100ms | <1ms |
| Debugging | Dificil (logs remote) | Ușor (logs local) |
| Compatibilitate | Probleme versiune MCP | Perfect compatibil |
| Mentenanță | Docker updates | pip updates |
| **Recomandat** | ❌ Nu | ✅ **Da** |

## Concluzie

Rularea locală pe Windows este **soluția recomandată** pentru integrarea cu Bob. Este mai simplă, mai rapidă, și elimină toate problemele de compatibilitate SSH/Docker.

Serverul Docker pe 192.168.1.7 poate rămâne pentru alte scopuri (API HTTP în viitor, testing, etc.), dar pentru Bob, rularea locală este cea mai bună opțiune.

---

**Made with Bob** 🤖