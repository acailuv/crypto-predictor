import asyncio
from multiprocessing import Process, Manager
import multiprocessing
import os
from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
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

def get_hyperparameters_data_from_user():
  file_name = u.get_menu_option("File Name (in ./svm-results/data folder): ", os.listdir(f"{u.SVM_RESULTS_FOLDER}/{u.SVM_RESULTS_FOLDER_DATA}"), False)

  return pd.read_excel(f"{u.SVM_RESULTS_FOLDER}/{u.SVM_RESULTS_FOLDER_DATA}/{file_name}")

def execute_ddqn_svm(env, df, pair_symbol):
  agent = ds.DDQNSVCAgent(env, df)
  episode_rewards, profits = u.mini_batch_train(env, agent, MAX_EPISODES, MAX_STEPS, BATCH_SIZE)

  result_df = u.generate_rewards_profits_dataframe(episode_rewards, profits)
  result_df.to_csv(f"{u.RESULTS_FOLDER}/DDQN-SVM_Results_{MAX_EPISODES}_{datetime.now()}-{pair_symbol}.csv")

  print(f"\n\n== DDQN + SVC COMPLETE ==")
  print(f"Average Rewards: {u.list_average(episode_rewards)} | Total Profits: {sum(profits)}")

def execute_ddqn(env, pair_symbol):
  agent = ddqn.DDQNAgent(env)
  episode_rewards, profits = u.mini_batch_train(env, agent, MAX_EPISODES, MAX_STEPS, BATCH_SIZE)

  result_df = u.generate_rewards_profits_dataframe(episode_rewards, profits)
  result_df.to_csv(f"{u.RESULTS_FOLDER}/DDQN_Results_{MAX_EPISODES}_{datetime.now()}-{pair_symbol}.csv")

  print(f"\n\n== Vanilla DDQN COMPLETE ==")
  print(f"Average Rewards: {u.list_average(episode_rewards)} | Total Profits: {sum(profits)}")

