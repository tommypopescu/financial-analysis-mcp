# Portfolio Management - Testing Guide

## Obiectiv Principal
Să analizăm cum să investim cash-ul disponibil (0.98% RON) în mod optim, ținând cont de:
- Portofoliul existent (17 poziții)
- Alocările țintă (target allocations)
- Oportunități de rebalansare
- Analiza tehnică a ticker-elor

## Situația Actuală

### Portfolio1 - Main Family Portfolio
**Total Holdings**: 17 Romanian stocks
**Cash Disponibil**: 0.98% RON (pentru investiții noi)
**Titluri de Stat**: 15.21% (R3207AE, R3508AE, R3509AE, R3511AE) - NU se analizează

### Poziția Dominantă - Necesită Rebalansare
- **TLV.RO (Banca Transilvania)**: 48.46% actual vs 40% țintă
  - **OVERWEIGHT cu 8.46%** - trebuie redusă prin diversificare

### Top 5 Holdings
1. TLV.RO: 48.46% (țintă: 40%) - **REDUCE**
2. SNP.RO: 7.25% (țintă: 8%) - aproape de țintă
3. DIGI.RO: 5.93% (țintă: 7%) - **INCREASE**
4. EL.RO: 3.52% (țintă: 5%) - **INCREASE**
5. TEL.RO: 3.05% (țintă: 4%) - **INCREASE**

### Sectoare
- **Financiare**: 48.46% (TLV) + 1.53% (ONE) = 49.99% - DOMINANT
- **Energie**: 7.25% (SNP) + 2.41% (SNG) + 1.70% (SNN) + 0.38% (PE) = 11.74%
- **Utilități**: 3.52% (EL) + 3.05% (TEL) + 1.14% (TGN) = 7.71%
- **Comunicații**: 5.93% (DIGI)
- **Tehnologie**: 1.06% (AROBS)
- **Diverse**: 2.88% (DN) + 2.86% (AQ) + 1.07% (SFG) + 0.44% (M) + 0.12% (TRP) + 0.03% (EAI) = 7.40%

## Tool-uri Disponibile

### 1. `list_portfolios`
Lista toate portofoliile cu informații sumare.

**Test Command pentru Bob**:
```
Folosește tool-ul list_portfolios pentru a vedea portofoliile disponibile
```

**Expected Output**:
- portfolio1: Main Family Portfolio
- Total value, number of holdings
- Last updated date

---

### 2. `get_portfolio`
Obține detalii complete despre un portofoliu specific.

**Test Command pentru Bob**:
```
Folosește get_portfolio cu portfolio_id="portfolio1" pentru a vedea toate holdings și alocările curente
```

**Expected Output**:
- Lista completă de 17 holdings cu shares, avg_price, current_price
- Current allocations (%)
- Target allocations (%)
- Deviations from target
- Cash position

---

### 3. `analyze_portfolio_allocation`
Analizează alocările curente vs țintă și generează recomandări de rebalansare.

**Test Command pentru Bob**:
```
Folosește analyze_portfolio_allocation cu portfolio_id="portfolio1" pentru a vedea ce poziții trebuie rebalansate
```

**Expected Output**:
- **OVERWEIGHT positions**: TLV.RO (48.46% vs 40% target) = +8.46%
- **UNDERWEIGHT positions**: 
  - DIGI.RO (5.93% vs 7% target) = -1.07%
  - EL.RO (3.52% vs 5% target) = -1.48%
  - TEL.RO (3.05% vs 4% target) = -0.95%
  - SNG.RO (2.41% vs 5% target) = -2.59%
  - SNN.RO (1.70% vs 3% target) = -1.30%
  - AROBS.RO (1.06% vs 3% target) = -1.94%
  - M.RO (0.44% vs 2% target) = -1.56%
  - PE.RO (0.38% vs 2% target) = -1.62%
  - ONE.RO (1.53% vs 3% target) = -1.47%
  - TGN.RO (1.14% vs 2% target) = -0.86%
  - SFG.RO (1.07% vs 2% target) = -0.93%
  - TRP.RO (0.12% vs 1% target) = -0.88%
- **Rebalancing recommendations**: Cum să folosim cash-ul de 0.98% pentru a ne apropia de ținte

---

### 4. `get_investment_recommendation`
Obține recomandare personalizată pentru un ticker specific, ținând cont de contextul portofoliului.

**Test Commands pentru Bob**:

#### Test 1: Ticker UNDERWEIGHT (DIGI.RO)
```
Folosește get_investment_recommendation cu:
- portfolio_id="portfolio1"
- ticker="DIGI.RO"
- investment_amount=1000

Ar trebui să primești recomandare STRONG BUY deoarece:
1. DIGI.RO este UNDERWEIGHT (5.93% vs 7% target)
2. Analiza tehnică arată semnale pozitive
3. Investiția ajută la rebalansare
```

#### Test 2: Ticker OVERWEIGHT (TLV.RO)
```
Folosește get_investment_recommendation cu:
- portfolio_id="portfolio1"
- ticker="TLV.RO"
- investment_amount=1000

Ar trebui să primești recomandare HOLD sau REDUCE deoarece:
1. TLV.RO este deja OVERWEIGHT (48.46% vs 40% target)
2. Chiar dacă analiza tehnică e pozitivă, portofoliul e prea concentrat
3. Cash-ul ar trebui investit în poziții UNDERWEIGHT
```

