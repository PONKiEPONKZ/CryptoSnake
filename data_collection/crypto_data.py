import yfinance as yf
import logging
from utils import config
from utils.config import selected_ticker


def get_crypto_data():
    # Retrieve historical data from Yahoo Finance
    print()
    print("Retrieving historical data for " + config.selected_ticker + "...")
    logging.debug("Retrieving historical data for %s", config.selected_ticker)
    ticker_data = yf.Ticker(config.selected_ticker)
    logging.debug("Retrieved data for %s", config.selected_ticker)

    # Get historical market data
    historical_data = ticker_data.history(period="max")
    logging.debug("Retrieved historical data for %s", config.selected_ticker)

    # Filter for necessary columns
    historical_data = historical_data[["Open", "High", "Low", "Close", "Volume"]]

    # Drop NaN values
    historical_data = historical_data.dropna()

    logging.debug("Filtered data for %s", config.selected_ticker)

    return historical_data
