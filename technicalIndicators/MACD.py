# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: Treacher
"""

# %% 0. Notes

'''
Moving Average Convergence Divergence (MACD) is a trend-following momentum
indicator that shows the relationship between two moving averages of a
security’s price

Basic idea:
    1) Compute a fast exponential moving average (EMA) of asset's close price
    2) Compute a slow exponential moving average of asset's close price
    3) Define the MACD line as the fast EMA minus the slow EMA
    4) Define the signal line as the (fastest) signal EMA of the MACD line

Traders may buy the security when the MACD crosses above its signal line and
sell (short) the security when the MACD crosses below the signal line
'''

# %% 1. Function definition


def MACD(ohlcv, fastEMA=12, slowEMA=26, signalEMA=9, returnEMAs=None):
    """
    Parameters
    ----------
    ohlcv : Dataframe
        Contains the open, high, low, close and volume information for an asset
            Must contain a column called 'Adj Close'
    fastEMA : int
        Number of periods for fast exponential moving average of close price
            Typical value = 12 periods
    slowEMA : int
        Number of periods for slow exponential moving average of close price
            Typical value = 26 periods
    signalEMA : int
        Number of periods for exponential moving average of the MACD line
            Typical value = 9 periods
    fullReturn : str
        If not nil then return the dataframe with the fast and slow EMAs

    Returns
    -------
    macd : Dataframe
        Contains the MACD line
    signal: Dataframe
        Contains the signal line
    
    Package requirements
    -------
    pandas as pd
    """

    # Don't want to make any actual changes to the original data
    df = ohlcv.copy()
    price = df['Adj Close']

    if returnEMAs is None:  # If nothing is specified...
        fastMA = price.ewm(span=fastEMA, min_periods=fastEMA).mean()
        slowMA = price.ewm(span=slowEMA, min_periods=slowEMA).mean()
        df['macd'] = fastMA - slowMA
        df['signal'] = df['macd'].ewm(span=signalEMA, min_periods=signalEMA).mean()
    else:  # If a 'fullReturn' is specified then give the EMAs back in the df
        df['fastMA'] = price.ewm(span=fastEMA, min_periods=fastEMA).mean()
        df['slowMA'] = price.ewm(span=slowEMA, min_periods=slowEMA).mean()
        df['macd'] = df['fastMA'] - df['slowMA']
        df['signal'] = df['macd'].ewm(span=signalEMA, min_periods=signalEMA).mean()

    return df
