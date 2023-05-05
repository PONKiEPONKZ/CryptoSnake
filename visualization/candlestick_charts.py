import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data_analysis import technical_analysis
from data_analysis.technical_analysis import OVERBOUGHT_LEVEL, OVERSOLD_LEVEL

from utils import config

selected_ticker = config.selected_ticker


class CandlestickCharts:
    def __init__(self):
        pass

    def plot_candlestick_chart(self, crypto_data, technical_analysis_results):
        if technical_analysis_results is None:
            print("Error: technical analysis not available")
            return

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
                name="Price",
                increasing_line_color='green',
                decreasing_line_color='red',
            ),
            row=1,
            col=1,
        )

        # Add moving averages to top subplot
        fig.add_trace(
            go.Scatter(x=crypto_data.index, y=technical_analysis_results["SMA"], name="SMA", 
                       line=dict(color='blue')),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(x=crypto_data.index, y=technical_analysis_results["EMA"], name="EMA",
                       line=dict(color='orange')),
            row=1,
            col=1,
        )

        # Add Bollinger Bands chart to top subplot
        fig.add_trace(
            go.Scatter(
                x=crypto_data.index,
                y=technical_analysis_results["Upper"],
                name="Upper Bollinger Band",
                line={"color": "red"},
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=crypto_data.index,
                y=technical_analysis_results["Middle"],
                name="Middle Bollinger Band",
                line={"color": "blue"},
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=crypto_data.index,
                y=technical_analysis_results["Lower"],
                name="Lower Bollinger Band",
                line={"color": "green"},
            ),
            row=1,
            col=1,
        )

        # Add MACD chart to bottom subplot        
        fig.add_trace(
            go.Scatter(
                x=crypto_data.index,
                y=technical_analysis_results["MACD"],
                name="MACD",
                line={"color": "blue"},
            ),
            row=2,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=crypto_data.index,
                y=technical_analysis_results["Signal"],
                name="Signal",
                line={"color": "red"},
            ),
            row=2,
            col=1,
        )
        fig.add_trace(
            go.Bar(
                x=crypto_data.index,
                y=technical_analysis_results["Hist"],
                name="MACD Histogram",
                marker={"color": "grey"},
            ),
            row=2,
            col=1,
        )

        # Add RSI chart to bottom subplot
        fig.add_trace(
            go.Scatter(
                x=crypto_data.index,
                y=technical_analysis_results["RSI"],
                name="RSI",
                line={"color": "purple"},
            ),
            row=2,
            col=1,
        )
        
        #Add horizontal line for overbought and oversold levels on RSI chart
        fig.add_shape(
            type="line",
            x0=crypto_data.index[0],
            x1=crypto_data.index[-1],
            y0=technical_analysis.OVERBOUGHT_LEVEL,
            y1=technical_analysis.OVERBOUGHT_LEVEL,
            line=dict(color="red", width=1, dash="dashdot"),
            row=2,
            col=1,
        )
        fig.add_shape(
            type="line",
            x0=crypto_data.index[0],
            x1=crypto_data.index[-1],
            y0=technical_analysis.OVERSOLD_LEVEL,
            y1=technical_analysis.OVERSOLD_LEVEL,
            line=dict(color="green", width=1, dash="dashdot"),
            row=2,
            col=1,
        )

        # Update layout settings
        fig.update_layout(
            title=f"{selected_ticker} Stock Analysis",
            template="plotly_dark",
            xaxis_rangeslider_visible=False,
            xaxis=dict(type="category"),
            height=800,
            hovermode="x unified",
        )

        # Display chart
        fig.show()
        
        return fig
       
