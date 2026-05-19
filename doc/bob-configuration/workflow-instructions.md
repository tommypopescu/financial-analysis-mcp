# Workflow Instructions Configuration

## Overview

Workflow instruction files provide detailed, step-by-step guidance for Bob when operating in Financial Analyst mode. These XML files complement the mode definition in `custom_modes.yaml` by providing:
- Detailed analysis workflows
- Decision trees and logic
- Examples and templates
- Best practices and guidelines

## File Locations

```
.bob/rules-financial-analyst/
├── 1_analysis_workflow.xml    # 5-phase analysis framework (398 lines)
└── 2_analysis_examples.xml    # Educational examples (827 lines)
```

## Why XML Format?

XML is used for workflow instructions because:
- ✅ Structured and hierarchical
- ✅ Easy to parse and validate
- ✅ Supports complex nested content
- ✅ Can include code examples and templates
- ✅ Bob can process it efficiently

## File 1: Analysis Workflow (1_analysis_workflow.xml)

### Purpose

Defines the complete 5-phase analysis framework that Bob must follow for every stock analysis.

### Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<workflow>
    <metadata>
        <title>Financial Analysis Workflow</title>
        <version>1.0</version>
        <description>5-phase comprehensive analysis framework</description>
    </metadata>
    
    <phases>
        <phase id="1" name="Data Collection">
            <!-- Phase 1 details -->
        </phase>
        <phase id="2" name="Technical Analysis">
            <!-- Phase 2 details -->
        </phase>
        <!-- ... more phases -->
    </phases>
    
    <decision_trees>
        <!-- Decision logic -->
    </decision_trees>
    
    <quality_checks>
        <!-- Validation rules -->
    </quality_checks>
</workflow>
```

### Key Sections

#### 1. Phase Definitions

Each phase includes:
- **Objective**: What to accomplish
- **Tools**: Which MCP tools to use
- **Steps**: Detailed step-by-step process
- **Output**: Expected results
- **Quality Checks**: Validation criteria

**Example - Phase 1: Data Collection**:
```xml
<phase id="1" name="Data Collection">
    <objective>
        Gather all necessary market data and technical indicators
    </objective>
    
    <tools>
        <tool>fetch_ticker_data</tool>
        <tool>get_current_price</tool>
        <tool>calculate_all_indicators</tool>
    </tools>
    
    <steps>
        <step order="1">
            <action>Fetch historical OHLCV data (3-6 months)</action>
            <tool>fetch_ticker_data</tool>
            <parameters>
                <ticker>User-provided ticker symbol</ticker>
                <period>6mo</period>
            </parameters>
        </step>
        <!-- More steps -->
    </steps>
    
    <output>
        <item>Current price</item>
        <item>All 7 technical indicators calculated</item>
        <item>Historical price data</item>
    </output>
    
    <quality_checks>
        <check>Minimum 60 days of data</check>
        <check>All indicators successfully calculated</check>
        <check>No missing data points</check>
    </quality_checks>
</phase>
```

#### 2. Decision Trees

Provides logic for making decisions:
```xml
<decision_trees>
    <tree id="trend_assessment">
        <question>Is EMA50 > EMA200?</question>
        <yes>
            <question>Is Price > EMA50?</question>
            <yes>
                <result>Uptrend Confirmed</result>
                <action>Proceed to momentum check</action>
            </yes>
            <no>
                <result>Weak Uptrend</result>
                <action>Caution, check other indicators</action>
            </no>
        </yes>
        <no>
            <result>Downtrend or Neutral</result>
            <action>Consider SELL/HOLD</action>
        </no>
    </tree>
</decision_trees>
```

#### 3. Quality Checks

Validation rules before delivering recommendation:
```xml
<quality_checks>
    <category name="Data Quality">
        <check>Minimum 60 days of historical data</check>
        <check>All 7 indicators calculated</check>
        <check>Current price is recent (< 1 day old)</check>
    </category>
    
    <category name="Analysis Completeness">
        <check>All 5 phases completed</check>
        <check>Trend direction identified</check>
        <check>Scenarios developed with probabilities</check>
    </category>
    
    <category name="Risk Management">
        <check>Position size calculated</check>
        <check>Stop loss defined</check>
        <check>Risk/reward ratio ≥ 1:2</check>
    </category>
