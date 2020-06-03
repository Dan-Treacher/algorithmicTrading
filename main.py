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
startDate = '2019-01-01'
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

# %% 4. Loop through the data and append the technical indicator columns

tickers = list(data.keys())  # Any tickers that didn't load shouldn't survive
for ticker in tickers:
    data[ticker] = ti.MACD(data[ticker])
    data[ticker]['macd slope'] = data[ticker]['macd'].rolling(window=40).apply(ti.scalarSlope)
    data[ticker] = ti.Stochastic(data[ticker])
    print('Adding technical indicators for {:s}'.format(ticker))


# %% 6. Plot some of the indicators to check it's working

df = ti.Stochastic(data['MSFT'], n=28)  # Placeholder for one of the ticker dataframes

fig, ax = plt.subplots()
ax.plot(df['close'], color='blue', label='close')
ax2 = ax.twinx()
ax2.plot(df['stochastic'], color='red', label='stochastic')
fig.legend(loc='upper left', bbox_to_anchor=(0,1), bbox_transform=ax.transAxes)
plt.show()


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