import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
import pandas as pd 
from data_analysis import technical_analysis
from data_analysis.technical_analysis import OVERBOUGHT_LEVEL, OVERSOLD_LEVEL
from utils import config
from utils.config import selected_ticker, selected_ticker_image_url

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
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05, 
                            row_heights=[0.5, 0.2, 0.3])

        # Add candlestick chart to top subplot
        fig.add_trace(
            go.Candlestick(
                x=crypto_data.index,
                open=crypto_data["Open"],
                high=crypto_data["High"],
                low=crypto_data["Low"],
                close=crypto_data["Close"],
                increasing=dict(line=dict(color=config.BULLISH_COLOR)),
                decreasing=dict(line=dict(color=config.BEARISH_COLOR)),
                name="Price",
            ),
            row=1,
            col=1
        )

        # Add technical analysis indicators to top or bottom subplot
        for key, value in technical_analysis_results.items():
            if key in ['SMA', 'SMA20', 'SMA50', 'EMA', 'EMA20', 'EMA50', 'Upper', 'Middle', 'Lower']:
                # Add to top subplot
                fig.add_trace(
                    go.Scatter(
                        x=crypto_data.index,
                        y=value,
                        name=key,
                        line=dict(width=1)
                    ),
                    row=1,
                    col=1
                )
            elif key in ['RSI', 'MACD', 'Signal', 'Hist']:
                # Add to bottom subplot
                fig.add_trace(
                    go.Scatter(
                        x=crypto_data.index,
                        y=value,
                        name=key,
                        line=dict(width=1)
                    ),
                    row=3,
                    col=1
                )

        # Add volume chart to middle subplot
        fig.add_trace(
            go.Bar(
                x=crypto_data.index,
                y=crypto_data["Volume"],
                marker=dict(
                    color=crypto_data["Close"].diff().fillna(0).apply(
                        lambda x: config.VOLUME_COLOR_MAPPING["static"] if x == 0 else (
                            config.VOLUME_COLOR_MAPPING["increase"] if x > 0 else config.VOLUME_COLOR_MAPPING["decrease"]
                        )
                    )
                ),
                name="Volume"
            ),
            row=2,
            col=1
        )

        # Add on-balance volume (OBV) indicator to volume chart
        obv = technical_analysis.on_balance_volume(crypto_data)
        fig.add_trace(
            go.Scatter(
                x=obv.index.tolist(),  # Convert to list of datetime values
                y=obv,
                name="OBV",
                line=dict(width=1)
            ),
            row=2,
            col=1
        )

        # Add volume-weighted average price (VWAP) indicator to volume chart
        vwap = technical_analysis.get_vwap(crypto_data)
        fig.add_trace(
            go.Scatter(
                x=crypto_data.index,
                y=vwap,
                name="VWAP",
                line=dict(width=1)
            ),
            row=2,
            col=1
        )

        # Add horizontal lines for overbought and oversold levels
        fig.add_shape(
            type="line",
            x0=start_date,
            y0=OVERBOUGHT_LEVEL,
            x1=end_date,
            y1=OVERBOUGHT_LEVEL,
            line=dict(color=config.OVERBOUGHT_COLOR, width=1, dash="dot"),
            row=3,
            col=1
        )
        fig.add_shape(
            type="line",
            x0=start_date,
            y0=OVERSOLD_LEVEL,
            x1=end_date,
            y1=OVERSOLD_LEVEL,
            line=dict(color=config.OVERSOLD_COLOR, width=1, dash="dot"),
            row=3,
            col=1
        )

        # Set axis properties
        fig.update_xaxes(
            rangeslider=dict(visible=False),
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1D", step="day", stepmode="backward"),
                    dict(count=7, label="1W", step="day", stepmode="backward"),
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(count=3, label="3Y", step="year", stepmode="backward"),
                    dict(step="all")
                ]),
                font=dict(color=config.AXIS_FONT_COLOR),
                bgcolor=config.AXIS_BG_COLOR,
                borderwidth=0,
                x=0.02,
                y=1.05,
                xanchor="left",
                yanchor="top"
            ),
            tickfont=dict(color=config.AXIS_FONT_COLOR)
        )

        fig.update_yaxes(
            title="Price (USD)",
            tickformat=".8f"),
            title_font=dict(color=config.AXIS_FONT_COLOR),
            tickfont=dict(color=config.AXIS_FONT_COLOR),
            gridcolor=config.GRID_COLOR,
            zerolinecolor=config.ZEROLINE_COLOR,
            row=1,
            col=1
        )

        fig.update_yaxes(
            title="Volume",
            title_font=dict(color=config.AXIS_FONT_COLOR),
            tickfont=dict(color=config.AXIS_FONT_COLOR),
            gridcolor=config.GRID_COLOR,
            zerolinecolor=config.ZEROLINE_COLOR,
            row=2,
            col=1
        )

        fig.update_yaxes(
            title="Indicator",
            title_font=dict(color=config.AXIS_FONT_COLOR),
            tickfont=dict(color=config.AXIS_FONT_COLOR),
            gridcolor=config.GRID_COLOR,
            zerolinecolor=config.ZEROLINE_COLOR,
            row=3,
            col=1
        )

        # Set figure layout properties
        fig.update_layout(
            title=dict(
                text=f"{selected_ticker} Historical Price Chart",
                font=dict(color=config.TITLE_FONT_COLOR)
            ),
            title_x=0.5,
            title_y=0.95,
            plot_bgcolor=config.PLOT_BG_COLOR,
            paper_bgcolor=config.PAPER_BG_COLOR,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            
            xaxis=dict(
                rangeslider=dict(
                    visible=False,
                    range=[start_date, end_date]
                ),
                type="date",
                gridcolor=config.GRID_COLOR,
                linecolor=config.LINE_COLOR,
                tickfont=dict(color=config.TICK_FONT_COLOR),
                showspikes=True,
                spikemode='across',
                spikesnap='cursor',
                spikethickness=1,
                spikecolor=config.SPIKE_COLOR,
                spikedash="solid",
                showline=True,
                showgrid=True,
            ),
            yaxis=dict(
                title="Price (USD)", tickformat=".8f",
                titlefont=dict(color=config.AXIS_TITLE_COLOR),
                tickfont=dict(color=config.TICK_FONT_COLOR),
                gridcolor=config.GRID_COLOR,
                linecolor=config.LINE_COLOR,
                showline=True,
                showgrid=True,
            ),
            yaxis2=dict(
                title="Volume",
                titlefont=dict(color=config.AXIS_TITLE_COLOR),
                tickfont=dict(color=config.TICK_FONT_COLOR),
                gridcolor=config.GRID_COLOR,
                linecolor=config.LINE_COLOR,
                showline=True,
                showgrid=True,
                side="right"
            ),
            yaxis3=dict(
                title="",
                titlefont=dict(color=config.AXIS_TITLE_COLOR),
                tickfont=dict(color=config.TICK_FONT_COLOR),
                gridcolor=config.GRID_COLOR,
                linecolor=config.LINE_COLOR,
                showline=True,
                showgrid=True,
                range=[0, 100],
                side="right",
                overlaying="y2"
            )
        )
        # Add annotations for overbought/oversold levels
        fig.add_annotation(
            xref="paper", yref="y3",
            x=0.97, y=OVERBOUGHT_LEVEL,
            text=f"Overbought ({OVERBOUGHT_LEVEL:.1f})",
            showarrow=False,
            font=dict(color=config.OVERBOUGHT_COLOR)
        )
        fig.add_annotation(
            xref="paper", yref="y3",
            x=0.97, y=OVERSOLD_LEVEL,
            text=f"Oversold ({OVERSOLD_LEVEL:.1f})",
            showarrow=False,
            font=dict(color=config.OVERSOLD_COLOR)
        )

        # Add company logo to the bottom of the chart
        if selected_ticker_image_url is not None:
            if os.path.exists(selected_ticker_image_url):
                image = Image.open(selected_ticker_image)
                image_width = image.size[0]
                image_height = image.size[1]
                scale_factor = 0.15
                resized_width = int(image_width * scale_factor)
                resized_height = int(image_height * scale_factor)
                image = image.resize((resized_width, resized_height), resample=Image.BOX)
                fig.add_layout_image(
                    dict(
                        source=selected_ticker_image_url,
                        xref="paper",
                        yref="paper",
                        x=0.02,
                        y=0.02,
                        sizex=resized_width,
                        sizey=resized_height,
                        xanchor="left",
                        yanchor="bottom"
                    )
                )

        # Show plot
        fig.show()
