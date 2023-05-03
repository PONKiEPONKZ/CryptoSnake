import plotly.graph_objects as go
from data_analysis import technical_analysis
from utils import config

selected_ticker = config.selected_ticker

class CandlestickCharts:
    def __init__(self):
        pass
    
    def plot_candlestick_chart(self, df, technical_analysis_results):
        if technical_analysis_results is None:
            print('Error: technical analysis not available')
            return

        fig = go.Figure()
        
        # Add candlestick chart
        fig.add_trace(go.Candlestick(x=df.index,
                                     open=df['Open'],
                                     high=df['High'],
                                     low=df['Low'],
                                     close=df['Close'],
                                     name='Price'))
    
        # Add moving averages
        fig.add_trace(go.Scatter(x=df.index, y=technical_analysis_results['SMA'], name='SMA'))
        fig.add_trace(go.Scatter(x=df.index, y=technical_analysis_results['EMA'], name='EMA'))

        # Add Bollinger Bands chart
        fig.add_trace(go.Scatter(x=df.index, y=technical_analysis_results['Upper'], name='Upper Bollinger Band', line={'color': 'red'}))
        fig.add_trace(go.Scatter(x=df.index, y=technical_analysis_results['Middle'], name='Middle Bollinger Band', line={'color': 'blue'}))
        fig.add_trace(go.Scatter(x=df.index, y=technical_analysis_results['Lower'], name='Lower Bollinger Band', line={'color': 'green'}))

        # Add RSI chart
        fig.add_trace(go.Scatter(x=df.index, y=technical_analysis_results['RSI'], name='RSI', line={'color': 'purple'}))
        fig.add_shape(type='line', x0=df.index[0], y0=30, x1=df.index[len(df)-1], y1=30, line={'color': 'red', 'dash': 'dash'})
        fig.add_shape(type='line', x0=df.index[0], y0=70, x1=df.index[len(df)-1], y1=70, line={'color': 'red', 'dash': 'dash'})

        # Add MACD chart
        fig.add_trace(go.Scatter(x=df.index, y=technical_analysis_results['MACD'], name='MACD', line={'color': 'blue'}))
        fig.add_trace(go.Scatter(x=df.index, y=technical_analysis_results['Signal'], name='Signal', line={'color': 'red'}))
        fig.add_trace(go.Bar(x=df.index, y=technical_analysis_results['Hist'], name='MACD Histogram', marker={'color': 'grey'}))

        fig.update_layout(
            title='Technical Analysis for {}'.format(selected_ticker),
            xaxis_title='Date',
            yaxis_title='Price',
            yaxis=dict(
            range=[0, 100] # Set the range of the y-axis to zoom in on the price
            ),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            margin=dict(l=0, r=0, t=30, b=0),
            template=('plotly_dark')
            )
        fig.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=3, label="3y", step="year", stepmode="backward"),
                dict(count=5, label="5y", step="year", stepmode="backward"),
                dict(count=10, label="10y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

        fig.show()
