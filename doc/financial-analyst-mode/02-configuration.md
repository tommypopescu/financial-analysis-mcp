# Financial Analyst Mode - Configuration

Complete guide for configuring Bob's Financial Analyst Mode.

## Prerequisites

Before configuring the mode, ensure:
1. ✅ MCP Server is deployed and running (http://192.168.1.7:8000)
2. ✅ MCP Wrapper is installed (`C:\Users\O82652826\financial-analysis-mcp-wrapper.py`)
3. ✅ Bob is installed and running
4. ✅ Python 3.8+ is available on Windows

## Configuration Files

### File Locations

```
C:\Users\O82652826\
├── financial-analysis-mcp-wrapper.py          # MCP wrapper
└── .git\
    └── .bob\
        ├── custom_modes.yaml                   # Mode configuration
        └── rules-financial-analyst\            # Mode instructions
            ├── 1_analysis_workflow.xml
            └── 2_analysis_examples.xml

C:\Users\O82652826\AppData\Local\Programs\IBM Bob\
└── mcp_settings.json                          # MCP server connection
```

## Step-by-Step Configuration

### Step 1: Configure MCP Connection

**File**: `C:\Users\O82652826\AppData\Local\Programs\IBM Bob\mcp_settings.json`

```json
{
  "mcpServers": {
    "financial-analysis": {
      "command": "python",
      "args": [
        "C:\\Users\\O82652826\\financial-analysis-mcp-wrapper.py"
      ],
      "env": {}
    }
  }
}
```

**Key Points**:
- Server name: `financial-analysis` (referenced in mode config)
- Command: `python` (or full path if needed: `C:\\Python311\\python.exe`)
- Args: Full path to wrapper script (use double backslashes)
- Env: Empty object (no environment variables needed)

**Verification**:
```powershell
# Test wrapper manually
python C:\Users\O82652826\financial-analysis-mcp-wrapper.py
# Input: {"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}
# Should return list of 7 tools
```

---

### Step 2: Add Mode Configuration

**File**: `C:\Users\O82652826\.git\.bob\custom_modes.yaml`

```yaml
- slug: financial-analyst
  name: 📊 Financial Analyst
  roleDefinition: |
    You are Bob, a financial analyst specializing in comprehensive stock market analysis for medium-term investors (3-12 months investment horizon).
    
    Your expertise includes:
    - Technical analysis using multiple indicators (EMA, RSI, MACD, ADX, Stochastic, Bollinger Bands, MFI)
    - Risk assessment and position sizing strategies
    - Scenario-based planning (bullish, bearish, neutral)
    - Clear, unequivocal investment recommendations (BUY/SELL/HOLD)
    
    Your analysis philosophy:
    - Safety first: Capital preservation is paramount
    - Multiple indicator confirmation: Never rely on single indicator
    - Clear communication: No jargon without explanation
    - Actionable strategies: Specific entry/exit points with stop-loss levels
    - Risk management: Risk-reward ratios ≥ 2:1
    
    You provide comprehensive analysis reports that include:
    1. Technical indicator analysis with interpretations
    2. Three scenarios (bullish, bearish, neutral) with probabilities
    3. Risk metrics (stop-loss, position sizing, profit targets)
    4. Unequivocal verdict (BUY/SELL/HOLD) with clear reasoning
    5. Entry and exit strategies with specific price levels
    
    You are direct, professional, and focused on helping investors make informed decisions based on technical analysis.
  
  whenToUse: |
    Use this mode when performing comprehensive stock market analysis for investment decisions. This includes:
    - Analyzing individual stock tickers for buy/sell/hold decisions
    - Evaluating portfolio diversification opportunities
    - Assessing technical indicators (EMA, RSI, MACD) for medium-term investments
    - Generating detailed investment reports with clear verdicts
    - Risk assessment and position sizing recommendations
    - Comparing multiple stocks for portfolio allocation
    - Reviewing existing positions for hold/sell decisions
    
    This mode is specifically designed for medium-term investors seeking safe, diversified investments with clear, actionable recommendations.
  
  groups:
    - read      # Can read files
    - mcp       # Can use MCP tools (REQUIRED for financial-analysis server)
    - command   # Can execute commands
```

**Key Configuration Elements**:

1. **slug**: `financial-analyst` - Used in `/mode financial-analyst` command
2. **name**: `📊 Financial Analyst` - Display name in mode list
3. **roleDefinition**: Defines Bob's personality and expertise in this mode
4. **whenToUse**: Helps Bob decide when to use this mode
5. **groups**: Permissions (MCP is REQUIRED for financial tools)

---

### Step 3: Add Workflow Instructions

**File**: `C:\Users\O82652826\.git\.bob\rules-financial-analyst\1_analysis_workflow.xml`

This file contains the 5-phase analysis workflow. See [bob-configuration/rules-financial-analyst/1_analysis_workflow.xml](../bob-configuration/rules-financial-analyst/1_analysis_workflow.xml) for complete content.

**Structure**:
```xml
<financial_analyst_workflow>
  <overview>...</overview>
  
  <phase_1_data_collection>
    <mcp_tools>...</mcp_tools>
    <data_requirements>...</data_requirements>
  </phase_1_data_collection>
  
  <phase_2_technical_analysis>
    <indicators>...</indicators>
    <interpretation_guidelines>...</interpretation_guidelines>
  </phase_2_technical_analysis>
  
  <phase_3_scenario_development>
    <bullish_scenario>...</bullish_scenario>
    <bearish_scenario>...</bearish_scenario>
    <neutral_scenario>...</neutral_scenario>
  </phase_3_scenario_development>
  
  <phase_4_risk_assessment>
    <stop_loss>...</stop_loss>
    <position_sizing>...</position_sizing>
    <profit_targets>...</profit_targets>
  </phase_4_risk_assessment>
  
  <phase_5_verdict_formulation>
    <decision_criteria>...</decision_criteria>
    <communication_template>...</communication_template>
  </phase_5_verdict_formulation>
</financial_analyst_workflow>
```

**Key Sections**:
- **Phase 1**: MCP tool usage for data collection
- **Phase 2**: Technical indicator interpretation rules
- **Phase 3**: Scenario probability calculations
- **Phase 4**: Risk management formulas
- **Phase 5**: Verdict decision tree

---

### Step 4: Add Educational Examples

**File**: `C:\Users\O82652826\.git\.bob\rules-financial-analyst\2_analysis_examples.xml`

This file contains educational content from Investopedia and real analysis examples. See [bob-configuration/rules-financial-analyst/2_analysis_examples.xml](../bob-configuration/rules-financial-analyst/2_analysis_examples.xml) for complete content.

**Structure**:
```xml
<financial_analyst_examples>
  <technical_analysis_fundamentals>
    <what_is_technical_analysis>...</what_is_technical_analysis>
    <key_principles>...</key_principles>
  </technical_analysis_fundamentals>
  
  <indicator_interpretation_guide>
    <ema_analysis>...</ema_analysis>
    <rsi_analysis>...</rsi_analysis>
    <macd_analysis>...</macd_analysis>
    <!-- ... other indicators ... -->
  </indicator_interpretation_guide>
  
  <complete_analysis_examples>
    <example_bullish_stock>...</example_bullish_stock>
    <example_bearish_stock>...</example_bearish_stock>
    <example_neutral_stock>...</example_neutral_stock>
  </complete_analysis_examples>
  
  <communication_templates>...</communication_templates>
  <quality_assurance_checklist>...</quality_assurance_checklist>
</financial_analyst_examples>
```

**Key Content**:
- Technical analysis fundamentals
- Indicator interpretation guidelines
- Complete analysis examples (bullish, bearish, neutral)
- Communication templates
- Quality assurance checklist

---

## Verification Steps

### 1. Check MCP Server Connection

```powershell
# Test MCP server directly
Invoke-RestMethod -Uri "http://192.168.1.7:8000/tools/list" -Method Post -ContentType "application/json" -Body '{}'
```

**Expected Output**: List of 7 tools

### 2. Check Wrapper

```powershell
# Test wrapper
python C:\Users\O82652826\financial-analysis-mcp-wrapper.py
```

**Input**:
```json
{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}
```

**Expected Output**: JSON-RPC response with tools list

### 3. Check Bob Configuration

1. Restart Bob
2. Check mode list: Should see "📊 Financial Analyst"
3. Switch mode: `/mode financial-analyst`
4. Check MCP status: Should see green indicator for "financial-analysis"

### 4. Test Mode Functionality

```
/mode financial-analyst
list tickers
```

**Expected Output**: List of 27 tickers from watchlist

---

## Troubleshooting Configuration

### Problem: Mode Not Appearing

**Check**:
1. File location: `C:\Users\O82652826\.git\.bob\custom_modes.yaml`
2. YAML syntax: Use YAML validator
3. Indentation: Use spaces, not tabs
4. Restart Bob

**Solution**:
```yaml
# Verify YAML structure
- slug: financial-analyst  # Must start with dash
  name: 📊 Financial Analyst
  roleDefinition: |        # Pipe for multi-line
    Content here...
  whenToUse: |
    Content here...
  groups:                  # List format
    - read
    - mcp
    - command
```

---

### Problem: MCP Server Not Connecting

**Check**:
1. Server running: `docker ps | grep financial-analysis-mcp`
2. Port accessible: `curl http://192.168.1.7:8000/tools/list`
3. Wrapper path correct in mcp_settings.json
4. Python available: `python --version`

**Solution**:
```json
// mcp_settings.json - Use full Python path if needed
{
  "mcpServers": {
    "financial-analysis": {
      "command": "C:\\Python311\\python.exe",  // Full path
      "args": ["C:\\Users\\O82652826\\financial-analysis-mcp-wrapper.py"]
    }
  }
}
```

---

### Problem: MCP Tools Not Working

**Check**:
1. Mode has MCP group: `groups: [read, mcp, command]`
2. Server name matches: "financial-analysis" in both files
3. Green indicator in Bob
4. Test tool manually: `list tickers`

**Solution**:
```yaml
# custom_modes.yaml - MCP group is REQUIRED
groups:
  - read
  - mcp      # This is essential!
  - command
```

---

### Problem: Workflow Instructions Not Loading

**Check**:
1. Files exist in correct location
2. XML syntax valid
3. File encoding UTF-8
4. No BOM (Byte Order Mark)

**Solution**:
```bash
# Verify files exist
ls C:\Users\O82652826\.git\.bob\rules-financial-analyst\

# Should show:
# 1_analysis_workflow.xml
# 2_analysis_examples.xml
```

---

## Advanced Configuration

### Custom Wrapper URL

If MCP server is on different host:

```python
# financial-analysis-mcp-wrapper.py
MCP_SERVER_URL = "http://192.168.1.7:8000"  # Change this
```

### Custom Ticker Watchlist

Add tickers to server's watchlist:

```
/mode financial-analyst
add ticker BRD.RO
```

Or edit directly on server:
```bash
ssh tommy@192.168.1.7
nano ~/financial-analysis-mcp/data/tickers.csv
```

### Multiple Environments

Create separate wrappers for different environments:

```
financial-analysis-mcp-wrapper-dev.py   → http://localhost:8000
financial-analysis-mcp-wrapper-prod.py  → http://192.168.1.7:8000
```

Update mcp_settings.json accordingly.

---

## Configuration Best Practices

### 1. File Backups

```powershell
# Backup configuration files
$date = Get-Date -Format "yyyyMMdd"
Copy-Item "C:\Users\O82652826\.git\.bob\custom_modes.yaml" `
          "C:\Users\O82652826\.git\.bob\custom_modes.yaml.$date.bak"
```

### 2. Version Control

Keep configuration in Git:
```bash
cd C:\Users\O82652826\.git
git add .bob/custom_modes.yaml
git add .bob/rules-financial-analyst/
git commit -m "Update Financial Analyst mode configuration"
```

### 3. Documentation

Document any custom changes:
```yaml
# custom_modes.yaml
# Modified: 2026-05-19
# Changes: Added custom risk thresholds
# Author: Your Name
```

### 4. Testing

Always test after configuration changes:
```
1. Restart Bob
2. /mode financial-analyst
3. list tickers
4. analyze AAPL
```

---

## Configuration Templates

### Minimal Configuration

For basic setup:

```yaml
- slug: financial-analyst
  name: 📊 Financial Analyst
  roleDefinition: |
    Financial analyst for stock market analysis.
  whenToUse: |
    Use for stock analysis.
  groups:
    - read
    - mcp
    - command
```

### Full Configuration

See complete files in [bob-configuration/](../bob-configuration/) directory.

---

## Related Documentation

- [Overview](01-overview.md) - Mode purpose and features
- [Workflow](03-workflow.md) - 5-phase analysis process
- [Usage Guide](04-usage-guide.md) - How to use the mode
- [Examples](05-examples.md) - Real analysis examples
- [Bob Configuration Files](../bob-configuration/) - Complete config files