# AI Context Documentation

## Overview

This directory contains comprehensive context information for AI assistants (Bob, Claude, etc.) to understand the project and make informed modifications.

## Purpose

These documents provide:
- ✅ High-level project overview
- ✅ Technical decisions and rationale
- ✅ Modification guidelines
- ✅ Historical troubleshooting knowledge

## Target Audience

- **AI Assistants**: Bob, Claude, GPT-4, etc.
- **Future Developers**: Understanding project evolution
- **Maintainers**: Context for decision-making

## Document Structure

### 1. [Project Overview](01-project-overview.md)
**What**: Complete project description
**Content**:
- Project goals and objectives
- System architecture overview
- Key components and their roles
- Technology stack
- Current status

**Use When**:
- Starting work on the project
- Need high-level understanding
- Explaining project to others

### 2. [Technical Decisions](02-technical-decisions.md)
**What**: Key technical choices and rationale
**Content**:
- Why HTTP transport instead of stdio
- Why FastAPI for MCP server
- Why Docker deployment
- Why specific technical indicators
- Why 5-phase analysis framework

**Use When**:
- Questioning existing architecture
- Considering alternatives
- Making new technical decisions
- Understanding trade-offs

### 3. [Modification Guide](03-modification-guide.md)
**What**: How to make changes safely
**Content**:
- Adding new MCP tools
- Modifying analysis workflow
- Updating technical indicators
- Changing Bob mode behavior
- Testing and validation

**Use When**:
- Adding new features
- Fixing bugs
- Refactoring code
- Updating dependencies

### 4. [Troubleshooting History](04-troubleshooting-history.md)
**What**: Problems encountered and solutions
**Content**:
- stdio compatibility issues
- DataFrame serialization errors
- GitHub Actions workflow problems
- MultiIndex handling bugs
- Bob configuration conflicts

**Use When**:
- Encountering similar issues
- Understanding past problems
- Avoiding known pitfalls
- Learning from history

## How to Use This Documentation

### For AI Assistants

**Initial Context Loading**:
```
1. Read project-overview.md first
2. Scan technical-decisions.md for architecture understanding
3. Reference modification-guide.md when making changes
4. Check troubleshooting-history.md for known issues
```

**During Task Execution**:
```
1. Consult modification-guide.md for relevant section
2. Review technical-decisions.md for constraints
3. Check troubleshooting-history.md for similar issues
4. Update documentation if new patterns emerge
```

**After Completing Changes**:
```
1. Update modification-guide.md with new patterns
2. Add to troubleshooting-history.md if issues encountered
3. Update technical-decisions.md if architecture changed
```

### For Human Developers

**Getting Started**:
```bash
# Read in order:
1. doc/ai-context/01-project-overview.md
2. doc/README.md
3. doc/mcp-server/01-architecture.md
4. doc/financial-analyst-mode/01-overview.md
```

**Making Changes**:
```bash
# Consult:
1. doc/ai-context/03-modification-guide.md
2. Relevant component documentation
3. doc/ai-context/02-technical-decisions.md
```

**Troubleshooting**:
```bash
# Check:
1. doc/ai-context/04-troubleshooting-history.md
2. doc/mcp-server/04-troubleshooting.md
3. GitHub Issues
```

## Document Maintenance

### When to Update

**Project Overview**:
- Major feature additions
- Architecture changes
- Technology stack updates
- Status changes

**Technical Decisions**:
- New architectural choices
- Alternative approaches considered
- Trade-off analysis
- Lessons learned

**Modification Guide**:
- New modification patterns
- Updated procedures
- New best practices
- Tool updates

**Troubleshooting History**:
- New issues encountered
- Solutions discovered
- Workarounds implemented
- Bugs fixed

### How to Update

1. **Identify Change Type**:
   - Feature addition → Update project-overview.md + modification-guide.md
   - Bug fix → Update troubleshooting-history.md
   - Architecture change → Update technical-decisions.md + project-overview.md
   - Process improvement → Update modification-guide.md

