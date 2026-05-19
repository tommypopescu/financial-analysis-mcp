"""
Configuration management for Financial Analysis MCP Server
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Server Configuration
    MCP_SERVER_PORT: int = int(os.getenv('MCP_SERVER_PORT', '3000'))
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    # Data Configuration
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / 'data'
    TICKER_CSV_PATH: Path = Path(os.getenv('TICKER_CSV_PATH', str(DATA_DIR / 'tickers.csv')))
    
    # Cache Configuration
    CACHE_ENABLED: bool = os.getenv('CACHE_ENABLED', 'true').lower() == 'true'
    CACHE_TTL: int = int(os.getenv('CACHE_TTL', '300'))  # 5 minutes default
    
    # Market Data Configuration
    DEFAULT_PERIOD: str = os.getenv('DEFAULT_PERIOD', '1y')
    DEFAULT_INTERVAL: str = os.getenv('DEFAULT_INTERVAL', '1d')
    
    # Technical Indicators Default Parameters
    RSI_WINDOW: int = int(os.getenv('RSI_WINDOW', '14'))
    MACD_FAST: int = int(os.getenv('MACD_FAST', '12'))
    MACD_SLOW: int = int(os.getenv('MACD_SLOW', '26'))
    MACD_SIGNAL: int = int(os.getenv('MACD_SIGNAL', '9'))
    ADX_PERIOD: int = int(os.getenv('ADX_PERIOD', '14'))
    
    # Analysis Configuration
    ANALYSIS_MONTHS: int = int(os.getenv('ANALYSIS_MONTHS', '6'))
    
    @classmethod
    def ensure_directories(cls):
        """Ensure required directories exist"""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_ticker_csv_path(cls) -> Path:
        """Get ticker CSV path, ensuring it exists"""
        cls.ensure_directories()
        if not cls.TICKER_CSV_PATH.exists():
            # Create empty CSV with header
            cls.TICKER_CSV_PATH.write_text('ticker\n')
        return cls.TICKER_CSV_PATH


# Initialize configuration
config = Config()
config.ensure_directories()

# Made with Bob
