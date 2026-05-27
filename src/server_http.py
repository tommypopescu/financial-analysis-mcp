"""
Financial Analysis MCP Server - HTTP Transport
HTTP-based server for better compatibility with Bob
"""
import asyncio
import logging
import pandas as pd
from typing import Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from .tools import (
    fetch_ticker_data, get_current_price, get_ticker_info,
    calculate_rsi, calculate_macd, calculate_all_indicators,
    generate_investment_summary, screen_tickers,
    list_tickers, add_ticker, remove_ticker
)

# ============================================================================
# PORTFOLIO MANAGEMENT ADDITION - START
# Added: 2026-05-19 for family portfolio tracking (2 portfolios)
# Can be safely removed by reverting to commit aa150c1 if issues occur
# ============================================================================
from .tools.portfolio import (
    list_portfolios, get_portfolio, add_holding, remove_holding,
    set_target_allocation, analyze_portfolio_allocation,
    get_portfolio_performance, get_investment_recommendation
)
# ============================================================================
# PORTFOLIO MANAGEMENT ADDITION - END
# ============================================================================
from .config import config

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Financial Analysis MCP Server",
    description="MCP Server for financial data analysis and technical indicators",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ToolRequest(BaseModel):
    """Request model for tool calls"""
    name: str
    arguments: dict[str, Any] = {}


class ToolResponse(BaseModel):
    """Response model for tool calls"""
    success: bool
    result: Any = None
    error: str | None = None


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Financial Analysis MCP Server",
        "version": "1.0.0",
        "status": "running",
        "transport": "http"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/tools")
async def list_tools():
    """List all available tools"""
    return {
        "tools": [
            {
                "name": "fetch_ticker_data",
                "description": "Fetch historical price and volume data for a stock ticker",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string", "description": "Stock ticker symbol"},
                        "period": {"type": "string", "description": "Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)"},
                        "interval": {"type": "string", "description": "Data interval (1m, 5m, 1h, 1d, 1wk, 1mo)"}
                    },
                    "required": ["ticker"]
                }
            },
            {
                "name": "get_current_price",
                "description": "Get current/latest price for a ticker",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string", "description": "Stock ticker symbol"}
                    },
                    "required": ["ticker"]
                }
            },
            {
                "name": "calculate_all_indicators",
                "description": "Calculate all technical indicators (RSI, MACD, ADX, etc.) for a ticker",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string", "description": "Stock ticker symbol"},
                        "period": {"type": "string", "description": "Data period"}
                    },
                    "required": ["ticker"]
                }
            },
            {
                "name": "generate_investment_summary",
                "description": "Generate comprehensive investment analysis with buy/sell/hold recommendation",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string", "description": "Stock ticker symbol"}
                    },
                    "required": ["ticker"]
                }
            },
            {
                "name": "list_tickers",
                "description": "List all tickers in watchlist",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "add_ticker",
                "description": "Add ticker to watchlist",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string", "description": "Ticker to add"}
                    },
                    "required": ["ticker"]
                }
            },
            {
                "name": "screen_tickers",
                "description": "Screen watchlist for investment opportunities",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "criteria": {"type": "object", "description": "Screening criteria (e.g., rsi_below: 30)"}
                    }
                }
            },
            # ============================================================================
            # PORTFOLIO TOOLS - START (Added 2026-05-19)
            # ============================================================================
            {
                "name": "list_portfolios",
                "description": "List all family portfolios with summary information",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_portfolio",
                "description": "Get detailed portfolio information including holdings and allocations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "portfolio_id": {"type": "string", "description": "Portfolio identifier (portfolio1 or portfolio2)"}
                    },
                    "required": ["portfolio_id"]
                }
            },
            {
                "name": "add_holding",
                "description": "Add or update a holding in portfolio",
                "inputSchema": {
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
            },
            {
                "name": "set_target_allocation",
                "description": "Set target allocation percentage for a ticker in portfolio",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "portfolio_id": {"type": "string", "description": "Portfolio identifier"},
                        "ticker": {"type": "string", "description": "Stock ticker symbol"},
                        "target_weight_pct": {"type": "number", "description": "Target weight percentage (0-100)"},
                        "notes": {"type": "string", "description": "Optional notes"}
                    },
                    "required": ["portfolio_id", "ticker", "target_weight_pct"]
                }
            },
            {
                "name": "analyze_portfolio_allocation",
                "description": "Analyze portfolio allocation vs targets and get rebalancing recommendations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "portfolio_id": {"type": "string", "description": "Portfolio identifier"}
                    },
                    "required": ["portfolio_id"]
                }
            },
            {
                "name": "get_portfolio_performance",
                "description": "Get portfolio performance history, returns, and optional benchmark comparison",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "portfolio_id": {"type": "string", "description": "Portfolio identifier (portfolio1 or portfolio2)"},
                        "period": {"type": "string", "description": "Historical period (1mo, 3mo, 6mo, 1y, 2y, 5y, max)"},
                        "benchmark_ticker": {"type": "string", "description": "Optional benchmark ticker for comparison"}
                    },
                    "required": ["portfolio_id"]
                }
            },
            {
                "name": "get_investment_recommendation",
                "description": "Get personalized investment recommendation considering portfolio context",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "portfolio_id": {"type": "string", "description": "Portfolio identifier"},
                        "ticker": {"type": "string", "description": "Stock ticker to analyze"},
                        "investment_amount": {"type": "number", "description": "Amount to potentially invest"}
                    },
                    "required": ["portfolio_id", "ticker", "investment_amount"]
                }
            }
            # ============================================================================
            # PORTFOLIO TOOLS - END
            # ============================================================================
        ]
    }


