# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: Treacher

Contains: MACD, ATR, Slope
"""

# %% 0. Import libraries required by functions

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


# %% 1. Average True Range (ATR)

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
    df.columns = map(str.lower, df.columns)  # Force columns names lowercase

    df['H-L'] = abs(df['high'] - df['low'])
    df['H-PC'] = abs(df['high'] - df['close'].shift(1))
    df['L-PC'] = abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)
    df['ATR'] = df['TR'].rolling(window=simpleMovingAverage).mean()

    if returnAllRanges is False:
        df = df.drop(['H-L', 'H-PC', 'L-PC', 'TR'], axis=1, inplace=True)
        return df
    else:
        return df

# %% 2. Moving Average Convergence Divergence (MACD)


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


def MACD(ohlcv, fastEMA=12, slowEMA=26, signalEMA=9, returnEMAs=False):
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
    df.columns = map(str.lower, df.columns)  # Force columns names lowercase

    # Need to pick out the correct column - there might not be an 'Adj Close'
    alternatives = ['adj close', 'close']
    close = [s for s in df.columns.tolist() if any(xs in s for xs in alternatives)]

    # Take the first matching string as this will be adjusted close if available
    df['fastMA'] = df[close[0]].ewm(span=fastEMA, min_periods=fastEMA).mean()
    df['slowMA'] = df[close[0]].ewm(span=slowEMA, min_periods=slowEMA).mean()
    df['macd'] = df['fastMA'] - df['slowMA']
    df['signal'] = df['macd'].ewm(span=signalEMA, min_periods=signalEMA).mean()

    if returnEMAs is False:
        df.drop(['fastMA', 'slowMA'], axis=1, inplace=True)
        return df
    else:
        return df

# %% 3. Slope of data


'''
Function to calculate the slope of a series of n datapoints

Basic idea:
    Give the function n datapoints of e.g. price, MACD or whatever
    Use SciKit Learn linear regression to work out a straight line fit
    Use trigonometry to calculate what the angle is from the straight line
'''


def vectorSlope(dataPoints, n=40):
    """
    Parameters
    ----------
    dataPoints : DataFrame
        These are the (1D) datapoints you're trying to extract a slope from
    n : int
        The number of points to include in the calculation
            The lower the n value, the more unstable the angle.
            Higher n values smooth the slope calculation

    Returns
    -------
    intercept : float
        y - axis value of the intercept at x = 0
    angle : float
        Slope of the line incoporating n points

    Package requirements
    -------
    pandas as pd\n
    numpy as np\n
    from sklearn.linear_model import LinearRegression
    """

    #if 'LinearRegression' not in dir():
    #    from sklearn.linear_model import LinearRegression

    lr = LinearRegression()  # Instantiate a linear regression object
    angles = []  # Each time you add a datapoint, you'll need new slope

    # Loop over the data
    for i in range(n, len(dataPoints)-1):
        # x and y data
        x = np.arange(n)
        y = dataPoints[i-n:i]

        # Scale the axes so they're not all squished up at x=0
        y_scaled = (y - y.min())/(y.max() - y.min())
        x_scaled = (x - x.min())/(x.max() - x.min())

        lr.fit(x_scaled[:, None], y_scaled[:, None])
        angles.append(lr.coef_[0][0])
        
    slope_angle = (np.rad2deg(np.arctan(np.array(angles))))

    return slope_angle

# %% 3. Rolling slope of data


'''
Function to calculate the scalar slope of a rolling window of n datapoints

Basic idea:
    Give the function a window of n datapoints of e.g. price, MACD or whatever
    Use SciKit Learn linear regression to work out a straight line fit
    Use trigonometry to calculate what the angle is from the straight line
'''


def scalarSlope(dataPoints):
    """
    Parameters
    ----------
    dataPoints : DataFrame
        These are the (1D) datapoints you're trying to extract a slope from

    Returns
    -------
    angle : float
        Slope of the line incoporating n points

    Package requirements
    -------
    pandas as pd\n
    numpy as np\n
    from sklearn.linear_model import LinearRegression
    """

    lr = LinearRegression()  # Instantiate a linear regression object

    # x and y data
    x = np.arange(len(dataPoints))
    y = dataPoints

    # Scale the axes so they're not all squished up at x=0
    y_scaled = (y - y.min())/(y.max() - y.min())
    x_scaled = (x - x.min())/(x.max() - x.min())

    lr.fit(x_scaled[:, None], y_scaled[:, None])
    angle = np.rad2deg(np.arctan(np.array(lr.coef_[0][0])))
    
    return angle
        
