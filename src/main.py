import ccxt_engine as ce
import crypto_trading_environment as cte
import ddqn

import pandas as pd

MAX_EPISODES = 1000
MAX_STEPS = 500
BATCH_SIZE = 32

opt = input("[Menu]\n1. Load BTC/IDR Data (Indodax)\n2. Trade!\n> ")

if opt == "1":
  ccxt_engine = ce.CCXTIndodaxEngine(2012, 2022, 'BTC/IDR', True)
  ccxt_engine.load_data()
elif opt == "2":
  df = pd.read_csv('./res/BTCIDR.csv')

  env = cte.CryptoTradingEnvironment(df)
  agent = ddqn.DQNAgent(env)
  episode_rewards = ddqn.mini_batch_train(env, agent, MAX_EPISODES, MAX_STEPS, BATCH_SIZE)
else:
  print("Unknown Option! Exiting...")