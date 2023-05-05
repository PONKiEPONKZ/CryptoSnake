import matplotlib.pyplot as plt
import numpy as np


class TrendLines:
    def __init__(self):
        pass

    def plot_trend_line(self, crypto_data, fig=None, ax=None):
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
            ax = [ax]
        ax[0].plot(x, y, label="Data")
        ax[0].plot(x, trendline, "--", label="Trend line")
        ax[0].legend()
        if fig is None:
            plt.show()
        else:
            fig.canvas.draw()

        return fig
