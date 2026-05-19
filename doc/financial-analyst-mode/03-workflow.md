# Financial Analyst Mode - Analysis Workflow

## Table of Contents
1. [Overview](#overview)
2. [5-Phase Analysis Framework](#5-phase-analysis-framework)
3. [Phase 1: Data Collection](#phase-1-data-collection)
4. [Phase 2: Technical Analysis](#phase-2-technical-analysis)
5. [Phase 3: Scenario Planning](#phase-3-scenario-planning)
6. [Phase 4: Risk Assessment](#phase-4-risk-assessment)
7. [Phase 5: Investment Decision](#phase-5-investment-decision)
8. [Workflow Diagram](#workflow-diagram)
9. [Decision Trees](#decision-trees)
10. [Quality Assurance](#quality-assurance)

---

## Overview

The Financial Analyst Mode follows a rigorous 5-phase analysis framework designed to provide comprehensive, unbiased investment recommendations. Each phase builds upon the previous one, ensuring a thorough evaluation of the investment opportunity.

### Key Principles

1. **Systematic Approach**: Follow the same process for every analysis
2. **Data-Driven**: Base decisions on quantitative indicators
3. **Risk-Aware**: Always consider downside scenarios
4. **Unbiased**: Let the data speak, not emotions
5. **Actionable**: Provide clear, implementable recommendations

---

## 5-Phase Analysis Framework

```
Phase 1: Data Collection
    ↓
Phase 2: Technical Analysis
    ↓
Phase 3: Scenario Planning
    ↓
Phase 4: Risk Assessment
    ↓
Phase 5: Investment Decision
```

Each phase has specific objectives, tools, and outputs that feed into the next phase.

---

## Phase 1: Data Collection

### Objective
Gather all necessary market data and technical indicators for the target ticker.

### Tools Used
- `fetch_ticker_data` - Historical OHLCV data (3-6 months)
- `get_current_price` - Latest price quote
- `calculate_all_indicators` - All 7 technical indicators

### Data Points Collected

#### Price Data
- Current price
- 52-week high/low
- Average volume (20-day)
- Price change (1D, 1W, 1M, 3M)

#### Technical Indicators
1. **EMA50 & EMA200** - Trend direction
2. **RSI (14)** - Momentum and overbought/oversold
3. **MACD** - Trend confirmation
4. **ADX** - Trend strength
5. **Stochastic Oscillator** - Short-term momentum
6. **Bollinger Bands** - Volatility and price extremes
7. **MFI** - Volume-weighted momentum

### Output
Complete dataset with all indicators calculated and ready for analysis.

### Quality Checks
- ✅ Minimum 60 days of historical data
- ✅ All 7 indicators successfully calculated
- ✅ No missing or invalid data points
- ✅ Current price within reasonable range

---

## Phase 2: Technical Analysis

### Objective
Interpret technical indicators to understand current market conditions and trend strength.

### Analysis Components

#### 2.1 Trend Analysis

**EMA Crossover Analysis**
```
Golden Cross (Bullish):
- EMA50 > EMA200
- Price > EMA50
- Uptrend confirmed

Death Cross (Bearish):
- EMA50 < EMA200
- Price < EMA50
- Downtrend confirmed

Neutral:
- EMAs close together
- Price between EMAs
- No clear trend
```

**Trend Strength (ADX)**
```
Strong Trend: ADX > 25
- High confidence in trend direction
- Suitable for trend-following strategies

Weak Trend: ADX < 20
- Low confidence in trend
- Range-bound market
- Avoid trend-following strategies

Moderate: 20 ≤ ADX ≤ 25
- Developing trend
- Monitor for strengthening
```

#### 2.2 Momentum Analysis

**RSI Interpretation**
```
Overbought: RSI > 70
- Potential reversal down
- Consider taking profits
- Wait for pullback

Oversold: RSI < 30
- Potential reversal up
- Buying opportunity
- Confirm with other indicators

Neutral: 30 ≤ RSI ≤ 70
- Normal trading range
- No extreme conditions
```

**MACD Signals**
```
Bullish:
- MACD line > Signal line
- Histogram positive and growing
- Momentum increasing

Bearish:
- MACD line < Signal line
- Histogram negative and growing
- Momentum decreasing

Divergence:
- Price makes new high/low
- MACD doesn't confirm
- Potential reversal signal
```

#### 2.3 Volatility Analysis

**Bollinger Bands**
```
Price at Upper Band:
- Overbought condition
- High volatility
- Potential reversal or continuation

Price at Lower Band:
- Oversold condition
- High volatility
- Potential bounce

Price in Middle:
- Normal volatility
- No extreme conditions
- Trend-following appropriate

Band Squeeze:
- Low volatility
- Potential breakout coming
- Prepare for increased movement
```

#### 2.4 Volume Analysis

**Money Flow Index (MFI)**
```
High MFI (> 80):
- Strong buying pressure
- Overbought with volume confirmation
- Caution advised

Low MFI (< 20):
- Strong selling pressure
- Oversold with volume confirmation
- Potential buying opportunity

Divergence:
- Price trend vs MFI trend
- Volume not confirming price
- Potential reversal
```

### Output
Comprehensive technical assessment with:
- Trend direction and strength
- Momentum status
- Volatility conditions
- Volume confirmation
- Key support/resistance levels

---

## Phase 3: Scenario Planning

### Objective
Develop multiple scenarios (bullish, bearish, neutral) with probability assessments and price targets.

### Scenario Development Process

#### 3.1 Bullish Scenario

**Conditions Required**
- EMA50 > EMA200 (Golden Cross)
- RSI between 40-70 (healthy momentum)
- MACD bullish crossover
- ADX > 20 (trend strength)
- Price above EMA50

**Probability Assessment**
```
High Probability (60-80%):
- All 5+ indicators bullish
- Strong trend (ADX > 25)
- Volume confirming (MFI > 50)

Medium Probability (40-60%):
- 3-4 indicators bullish
- Moderate trend (ADX 20-25)
- Mixed volume signals

Low Probability (20-40%):
- 1-2 indicators bullish
- Weak trend (ADX < 20)
- Volume not confirming
```

**Price Targets**
- **Conservative**: +5-10% (1-2 months)
- **Moderate**: +10-20% (3-6 months)
- **Aggressive**: +20-30% (6-12 months)

**Catalysts**
- Technical breakout above resistance
- Increasing volume
- Sector rotation into stock
- Positive market sentiment

#### 3.2 Bearish Scenario

**Conditions Required**
- EMA50 < EMA200 (Death Cross)
- RSI < 40 (weak momentum)
- MACD bearish crossover
- ADX > 20 (downtrend strength)
- Price below EMA50

**Probability Assessment**
```
High Probability (60-80%):
- All 5+ indicators bearish
- Strong downtrend (ADX > 25)
- Volume confirming (MFI < 50)

Medium Probability (40-60%):
- 3-4 indicators bearish
- Moderate downtrend (ADX 20-25)
- Mixed volume signals

Low Probability (20-40%):
- 1-2 indicators bearish
- Weak downtrend (ADX < 20)
- Volume not confirming
```

**Price Targets**
- **Conservative**: -5-10% (1-2 months)
- **Moderate**: -10-20% (3-6 months)
- **Aggressive**: -20-30% (6-12 months)

**Catalysts**
- Technical breakdown below support
- Decreasing volume
- Sector rotation out of stock
- Negative market sentiment

#### 3.3 Neutral Scenario

**Conditions Required**
- EMAs close together or crossing
- RSI between 40-60
- MACD near zero line
- ADX < 20 (no clear trend)
- Price oscillating around EMAs

**Probability Assessment**
```
High Probability (60-80%):
- All indicators neutral
- Very weak trend (ADX < 15)
- Sideways price action

Medium Probability (40-60%):
- Mixed signals
- Weak trend (ADX 15-20)
- Consolidation pattern

Low Probability (20-40%):
- Some directional bias
- Developing trend (ADX approaching 20)
- Breakout potential
```

**Price Range**
- **Expected**: ±5% around current price
- **Support**: Recent lows
- **Resistance**: Recent highs

**Catalysts**
- Market indecision
- Awaiting news/events
- Consolidation before breakout
- Low volatility environment

### Scenario Weighting

Calculate weighted expected return:
```
Expected Return = (Bullish% × Bullish Target) + 
                  (Bearish% × Bearish Target) + 
                  (Neutral% × Neutral Target)

Example:
- Bullish: 60% probability × +15% target = +9%
- Bearish: 20% probability × -10% target = -2%
- Neutral: 20% probability × 0% target = 0%
Expected Return = +7%
```

### Output
Three detailed scenarios with:
- Probability percentages (must sum to 100%)
- Price targets with timeframes
- Key catalysts and triggers
- Weighted expected return

---

## Phase 4: Risk Assessment

### Objective
Identify and quantify risks, establish risk management parameters.

### Risk Categories

#### 4.1 Technical Risks

**Trend Reversal Risk**
```
High Risk:
- Price at extreme levels (RSI > 70 or < 30)
- Divergence between price and indicators
- Weakening trend (ADX declining)

Medium Risk:
- Price approaching key levels
- Mixed indicator signals
- Moderate trend strength

Low Risk:
- Strong trend confirmation
- All indicators aligned
- Price in middle of range
```

**Volatility Risk**
```
High Volatility:
- Bollinger Bands widening
- Large daily price swings (> 3%)
- Unpredictable movements

Medium Volatility:
- Normal band width
- Moderate price swings (1-3%)
- Predictable patterns

Low Volatility:
- Bollinger Bands squeezing
- Small price swings (< 1%)
- Potential breakout building
```

#### 4.2 Market Risks

**Systematic Risk**
- Overall market conditions
- Economic indicators
- Sector performance
- Correlation with indices

**Liquidity Risk**
- Average daily volume
- Bid-ask spread
- Market depth
- Ability to exit position

#### 4.3 Position Sizing

**Risk Per Trade**
```
Conservative: 1-2% of portfolio
- New investors
- High volatility stocks
- Uncertain market conditions

Moderate: 2-3% of portfolio
- Experienced investors
- Medium volatility stocks
- Normal market conditions

Aggressive: 3-5% of portfolio
- Very experienced investors
- Low volatility stocks
- Strong conviction trades
```

**Position Size Calculator**
```
Position Size = (Portfolio Value × Risk%) / 
                (Entry Price - Stop Loss Price)

Example:
- Portfolio: €10,000
- Risk: 2% = €200
- Entry: €50
- Stop Loss: €45
- Position Size = €200 / (€50 - €45) = 40 shares
```

#### 4.4 Stop Loss Levels

**Technical Stop Loss**
```
Tight Stop (2-3%):
- Below recent swing low
- Below EMA50
- For short-term trades

Medium Stop (5-7%):
- Below EMA200
- Below major support
- For medium-term holds

Wide Stop (10-12%):
- Below 52-week low
- Below major trend line
- For long-term positions
```

**Trailing Stop Loss**
```
As price moves up:
- Move stop loss up
- Lock in profits
- Protect gains

Example:
- Entry: €50
- Initial Stop: €45 (-10%)
- Price rises to €60
- New Stop: €54 (-10% from €60)
```

#### 4.5 Profit Targets

**Multi-Target Strategy**
```
Target 1 (30% of position):
- Conservative target (+5-10%)
- Take partial profits
- Reduce risk

Target 2 (40% of position):
- Moderate target (+10-20%)
- Main profit taking
- Secure gains

Target 3 (30% of position):
- Aggressive target (+20-30%)
- Let winners run
- Maximum upside
```

### Risk/Reward Ratio

**Minimum Acceptable Ratio: 1:2**
```
Risk: €5 per share (stop loss)
Reward: €10 per share (target)
Ratio: 1:2 ✅ Acceptable

Risk: €10 per share
Reward: €8 per share
Ratio: 1:0.8 ❌ Not acceptable
```

### Output
Complete risk management plan with:
- Risk level assessment (Low/Medium/High)
- Position sizing recommendation
- Stop loss levels (initial and trailing)
- Profit targets (multiple levels)
- Risk/reward ratio
- Maximum loss per trade

---

## Phase 5: Investment Decision

### Objective
Synthesize all analysis into a clear, actionable recommendation with specific entry/exit parameters.

### Decision Framework

#### 5.1 Signal Scoring System

**Bullish Signals (1 point each)**
- ✅ EMA50 > EMA200 (Golden Cross)
- ✅ Price > EMA50
- ✅ RSI between 40-70
- ✅ MACD bullish crossover
- ✅ ADX > 20
- ✅ Stochastic bullish
- ✅ MFI > 50

**Bearish Signals (-1 point each)**
- ❌ EMA50 < EMA200 (Death Cross)
- ❌ Price < EMA50
- ❌ RSI < 30 or > 70
- ❌ MACD bearish crossover
- ❌ ADX declining
- ❌ Stochastic bearish
- ❌ MFI < 50

**Score Interpretation**
```
+5 to +7: STRONG BUY
+3 to +4: BUY
+1 to +2: WEAK BUY
0: HOLD
-1 to -2: WEAK SELL
-3 to -4: SELL
-5 to -7: STRONG SELL
```

#### 5.2 Decision Matrix

```
┌─────────────────┬──────────┬──────────┬──────────┐
│ Trend Strength  │ Momentum │ Volume   │ Decision │
├─────────────────┼──────────┼──────────┼──────────┤
│ Strong Up       │ Bullish  │ High     │ BUY      │
│ Strong Up       │ Bullish  │ Low      │ HOLD     │
│ Strong Up       │ Bearish  │ Any      │ HOLD     │
│ Weak/Neutral    │ Bullish  │ High     │ HOLD     │
│ Weak/Neutral    │ Any      │ Low      │ HOLD     │
│ Strong Down     │ Bearish  │ High     │ SELL     │
│ Strong Down     │ Bearish  │ Low      │ HOLD     │
│ Strong Down     │ Bullish  │ Any      │ HOLD     │
└─────────────────┴──────────┴──────────┴──────────┘
```

#### 5.3 Final Recommendation Format

**BUY Recommendation**
```
VERDICT: BUY

Entry Strategy:
- Primary Entry: [Price] (current market)
- Alternative Entry: [Price] (on pullback to EMA50)
- Position Size: [X] shares ([Y]% of portfolio)

Profit Targets:
- Target 1: [Price] (+X%) - Take 30% profit
- Target 2: [Price] (+Y%) - Take 40% profit
- Target 3: [Price] (+Z%) - Take 30% profit

Risk Management:
- Stop Loss: [Price] (-X%)
- Risk/Reward: 1:[Ratio]
- Maximum Loss: €[Amount]

Timeframe: [X] months

Rationale:
- [Key bullish factors]
- [Technical confirmation]
- [Risk justification]
```

**HOLD Recommendation**
```
VERDICT: HOLD

Current Assessment:
- Mixed signals present
- No clear directional bias
- Risk/reward not favorable

Action Plan:
- Monitor for [specific conditions]
- Re-evaluate when [trigger occurs]
- Consider entry if [criteria met]

Alternative:
- Wait for pullback to [support level]
- Wait for breakout above [resistance level]

Timeframe: Re-assess in [X] weeks
```

**SELL Recommendation**
```
VERDICT: SELL (or DON'T BUY)

Exit Strategy (if holding):
- Immediate Exit: [Price] (current market)
- Stop Loss: [Price] (if price bounces)
- Exit 100% of position

Avoid Entry Because:
- [Key bearish factors]
- [Technical warnings]
- [Risk concerns]

Alternative Opportunities:
- Consider [other tickers] instead
- Wait for [specific conditions]

Timeframe: Re-assess in [X] months
```

### 5.4 Confidence Levels

```
High Confidence (80-100%):
- All indicators aligned
- Strong trend confirmation
- Clear risk/reward
- Actionable immediately

Medium Confidence (60-80%):
- Most indicators aligned
- Some conflicting signals
- Acceptable risk/reward
- Monitor closely

Low Confidence (40-60%):
- Mixed signals
- Unclear trend
- Marginal risk/reward
- Wait for clarity
```

### Output
Final investment recommendation including:
- **Clear Verdict**: BUY / HOLD / SELL
- **Confidence Level**: High / Medium / Low
- **Entry Parameters**: Price, timing, position size
- **Exit Parameters**: Profit targets, stop loss
- **Timeframe**: Expected holding period
- **Rationale**: Key reasons for decision
- **Alternatives**: What to do if conditions change

---

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    START ANALYSIS                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  PHASE 1: DATA COLLECTION                               │
│  • Fetch historical data (3-6 months)                   │
│  • Get current price                                    │
│  • Calculate all 7 indicators                           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  PHASE 2: TECHNICAL ANALYSIS                            │
│  • Analyze trend (EMA, ADX)                             │
│  • Assess momentum (RSI, MACD, Stochastic)              │
│  • Check volatility (Bollinger Bands)                   │
│  • Confirm volume (MFI)                                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  PHASE 3: SCENARIO PLANNING                             │
│  • Develop bullish scenario (probability + targets)     │
│  • Develop bearish scenario (probability + targets)     │
│  • Develop neutral scenario (probability + range)       │
│  • Calculate weighted expected return                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  PHASE 4: RISK ASSESSMENT                               │
│  • Identify technical risks                             │
│  • Calculate position size                              │
│  • Set stop loss levels                                 │
│  • Define profit targets                                │
│  • Verify risk/reward ratio (min 1:2)                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  PHASE 5: INVESTMENT DECISION                           │
│  • Calculate signal score                               │
│  • Apply decision matrix                                │
│  • Determine verdict (BUY/HOLD/SELL)                    │
│  • Set confidence level                                 │
│  • Format final recommendation                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              DELIVER RECOMMENDATION                      │
│  • Clear verdict with rationale                         │
│  • Specific entry/exit parameters                       │
│  • Risk management plan                                 │
│  • Timeframe and monitoring plan                        │
└─────────────────────────────────────────────────────────┘
```

---

## Decision Trees

### Tree 1: Initial Trend Assessment

```
Is EMA50 > EMA200?
├─ YES (Golden Cross)
│  └─ Is Price > EMA50?
│     ├─ YES → Uptrend Confirmed → Proceed to Momentum Check
│     └─ NO → Weak Uptrend → Caution, check other indicators
│
└─ NO (Death Cross or Neutral)
   └─ Is Price < EMA50?
      ├─ YES → Downtrend Confirmed → Consider SELL/HOLD
      └─ NO → Neutral/Consolidation → Wait for clarity
```

### Tree 2: Momentum Confirmation

```
Is RSI between 40-70?
├─ YES (Healthy Momentum)
│  └─ Is MACD Bullish?
│     ├─ YES → Strong Momentum → Proceed to Volume Check
│     └─ NO → Weak Momentum → Reduce confidence
│
├─ RSI > 70 (Overbought)
│  └─ Wait for pullback or avoid entry
│
└─ RSI < 30 (Oversold)
   └─ Potential buying opportunity if trend supports
```

### Tree 3: Volume Confirmation

```
Is MFI > 50?
├─ YES (Buying Pressure)
│  └─ Is ADX > 20?
│     ├─ YES → Strong Trend with Volume → BUY Signal
│     └─ NO → Weak Trend → HOLD, wait for strength
│
└─ NO (Selling Pressure)
   └─ Is trend still bullish?
      ├─ YES → Divergence Warning → Reduce position size
      └─ NO → Bearish Confirmation → SELL/AVOID
```

### Tree 4: Risk/Reward Decision

```
Calculate Risk/Reward Ratio
├─ Ratio ≥ 1:2 (Acceptable)
│  └─ Is confidence HIGH?
│     ├─ YES → Full position size
│     └─ NO → Reduced position size
│
└─ Ratio < 1:2 (Not Acceptable)
   └─ HOLD → Wait for better setup
```

---

## Quality Assurance

### Pre-Delivery Checklist

Before delivering any recommendation, verify:

#### Data Quality
- [ ] Minimum 60 days of historical data
- [ ] All 7 indicators calculated successfully
- [ ] No missing or anomalous data points
- [ ] Current price is recent (< 1 day old)

#### Analysis Completeness
- [ ] All 5 phases completed
- [ ] Trend direction clearly identified
- [ ] Momentum status assessed
- [ ] Volume confirmation checked
- [ ] All scenarios developed with probabilities

#### Risk Management
- [ ] Position size calculated
- [ ] Stop loss level defined
- [ ] Profit targets set (multiple levels)
- [ ] Risk/reward ratio ≥ 1:2
- [ ] Maximum loss per trade specified

#### Recommendation Clarity
- [ ] Verdict is unequivocal (BUY/HOLD/SELL)
- [ ] Entry price specified
- [ ] Exit parameters defined
- [ ] Timeframe stated
- [ ] Rationale provided
- [ ] Confidence level assigned

#### Consistency Checks
- [ ] Verdict matches signal score
- [ ] Scenarios align with technical analysis
- [ ] Risk parameters are realistic
- [ ] Timeframe matches strategy
- [ ] No contradictions in analysis

### Common Pitfalls to Avoid

1. **Confirmation Bias**
   - Don't cherry-pick indicators
   - Consider all signals equally
   - Acknowledge conflicting data

2. **Overconfidence**
   - Don't ignore risks
   - Don't oversize positions
   - Don't skip stop losses

3. **Analysis Paralysis**
   - Don't wait for perfect setup
   - Make decision with available data
   - Accept some uncertainty

4. **Recency Bias**
   - Don't overweight recent price action
   - Consider full historical context
   - Look at multiple timeframes

5. **Anchoring**
   - Don't fixate on entry price
   - Adjust to new information
   - Be flexible with targets

### Continuous Improvement

After each analysis:
1. Document the recommendation
2. Track actual outcomes
3. Review what worked/didn't work
4. Refine decision criteria
5. Update probability estimates

---

## Summary

The 5-phase workflow ensures:
- **Systematic**: Same process every time
- **Comprehensive**: All factors considered
- **Risk-Aware**: Downside always evaluated
- **Actionable**: Clear entry/exit parameters
- **Accountable**: Documented rationale

By following this workflow rigorously, the Financial Analyst Mode delivers consistent, high-quality investment recommendations suitable for medium-term investors seeking safe, diversified portfolios.

---

**Next Steps:**
- Review [Usage Guide](04-usage-guide.md) for practical examples
- See [Analysis Examples](05-examples.md) for real-world cases
- Consult [Configuration](02-configuration.md) for setup details