</quality_checks>
```

### Content Highlights

**Phase 1: Data Collection** (Lines 15-85)
- Tool usage instructions
- Data validation requirements
- Error handling

**Phase 2: Technical Analysis** (Lines 87-195)
- Indicator interpretation rules
- Trend identification logic
- Momentum assessment criteria

**Phase 3: Scenario Planning** (Lines 197-285)
- Bullish/bearish/neutral scenarios
- Probability assessment methods
- Price target calculation

**Phase 4: Risk Assessment** (Lines 287-345)
- Position sizing formulas
- Stop loss placement rules
- Risk/reward calculation

**Phase 5: Investment Decision** (Lines 347-398)
- Signal scoring system
- Decision matrix
- Verdict formatting requirements

## File 2: Analysis Examples (2_analysis_examples.xml)

### Purpose

Provides educational examples showing how to apply the workflow to real stocks.

### Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<examples>
    <metadata>
        <title>Financial Analysis Examples</title>
        <version>1.0</version>
        <source>Educational examples based on Investopedia principles</source>
    </metadata>
    
    <example id="1" type="strong_buy">
        <!-- Complete analysis example -->
    </example>
    
    <example id="2" type="hold">
        <!-- Complete analysis example -->
    </example>
    
    <!-- More examples -->
</examples>
```

### Example Types

1. **Strong Buy** (Lines 15-185)
   - All indicators bullish
   - Clear uptrend
   - Good risk/reward
   - Example: AAPL analysis

2. **Hold - Mixed Signals** (Lines 187-295)
   - Conflicting indicators
   - Weak trend
   - Unclear direction
   - Example: TSLA analysis

3. **Sell - Downtrend** (Lines 297-405)
   - Bearish indicators
   - Death Cross
   - Negative momentum
   - Example: META analysis

4. **Romanian Stock** (Lines 407-515)
   - BVB-specific considerations
   - Currency risk
   - Liquidity issues
   - Example: TLV analysis

5. **Portfolio Comparison** (Lines 517-625)
   - Multiple stock analysis
   - Ranking methodology
   - Allocation strategy
   - Example: AAPL vs MSFT vs GOOGL

6. **Oversold Opportunity** (Lines 627-735)
   - RSI < 30 screening
   - Bounce potential
   - Entry timing
   - Example: NVDA analysis

7. **Profit Taking** (Lines 737-827)
   - Existing position review
   - Partial profit strategy
   - Trailing stop usage
   - Example: AAPL at +17.9%

### Example Structure

Each example includes:
```xml
<example id="1" type="strong_buy">
    <ticker>AAPL</ticker>
    <scenario>Strong uptrend with healthy momentum</scenario>
    
    <phase1_data>
        <current_price>185.50</current_price>
        <indicators>
            <ema50>178.20</ema50>
            <ema200>172.45</ema200>
            <rsi>62.5</rsi>
            <!-- More indicators -->
        </indicators>
    </phase1_data>
    
    <phase2_analysis>
        <trend>Strong uptrend (Golden Cross)</trend>
        <momentum>Healthy (RSI 62.5)</momentum>
        <!-- More analysis -->
    </phase2_analysis>
    
    <phase3_scenarios>
        <bullish probability="65%">
            <target>205.00</target>
            <timeframe>3-4 months</timeframe>
        </bullish>
        <!-- More scenarios -->
    </phase3_scenarios>
    
    <phase4_risk>
        <position_size>2-3% of portfolio</position_size>
        <stop_loss>176.50</stop_loss>
        <risk_reward>1:2.17</risk_reward>
    </phase4_risk>
    
    <phase5_verdict>
        <decision>BUY</decision>
        <confidence>High (85%)</confidence>
        <rationale>
            All 7 indicators bullish, strong trend, good risk/reward
        </rationale>
    </phase5_verdict>
</example>
```