2. **Make Updates**:
   ```bash
   # Edit relevant file
   vim doc/ai-context/XX-filename.md
   
   # Add entry with date and description
   # Include context and rationale
   ```

3. **Commit Changes**:
   ```bash
   git add doc/ai-context/
   git commit -m "docs: Update AI context - [brief description]"
   git push origin master
   ```

## Integration with Other Documentation

### Relationship to Component Docs

```
AI Context (High-level, conceptual)
    ↓
Component Docs (Detailed, technical)
    ↓
Code (Implementation)
```

**Example Flow**:
```
User wants to add new indicator
    ↓
1. Read ai-context/03-modification-guide.md
   → Understand general process
    ↓
2. Read mcp-server/05-development.md
   → Get specific implementation steps
    ↓
3. Read mcp-server/02-api-reference.md
   → Understand API structure
    ↓
4. Implement changes
    ↓
5. Update ai-context/03-modification-guide.md
   → Document new pattern if applicable
```

### Cross-References

AI Context documents reference:
- MCP Server documentation
- Financial Analyst Mode documentation
- Bob Configuration documentation
- Code files and examples

Component documentation references:
- AI Context for rationale
- Other component docs for integration
- Code examples for implementation

## Best Practices

### For AI Assistants

1. **Always Read Context First**:
   - Don't assume based on code alone
   - Understand rationale behind decisions
   - Check for known issues

2. **Update Documentation**:
   - Add new patterns to modification guide
   - Document issues in troubleshooting history
   - Update technical decisions if architecture changes

3. **Maintain Consistency**:
   - Follow existing patterns
   - Use established terminology
   - Respect architectural decisions

4. **Ask When Uncertain**:
   - Use ask_followup_question tool
   - Don't make assumptions
   - Clarify requirements

### For Human Developers

1. **Keep Context Updated**:
   - Document decisions as you make them
   - Add troubleshooting entries immediately
   - Update guides with new patterns

2. **Write for AI Consumption**:
   - Be explicit and detailed
   - Include rationale and context
   - Use clear structure

3. **Cross-Reference Properly**:
   - Link to related documentation
   - Reference code files
   - Provide examples

4. **Review Regularly**:
   - Check for outdated information
   - Update with new learnings
   - Remove obsolete content

## Quick Reference

### Common Tasks

| Task | Primary Document | Supporting Docs |
|------|-----------------|-----------------|
| Add new MCP tool | modification-guide.md | mcp-server/05-development.md |
| Modify analysis workflow | modification-guide.md | financial-analyst-mode/03-workflow.md |
| Fix bug | troubleshooting-history.md | Component troubleshooting docs |
| Understand architecture | project-overview.md | mcp-server/01-architecture.md |
| Make technical decision | technical-decisions.md | All component docs |
| Deploy changes | modification-guide.md | mcp-server/03-deployment.md |

### Document Sizes

| Document | Lines | Purpose |
|----------|-------|---------|
| README.md | 350+ | Navigation and overview |
| project-overview.md | 800+ | Complete project context |
| technical-decisions.md | 900+ | Decision rationale |
| modification-guide.md | 1000+ | Change procedures |
| troubleshooting-history.md | 700+ | Issue solutions |

**Total**: ~3,750+ lines of AI context documentation

## Related Documentation

- [Main Documentation Index](../README.md)
- [MCP Server Documentation](../mcp-server/)
- [Financial Analyst Mode Documentation](../financial-analyst-mode/)
- [Bob Configuration Documentation](../bob-configuration/)

## Summary

AI Context documentation provides:
- ✅ High-level project understanding
- ✅ Technical decision rationale
- ✅ Safe modification procedures
- ✅ Historical troubleshooting knowledge
- ✅ Integration with component docs

**Key Benefits**:
1. Faster onboarding for AI assistants
2. Consistent decision-making
3. Reduced repeated mistakes
4. Better code quality
5. Preserved institutional knowledge

**Maintenance**:
- Update after significant changes
- Document new patterns
- Record troubleshooting solutions
- Keep cross-references current