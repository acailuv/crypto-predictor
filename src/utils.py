import os
import pickle

import pandas as pd

RESOURCE_FOLDER = "./res"

DOWNTREND = 0
SIDEWAYS = 1
UPTREND = 2

def alphanumeric_only(s):
  return "".join(filter(str.isalnum, s))

def is_int(n):
  try:
    int(n)
    return True
  except ValueError:
    return False

def get_int(msg):
  n = input(msg)

  while not is_int(n):
    print("Invalid Input. Try Again.\n\n")
    n = input(msg)
  
  return int(n)

def get_alphanumeric(msg):
  return alphanumeric_only(input(msg))

def get_option(msg, convert_to_int=True):
  if convert_to_int:
    return get_int(msg)
  else:
    return input(msg)

def get_menu_option(msg, valid_options, convert_to_int=True):
  opt = get_option(msg, convert_to_int)

  while opt not in valid_options:
    print(f"Invalid Option. Your Option [{opt}] does not exists in option choices: {valid_options}\n\n")
    opt = get_option(msg, convert_to_int)
  
  return opt

def load_pickle(file_dir):
  try:
    f = open(file_dir, "rb")
    data = pickle.load(f)
    f.close()
    return data
  except EOFError:
    return []

def save_pickle(data, file_dir):
  try:
    f = open(file_dir, "wb")
    pickle.dump(data, f)
    f.close()
    return True
  except:
    return False

def get_res_directory_map(debug=False):
    directory_map = {}
    for f in os.listdir(RESOURCE_FOLDER):
      directory_map[f] = True
    
    if debug:
      print(f"\n\nDirectory Map:\n{directory_map}")
    
    return directory_map

def check_file_in_res_directory(file_name):
  try:
    return get_res_directory_map()[file_name]
  except:
    return False

def evaluate_trends(data, debug=False):
    data_with_trend = []

    for i, candle in enumerate(data):
      if i == len(data)-1:
        break # loop is finished, erase the final row

      current_candle = candle
      next_candle = data[i+1]
      
      open_price = candle[1]
      next_close_price = next_candle[4]

      if open_price < next_close_price:
        current_candle.append(UPTREND)
      elif open_price == next_close_price:
        current_candle.append(SIDEWAYS)
      else:
        current_candle.append(DOWNTREND)
      
      data_with_trend.append(current_candle)
    
    if debug:
      print(f"\n\nTrend Processing Complete!\n> Results:\n{data_with_trend}")
  
    return data_with_trend

def transform_to_dataframe_with_trend(data_with_trend):
  header = ["Timestamp", "Open", "High", "Low", "Close", "Volume", "Trend"]
  data_df = pd.DataFrame(data_with_trend, columns=header)

  return data_df

def list_average(ls):
  return sum(ls)/len(ls)
