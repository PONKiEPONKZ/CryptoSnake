import yfinance as yf
from utils import config
from utils.logger import Logger
from utils.config import selected_ticker

logger = Logger()

def get_crypto_data():
    # Retrieve historical data from Yahoo Finance
    print()
    print("Retrieving historical data for " + config.selected_ticker + "...") 
    logger.log_info(f"Retrieving historical data for {config.selected_ticker}")

    ticker_data = yf.Ticker(config.selected_ticker)
    logger.log_info("Retrieved data for {config.selected_ticker}")

    # Get historical market data
    historical_data = ticker_data.history(period="max")
    logger.log_info("Retrieved historical data for {config.selected_ticker}")

    # Filter for necessary columns
    historical_data = historical_data[["Open", "High", "Low", "Close", "Volume"]]

    # Drop NaN values
    historical_data = historical_data.dropna()

    logger.log_info("Filtered data for {config.selected_ticker}")

    return historical_data
