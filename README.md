# Financial Analysis MCP Server

A Model Context Protocol (MCP) server that provides comprehensive financial analysis tools for automated investment analysis using technical indicators.

## 🎯 Features

- **Real-time Market Data**: Fetch stock data using yfinance
- **Technical Indicators**: RSI, MACD, ADX, Supertrend, Stochastic, Bollinger Bands, OBV, MFI
- **Investment Analysis**: Generate summaries, signals, and risk metrics
- **Ticker Management**: Manage watchlists via CSV
- **Docker Deployment**: Containerized for easy deployment
- **CI/CD Pipeline**: Automated testing and deployment via GitHub Actions

## 🏗️ Architecture

```
financial-analysis-mcp/
├── src/
│   ├── server.py              # Main MCP server
│   ├── tools/
│   │   ├── data_extraction.py # Market data fetching
│   │   ├── indicators.py      # Technical indicators
│   │   ├── analysis.py        # Investment analysis
│   │   └── ticker_mgmt.py     # Ticker management
│   ├── utils/
│   │   ├── calculations.py    # Core calculations
│   │   └── helpers.py         # Utility functions
│   └── config.py              # Configuration
├── data/
│   └── tickers.csv            # Ticker watchlist
├── tests/                     # Unit tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # CI/CD pipeline
├── Dockerfile                 # Container definition
├── docker-compose.yml         # Local testing
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Quick Start

### Local Development

```bash
# Clone repository
git clone <your-repo-url>
cd financial-analysis-mcp

# Install dependencies
pip install -r requirements.txt

# Run server
python src/server.py
```

### Docker Deployment

```bash
# Build image
docker build -t financial-analysis-mcp:latest .

# Run container
docker-compose up -d

# View logs
docker-compose logs -f
```

## 🔧 Configuration

Configure the server via environment variables or `.env` file:

```env
# Server Configuration
MCP_SERVER_PORT=3000
LOG_LEVEL=INFO

# Data Configuration
TICKER_CSV_PATH=/app/data/tickers.csv
CACHE_ENABLED=true
CACHE_TTL=300

# Market Data
DEFAULT_PERIOD=1y
DEFAULT_INTERVAL=1d
```

## 📊 Available Tools

### Data Extraction
- `fetch_ticker_data` - Get historical price/volume data
- `get_current_price` - Real-time price information
- `get_ticker_info` - Company fundamentals

### Technical Indicators
- `calculate_rsi` - Relative Strength Index
- `calculate_macd` - MACD with signal line
- `calculate_adx` - Average Directional Index
- `calculate_supertrend` - Supertrend indicator
- `calculate_stochastic` - Stochastic oscillator
- `calculate_bollinger_bands` - Bollinger Bands
- `calculate_obv` - On-Balance Volume
- `calculate_mfi` - Money Flow Index
- `calculate_all_indicators` - All indicators at once

### Analysis Tools
- `generate_investment_summary` - Comprehensive analysis
- `detect_signals` - Buy/sell/hold signals
- `calculate_risk_metrics` - Risk analysis
- `compare_tickers` - Multi-ticker comparison
- `screen_tickers` - Watchlist screening

### Ticker Management
- `list_tickers` - Get all tickers
- `add_ticker` - Add to watchlist
- `remove_ticker` - Remove from watchlist
- `validate_ticker` - Check ticker validity

## 🤖 Usage with Bob/Claude

Once deployed, you can interact with the MCP server through Bob:

```
"Analyze AAPL and tell me if it's a good buy"
"Screen my watchlist for stocks with RSI below 30"
"Compare MSFT, GOOGL, and AMZN momentum"
"Generate weekly investment report for all tickers"
```

## 🔄 CI/CD Pipeline

The project includes automated CI/CD via GitHub Actions:

1. **Build**: Builds Docker image on push
2. **Test**: Runs unit tests
3. **Push**: Pushes image to registry
4. **Deploy**: Deploys to OMV server (on main branch)

## 🖥️ OMV Server Deployment

### Prerequisites
- Docker installed on OMV server
- SSH access configured
- Docker registry access (optional)

### Deployment Steps

1. **Configure secrets** in GitHub repository:
   - `OMV_HOST`: Server hostname/IP
   - `OMV_USER`: SSH username
   - `OMV_SSH_KEY`: SSH private key
   - `DOCKER_REGISTRY_USER`: Docker registry username (optional)
   - `DOCKER_REGISTRY_TOKEN`: Docker registry token (optional)

2. **Push to main branch**:
   ```bash
   git push origin main
   ```

3. **Monitor deployment**:
   - Check GitHub Actions workflow
   - SSH to OMV server and verify: `docker ps`

### Manual Deployment

```bash
# On OMV server
cd /path/to/deployment
git pull origin main
docker-compose down
docker-compose up -d --build
```

## 📝 Development

### Adding New Tools

1. Create tool function in appropriate module
2. Register tool in `server.py`
3. Add tests in `tests/`
4. Update documentation

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_indicators.py
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: Cannot fetch market data
- Check internet connection
- Verify ticker symbol is valid
- Check yfinance API status

**Issue**: Container won't start
- Check logs: `docker-compose logs`
- Verify port 3000 is available
- Check environment variables

**Issue**: Bob can't connect to MCP server
- Verify server is running: `docker ps`
- Check Bob's MCP configuration
- Verify network connectivity

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Submit pull request

## 📧 Support

For issues and questions:
- Open GitHub issue
- Check documentation
- Review logs for errors