import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class TrendLines:
    def __init__(self):
        pass

    def plot_trend_lines(self, crypto_data, candlestick_data):
        # extract closing prices from the crypto data
        close_prices = crypto_data["Close"]
        # create x and y arrays for linear regression
        x = np.array(range(len(close_prices)))
        y = np.array(close_prices)

        # fit a linear regression line to the data
        coefficients = np.polyfit(x, y, 1)
        polynomial = np.poly1d(coefficients)
        trendline = polynomial(x)

        # plot the data and trend line
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=candlestick_data.index,
                                     open=candlestick_data['Open'],
                                     high=candlestick_data['High'],
                                     low=candlestick_data['Low'],
                                     close=candlestick_data['Close'], name="Candlestick"))
        fig.add_trace(go.Scatter(x=crypto_data.index, y=trendline,
                                 mode='lines', name='Trend line'))
        fig.update_layout(title="Trend lines")
        return fig
