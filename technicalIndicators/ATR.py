# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: Treacher
"""

# %% 0. Notes

'''
Average true range (ATR) is a measure of market volatility

The true range indicator is taken as the max of the following: 
    1) Current high less the current low
    2) The absolute value of the current high less the previous close
    3) The absolute value of the current low less the previous close
The average true range (ATR) is then a moving average of the true ranges

Traders may buy the security when the MACD crosses above its signal line and
sell (short) the security when the MACD crosses below the signal line
'''

# %% 1. Function definition


def ATR(ohlcv, simpleMovingAverage=14, returnAllRanges=False):
    """
    ohlcv : Dataframe
        Contains the open, high, low, close and volume information for an asset
            Must contain columns called ['High', 'Low', 'Close']
    simpleMovingAverage : int
        Number of periods for fast exponential moving average of close price
            Typical value = 12 periods
    returnAllRanges : str
        If specified, enables you to return a dataframe with all the computed ranges

    Returns
    -------
    atr : Dataframe
        Average true range of the asset

    Package requirements
    -------
    pandas as pd
    """

    df = ohlcv.copy()

    df['H-L'] = abs(df['High'] - df['Low'])
    df['H-PC'] = abs(df['High'] - df['Close'].shift(1))
    df['L-PC'] = abs(df['Low'] - df['Close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)
    df['ATR'] = df['TR'].rolling(window=simpleMovingAverage).mean()

    if returnAllRanges is False:
        df = df.drop(['H-L', 'H-PC', 'L-PC', 'TR'], axis=1, inplace=True)
        return df
    else:
        return df
