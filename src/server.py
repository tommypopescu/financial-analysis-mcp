"""
Financial Analysis MCP Server
Main server implementation using Model Context Protocol
"""
import asyncio
import logging
import pandas as pd
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .tools import (
    fetch_ticker_data, get_current_price, get_ticker_info,
    calculate_rsi, calculate_macd, calculate_all_indicators,
    generate_investment_summary, screen_tickers,
    list_tickers, add_ticker, remove_ticker,
    list_portfolios, get_portfolio, add_holding, remove_holding,
    set_target_allocation, analyze_portfolio_allocation,
    get_portfolio_performance, get_investment_recommendation
)
from .config import config

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create MCP server
app = Server("financial-analysis-mcp")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools"""
    return [
        Tool(
            name="fetch_ticker_data",
            description="Fetch historical price and volume data for a stock ticker",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"},
                    "period": {"type": "string", "description": "Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)"},
                    "interval": {"type": "string", "description": "Data interval (1m, 5m, 1h, 1d, 1wk, 1mo)"}
                },
                "required": ["ticker"]
            }
        ),
        Tool(
            name="get_current_price",
            description="Get current/latest price for a ticker",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"}
                },
                "required": ["ticker"]
            }
        ),
        Tool(
            name="calculate_all_indicators",
            description="Calculate all technical indicators (RSI, MACD, ADX, etc.) for a ticker",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"},
                    "period": {"type": "string", "description": "Data period"}
                },
                "required": ["ticker"]
            }
        ),
        Tool(
            name="generate_investment_summary",
            description="Generate comprehensive investment analysis with buy/sell/hold recommendation",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"}
                },
                "required": ["ticker"]
            }
        ),
        Tool(
            name="list_tickers",
            description="List all tickers in watchlist",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="add_ticker",
            description="Add ticker to watchlist",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Ticker to add"}
                },
                "required": ["ticker"]
            }
        ),
        Tool(
            name="screen_tickers",
            description="Screen watchlist for investment opportunities",
            inputSchema={
                "type": "object",
                "properties": {
                    "criteria": {"type": "object", "description": "Screening criteria (e.g., rsi_below: 30)"}
                }
            }
        ),
        Tool(
            name="list_portfolios",
            description="List all family portfolios with summary information",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="get_portfolio",
            description="Get detailed portfolio information including holdings and allocations",
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id": {"type": "string", "description": "Portfolio identifier (portfolio1 or portfolio2)"}
                },
                "required": ["portfolio_id"]
            }
        ),
        Tool(
            name="add_holding",
            description="Add or update a holding in portfolio",
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id": {"type": "string", "description": "Portfolio identifier"},
                    "ticker": {"type": "string", "description": "Stock ticker symbol"},
                    "shares": {"type": "number", "description": "Number of shares"},
                    "avg_price": {"type": "number", "description": "Average purchase price per share"},
                    "purchase_date": {"type": "string", "description": "Purchase date (YYYY-MM-DD, optional)"},
                    "notes": {"type": "string", "description": "Optional notes"}
                },
                "required": ["portfolio_id", "ticker", "shares", "avg_price"]
            }
        ),
        Tool(
            name="set_target_allocation",
            description="Set target allocation percentage for a ticker in portfolio",
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id": {"type": "string", "description": "Portfolio identifier"},
                    "ticker": {"type": "string", "description": "Stock ticker symbol"},
                    "target_weight_pct": {"type": "number", "description": "Target weight percentage (0-100)"},
                    "notes": {"type": "string", "description": "Optional notes"}
                },
                "required": ["portfolio_id", "ticker", "target_weight_pct"]
            }
        ),
        Tool(
            name="analyze_portfolio_allocation",
            description="Analyze portfolio allocation vs targets and get rebalancing recommendations",
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id": {"type": "string", "description": "Portfolio identifier"}
                },
                "required": ["portfolio_id"]
            }
        ),
        Tool(
            name="get_portfolio_performance",
            description="Get portfolio performance history, returns, and optional benchmark comparison",
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id": {"type": "string", "description": "Portfolio identifier (portfolio1 or portfolio2)"},
                    "period": {"type": "string", "description": "Historical period (1mo, 3mo, 6mo, 1y, 2y, 5y, max)"},
                    "benchmark_ticker": {"type": "string", "description": "Optional benchmark ticker for comparison"}
                },
                "required": ["portfolio_id"]
            }
        ),
        Tool(
            name="get_investment_recommendation",
            description="Get personalized investment recommendation considering portfolio context",
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id": {"type": "string", "description": "Portfolio identifier"},
                    "ticker": {"type": "string", "description": "Stock ticker to analyze"},
                    "investment_amount": {"type": "number", "description": "Amount to potentially invest"}
                },
                "required": ["portfolio_id", "ticker", "investment_amount"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""
    try:
        logger.info(f"Tool called: {name} with args: {arguments}")
        
        if name == "fetch_ticker_data":
            result = fetch_ticker_data(**arguments)
        elif name == "get_current_price":
            result = get_current_price(**arguments)
        elif name == "calculate_all_indicators":
            ticker = arguments['ticker']
            data = fetch_ticker_data(ticker, arguments.get('period', '1y'))
            if data['success']:
                # Reconstruct DataFrame from data dict
                df = pd.DataFrame({
                    'Open': data['data']['open'],
                    'High': data['data']['high'],
                    'Low': data['data']['low'],
                    'Close': data['data']['close'],
                    'Volume': data['data']['volume']
                }, index=pd.to_datetime(data['data']['dates']))
                result = calculate_all_indicators(df)
            else:
                result = data
        elif name == "generate_investment_summary":
            ticker = arguments['ticker']
            data = fetch_ticker_data(ticker, '1y')
            if data['success']:
                # Reconstruct DataFrame from data dict
                df = pd.DataFrame({
                    'Open': data['data']['open'],
                    'High': data['data']['high'],
                    'Low': data['data']['low'],
                    'Close': data['data']['close'],
                    'Volume': data['data']['volume']
                }, index=pd.to_datetime(data['data']['dates']))
                result = generate_investment_summary(df, ticker)
            else:
                result = data
        elif name == "list_tickers":
            result = list_tickers()
        elif name == "add_ticker":
            result = add_ticker(**arguments)
        elif name == "screen_tickers":
            tickers_data = list_tickers()
            if tickers_data['success']:
                result = screen_tickers(tickers_data['tickers'], arguments.get('criteria', {}))
            else:
                result = tickers_data
        elif name == "list_portfolios":
            result = list_portfolios()
        elif name == "get_portfolio":
            result = get_portfolio(**arguments)
        elif name == "add_holding":
            result = add_holding(**arguments)
        elif name == "set_target_allocation":
            result = set_target_allocation(**arguments)
        elif name == "analyze_portfolio_allocation":
            result = analyze_portfolio_allocation(**arguments)
        elif name == "get_portfolio_performance":
            result = get_portfolio_performance(**arguments)
        elif name == "get_investment_recommendation":
            result = get_investment_recommendation(**arguments)
        else:
            result = {"success": False, "error": f"Unknown tool: {name}"}
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error in tool {name}: {str(e)}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Main server entry point"""
    logger.info("Starting Financial Analysis MCP Server...")
    logger.info("Server is ready and waiting for connections...")
    
    # Keep server running indefinitely
    try:
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())
    except Exception as e:
        logger.error(f"Server error: {e}")
        # Keep container alive even if stdio fails
        logger.info("Server will keep running for Docker health checks...")
        while True:
            await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
