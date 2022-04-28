import os
from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import shutup
from sklearnex import patch_sklearn

import ccxt_indodax_engine as cie
import crypto_trading_environment as cte
import ddqn
import ddqn_svc as ds
import svc
import utils as u

shutup.please() # disable redundant warnings
patch_sklearn() # accelerates sklearn
matplotlib.use("TkAgg")

MAX_EPISODES = 1000
MAX_STEPS = 500
BATCH_SIZE = 32


def get_data_from_user():
  pair_symbol = u.get_alphanumeric("Pair Symbol (e.g. BTC/IDR): ")
  start_year = u.get_int("Start Year: ")
  end_year = u.get_int("End Year: ")

  return pd.read_csv(f"{u.RESOURCE_FOLDER}/{pair_symbol}_{start_year}-{end_year}.csv")

def get_result_data_from_user():
  file_name = u.get_menu_option("File Name (in ./results folder): ", os.listdir(u.RESULTS_FOLDER), False)

  return pd.read_csv(f"{u.RESULTS_FOLDER}/{file_name}")

def execute_ddqn_svm(env, df):
  agent = ds.DDQNSVCAgent(env, df)
  episode_rewards, profits = u.mini_batch_train(env, agent, MAX_EPISODES, MAX_STEPS, BATCH_SIZE)

  result_df = u.generate_rewards_profits_dataframe(episode_rewards, profits)
  result_df.to_csv(f"{u.RESULTS_FOLDER}/DDQN-SVM_Results_{MAX_EPISODES}_{datetime.now()}.csv")

  print(f"\n\n== DDQN + SVC COMPLETE ==")
  print(f"Average Rewards: {u.list_average(episode_rewards)} | Total Profits: {sum(profits)}")

def execute_ddqn(env):
  agent = ddqn.DDQNAgent(env)
  episode_rewards, profits = u.mini_batch_train(env, agent, MAX_EPISODES, MAX_STEPS, BATCH_SIZE)

  result_df = u.generate_rewards_profits_dataframe(episode_rewards, profits)
  result_df.to_csv(f"{u.RESULTS_FOLDER}/DDQN_Results_{MAX_EPISODES}_{datetime.now()}.csv")

  print(f"\n\n== Vanilla DDQN COMPLETE ==")
  print(f"Average Rewards: {u.list_average(episode_rewards)} | Total Profits: {sum(profits)}")

def train_svc():
  df = get_data_from_user()
  data_sample_count = u.get_int("Data Sampling Count: ")
  kernel_type = u.get_menu_option("Kernel Type ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed']: ", ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed'], False)
  classifier = svc.SupportVectorClassifier(df, data_sample_count, kernel_type)

  print(f"\nModel Construction Complete!")
  classifier.evaluate_classifier()


opt = u.get_menu_option("\n[Data Load]\n 1. Load BTC/IDR Data (Indodax)\n[AI Evaluation]\n 2. DDQN\n 3. DDQN + SVC\n 4. DDQN + SVC [VS] DDQN\n[Model Training]\n 5. Train SVC\n[Data Visualization]\n 6. Visualize AI Data\n@> ", [1, 2, 3, 4, 5, 6])

if opt == 1:
  start_year = u.get_int("Start Year: ")
  end_year = u.get_int("End Year: ")

  ccxt_engine = cie.CCXTIndodaxEngine(True)
  ccxt_engine.load_data(start_year, end_year, 'BTC/IDR')

elif opt == 2:
  df = get_data_from_user()
  env = cte.CryptoTradingEnvironment(df)

  execute_ddqn(env)

elif opt == 3:
  df = get_data_from_user()
  env = cte.CryptoTradingEnvironment(df)

  execute_ddqn_svm(env, df)
  
elif opt == 4:
  df = get_data_from_user()
  env = cte.CryptoTradingEnvironment(df)
  
  execute_ddqn_svm(env, df)

  env.reset() # reseting environment just in case
  
  execute_ddqn(env)

elif opt == 5:
  train_svc()

elif opt == 6:
  df = get_result_data_from_user()
  plt.plot(df["Episode #"], df["Rewards"], df["Profits"])
  plt.show()
