import pandas as pd
import plotly.graph_objs as go
import sys
import talib

OVERBOUGHT_LEVEL = 70
OVERSOLD_LEVEL = 30

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

def on_balance_volume(df):
    obv = talib.OBV(df['Close'], df['Volume'])
    return obv

def get_vma(df, period):
    volume = df['Volume']
    close = df['Close']
    cum_volume = volume.cumsum()
    cum_volume_price = (volume * (close + df['Open'] + df['Low'] + df['High']) / 4).cumsum()
    return cum_volume_price / cum_volume

def get_vwap(df):
    volume = df['Volume']
    close = df['Close']
    tp = (df['High'] + df['Low'] + df['Close']) / 3
    cum_volume = volume.cumsum()
    cum_volume_price = (volume * tp).cumsum()
    return cum_volume_price / cum_volume

def perform_technical_analysis(df):
    if len(df) < 5:
        print('Error: not enough data to perform technical analysis')
        return None

    print("Performing technical anaylsis...")

    sma = get_sma(df, 10)
    sma20 = get_sma(df, 20)
    sma50 = get_sma(df, 50)
    ema = get_ema(df, 10)
    ema20 = get_ema(df, 20)
    ema50 = get_ema(df, 50)
    rsi = get_rsi(df, 14)
    vma = get_vma(df, 10)
    vwap = get_vwap(df)
    macd, signal, hist = get_macd(df)
    upper, middle, lower = get_bollinger_bands(df)
    
    print(df.index)
    
    obv = on_balance_volume(df)
    
    if any(x is None for x in [sma, ema, rsi, macd, signal, hist, upper, middle, lower, obv]):
        print('Error: technical analysis calculation failed')
        return None
    
    technical_analysis_results = {
        'SMA': sma,
        'SMA20': sma20,
        'SMA50': sma50,
        'EMA': ema,
        'EMA20': ema20,
        'EMA50': ema50,
        'RSI': rsi,
        'MACD': macd,
        'Signal': signal,
        'Hist': hist,
        'Upper': upper,
        'Middle': middle,
        'Lower': lower,
        'OBV': obv,
        'VMA': vma
    }
    
    return technical_analysis_results
