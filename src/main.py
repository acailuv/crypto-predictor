from datetime import datetime

import pandas as pd
import shutup
from sklearnex import patch_sklearn

import ccxt_indodax_engine as cie
import crypto_trading_environment as cte
import ddqn
import ddqn_svc as ds
import utils as u

shutup.please() # disable redundant warnings
patch_sklearn() # accelerates sklearn

MAX_EPISODES = 250
MAX_STEPS = 500
BATCH_SIZE = 32


def get_data_from_user():
  pair_symbol = u.get_alphanumeric("Pair Symbol (e.g. BTC/IDR): ")
  start_year = u.get_int("Start Year: ")
  end_year = u.get_int("End Year: ")

  return pd.read_csv(f"{u.RESOURCE_FOLDER}/{pair_symbol}_{start_year}-{end_year}.csv")

def execute_ddqn_svm(env, df):
  agent = ds.DDQNSVCAgent(env, df)
  episode_rewards, profits = u.mini_batch_train(env, agent, MAX_EPISODES, MAX_STEPS, BATCH_SIZE)

  result_df = u.generate_rewards_profits_dataframe(episode_rewards, profits)
  result_df.to_csv(f"{u.RESULTS_FOLDER}/DDQN-SVM_Results_{datetime.now()}.csv")

  print(f"\n\n== DDQN + SVC COMPLETE ==")
  print(f"Average Rewards: {u.list_average(episode_rewards)} | Total Profits: {sum(profits)}")

def execute_ddqn(env):
  agent = ddqn.DDQNAgent(env)
  episode_rewards, profits = u.mini_batch_train(env, agent, MAX_EPISODES, MAX_STEPS, BATCH_SIZE)

  result_df = u.generate_rewards_profits_dataframe(episode_rewards, profits)
  result_df.to_csv(f"{u.RESULTS_FOLDER}/DDQN_Results_{datetime.now()}.csv")

  print(f"\n\n== Vanilla DDQN COMPLETE ==")
  print(f"Average Rewards: {u.list_average(episode_rewards)} | Total Profits: {sum(profits)}")


opt = u.get_menu_option("[Menu]\n1. Load BTC/IDR Data (Indodax)\n2. DDQN\n3. DDQN + SVC\n4. DDQN + SVC [VS] DDQN\n> ", [1, 2, 3, 4])

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
