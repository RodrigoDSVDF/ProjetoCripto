# calculations.py
import pandas as pd

def calculate_moving_averages(df, window=30):
    df['SMA'] = df['fechamento'].rolling(window=window).mean()
    return df

def calculate_rsi(df, periods=14):
    delta = df['fechamento'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    avg_gain = gain.rolling(window=periods, min_periods=periods).mean()
    avg_loss = loss.rolling(window=periods, min_periods=periods).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def calculate_macd(df, span1=12, span2=26, signal=9):
    df['MACD_line'] = df['fechamento'].ewm(span=span1, adjust=False).mean() - df['fechamento'].ewm(span=span2, adjust=False).mean()
    df['MACD_signal'] = df['MACD_line'].ewm(span=signal, adjust=False).mean()
    return df