#### Test 3: Ticker cu Alocare Mică (AROBS.RO)
```
Folosește get_investment_recommendation cu:
- portfolio_id="portfolio1"
- ticker="AROBS.RO"
- investment_amount=1000

Ar trebui să primești recomandare STRONG BUY deoarece:
1. AROBS.RO este semnificativ UNDERWEIGHT (1.06% vs 3% target = -1.94%)
2. Sector tehnologie - diversificare bună
3. Investiția ajută la rebalansare
```

---

## Workflow Complet de Testare

### Pas 1: Verifică Starea Portofoliului
```
Bob, folosește list_portfolios și get_portfolio pentru a vedea situația actuală
```

### Pas 2: Analizează Rebalansarea
```
Bob, folosește analyze_portfolio_allocation pentru portfolio1 și spune-mi:
1. Care sunt pozițiile OVERWEIGHT?
2. Care sunt pozițiile UNDERWEIGHT?
3. Cum ar trebui să investesc cash-ul de 0.98%?
```

### Pas 3: Obține Recomandări Specifice
```
Bob, pentru fiecare ticker UNDERWEIGHT din top 5, folosește get_investment_recommendation cu 1000 RON și spune-mi:
1. Care ticker are cel mai bun raport risc/recompensă?
2. Care ticker ajută cel mai mult la rebalansare?
3. Care ticker are cele mai bune semnale tehnice?

Tickers de analizat:
- DIGI.RO (5.93% vs 7% target)
- EL.RO (3.52% vs 5% target)
- SNG.RO (2.41% vs 5% target)
- SNN.RO (1.70% vs 3% target)
- AROBS.RO (1.06% vs 3% target)
```

### Pas 4: Decizie Finală
```
Bob, pe baza analizelor de mai sus, recomandă-mi:
1. În ce ticker să investesc cash-ul de 0.98%?
2. Cât să investesc în fiecare?
3. De ce această alocare e optimă?
```

---

## Rezultate Așteptate

### Recomandare Optimă de Investiție
Având în vedere:
- Cash disponibil: 0.98% din portofoliu
- TLV.RO OVERWEIGHT cu 8.46%
- Multiple poziții UNDERWEIGHT

**Strategia Recomandată**:
1. **NU investi în TLV.RO** - deja prea concentrat
2. **Prioritizează ticker-ele UNDERWEIGHT** cu:
   - Semnale tehnice pozitive (RSI < 70, MACD bullish)
   - Diversificare sectorială (evită concentrarea în financiare)
   - Potențial de creștere pe termen mediu

**Top Candidați pentru Investiție**:
1. **AROBS.RO** (-1.94% vs target) - Tehnologie, diversificare
2. **SNG.RO** (-2.59% vs target) - Energie, dividend stabil
3. **M.RO** (-1.56% vs target) - Healthcare, sector defensiv
4. **PE.RO** (-1.62% vs target) - Energie regenerabilă, creștere

---

## Notițe Importante

### Excluse din Analiză
- **R3207AE, R3508AE, R3509AE, R3511AE**: Titluri de stat (15.21%) - NU se analizează tehnic
- **RON cash**: 0.98% - disponibil pentru investiții

### Considerații Strategice
1. **Reduce concentrarea în TLV.RO** (48.46% → 40%)
2. **Diversifică sectorial** - crește tehnologie, energie, healthcare
3. **Folosește cash-ul strategic** - investește în poziții UNDERWEIGHT cu semnale pozitive
4. **Menține echilibrul** - nu crea noi concentrări

---

## Comenzi Rapide pentru Bob

```bash
# 1. Vezi portofoliul
list_portfolios
get_portfolio portfolio_id="portfolio1"

# 2. Analizează rebalansarea
analyze_portfolio_allocation portfolio_id="portfolio1"

# 3. Recomandări pentru investiție
get_investment_recommendation portfolio_id="portfolio1" ticker="AROBS.RO" investment_amount=1000
get_investment_recommendation portfolio_id="portfolio1" ticker="SNG.RO" investment_amount=1000
get_investment_recommendation portfolio_id="portfolio1" ticker="M.RO" investment_amount=1000
get_investment_recommendation portfolio_id="portfolio1" ticker="PE.RO" investment_amount=1000

# 4. Compară cu poziția dominantă (ar trebui să recomande HOLD/REDUCE)
get_investment_recommendation portfolio_id="portfolio1" ticker="TLV.RO" investment_amount=1000
```

---

## Success Criteria

✅ **Portfolio tools funcționează corect**:
- list_portfolios returnează portfolio1
- get_portfolio arată toate cele 17 holdings
- analyze_portfolio_allocation identifică TLV.RO ca OVERWEIGHT
- get_investment_recommendation consideră contextul portofoliului

✅ **Recomandările sunt inteligente**:
- Recomandă REDUCE/HOLD pentru TLV.RO (OVERWEIGHT)
- Recomandă BUY pentru ticker-e UNDERWEIGHT cu semnale pozitive
- Consideră diversificarea sectorială
- Ajută la rebalansare către ținte

✅ **Analiza e comprehensivă**:
- Combină analiza tehnică (RSI, MACD, EMA)
- Consideră alocările curente vs țintă
- Evaluează riscul de concentrare
- Oferă recomandări acționabile

---

**Data Creării**: 2026-05-19
**Status**: Ready for Testing
**Next Step**: Testează cu Bob în Financial Analyst mode