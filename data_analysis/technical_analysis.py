import pandas as pd
import plotly.graph_objs as go
import sys
import talib

def get_sma(df, period):
    return talib.SMA(df['Close'], timeperiod=period)

def get_ema(df, period):
    return talib.EMA(df['Close'], timeperiod=period)

def get_rsi(df, period):
    return talib.RSI(df['Close'], timeperiod=period)

def get_macd(df, fast_period=12, slow_period=26, signal_period=9):
    macd, signal, hist = talib.MACD(df['Close'], fastperiod=fast_period, slowperiod=slow_period, signalperiod=signal_period)
    return macd, signal, hist

def get_bollinger_bands(df, period=20, devup=2, devdn=2):
    upper, middle, lower = talib.BBANDS(df['Close'], timeperiod=period, nbdevup=devup, nbdevdn=devdn)
    return upper, middle, lower

print("Performing technical anaylsis...")

def perform_technical_analysis(df):
    if len(df) < 5:
        print('Error: not enough data to perform technical analysis')
        return None
    
    sma = get_sma(df, 10)
    ema = get_ema(df, 10)
    rsi = get_rsi(df, 14)
    macd, signal, hist = get_macd(df)
    upper, middle, lower = get_bollinger_bands(df)
    
    if any(x is None for x in [sma, ema, rsi, macd, signal, hist, upper, middle, lower]):
        print('Error: technical analysis calculation failed')
        return None
    
    technical_analysis_results = {
        'SMA': sma,
        'EMA': ema,
        'RSI': rsi,
        'MACD': macd,
        'Signal': signal,
        'Hist': hist,
        'Upper': upper,
        'Middle': middle,
        'Lower': lower
    }
    
    return technical_analysis_results