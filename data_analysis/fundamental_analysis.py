import yfinance as yf

class FundamentalAnalysis:
    def __init__(self):
        pass

    def get_market_cap(self, symbol):
        # function to get market capitalization of a given symbol
        # Example implementation using yfinance library
        stock = yf.Ticker(symbol)
        info = stock.info
        return info.get('marketCap', None)

    def get_earnings_per_share(self, symbol):
        # function to get earnings per share of a given symbol
        # Example implementation using yfinance library
        import yfinance as yf
        stock = yf.Ticker(symbol)
        info = stock.info
        return info.get('trailingEps', None)

    def get_price_to_earnings_ratio(self, symbol):
        # function to get price-to-earnings ratio of a given symbol
        # Example implementation using yfinance library
        import yfinance as yf
        stock = yf.Ticker(symbol)
        info = stock.info
        return info.get('trailingPE', None)