def train_svc():
  df = get_data_from_user()
  data_sample_count = u.get_int("Data Sampling Count: ")
  kernel_type = u.get_menu_option("Kernel Type ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed']: ", ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed'], False)
  pair_symbol = u.get_alphanumeric("Training Pair Symbol (e.g. BTC/IDR): ")
  gamma = u.get_int("Gamma: ")
  C = u.get_int("C: ")
  classifier = svc.SupportVectorClassifier(df, data_sample_count, kernel_type, pair_symbol, gamma, C)

  print(f"\nModel Construction Complete!")
  classifier.evaluate_classifier()

def generate_model(accuracy_data, df, data_sample_count, kernel_type, pair_symbol, gamma, C, save_model_flag):
  model = svc.SupportVectorClassifier(df, data_sample_count, kernel_type, pair_symbol, gamma, C, save_model_flag)
  
  accuracy_data["Gamma"].append(gamma)
  accuracy_data["C"].append(C)
  accuracy_data["Accuracy (%)"].append(model.get_accuracy())


def save_hyperparameter_performance(accuracy_data, pair_symbol, max_iteration):
  accuracy_data = dict(accuracy_data)
  accuracy_data["Gamma"] = list(accuracy_data["Gamma"])
  accuracy_data["C"] = list(accuracy_data["C"])
  accuracy_data["Accuracy (%)"] = list(accuracy_data["Accuracy (%)"])

  file_name = f"SVM-Hyperparameters_{pair_symbol}_{max_iteration}.xlsx"
  file_path = f"{u.SVM_RESULTS_FOLDER}/{u.SVM_RESULTS_FOLDER_DATA}/{file_name}"

  if file_name in os.listdir(f"{u.SVM_RESULTS_FOLDER}/{u.SVM_RESULTS_FOLDER_DATA}"):
    os.remove(file_path)

  accuracy_data_df = pd.DataFrame(accuracy_data)
  accuracy_data_df.sort_values(["Gamma", "C"])
  accuracy_data_df.to_excel(file_path)

def train_svc_batch():
  df = get_data_from_user()
  data_sample_count = u.get_int("Data Sampling Count: ")
  kernel_type = u.get_menu_option("Kernel Type ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed']: ", ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed'], False)
  pair_symbol = u.get_alphanumeric("Training Pair Symbol (e.g. BTC/IDR): ")
  save_model_flag = u.get_boolchar("Save Model?")

  with Manager() as M:
    Min = 1
    Max = 100

    accuracy_data = M.dict({
      "Gamma": M.list(),
      "C": M.list(),
      "Accuracy (%)": M.list()
    })

    pool = multiprocessing.Pool(processes=6)

    for gamma in range(Min, Max+1, 1):
      for C in range(Min, Max+1, 1):
        i = gamma-1
        scaled_sample_count = int(data_sample_count/(Max-i))
        pool.apply_async(generate_model, args=(accuracy_data, df, scaled_sample_count, kernel_type, pair_symbol, gamma, C, save_model_flag))
    
    pool.close()
    pool.join()

    save_hyperparameter_performance(accuracy_data, pair_symbol, Max)
    print(f"\nModel Construction Complete! Total Built Model: {len(accuracy_data['Gamma'])}")


opt = u.get_menu_option("\n[Data Load]\n 1. Fetch Data (Indodax)\n[AI Evaluation]\n 2. DDQN\n 3. DDQN + SVC\n 4. DDQN + SVC [VS] DDQN\n 41. SVC\n[Model Training]\n 5. Train SVC\n 6. Train SVC Batch\n[Data Visualization]\n 7. Visualize AI Profits Across Episodes\n 8. Visualize AI Accumulative Profits\n 9. Visualize Hyperparameters Sheet\n@> ", [1, 2, 3, 4, 41, 5, 6, 7, 8, 9])

if opt == 1:
  start_year = u.get_int("Start Year: ")
  end_year = u.get_int("End Year: ")
  pair = u.get_menu_option("Select Pair (e.g. BTC/IDR): ", ["BTC/IDR", "ETH/IDR", "USDT/IDR"], False)

  ccxt_engine = cie.CCXTIndodaxEngine(True)
  ccxt_engine.load_data(start_year, end_year, pair)

elif opt == 2:
  df = get_data_from_user()
  env = cte.CryptoTradingEnvironment(df)

  pair_symbol = u.get_alphanumeric("Training Pair Symbol (e.g. BTC/IDR): ")
  execute_ddqn(env, pair_symbol)

elif opt == 3:
  df = get_data_from_user()
  env = cte.CryptoTradingEnvironment(df)

  pair_symbol = u.get_alphanumeric("Training Pair Symbol (e.g. BTC/IDR): ")
  execute_ddqn_svm(env, df, pair_symbol)
  
elif opt == 4:
  df = get_data_from_user()
  env = cte.CryptoTradingEnvironment(df)
  
  pair_symbol = u.get_alphanumeric("Training Pair Symbol (e.g. BTC/IDR): ")
  execute_ddqn_svm(env, df, pair_symbol)

  env.reset() # reseting environment just in case
  
  execute_ddqn(env, pair_symbol)

elif opt == 41:
  df = get_data_from_user()
  data_sample_count = u.get_int("Data Sampling Count: ")
  kernel_type = u.get_menu_option("Kernel Type ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed']: ", ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed'], False)
  pair_symbol = u.get_alphanumeric("Training Pair Symbol (e.g. BTC/IDR): ")
  gamma = u.get_int("Gamma: ")
  C = u.get_int("C: ")

  classifier = svc.SupportVectorClassifier(df, data_sample_count, kernel_type, pair_symbol, gamma, C)

  env = cte.CryptoTradingEnvironmentSVM(df, classifier)
  env.simulate_trade()

  result_df = u.generate_profits_dataframe(env.profits)
  result_df.to_csv(f"{u.RESULTS_FOLDER}/SVM_Results_{MAX_EPISODES}_{datetime.now()}-{pair_symbol}.csv")

elif opt == 5:
  train_svc()

elif opt == 6:
  train_svc_batch()

elif opt == 7:
  df = get_result_data_from_user()
  plt.plot(df["Episode #"], df["Profits"], df["Profits"])
  plt.show()

elif opt == 8:
  df = get_result_data_from_user()
  plt.plot(df["Episode #"], df["Profits"], df["Accumulative Profits"])
  plt.show()

elif opt == 9:
  df = get_hyperparameters_data_from_user()
  file_name = u.get_alphanumeric("Save As: ")
  
  fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
  # ax.view_init(40, 50)

  # Make data.
  gammas = list(set(df["Gamma"].to_list()))
  Cs = list(set(df["C"].to_list()))

  Y = np.array(gammas)
  X = np.array(Cs)
  X, Y = np.meshgrid(X, Y)

  zList = []

  for gamma in gammas:
    curr_plot = []
    
    for C in Cs:
      row = df[(df["Gamma"] == gamma) & (df["C"] == C)]
      curr_plot.append(row["Accuracy (%)"].to_list()[0])
    
    zList.append(curr_plot)

  Z = np.array(zList)

  # Plot the surface.
  surf = ax.plot_surface(X, Y, Z, cmap='viridis', linewidth=10, antialiased=False)
  # surf = ax.contour3D(X, Y, Z, 50, cmap="binary")
  # surf = ax.scatter3D(X, Y, Z, c=Z, cmap='viridis')

  fig.colorbar(surf, ax = ax, shrink = 0.5, aspect = 5)
  ax.set_xlabel("C")
  ax.set_ylabel("Gamma")
  ax.set_zlabel("Accuracy (%)")
  plt.savefig(f"{u.SVM_RESULTS_FOLDER}/{u.SVM_RESULTS_FOLDER_GRAPHICS}/{file_name}")
