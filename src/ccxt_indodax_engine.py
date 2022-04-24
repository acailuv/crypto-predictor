import math
import os
import time

import ccxt
import pandas as pd

import utils
import utils as u

TIMEFRAME = "1m"
TIMEFRAME_MULTI = 60*1000
ERROR_DELAY = 15

class CCXTIndodaxEngine:
  def __init__(self, debug=False):
    self.indodax = ccxt.indodax()
    self.debug = debug

    if self.debug:
      print("\n\n[Indodax] CCXT Engine is Ready!")
      print(f"> Debug Mode: {self.debug}")

  def download_data(self, start_time, end_time, pair_symbol, file_name):
    data = []
    cache_file_dir = f"{u.RESOURCE_FOLDER}/{file_name}.cache"
    cache_file_name = f"{file_name}.cache"
    
    if u.check_file_in_res_directory(cache_file_name):
      data = u.load_pickle(cache_file_dir)
      if data == None:
        data = []
      else:
        if self.debug:
          print(f"\n\nCache Data Found! (Downloaded Data: {len(data)}) Continuing Download...")
        start_time = len(data) * TIMEFRAME_MULTI

    candle_no = math.ceil((int(end_time) - int(start_time)) / TIMEFRAME_MULTI)

    if self.debug:
      print("\n\nDownloading...")
    
    while start_time < end_time:
      try:
        candles = self.indodax.fetch_ohlcv(pair_symbol, TIMEFRAME, start_time)
        start_time += len(candles) * TIMEFRAME_MULTI
        data += candles

        u.save_pickle(data, cache_file_dir)

        if self.debug:
          download_percentage = round((len(data)/candle_no)*100, 6)
          print(f"{len(data)} of {candle_no} candles loaded....\t({len(candles)} Data/s) -- {download_percentage} %", end="\r")
      except (ccxt.ExchangeError, ccxt.AuthenticationError, ccxt.ExchangeNotAvailable, ccxt.RequestTimeout) as error:
        print("Got an error", type(error).__name__, error.args, ", retrying in", ERROR_DELAY, "seconds...")
        time.sleep(ERROR_DELAY)
    
    os.remove(cache_file_dir)
    return data

  def load_data(self, start_year, end_year, pair_symbol):
    start_time = self.indodax.parse8601(f"{start_year}-01-01 00:00:00")
    end_time = self.indodax.parse8601(f"{end_year}-12-31 23:59:59")
    file_name = f"{utils.alphanumeric_only(pair_symbol)}_{start_year}-{end_year}.csv"

    if u.check_file_in_res_directory(file_name):
      res = pd.read_csv(f"{u.RESOURCE_FOLDER}/{file_name}")

      if self.debug:
        print(f"\n\nData File Found!\n{file_name}:\n{res}")
      return res
    
    if self.debug:
      print("\n\nData File Not Found! Downloading from CCXT...")

    data = self.download_data(start_time, end_time, pair_symbol, file_name)
    data_with_trend = u.evaluate_trends(data)
    data_df = u.transform_to_dataframe_with_trend(data_with_trend)

    data_df.to_csv(f"{u.RESOURCE_FOLDER}/{file_name}")

    if self.debug:
      print(f"\n\nDownload Complete!\n> Raw Form:\n{data}\n> DataFrame Form:\n{data_df}")

    return data_df
