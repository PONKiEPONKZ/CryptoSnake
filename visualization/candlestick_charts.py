import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data_analysis import technical_analysis
from data_analysis.technical_analysis import OVERBOUGHT_LEVEL, OVERSOLD_LEVEL

from utils import config
from utils.config import selected_ticker


class CandlestickCharts:
    def __init__(self):
        pass
    
    def plot_candlestick_chart(self, crypto_data, technical_analysis_results):
        if technical_analysis_results is None:
            print("Error: technical analysis not available")
            return

        # Define start and end dates for range slider
        start_date = crypto_data.index[0]
        end_date = crypto_data.index[-1]

        # Create subplots with shared x-axis
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, 
                            row_heights=[0.7, 0.3])

        # Add candlestick chart to top subplot
        fig.add_trace(
            go.Candlestick(
                x=crypto_data.index,
                open=crypto_data["Open"],
                high=crypto_data["High"],
                low=crypto_data["Low"],
                close=crypto_data["Close"],
                name=config.selected_ticker.upper()
            ),
            row=1,
            col=1
        )

        # Add technical analysis indicators to top subplot
        fig.add_trace(
            go.Scatter(
                x=crypto_data.index,
                y=technical_analysis_results["EMA20"],
                name="EMA20",
                line=dict(width=1)
            ),
            row=1,
            col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=crypto_data.index,
                y=technical_analysis_results["EMA50"],
                name="EMA50",
                line=dict(width=1)
            ),
            row=1,
            col=1
                )
        fig.add_trace(
            go.Scatter(
                x=crypto_data.index,
                y=technical_analysis_results["Upper"],
                name="Upper Band",
                line=dict(width=1)
            ),
            row=1,
            col=1
        )

        fig.add_trace(
            go.Scatter(
                x=crypto_data.index,
                y=technical_analysis_results["Middle"],
                name="Middle Band",
                line=dict(width=1)
            ),
            row=1,
            col=1
        )

        fig.add_trace(
            go.Scatter(
                x=crypto_data.index,
                y=technical_analysis_results["Lower"],
                name="Lower Band",
                line=dict(width=1)
            ),
            row=1,
            col=1
        )
        
        # Add MACD histogram to bottom subplot
        fig.add_trace(
            go.Bar(
                x=crypto_data.index,
                y=technical_analysis_results["MACD"],
                name="MACD Histogram"
            ),
            row=1,
            col=1
        )
        
        # Add volume chart to bottom subplot
        fig.add_trace(
            go.Bar(
                x=crypto_data.index,
                y=crypto_data["Volume"],
                name="Volume"
            ),
            row=2,
            col=1
        )
               
        fig.add_trace(
            go.Scatter(
                x=crypto_data.index,
                y=[OVERBOUGHT_LEVEL] * len(crypto_data),
                name="Overbought",
                line=dict(color="red", width=1, dash="dash")
            ),
            row=2,
            col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=crypto_data.index,
                y=[OVERSOLD_LEVEL] * len(crypto_data),
                name="Oversold",
                line=dict(color="green", width=1, dash="dash")
            ),
            row=2,
            col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=crypto_data.index,
                y=technical_analysis_results["RSI"],
                name="RSI",
                line=dict(width=1)
            ),
            row=2,
            col=1
        )
        
        fig.update_yaxes(range=[0, 100], row=2, col=1)
        
        # Add range slider to bottom subplot
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1D", step="day", stepmode="backward"),
                        dict(count=7, label="1W", step="day", stepmode="backward"),
                        dict(count=1, label="1M", step="month", stepmode="backward"),
                        dict   (count=6, label="6M", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1Y", step="year", stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                color = "grey",
                rangeslider=dict(
                    visible=False
                ),
                type="date"
            )
        )
        # Update layout
        fig.update_layout(
            title=f"{config.selected_ticker.upper()} Candlestick Chart",
            template="plotly_dark",
            xaxis_rangeslider_visible=False,
            hovermode="x unified",
            height=config.PLOT_HEIGHT,
            yaxis=dict(title="Price", tickformat=".8f"), # format y-axis as currency
            yaxis2=dict(title="Volume"),
        )

        # Show plot
        fig.show()