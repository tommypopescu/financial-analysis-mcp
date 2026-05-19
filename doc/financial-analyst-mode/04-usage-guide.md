# Financial Analyst Mode - Usage Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Basic Usage](#basic-usage)
3. [Advanced Usage](#advanced-usage)
4. [Command Reference](#command-reference)
5. [Interpreting Results](#interpreting-results)
6. [Common Scenarios](#common-scenarios)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Prerequisites

Before using Financial Analyst Mode, ensure:
1. ✅ MCP server is running at `http://192.168.1.7:8000`
2. ✅ Bob is configured with Financial Analyst mode
3. ✅ You have basic understanding of stock tickers
4. ✅ You understand investment risks

### Activating the Mode

**Method 1: Direct Activation**
```
Switch to Financial Analyst mode
```

**Method 2: Automatic Activation**
Bob will automatically switch to this mode when you:
- Ask about stock analysis
- Request investment recommendations
- Mention ticker symbols
- Ask about buy/sell decisions

### Quick Start Example

```
User: Analizează acțiunea AAPL

Bob will:
1. Switch to Financial Analyst mode
2. Fetch AAPL data from Yahoo Finance
3. Calculate all technical indicators
4. Perform 5-phase analysis
5. Deliver BUY/HOLD/SELL recommendation
```

---

## Basic Usage

### Analyzing a Single Stock

**US Stocks**
```
Analizează AAPL
Analizează acțiunea Microsoft (MSFT)
Ce părere ai despre Tesla?
```

**Romanian Stocks**
```
Analizează TLV
Analizează acțiunea Banca Transilvania
Ce părere ai despre SNP?
```

**German Stocks**
```
Analizează SAP
Analizează acțiunea Siemens
Ce părere ai despre BMW?
```

### What You'll Get

Every analysis includes:

1. **Executive Summary**
   - Current price and trend
   - Key technical indicators
   - Overall market sentiment

2. **Technical Analysis**
   - Trend direction (EMA50/EMA200)
   - Momentum status (RSI, MACD)
   - Trend strength (ADX)
   - Volume confirmation (MFI)

3. **Scenario Planning**
   - Bullish scenario (probability + targets)
   - Bearish scenario (probability + targets)
   - Neutral scenario (probability + range)
   - Weighted expected return

4. **Risk Assessment**
   - Position sizing recommendation
   - Stop loss levels
   - Profit targets (3 levels)
   - Risk/reward ratio
   - Maximum loss per trade

5. **Investment Decision**
   - Clear verdict: **BUY** / **HOLD** / **SELL**
   - Confidence level: High / Medium / Low
   - Entry price and timing
   - Exit strategy
   - Timeframe (3-12 months)
   - Detailed rationale

---

## Advanced Usage

### Comparing Multiple Stocks

```
Compară AAPL cu MSFT pentru investiție
Care este mai bună: TLV sau SNP?
Analizează AAPL, GOOGL și MSFT și recomandă cea mai bună
```

Bob will:
- Analyze each stock individually
- Compare technical indicators
- Rank by investment potential
- Recommend the best option

### Portfolio Diversification

```
Am €10,000. Recomandă un portofoliu diversificat
Vreau să investesc în 3-5 acțiuni. Ce îmi recomanzi?
Cum să diversific între US și România?
```

Bob will:
- Suggest multiple stocks
- Allocate percentages
- Balance risk across sectors
- Consider correlation

### Monitoring Existing Positions

```
Dețin AAPL la €150. Ar trebui să vând?
Am cumpărat TLV acum 2 luni. Ce fac?
Când să iau profit din MSFT?
```

Bob will:
- Analyze current technical status
- Compare with your entry price
- Recommend HOLD or SELL
- Suggest profit-taking levels

### Screening for Opportunities

```
Caută acțiuni cu RSI sub 30
Care acțiuni sunt oversold acum?
Găsește oportunități de cumpărare
```

Bob will:
- Screen watchlist (27 tickers)
- Filter by criteria
- Rank by potential
- Provide top recommendations

### Setting Alerts

```
Anunță-mă când AAPL ajunge la €140
Vreau să știu când TLV trece de EMA50
Alertă când RSI pentru MSFT scade sub 30
```

Bob will:
- Note your alert criteria
- Suggest monitoring frequency
- Explain what to watch for

---

## Command Reference

### Analysis Commands

| Command | Description | Example |
|---------|-------------|---------|
| `Analizează [TICKER]` | Full analysis | `Analizează AAPL` |
| `Ce părere ai despre [TICKER]` | Quick opinion | `Ce părere ai despre TLV` |
| `Ar trebui să cumpăr [TICKER]?` | Buy recommendation | `Ar trebui să cumpăr MSFT?` |
| `[TICKER] este o investiție bună?` | Investment assessment | `AAPL este o investiție bună?` |

### Comparison Commands

| Command | Description | Example |
|---------|-------------|---------|
| `Compară [TICKER1] cu [TICKER2]` | Compare two stocks | `Compară AAPL cu MSFT` |
| `Care este mai bună: [T1] sau [T2]?` | Which is better | `Care este mai bună: TLV sau SNP?` |
| `Analizează [T1], [T2] și [T3]` | Multiple analysis | `Analizează AAPL, GOOGL, MSFT` |

### Portfolio Commands

| Command | Description | Example |
|---------|-------------|---------|
| `Recomandă un portofoliu` | Portfolio suggestion | `Recomandă un portofoliu diversificat` |
| `Am €[X]. Ce să cumpăr?` | Investment allocation | `Am €10,000. Ce să cumpăr?` |
| `Diversifică €[X]` | Diversification plan | `Diversifică €5,000` |

### Monitoring Commands

| Command | Description | Example |
|---------|-------------|---------|
| `Dețin [TICKER] la €[X]` | Position review | `Dețin AAPL la €150` |
| `Când să vând [TICKER]?` | Exit timing | `Când să vând TLV?` |
| `Ar trebui să mai țin [TICKER]?` | Hold decision | `Ar trebui să mai țin MSFT?` |

### Screening Commands

| Command | Description | Example |
|---------|-------------|---------|
| `Caută acțiuni cu RSI < 30` | RSI screening | `Caută acțiuni oversold` |
| `Care acțiuni sunt în uptrend?` | Trend screening | `Care acțiuni sunt bullish?` |
| `Găsește oportunități` | General screening | `Găsește oportunități de cumpărare` |

---

## Interpreting Results

### Understanding the Verdict

#### BUY Recommendation

```
VERDICT: BUY
Confidence: High (85%)

Entry: €150.00 (current market)
Stop Loss: €142.50 (-5%)
Target 1: €157.50 (+5%) - Take 30% profit
Target 2: €165.00 (+10%) - Take 40% profit
Target 3: €172.50 (+15%) - Take 30% profit

Risk/Reward: 1:2.5
Position Size: 2-3% of portfolio
Timeframe: 3-6 months
```

**What This Means:**
- ✅ Strong buy signal based on technical analysis
- ✅ High confidence (85%) - most indicators bullish
- ✅ Clear entry point at current price
- ✅ Risk is well-defined (stop loss at -5%)
- ✅ Multiple profit targets for staged exit
- ✅ Good risk/reward ratio (1:2.5)
- ✅ Suitable position size (2-3% of portfolio)
- ✅ Medium-term hold (3-6 months)

**Action Steps:**
1. Buy at current price (€150)
2. Set stop loss at €142.50
3. Set alerts for profit targets
4. Monitor weekly
5. Take profits at each target level

#### HOLD Recommendation

```
VERDICT: HOLD
Confidence: Medium (65%)

Current Status: Mixed signals
- Trend: Neutral (EMAs converging)
- Momentum: Weak (RSI 45)
- Volume: Low (MFI 48)

Action: Wait for clarity
Re-evaluate: In 2-3 weeks
Watch for: Breakout above €155 or breakdown below €145
```

**What This Means:**
- ⚠️ No clear directional bias
- ⚠️ Not enough conviction to buy or sell
- ⚠️ Risk/reward not favorable at current levels
- ⚠️ Better to wait for clearer setup

**Action Steps:**
1. Don't enter new position
2. If holding, keep position
3. Monitor for breakout/breakdown
4. Re-analyze in 2-3 weeks
5. Set alerts at key levels (€155, €145)

#### SELL Recommendation

```
VERDICT: SELL (or DON'T BUY)
Confidence: High (80%)

Current Status: Bearish
- Trend: Downtrend (Death Cross)
- Momentum: Weak (RSI 35)
- Volume: Selling pressure (MFI 40)

If Holding:
- Exit at current price (€150)
- Or set stop loss at €148 (-1.3%)

If Not Holding:
- Avoid entry
- Wait for reversal signals
- Re-evaluate in 1-2 months
```

**What This Means:**
- ❌ Strong sell signal based on technical analysis
- ❌ High confidence (80%) - most indicators bearish
- ❌ Downtrend confirmed
- ❌ Risk of further decline

**Action Steps (If Holding):**
1. Exit position at current price
2. Or set tight stop loss
3. Don't average down
4. Accept the loss if needed
5. Move capital to better opportunities

**Action Steps (If Not Holding):**
1. Don't enter position
2. Add to watchlist
3. Wait for reversal signals
4. Re-analyze in 1-2 months

### Understanding Confidence Levels

**High Confidence (80-100%)**
- All or most indicators aligned
- Clear trend direction
- Strong volume confirmation
- Low ambiguity
- **Action**: Follow recommendation with full conviction

**Medium Confidence (60-80%)**
- Most indicators aligned
- Some conflicting signals
- Moderate trend strength
- Some ambiguity
- **Action**: Follow recommendation but reduce position size

**Low Confidence (40-60%)**
- Mixed signals
- Unclear trend
- Weak volume
- High ambiguity
- **Action**: Wait for better setup or skip

### Understanding Risk/Reward Ratios

```
1:3 or better → Excellent (take the trade)
1:2 to 1:3 → Good (acceptable)
1:1.5 to 1:2 → Fair (marginal)
Below 1:1.5 → Poor (avoid)
```

**Example:**
```
Entry: €100
Stop Loss: €95 (risk: €5)
Target: €110 (reward: €10)
Ratio: 1:2 ✅ Good
```

### Understanding Position Sizing

**Conservative (1-2% risk)**
- New to investing
- High volatility stock
- Uncertain market
- **Example**: €10,000 portfolio → Risk €100-200 per trade

**Moderate (2-3% risk)**
- Experienced investor
- Medium volatility stock
- Normal market
- **Example**: €10,000 portfolio → Risk €200-300 per trade

**Aggressive (3-5% risk)**
- Very experienced investor
- Low volatility stock
- High conviction trade
- **Example**: €10,000 portfolio → Risk €300-500 per trade

---

## Common Scenarios

### Scenario 1: First Time Investor

**Situation**: You have €5,000 to invest and want to start.

**Approach**:
```
User: Am €5,000 și vreau să încep să investesc. Ce îmi recomanzi?

Bob will:
1. Suggest 3-5 diversified stocks
2. Allocate conservative percentages
3. Explain each recommendation
4. Provide risk management plan
5. Set realistic expectations
```

**Expected Output**:
```
Recommended Portfolio (€5,000):

1. AAPL - €1,500 (30%)
   - Verdict: BUY
   - Stop Loss: -5%
   - Target: +10-15% in 6 months

2. MSFT - €1,500 (30%)
   - Verdict: BUY
   - Stop Loss: -5%
   - Target: +10-15% in 6 months

3. TLV - €1,000 (20%)
   - Verdict: BUY
   - Stop Loss: -7%
   - Target: +15-20% in 6 months

4. Cash Reserve - €1,000 (20%)
   - For opportunities
   - For averaging down
   - For emergencies

Total Risk: 2% per position
Expected Return: +12-18% in 6-12 months
Diversification: US (60%) + Romania (20%) + Cash (20%)
```

### Scenario 2: Existing Position Review

**Situation**: You bought AAPL 2 months ago at €140, now it's €155.

**Approach**:
```
User: Am cumpărat AAPL acum 2 luni la €140. Acum este €155. Ce fac?

Bob will:
1. Calculate your current profit (+10.7%)
2. Analyze current technical status
3. Compare with original entry thesis
4. Recommend HOLD or SELL
5. Suggest profit-taking strategy
```

**Expected Output**:
```
Position Review: AAPL

Entry: €140 (2 months ago)
Current: €155
Profit: +€15 (+10.7%) ✅

Current Technical Status:
- Trend: Still bullish (EMA50 > EMA200)
- Momentum: Strong (RSI 65)
- Volume: Confirming (MFI 58)

VERDICT: HOLD (Take Partial Profit)

Action Plan:
1. Take 30% profit now at €155
   - Lock in €4.50 per share
   - Reduce risk exposure

2. Hold 70% with trailing stop at €147 (-5%)
   - Let winners run
   - Protect remaining gains

3. Next target: €165 (+17.8%)
   - Take another 40% profit
   - Final 30% rides to €172

Rationale:
- Original thesis still valid
- Trend remains strong
- Taking partial profits reduces risk
- Trailing stop protects gains
```

### Scenario 3: Market Correction

**Situation**: Market dropped 5% today, your stocks are down.

**Approach**:
```
User: Piața a scăzut 5% astăzi. Ce fac cu pozițiile mele?

Bob will:
1. Assess if it's market-wide or stock-specific
2. Check if stop losses were hit
3. Evaluate if thesis changed
4. Recommend HOLD, SELL, or BUY MORE
5. Provide perspective on volatility
```

**Expected Output**:
```
Market Correction Analysis

Market Status: -5% (broad selloff)
Your Positions:
- AAPL: -4% (in line with market)
- MSFT: -3% (outperforming)
- TLV: -6% (underperforming)

Assessment:
✅ This is normal market volatility
✅ No fundamental changes
✅ Technical trends still intact
✅ Stop losses not hit

VERDICT: HOLD ALL POSITIONS

Action Plan:
1. Don't panic sell
2. Don't check prices every hour
3. Review stop losses (keep them)
4. Consider buying more if:
   - You have cash reserves
   - Stocks hit support levels
   - RSI becomes oversold

Perspective:
- 5% corrections are normal (happen 3x/year)
- Your diversification is working
- Stick to your plan
- Volatility creates opportunities

Opportunity:
If market drops another 5-10%:
- AAPL at €140 → Strong BUY
- MSFT at €380 → Strong BUY
- TLV at €18 → Strong BUY
```

### Scenario 4: Screening for Opportunities

**Situation**: You have cash and want to find good entry points.

**Approach**:
```
User: Am €3,000 cash. Caută oportunități de cumpărare.

Bob will:
1. Screen all 27 tickers in watchlist
2. Filter by technical criteria
3. Rank by potential
4. Provide top 3-5 recommendations
5. Explain why each is attractive
```

**Expected Output**:
```
Screening Results (27 tickers analyzed)

Top Opportunities:

1. GOOGL - STRONG BUY ⭐⭐⭐
   Current: €135
   Status: Oversold (RSI 28)
   Trend: Uptrend intact (above EMA200)
   Entry: €135 (now)
   Target: €150 (+11%)
   Stop: €128 (-5%)
   Risk/Reward: 1:2.2
   Allocation: €1,000 (33%)

2. SNP - BUY ⭐⭐
   Current: €0.42
   Status: Pullback to EMA50
   Trend: Strong uptrend (ADX 28)
   Entry: €0.42 (now)
   Target: €0.48 (+14%)
   Stop: €0.39 (-7%)
   Risk/Reward: 1:2.0
   Allocation: €800 (27%)

3. NVDA - BUY ⭐⭐
   Current: €480
   Status: Consolidation breakout
   Trend: Bullish (Golden Cross)
   Entry: €480 (now)
   Target: €528 (+10%)
   Stop: €456 (-5%)
   Risk/Reward: 1:2.0
   Allocation: €800 (27%)

4. Cash Reserve: €400 (13%)

Total Allocation: €3,000
Expected Return: +11-14% in 3-6 months
Risk per position: 2-3%
Diversification: US Tech (60%) + Romania (27%) + Cash (13%)
```

### Scenario 5: Long-Term Hold Decision

**Situation**: You've held a stock for 6 months, wondering if you should continue.

**Approach**:
```
User: Dețin MSFT de 6 luni. Ar trebui să mai țin sau să vând?

Bob will:
1. Review 6-month performance
2. Analyze current technical status
3. Compare with original thesis
4. Assess future potential
5. Recommend HOLD or SELL
```

**Expected Output**:
```
Long-Term Hold Review: MSFT (6 months)

Performance:
- Entry: €350 (6 months ago)
- Current: €410
- Profit: +€60 (+17.1%) ✅
- Market: +8% (outperforming)

Current Technical Status:
- Trend: Strong uptrend (EMA50 > EMA200)
- Momentum: Healthy (RSI 58)
- Volume: Strong (MFI 62)
- ADX: 26 (strong trend)

VERDICT: CONTINUE HOLDING ⭐

Rationale:
✅ Excellent performance (+17% vs market +8%)
✅ Trend remains strong
✅ No signs of reversal
✅ Momentum healthy (not overbought)
✅ Volume confirming uptrend

Action Plan:
1. Keep holding
2. Raise trailing stop to €390 (-5%)
   - Protects +11% profit
   - Allows for normal volatility

3. Next profit target: €450 (+28%)
   - Take 50% profit
   - Let rest run

4. Re-evaluate in 3 months

Alternative (If you need cash):
- Can take 30-50% profit now
- Lock in gains
- Keep rest for further upside
```

---

## Best Practices

### 1. Always Use Stop Losses

**Why**: Protects capital from large losses

**How**:
```
✅ Set stop loss immediately after entry
✅ Use technical levels (below EMA50, support)
✅ Typical range: 5-10% below entry
✅ Never remove stop loss
✅ Only move stop loss UP (trailing)
```

**Example**:
```
Entry: €100
Stop Loss: €95 (-5%)
If price rises to €110:
- Move stop to €104.50 (-5% from €110)
- Lock in profit
```

### 2. Take Partial Profits

**Why**: Reduces risk, locks in gains

**How**:
```
✅ Take 30% profit at first target
✅ Take 40% profit at second target
✅ Let 30% run to final target
✅ Adjust based on conviction
```

**Example**:
```
100 shares at €100:
- Target 1 (€110): Sell 30 shares
- Target 2 (€120): Sell 40 shares
- Target 3 (€130): Sell 30 shares
```

### 3. Diversify Properly

**Why**: Reduces portfolio risk

**How**:
```
✅ 3-5 stocks minimum
✅ Different sectors
✅ Different markets (US + Romania)
✅ Max 20-25% per position
✅ Keep 10-20% cash reserve
```

**Example Portfolio (€10,000)**:
```
- US Tech: €3,000 (30%)
- US Non-Tech: €2,000 (20%)
- Romanian: €2,000 (20%)
- German: €1,500 (15%)
- Cash: €1,500 (15%)
```

### 4. Position Sizing

**Why**: Controls risk per trade

**How**:
```
Position Size = (Portfolio × Risk%) / (Entry - Stop Loss)

Example:
- Portfolio: €10,000
- Risk: 2% = €200
- Entry: €100
- Stop: €95
- Size = €200 / (€100 - €95) = 40 shares
```

### 5. Keep a Trading Journal

**Why**: Learn from experience

**What to Record**:
```
✅ Entry date and price
✅ Rationale for entry
✅ Stop loss and targets
✅ Exit date and price
✅ Profit/loss
✅ What worked/didn't work
✅ Lessons learned
```

### 6. Don't Overtrade

**Why**: Reduces costs and emotional decisions

**How**:
```
✅ Wait for high-quality setups
✅ Don't force trades
✅ Quality over quantity
✅ Typical: 1-3 trades per month
✅ Hold positions 3-12 months
```

### 7. Manage Emotions

**Why**: Prevents costly mistakes

**How**:
```
✅ Follow your plan
✅ Don't panic sell
✅ Don't FOMO buy
✅ Accept losses as part of process
✅ Don't revenge trade
✅ Take breaks after losses
```

### 8. Regular Portfolio Review

**Why**: Ensures alignment with goals

**When**:
```
✅ Weekly: Quick check of positions
✅ Monthly: Detailed review
✅ Quarterly: Rebalancing
✅ Annually: Strategy review
```

**What to Check**:
```
✅ Are stop losses still valid?
✅ Have targets been hit?
✅ Has thesis changed?
✅ Is diversification maintained?
✅ Is risk per position appropriate?
```

---

## Troubleshooting

### Issue 1: Bob Doesn't Switch to Financial Analyst Mode

**Symptoms**:
- You ask about stocks but Bob doesn't analyze
- No technical indicators shown
- Generic response instead of detailed analysis

**Solutions**:
1. Explicitly request mode switch:
   ```
   Switch to Financial Analyst mode
   ```

2. Use clear stock-related keywords:
   ```
   Analizează acțiunea AAPL
   (instead of just "AAPL")
   ```

3. Check mode configuration:
   - Verify `.bob/custom_modes.yaml` exists
   - Verify mode is enabled

### Issue 2: "Ticker Not Found" Error

**Symptoms**:
```
Error: Ticker XYZ not found in Yahoo Finance
```

**Solutions**:
1. Verify ticker symbol:
   - US stocks: Use correct symbol (AAPL, MSFT, GOOGL)
   - Romanian stocks: Add .RO suffix (TLV.RO, SNP.RO)
   - German stocks: Add .DE suffix (SAP.DE, BMW.DE)

2. Check if ticker is tradeable:
   - Some tickers are delisted
   - Some are not available on Yahoo Finance

3. Try alternative ticker:
   - Some companies have multiple tickers
   - Check official exchange listing

### Issue 3: Insufficient Data

**Symptoms**:
```
Warning: Only 30 days of data available
Some indicators may be unreliable
```

**Solutions**:
1. This is normal for:
   - Newly listed stocks
   - Low-volume stocks
   - Recent IPOs

2. Interpretation:
   - Reduce confidence in analysis
   - Wait for more data (60+ days ideal)
   - Consider alternative tickers

3. Proceed with caution:
   - Smaller position size
   - Wider stop loss
   - Lower conviction

### Issue 4: Conflicting Signals

**Symptoms**:
```
Mixed signals:
- Trend: Bullish (EMA50 > EMA200)
- Momentum: Bearish (RSI 25)
- Volume: Neutral (MFI 50)
```

**Solutions**:
1. This is normal market behavior
2. Bob will recommend HOLD
3. Wait for clarity (2-3 weeks)
4. Don't force a trade
5. Look for alternative opportunities

### Issue 5: Analysis Takes Too Long

**Symptoms**:
- Bob takes >30 seconds to respond
- Timeout errors

**Solutions**:
1. Check MCP server status:
   ```powershell
   # On OMV server
   docker ps | grep financial-analysis
   ```

2. Check network connectivity:
   ```powershell
   # On Windows
   Test-NetConnection 192.168.1.7 -Port 8000
   ```

3. Restart MCP server if needed:
   ```bash
   # On OMV server
   docker restart financial-analysis-mcp
   ```

4. Check server logs:
   ```bash
   docker logs financial-analysis-mcp --tail 50
   ```

### Issue 6: Outdated Price Data

**Symptoms**:
```
Current Price: €150 (as of 2 days ago)
```

**Solutions**:
1. This is normal for:
   - Weekends (markets closed)
   - Holidays (markets closed)
   - After-hours (markets closed)

2. Yahoo Finance updates:
   - Real-time during market hours
   - Delayed 15-20 minutes after close
   - Next day for end-of-day data

3. If data is >1 business day old:
   - Check Yahoo Finance directly
   - Verify ticker symbol
   - Check if stock is suspended

### Issue 7: Recommendations Don't Match Expectations

**Symptoms**:
- You think it's a BUY, Bob says SELL
- You want to hold, Bob says SELL

**Solutions**:
1. Review Bob's rationale:
   - What indicators are bearish?
   - What risks were identified?
   - What scenarios were considered?

2. Check your bias:
   - Are you emotionally attached?
   - Are you ignoring red flags?
   - Are you hoping for recovery?

3. Get second opinion:
   - Analyze another similar stock
   - Compare technical indicators
   - Check market sentiment

4. Remember:
   - Bob is data-driven
   - Bob has no emotional attachment
   - Bob follows systematic process
   - Bob prioritizes capital preservation

---

## Summary

Financial Analyst Mode provides:
- ✅ Comprehensive technical analysis
- ✅ Clear BUY/HOLD/SELL recommendations
- ✅ Detailed risk management plans
- ✅ Multiple scenario planning
- ✅ Actionable entry/exit parameters

**Key Takeaways**:
1. Always use stop losses
2. Take partial profits
3. Diversify properly
4. Size positions correctly
5. Follow the plan
6. Manage emotions
7. Review regularly
8. Learn from experience

**Next Steps**:
- Review [Analysis Examples](05-examples.md) for real cases
- Study [Workflow](03-workflow.md) for methodology
- Check [Configuration](02-configuration.md) for setup

---

**Disclaimer**: This mode provides technical analysis based on historical data. Past performance does not guarantee future results. Always do your own research and consider your risk tolerance before investing.