@app.post("/tools/call")
async def call_tool(request: ToolRequest) -> ToolResponse:
    """Handle tool calls"""
    try:
        logger.info(f"Tool called: {request.name} with args: {request.arguments}")
        
        if request.name == "fetch_ticker_data":
            result = fetch_ticker_data(**request.arguments)
        elif request.name == "get_current_price":
            result = get_current_price(**request.arguments)
        elif request.name == "calculate_all_indicators":
            ticker = request.arguments['ticker']
            data = fetch_ticker_data(ticker, request.arguments.get('period', '1y'))
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
        elif request.name == "generate_investment_summary":
            ticker = request.arguments['ticker']
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
        elif request.name == "list_tickers":
            result = list_tickers()
        elif request.name == "add_ticker":
            result = add_ticker(**request.arguments)
        elif request.name == "screen_tickers":
            tickers_data = list_tickers()
            if tickers_data['success']:
                result = screen_tickers(tickers_data['tickers'], request.arguments.get('criteria', {}))
            else:
                result = tickers_data
        # ============================================================================
        # PORTFOLIO HANDLERS - START (Added 2026-05-19)
        # ============================================================================
        elif request.name == "list_portfolios":
            result = list_portfolios()
        elif request.name == "get_portfolio":
            result = get_portfolio(**request.arguments)
        elif request.name == "add_holding":
            result = add_holding(**request.arguments)
        elif request.name == "set_target_allocation":
            result = set_target_allocation(**request.arguments)
        elif request.name == "analyze_portfolio_allocation":
            result = analyze_portfolio_allocation(**request.arguments)
        elif request.name == "get_portfolio_performance":
            result = get_portfolio_performance(**request.arguments)
        elif request.name == "get_investment_recommendation":
            result = get_investment_recommendation(**request.arguments)
        # ============================================================================
        # PORTFOLIO HANDLERS - END
        # ============================================================================
        else:
            raise HTTPException(status_code=400, detail=f"Unknown tool: {request.name}")
        
        return ToolResponse(success=True, result=result)
        
    except Exception as e:
        logger.error(f"Error in tool {request.name}: {str(e)}")
        return ToolResponse(success=False, error=str(e))


def main():
    """Main server entry point"""
    logger.info("Starting Financial Analysis MCP Server (HTTP)...")
    logger.info(f"Server will listen on 0.0.0.0:{config.HTTP_PORT}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=config.HTTP_PORT,
        log_level=config.LOG_LEVEL.lower()
    )


if __name__ == "__main__":
    main()

# Made with Bob