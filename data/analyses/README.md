# Portfolio Analysis History

This directory contains historical portfolio analyses with timestamps for maintaining context and tracking investment decisions over time.

## Directory Structure

```
analyses/
├── README.md (this file)
├── YYYY-MM-DD_portfolio1_analysis.md
├── YYYY-MM-DD_portfolio2_analysis.md
├── YYYY-MM-DD_prices_snapshot.csv
├── YYYY-MM-DD_TICKER_analysis.md
└── ...
```

## File Naming Convention

### Portfolio Analyses
- **Format**: `YYYY-MM-DD_portfolio{N}_analysis.md`
- **Example**: `2026-05-19_portfolio1_analysis.md`
- **Content**: Complete portfolio analysis with recommendations, technical data, and risk management

### Individual Ticker Analyses
- **Format**: `YYYY-MM-DD_{TICKER}_analysis.md`
- **Example**: `2026-05-19_DIGI.RO_analysis.md`
- **Content**: Detailed technical analysis for a specific ticker

### Price Snapshots
- **Format**: `YYYY-MM-DD_prices_snapshot.csv`
- **Example**: `2026-05-19_prices_snapshot.csv`
- **Content**: CSV with all ticker prices and indicators for quick reference

## Usage

### For Bob Financial Analyst Mode

When starting a new analysis:
1. Check for existing analyses from today's date
2. If found, load and reference existing data instead of re-fetching
3. If not found, proceed with fresh analysis
4. After completion, save all results using the templates

### For Users

- Review historical recommendations to track performance
- Compare analyses across different dates
- Reference past technical conditions
- Build investment decision history

## File Templates

### Portfolio Analysis Template

Each portfolio analysis includes:
- Analysis date and time
- Portfolio composition summary
- Market conditions (closing prices)
- Technical analysis summary
- Investment recommendations with allocations
- Risk management strategy
- Monitoring plan
- Avoided investments with rationale

### Ticker Analysis Template

Each ticker analysis includes:
- Current market data (price, volume, 52-week high/low)
- Technical indicators (RSI, MACD, EMAs)
- Scenario analysis (bullish/neutral/bearish)
- Risk assessment
- Investment verdict (BUY/HOLD/SELL)
- Entry and exit strategies
- Monitoring plan

### Price Snapshot CSV

Columns:
- ticker
- price
- change_pct
- rsi
- macd
- ema50
- ema200
- status (BULLISH/BEARISH/OVERSOLD/OVERBOUGHT)
- recommendation (BUY/HOLD/SELL/AVOID)

## Best Practices

1. **Always save analyses immediately** after completion
2. **Include full technical data** in saved files
3. **Use consistent formatting** for easy parsing
4. **Reference historical analyses** when making new recommendations
5. **Keep CSV snapshots** for quick reference

## Retention Policy

- Keep all analyses indefinitely for historical reference
- Analyses older than 1 year can be archived to a separate directory if needed
- Never delete analyses without backing them up first

---

*This directory is managed by Bob Financial Analyst Mode*
*Last updated: 2026-05-19*