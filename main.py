# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: Treacher
"""

# %%% 0. Notes

# Script using the Alpaca trading api papertrading (demo account) to do some
# algorithmic trading on stocks

# https://pypi.org/project/alpaca-trade-api/


# %% 1. Import libraries

import alpaca_trade_api as tradeapi
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = 15

# Move to correct directory for importing technical indicators
import sys
import os
os.chdir('C:\\Users\\Dan\\Documents\\GitHub\\algorithmicTrading')

# Import technical indicators
import technicalIndicators as ti

# %% 2. Define constants

# Keys to make the connection to the endpoint
key_dir = 'C:\\Users\\Dan\\Documents\\Python Scripts\\apiKeys\\'
apiKey = open(key_dir + 'alpaca_apiKey.txt', 'r').read()
secretKey = open(key_dir + 'alpaca_secretKey.txt', 'r').read()
endPoint = 'https://paper-api.alpaca.markets'  # Specify this for demo account

# Define companies of interest
tickers = ['AXP', 'AAPL', 'BA', 'CAT', 'CVX', 'CSCO', 'DIS', 'DOW', 'XOM',
           'HD', 'IBM', 'INTC', 'JNJ', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT',
           'NKE', 'PFE', 'PG', 'TRV', 'UTX', 'UNH', 'VZ', 'V', 'WMT', 'WBA']

# Define dates between which we extract the stock data
startDate = '2020-01-01'
endDate = '2020-05-28'


# %% 3. Connect to api and pull data for the defined tickers

api = tradeapi.REST(apiKey, secretKey, endPoint, api_version='v2')
account = api.get_account()
# api.list_positions()

# Define the dictionary that will hold all the data for all the companies
data = {}
for ticker in tickers:
    try:
        # Pull the stock details for that ticker
        data[ticker] = api.get_aggs(ticker, 1, 'day', startDate, endDate).df
        print('Pulling ohlcv data for {:s}'.format(ticker))
    except:
        # If nothing is found, throw error and continue
        print('Error encountered pulling ohlcv data for {:s}'.format(ticker))


# %% 4. Plot the indicators that are the basis for the strategy

df = data['AAPL'].copy()
df['ADX'] = ti.ADX(df, n=14)  # Placeholder for one of the ticker dataframes
df[['signal', 'macd']] = ti.MACD(df, 12, 26, 9)

# Plot close price against ADX line
fig1, ax1 = plt.subplots()
ax1.plot(df['close'], linestyle='--', color='blue', label='close')
ax2 = ax1.twinx()
ax2.plot(df['ADX'], color='red', label='ADX')
ax1.set_xlabel('Date'), ax1.set_ylabel('Close price ($)'), ax2.set_ylabel('ADX')
fig1.legend(loc='upper left', bbox_to_anchor=(0,1), bbox_transform=ax.transAxes)
plt.show()

# Plot close price against macd and signal lines
fig2, ax3 = plt.subplots()
ax3.plot(df['close'], linestyle='--', color='blue', label='close')
ax4 = ax3.twinx()
ax4.plot(df['macd'], color='red', label='macd')
ax4.plot(df['signal'], color='black', label='signal')
ax3.set_xlabel('Date'), ax3.set_ylabel('Close price ($)'), ax4.set_ylabel('macd and signal')
fig2.legend(loc='upper left', bbox_to_anchor=(0,1), bbox_transform=ax.transAxes)
plt.show()

# First date when ADX > 25
#df.loc[df['ADX']>25].index[0]


# %% 5. Loop through the data and append the technical indicator columns

tickers = list(data.keys())  # Any tickers that didn't load shouldn't survive
for ticker in tickers:
    data[ticker][['signal', 'macd']] = ti.MACD(data[ticker], 12, 26, 9)
    data[ticker]['ADX'] = ti.ADX(data[ticker], 14)
    print('Adding technical indicators for {:s}'.format(ticker))


# %% 6. Define the trading strategy


def trade_signal(dfWithIndicators, l_s): # l_s is the long or short string (Need to know if you're already long or short for a certain position at the present time)
    "function to generate signal"
    signal = ""  # If there's no clear signal, return blank (no trade)
    df = copy.deepcopy(dfWithIndicators)

    # If you don't have an existing position for the current asset you're analysing    
    if l_s == "":  
        if df["bar_num"].tolist()[-1]>=nbars and df["macd"].tolist()[-1]>df["macd_sig"].tolist()[-1] and df["macd_slope"].tolist()[-1]>df["macd_sig_slope"].tolist()[-1]:
            signal = "Buy"
        elif df["bar_num"].tolist()[-1]<=-nbars and df["macd"].tolist()[-1]<df["macd_sig"].tolist()[-1] and df["macd_slope"].tolist()[-1]<df["macd_sig_slope"].tolist()[-1]:
            signal = "Sell"
            
    elif l_s == "long":  # If we have an existing long position
        if df["bar_num"].tolist()[-1]<=-nbars and df["macd"].tolist()[-1]<df["macd_sig"].tolist()[-1] and df["macd_slope"].tolist()[-1]<df["macd_sig_slope"].tolist()[-1]:
            signal = "Close_Sell"  # If you want to close and then immediately go short because the indicators are implying sell
        elif df["macd"].tolist()[-1]<df["macd_sig"].tolist()[-1] and df["macd_slope"].tolist()[-1]<df["macd_sig_slope"].tolist()[-1]:
            signal = "Close"  # With no clear signal, just close the position
            
                # Same as long, but in reverse
    elif l_s == "short":
        if df["bar_num"].tolist()[-1]>=nbars and df["macd"].tolist()[-1]>df["macd_sig"].tolist()[-1] and df["macd_slope"].tolist()[-1]>df["macd_sig_slope"].tolist()[-1]:
            signal = "Close_Buy"
        elif df["macd"].tolist()[-1]>df["macd_sig"].tolist()[-1] and df["macd_slope"].tolist()[-1]>df["macd_sig_slope"].tolist()[-1]:
            signal = "Close"
    return signal


# %% X.

'''
This is how to place an order using the api command

api.submit_order(
    symbol='SPY',
    side='buy',
    type='market',
    qty='100',
    time_in_force='day',
    order_class='bracket',
    take_profit=dict(
        limit_price='305.0',
    ),
    stop_loss=dict(
        stop_price='295.5',
        limit_price='295.5',
    )
)
'''