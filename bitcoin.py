

def CreateCsvFile():
    import pandas as pd
    import yfinance as yf
    import numpy as np
    import requests
    import matplotlib.pyplot as plt
    from datetime import datetime as dt
    from datetime import timedelta
    import os

    path = os.path.dirname(os.path.abspath(__file__))

    df = yf.download('btc-usd')
    df = df.drop(['Open', 'Adj Close', 'High', 'Low'], axis=1)
    df['Close'] = df.Close.round(decimals=2)
    df.index.name = 'timestamp'
    datefilter = df.index.min()
    df2 = pd.read_csv(f'{path}/bitcoin_history.csv')
    df2 = df2.drop(['open', 'high', 'low'], axis=1)
    df2['close'] = df2.close.round(decimals=2)
    df2.rename(columns = {'close' : 'Close'}, inplace=True)
    df2['time'] = pd.to_datetime(df2['time'], format='%Y/%m/%d')
    df2.set_index(['time'],inplace=True)
    df2.index.name = 'timestamp'
    df2 = df2.loc[(df2.index >= df2.index.min()) & (df2.index < datefilter)]
    df = pd.concat([df2, df], axis=0)

    for n in [20, 50, 100, 200, 350, 700, 1400]:
        df[f'{n} MA'] = df.Close.rolling(n).mean().round(decimals=2)
    df['200 Weeks Index'] = df['Close'] / df['1400 MA']
    df.rename(columns = {'1400 MA':'200 Weeks MA'}, inplace = True)
    df['2 Years Buy MA'] = df.Close.rolling(730).mean().round(decimals=2)
    df['2 Years Sell MA'] =  (df['2 Years Buy MA'] * 5).round(decimals=2)
    volatilidad = df["Close"].rolling(20).std()
    df['boll inf'] = (df['20 MA'] - 2 * volatilidad).round(decimals=2)
    df['boll sup'] = (df['20 MA'] + 2 * volatilidad).round(decimals=2)
    df['Pi Cycle 1'] = df.Close.rolling(111).mean().round(decimals=2)
    df['Pi Cycle 2'] = df['350 MA'] * 2

    url = 'https://api.alternative.me/fng/?limit=0'
    response = requests.get(url)
    df_fng = pd.DataFrame(response.json()['data'])
    df_fng['value'] = df_fng['value'].astype(int)
    df_fng['timestamp'] = pd.to_datetime(df_fng['timestamp'], unit='s')
    df_fng['Date'] = df_fng['timestamp']
    df_fng.set_index(['timestamp'],inplace=True)
    df_fng.drop(columns=['time_until_update'],inplace=True)

    df_fng.rename(columns = {'value' : 'F&G_Value'}, inplace=True)
    df_fng.rename(columns = {'value_classification' : 'F&G_Class'}, inplace=True)
    df_fng.index.name = 'timestamp'

    BTC = pd.merge(left=df, right=df_fng, how='left', left_on='timestamp', right_on='timestamp')
    BTC['timestamp'] = BTC.index

    BTC['MA Index _ 100 MA'] = BTC['100 MA'] / BTC['700 MA']
    BTC['MA Index _ 200 MA'] = BTC['200 MA'] / BTC['700 MA']
    BTC['MA Index _ MA Down'] = 1
    BTC['MA Index _ MA Bottom'] = BTC['MA Index _ 100 MA'].min()

    BTC['200 Weeks Index _ 200 Weeks Bottom'] = 1
    BTC['200 Weeks Index _ 200 Weeks Down'] = BTC['200 Weeks Index'].min()+BTC['200 Weeks Index'].max()*0.075
    BTC['200 Weeks Index _ Price'] = np.where(BTC['200 Weeks Index']>7.5,7.5,BTC['200 Weeks Index'])

    BTC['Pi Cycle Index _ Index'] = BTC['Pi Cycle 1'] / BTC['Pi Cycle 2']
    BTC['Pi Cycle Index _ Down'] = BTC['Pi Cycle Index _ Index'].min()+BTC['Pi Cycle Index _ Index'].max()*0.125
    BTC['Pi Cycle Index _ Top'] = 1
    BTC['Pi Cycle Index _ Bottom'] = BTC['Pi Cycle Index _ Index'].min()

    BTC['2 Years Index _ Index'] = BTC['Close'] / BTC['2 Years Buy MA']
    BTC['2 Years Index _ Down'] = 1
    BTC['2 Years Index _ Top'] = 5
    BTC['2 Years Index _ Bottom'] = BTC['2 Years Index _ Index'].min()
    max = BTC['2 Years Index _ Top']*2
    BTC['2 Years Index _ Index'] = np.where(BTC["2 Years Index _ Index"] > max,max,BTC["2 Years Index _ Index"])

    BTC.to_csv(f'{path}/bitcoin.csv', index=False, sep=',', mode='w')