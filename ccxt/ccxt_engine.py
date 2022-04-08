import os
import time
import pandas as pd
import ccxt
import utils

TIMEFRAME = '1m'
TIMEFRAME_MULTI = 60*1000
RESOURCE_FOLDER = "./res"
ERROR_DELAY = 15

class CCXTEngine:
  def __init__(self, start_year, end_year, pair_symbol, debug=False):
    self.indodax = ccxt.indodax()
    self.pair_symbol = pair_symbol
    self.start_time = self.indodax.parse8601(f"{start_year}-01-01 00:00:00")
    self.end_time = self.indodax.parse8601(f"{end_year}-01-01 23:59:59")
    self.file_name = f"{utils.strip_alphanumeric(pair_symbol)}.data"
    self.debug = debug

    if self.debug:
      print("CCXT Engine is Ready!")
      print(f"> Pair: {self.pair_symbol}\n> Start Timestamp: {self.start_time}\n> End Timestamp: {self.end_time}\n> Data File Name: {self.file_name}\n> Debug Mode: {self.debug}")

  def get_directory_map(self):
    directory_map = {}
    for f in os.listdir(RESOURCE_FOLDER):
      directory_map[f] = True
    
    if self.debug:
      print(f"\n\nDirectory Map:\n{directory_map}")
    
    return directory_map

  def check_file_in_directory(self):
    try:
      return self.get_directory_map()[self.file_name]
    except:
      return False

  def load_data(self):
    if self.check_file_in_directory():
      res = pd.read_pickle(f"{RESOURCE_FOLDER}/{self.file_name}")

      if self.debug:
        print(f"\n\nData File Found!\n{self.file_name}")
      return 
    
    if self.debug:
      print("\n\nData File Not Found! Downloading from CCXT...")

    data = []

    candle_no = (int(self.end_time) - int(self.start_time)) / TIMEFRAME_MULTI + 1

    if self.debug:
      print('Downloading...')
    
    while self.start_time < self.end_time:
        try:
            ohlcvs = self.indodax.fetch_ohlcv(self.pair_symbol, TIMEFRAME, self.start_time)
            self.start_time += len(ohlcvs) * TIMEFRAME_MULTI
            data += ohlcvs

            if self.debug:
              print(str(len(data)) + ' of ' + str(int(candle_no)) + ' candles loaded...')
        except (ccxt.ExchangeError, ccxt.AuthenticationError, ccxt.ExchangeNotAvailable, ccxt.RequestTimeout) as error:
            print('Got an error', type(error).__name__, error.args, ', retrying in', ERROR_DELAY, 'seconds...')
            time.sleep(ERROR_DELAY)

    header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
    data_df = pd.DataFrame(data, columns=header)

    data_df.to_pickle(f"{RESOURCE_FOLDER}/{self.file_name}")

    if self.debug:
      print(f"\n\nDownload Complete!\n> Dictionary Form:\n{data}\n> DataFrame Form:\n{data_df}")

    return data_df