## Creating Workflow Instructions

### Step 1: Create Directory

```bash
mkdir -p .bob/rules-financial-analyst
```

### Step 2: Create Workflow File

Create `.bob/rules-financial-analyst/1_analysis_workflow.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<workflow>
    <metadata>
        <title>Financial Analysis Workflow</title>
        <version>1.0</version>
    </metadata>
    
    <!-- Add phases, decision trees, quality checks -->
</workflow>
```

### Step 3: Create Examples File

Create `.bob/rules-financial-analyst/2_analysis_examples.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<examples>
    <metadata>
        <title>Financial Analysis Examples</title>
        <version>1.0</version>
    </metadata>
    
    <!-- Add examples -->
</examples>
```

### Step 4: Validate XML

Use online XML validator or:
```bash
xmllint --noout 1_analysis_workflow.xml
xmllint --noout 2_analysis_examples.xml
```

### Step 5: Test with Bob

1. Restart VS Code
2. Switch to Financial Analyst mode
3. Request analysis: "Analizează AAPL"
4. Verify Bob follows workflow

## How Bob Uses These Files

### 1. Mode Activation

When Financial Analyst mode is activated:
```
1. Bob loads custom_modes.yaml
2. Bob reads roleDefinition
3. Bob loads workflow instructions from .bob/rules-financial-analyst/
4. Bob combines all instructions
```

### 2. Analysis Execution

For each analysis request:
```
1. Bob follows Phase 1 (Data Collection)
   - Uses tools specified in workflow
   - Validates data quality
   
2. Bob follows Phase 2 (Technical Analysis)
   - Applies interpretation rules
   - Uses decision trees
   
3. Bob follows Phase 3 (Scenario Planning)
   - Develops scenarios per template
   - Calculates probabilities
   
4. Bob follows Phase 4 (Risk Assessment)
   - Applies formulas from workflow
   - Validates risk/reward
   
5. Bob follows Phase 5 (Investment Decision)
   - Uses decision matrix
   - Formats verdict per template
   
6. Bob runs quality checks
   - Validates completeness
   - Ensures all requirements met
```

### 3. Example Reference

Bob references examples when:
- User asks for similar analysis
- Bob needs clarification on format
- Bob wants to verify approach
- Bob needs to explain methodology

## Customization

### Add New Phase

```xml
<phase id="6" name="Fundamental Analysis">
    <objective>
        Analyze company fundamentals
    </objective>
    
    <tools>
        <tool>fetch_fundamentals</tool>
    </tools>
    
    <steps>
        <step order="1">
            <action>Fetch P/E ratio</action>
        </step>
        <!-- More steps -->
    </steps>
</phase>
```

### Add New Decision Tree

```xml
<tree id="volume_confirmation">
    <question>Is MFI > 50?</question>
    <yes>
        <result>Buying Pressure</result>
        <action>Bullish confirmation</action>
    </yes>
    <no>
        <result>Selling Pressure</result>
        <action>Bearish warning</action>
    </no>
</tree>
```

### Add New Example

```xml
<example id="8" type="dividend_stock">
    <ticker>KO</ticker>
    <scenario>Dividend stock analysis</scenario>
    
    <!-- Add all phases -->
    
    <special_considerations>
        <dividend_yield>3.2%</dividend_yield>
        <payout_ratio>75%</payout_ratio>
    </special_considerations>
</example>
```

### Modify Quality Checks

```xml
<quality_checks>
    <category name="Fundamental Analysis">
        <check>P/E ratio analyzed</check>
        <check>Debt-to-equity reviewed</check>
        <check>Revenue growth assessed</check>
    </category>
</quality_checks>
```

## Best Practices

### 1. Keep Workflow Detailed

Provide specific instructions:
```xml
<!-- Good -->
<step>
    <action>Calculate RSI using 14-period</action>
    <formula>RSI = 100 - (100 / (1 + RS))</formula>
    <interpretation>
        RSI > 70: Overbought
        RSI < 30: Oversold
    </interpretation>
</step>

<!-- Bad -->
<step>
    <action>Check RSI</action>
</step>
```

