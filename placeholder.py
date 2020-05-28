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

# Next two lines intend to import functions from other folder
import os
import sys
os.chdir('C:\\Users\\Dan\\Documents\\GitHub\\algorithmicTrading')
sys.path.append('/algorithmicTrading/technicalIndicators/')
#from technicalIndicators import ATR

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

# Define dates of interest
startDate = '2018-01-01'
endDate = '2020-01-01'


# %% 3. Connect to api and pull data for the defined tickers

api = tradeapi.REST(apiKey, secretKey, endPoint, api_version='v2')
account = api.get_account()
# api.list_positions()

# Define the dictionary that will hold all the data for all the companies
data = {}
for ticker in tickers:
    try:
        # Pull the stock details for that ticker
        data[ticker] = api.get_aggs('AAPL', 1, 'day', startDate, endDate).df
        print('Pulling ohlcv data for {:s}'.format(ticker))
    except:
        # If nothing is found, throw error and continue
        print('Error encountered pulling ohlcv data for {:s}'.format(ticker))



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