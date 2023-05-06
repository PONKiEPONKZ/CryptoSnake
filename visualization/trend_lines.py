import plotly.graph_objects as go
from plotly.subplots import make_subplots

class TrendLines:
    def __init__(self):
        pass

    def plot_trend_lines(self, crypto_data, candlestick_data, fig=None, ax=None):
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
        if ax is None:
            fig, ax = plt.subplots()
        ax.plot(candlestick_data.index, candlestick_data["Close"], label="Data")
        ax.plot(crypto_data.index, trendline, "--", label="Trend line")
        ax.legend()

        return fig, ax
