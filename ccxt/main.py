import ccxt
import time
import pandas as pd
import numpy as np

indodax = ccxt.indodax()

PAIR_SYMBOL = 'BTC/IDR'
TIMEFRAME = '1m'
TIMEFRAME_MULTI = 60*1000
START_TIME = indodax.parse8601('2022-01-10 00:00:00')
END_TIME = indodax.parse8601('2022-01-10 03:00:00')

DELAY = 15

data = []

candle_no = (int(END_TIME) - int(START_TIME)) / TIMEFRAME_MULTI + 1
print('Downloading...')
while START_TIME < END_TIME:
    try:
        ohlcvs = indodax.fetch_ohlcv(PAIR_SYMBOL, TIMEFRAME, START_TIME)
        START_TIME += len(ohlcvs) * TIMEFRAME_MULTI
        data += ohlcvs
        print(str(len(data)) + ' of ' + str(int(candle_no)) + ' candles loaded...')
    except (ccxt.ExchangeError, ccxt.AuthenticationError, ccxt.ExchangeNotAvailable, ccxt.RequestTimeout) as error:
        print('Got an error', type(error).__name__, error.args, ', retrying in', DELAY, 'seconds...')
        time.sleep(DELAY)

header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
df = pd.DataFrame(data, columns=header)

print(df)

df.to_pickle('BTCIDR.data')

rd = pd.read_pickle('BTCIDR.data')

print(rd)