### 2. Include Decision Logic

Provide clear decision trees:
```xml
<!-- Good -->
<tree>
    <question>Is RSI > 70?</question>
    <yes>
        <result>Overbought</result>
        <action>Wait for pullback</action>
    </yes>
    <no>
        <question>Is RSI < 30?</question>
        <yes>
            <result>Oversold</result>
            <action>Potential buy opportunity</action>
        </yes>
    </no>
</tree>

<!-- Bad -->
<tree>
    <question>Check RSI</question>
    <action>Decide</action>
</tree>
```

### 3. Provide Complete Examples

Include all phases in examples:
```xml
<!-- Good -->
<example>
    <phase1_data>...</phase1_data>
    <phase2_analysis>...</phase2_analysis>
    <phase3_scenarios>...</phase3_scenarios>
    <phase4_risk>...</phase4_risk>
    <phase5_verdict>...</phase5_verdict>
</example>

<!-- Bad -->
<example>
    <verdict>BUY</verdict>
</example>
```

### 4. Use Consistent Formatting

Maintain consistent structure:
```xml
<!-- Good -->
<indicator>
    <name>RSI</name>
    <value>62.5</value>
    <interpretation>Healthy momentum</interpretation>
</indicator>

<!-- Bad -->
<rsi>62.5 - healthy</rsi>
```

### 5. Validate XML

Always validate before committing:
```bash
xmllint --noout *.xml
```

## Troubleshooting

### Bob Doesn't Follow Workflow

**Problem**: Bob ignores workflow instructions

**Solutions**:
1. Check files exist in `.bob/rules-financial-analyst/`
2. Validate XML syntax
3. Restart VS Code
4. Check Bob console for errors
5. Verify mode is active

### XML Parse Errors

**Problem**: Bob shows XML parse error

**Solutions**:
1. Validate XML: `xmllint --noout file.xml`
2. Check for:
   - Unclosed tags
   - Special characters (use `<` for `<`)
   - Encoding issues
   - Invalid structure

### Workflow Not Loading

**Problem**: Bob doesn't load workflow files

**Solutions**:
1. Check directory name: `.bob/rules-financial-analyst/`
2. Check file names: `1_analysis_workflow.xml`, `2_analysis_examples.xml`
3. Check file permissions
4. Check file encoding (UTF-8)

### Examples Not Referenced

**Problem**: Bob doesn't use examples

**Solutions**:
1. Ensure examples file exists
2. Check example structure matches workflow
3. Add more examples for coverage
4. Reference examples explicitly in mode definition

## Integration with Custom Modes

Workflow instructions complement custom modes:

**custom_modes.yaml**:
- High-level role definition
- Tool permissions
- Activation triggers

**Workflow Instructions**:
- Detailed step-by-step process
- Decision logic
- Examples and templates
- Quality checks

Together they provide:
- ✅ Complete mode definition
- ✅ Detailed execution guidance
- ✅ Quality assurance
- ✅ Consistent results

## Related Documentation

- [Custom Modes Configuration](custom-modes.md)
- [MCP Wrapper Configuration](mcp-wrapper.md)
- [Financial Analyst Mode Workflow](../financial-analyst-mode/03-workflow.md)
- [Financial Analyst Mode Examples](../financial-analyst-mode/05-examples.md)

## Summary

Workflow instruction files:
- ✅ Provide detailed analysis framework
- ✅ Define 5-phase workflow
- ✅ Include decision trees and logic
- ✅ Offer educational examples
- ✅ Ensure consistent analysis quality
- ✅ Guide Bob's behavior in Financial Analyst mode

**Key Points**:
1. Located in `.bob/rules-financial-analyst/`
2. XML format for structure
3. Two files: workflow + examples
4. Complement custom_modes.yaml
5. Loaded automatically by Bob

**Next Steps**:
- Review [Analysis Workflow](../financial-analyst-mode/03-workflow.md)
- Study [Analysis Examples](../financial-analyst-mode/05-examples.md)
- Test workflow with real analysis
- Customize as needed