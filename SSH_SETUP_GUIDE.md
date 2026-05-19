# SSH Keys Setup Guide pentru Bob MCP Integration

## Problema
Bob nu poate conecta la serverul MCP pentru că SSH cere parolă interactiv, iar Bob nu poate introduce parola.

## Soluția: SSH Keys fără Parolă

### Pasul 1: Generează SSH Keys pe Windows

Deschide PowerShell ca Administrator și rulează:

```powershell
# Verifică dacă ai deja SSH keys
Test-Path ~\.ssh\id_rsa.pub

# Dacă nu există, generează-le (apasă Enter la toate întrebările pentru a accepta default-urile)
ssh-keygen -t rsa -b 4096 -C "bob-mcp-client"
```

**IMPORTANT**: Când te întreabă "Enter passphrase", apasă Enter (lasă gol) pentru a crea o cheie fără parolă.

### Pasul 2: Copiază Cheia Publică pe Server

```powershell
# Afișează cheia publică
Get-Content ~\.ssh\id_rsa.pub
```

Copiază output-ul (începe cu `ssh-rsa ...`).

### Pasul 3: Adaugă Cheia pe Serverul OMV

Conectează-te la server cu parolă (ultima dată):

```powershell
ssh root@192.168.1.7
```

Pe server, rulează:

```bash
# Creează directorul .ssh dacă nu există
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Adaugă cheia publică
echo "PASTE_YOUR_PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# Ieși din server
exit
```

### Pasul 4: Testează Conexiunea fără Parolă

```powershell
# Ar trebui să se conecteze fără să ceară parolă
ssh root@192.168.1.7 "echo 'SSH keys work!'"
```

Dacă vezi "SSH keys work!" fără să introducă parolă, configurarea este corectă! ✅

### Pasul 5: Testează MCP Server

```powershell
# Testează că poți porni MCP server-ul
ssh root@192.168.1.7 "docker exec -i financial-analysis-mcp python -m src.server"
```

Ar trebui să vezi output-ul MCP server-ului.

---

## Configurare Bob MCP (După SSH Keys Setup)

După ce SSH keys funcționează, configurația Bob din `mcp_settings.json` va funcționa automat:

```json
{
  "mcpServers": {
    "financial-analysis": {
      "type": "stdio",
      "command": "ssh",
      "args": [
        "root@192.168.1.7",
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

---

## Troubleshooting

### Problema: SSH încă cere parolă

**Cauze posibile:**
1. Cheia publică nu a fost adăugată corect în `~/.ssh/authorized_keys`
2. Permisiunile sunt greșite pe server
3. SSH agent nu rulează pe Windows

**Soluții:**

#### Verifică permisiunile pe server:
```bash
ssh root@192.168.1.7
ls -la ~/.ssh/
# Ar trebui să vezi:
# drwx------ (700) pentru .ssh/
# -rw------- (600) pentru authorized_keys
```

#### Pornește SSH agent pe Windows:
```powershell
# Verifică dacă SSH agent rulează
Get-Service ssh-agent

# Dacă nu rulează, pornește-l
Start-Service ssh-agent
Set-Service -Name ssh-agent -StartupType Automatic

# Adaugă cheia
ssh-add ~\.ssh\id_rsa
```

### Problema: "Connection closed" în Bob

**Cauze:**
1. SSH keys nu sunt configurate corect
2. Containerul nu rulează
3. Path-ul către Python sau src.server este greșit

**Verificări:**

```powershell
# 1. Verifică că SSH funcționează fără parolă
ssh root@192.168.1.7 "echo test"

# 2. Verifică că containerul rulează
ssh root@192.168.1.7 "docker ps | grep financial-analysis-mcp"

# 3. Testează MCP server manual
ssh root@192.168.1.7 "docker exec -i financial-analysis-mcp python -m src.server"
```

### Problema: Bob nu vede serverul MCP

**Soluție:**
1. Restartează Bob după modificarea `mcp_settings.json`
2. Verifică că JSON-ul este valid (fără virgule în plus, ghilimele corecte)
3. Verifică logs-urile Bob pentru erori

---

## Alternativă: SSH Config File

Pentru o configurație mai curată, poți crea un fișier SSH config:

**Locație:** `C:\Users\O82652826\.ssh\config`

```
Host omv-server
    HostName 192.168.1.7
    User root
    IdentityFile ~/.ssh/id_rsa
    StrictHostKeyChecking no
```

Apoi în `mcp_settings.json` folosește:

```json
{
  "command": "ssh",
  "args": [
    "omv-server",
    "docker",
    "exec",
    "-i",
    "financial-analysis-mcp",
    "python",
    "-m",
    "src.server"
  ]
}
```

---

## Verificare Finală

După configurare, testează tot flow-ul:

```powershell
# 1. SSH fără parolă
ssh root@192.168.1.7 "echo 'Step 1: SSH works'"

# 2. Container rulează
ssh root@192.168.1.7 "docker ps | grep financial-analysis-mcp"

# 3. MCP server pornește
ssh root@192.168.1.7 "docker exec -i financial-analysis-mcp python -c 'import mcp; print(\"Step 3: MCP imports work\")'"

# 4. Testează în Bob
# Deschide Bob și încearcă: "Analizează acțiunea AAPL"
```

---

## Checklist

- [ ] SSH keys generate pe Windows
- [ ] Cheie publică copiată pe server
- [ ] Permisiuni corecte pe server (700 pentru .ssh, 600 pentru authorized_keys)
- [ ] SSH funcționează fără parolă
- [ ] Container financial-analysis-mcp rulează
- [ ] MCP server poate fi pornit manual via SSH
- [ ] Bob MCP config actualizat în mcp_settings.json
- [ ] Bob restartat după modificarea config-ului
- [ ] Test în Bob: "Analizează acțiunea AAPL"

---

**Made with Bob** 🤖