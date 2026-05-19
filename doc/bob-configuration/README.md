# Bob Configuration Documentation

## Overview

This directory contains documentation for Bob's configuration files used in the Financial Analysis MCP Server project.

## Configuration Files

### 1. Custom Modes Configuration
- **File**: `.bob/custom_modes.yaml`
- **Purpose**: Defines custom Bob modes including Financial Analyst mode
- **Documentation**: [custom-modes.md](custom-modes.md)

### 2. MCP Server Configuration
- **File**: `financial-analysis-mcp-wrapper.py`
- **Purpose**: Python wrapper that bridges stdio MCP protocol to HTTP backend
- **Documentation**: [mcp-wrapper.md](mcp-wrapper.md)

### 3. Workflow Instructions
- **Directory**: `.bob/rules-financial-analyst/`
- **Files**:
  - `1_analysis_workflow.xml` - 5-phase analysis framework
  - `2_analysis_examples.xml` - Educational examples
- **Documentation**: [workflow-instructions.md](workflow-instructions.md)

## Quick Start

1. **Custom Modes**: Configure Bob modes in `.bob/custom_modes.yaml`
2. **MCP Wrapper**: Set up Python wrapper for MCP server connection
3. **Workflow Rules**: Add analysis workflow instructions to `.bob/rules-financial-analyst/`

## Related Documentation

- [MCP Server Documentation](../mcp-server/README.md)
- [Financial Analyst Mode Documentation](../financial-analyst-mode/README.md)
- [AI Context Documentation](../ai-context/README.md)

## File Locations

```
.bob/
├── custom_modes.yaml              # Bob custom modes configuration
└── rules-financial-analyst/       # Financial Analyst mode instructions
    ├── 1_analysis_workflow.xml    # 5-phase analysis framework
    └── 2_analysis_examples.xml    # Educational examples

C:/Users/O82652826/
└── financial-analysis-mcp-wrapper.py  # MCP stdio-to-HTTP wrapper
```

## Configuration Flow

```
┌─────────────────────────────────────────────────────────────┐
│                         Bob (VS Code)                        │
│  • Reads custom_modes.yaml for mode definitions            │
│  • Loads workflow instructions from rules-financial-analyst/│
│  • Connects to MCP server via wrapper                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              financial-analysis-mcp-wrapper.py               │
│  • Bridges stdio (Bob) to HTTP (MCP server)                │
│  • Handles JSON-RPC 2.0 protocol                           │
│  • Forwards requests to http://192.168.1.7:8000            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│         Financial Analysis MCP Server (Docker)               │
│  • Running on OMV server at 192.168.1.7:8000               │
│  • Provides 7 financial analysis tools                      │
│  • Fetches data from Yahoo Finance                          │
└─────────────────────────────────────────────────────────────┘
```

## Troubleshooting

### Bob Cannot Find Custom Mode
- Check `.bob/custom_modes.yaml` exists
- Verify YAML syntax is correct
- Restart VS Code

### MCP Connection Failed
- Verify wrapper is configured correctly
- Check MCP server is running: `docker ps | grep financial-analysis`
- Test connection: `Test-NetConnection 192.168.1.7 -Port 8000`

### Workflow Instructions Not Loading
- Check `.bob/rules-financial-analyst/` directory exists
- Verify XML files are valid
- Check file permissions

## Next Steps

- Review [Custom Modes Configuration](custom-modes.md)
- Set up [MCP Wrapper](mcp-wrapper.md)
- Configure [Workflow Instructions](workflow-instructions.md)