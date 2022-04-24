import pandas as pd

import ccxt_indodax_engine as cie
import crypto_trading_environment as cte
import ddqn
import utils as u

MAX_EPISODES = 1000
MAX_STEPS = 500
BATCH_SIZE = 32

opt = u.get_menu_option("[Menu]\n1. Load BTC/IDR Data (Indodax)\n2. Trade!\n> ", [1, 2])

if opt == 1:
  start_year = u.get_int("Start Year: ")
  end_year = u.get_int("End Year: ")

  ccxt_engine = cie.CCXTIndodaxEngine(True)
  ccxt_engine.load_data(start_year, end_year, 'BTC/IDR')
elif opt == 2:
  pair_symbol = u.get_alphanumeric("Pair Symbol (e.g. BTC/IDR): ")
  start_year = u.get_int("Start Year: ")
  end_year = u.get_int("End Year: ")
  df = pd.read_csv(f"{u.RESOURCE_FOLDER}/{pair_symbol}_{start_year}-{end_year}.csv")

  env = cte.CryptoTradingEnvironment(df)
  agent = ddqn.DQNAgent(env)
  episode_rewards = ddqn.mini_batch_train(env, agent, MAX_EPISODES, MAX_STEPS, BATCH_SIZE)
