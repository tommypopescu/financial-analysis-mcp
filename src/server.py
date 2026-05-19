"""
Financial Analysis MCP Server
Main server implementation using Model Context Protocol
"""
import asyncio
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .tools import (
    fetch_ticker_data, get_current_price, get_ticker_info,
    calculate_rsi, calculate_macd, calculate_all_indicators,
    generate_investment_summary, screen_tickers,
    list_tickers, add_ticker, remove_ticker
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
                result = calculate_all_indicators(data['dataframe'])
            else:
                result = data
        elif name == "generate_investment_summary":
            ticker = arguments['ticker']
            data = fetch_ticker_data(ticker, '1y')
            if data['success']:
                result = generate_investment_summary(data['dataframe'], ticker)
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
