import math
import random

import gym
import numpy as np
from gym import spaces

PRINCIPAL = 1000000
MAX_SHARE_PRICE = 10000000000
MAX_NUM_SHARES = 1000000000
MAX_ACCOUNT_BALANCE = 1000000000
MAX_STEPS = 500

class CryptoTradingEnvironment(gym.Env):
  def __init__(self, df):
    super(CryptoTradingEnvironment, self).__init__()
    # self.action_space = spaces.Box(low=np.array([0, 0]), high=np.array([3, 1]), dtype=np.float16)
    self.action_space = spaces.Discrete(3)
    self.df = df
    self.reward_range = (0, MAX_ACCOUNT_BALANCE)
    self.observation_space = spaces.Box(low=0, high=math.inf, shape=(6,6), dtype=np.float32)

    self.balance = PRINCIPAL
    self.net_worth = PRINCIPAL
    self.max_net_worth = PRINCIPAL
    self.shares_held = 0
    self.cost_basis = 0
    self.total_shares_sold = 0
    self.total_sales_value = 0
    self.current_step = 0

  def reset(self):
    # Reset the state of the environment to an initial state
    self.balance = PRINCIPAL
    self.net_worth = PRINCIPAL
    self.max_net_worth = PRINCIPAL
    self.shares_held = 0
    self.cost_basis = 0
    self.total_shares_sold = 0
    self.total_sales_value = 0
  
    # Set the current step to a random point within the data frame
    self.current_step = random.randint(0, len(self.df.loc[:, 'Open'].values) - 6)
    return self._next_observation()

  def _next_observation(self):
    # Get the data points for the last 5 days and scale to between 0-1
    frame = np.array([
      self.df.loc[self.current_step: self.current_step +
                  5, 'Open'].values / MAX_SHARE_PRICE,
      self.df.loc[self.current_step: self.current_step +
                  5, 'High'].values / MAX_SHARE_PRICE,
      self.df.loc[self.current_step: self.current_step +
                  5, 'Low'].values / MAX_SHARE_PRICE,
      self.df.loc[self.current_step: self.current_step +
                  5, 'Close'].values / MAX_SHARE_PRICE,
      self.df.loc[self.current_step: self.current_step +
                  5, 'Volume'].values / MAX_NUM_SHARES,
    ])
    # Append additional data and scale each value to between 0-1
    obs = np.append(frame, [[
      self.balance / MAX_ACCOUNT_BALANCE,
      self.max_net_worth / MAX_ACCOUNT_BALANCE,
      self.shares_held / MAX_NUM_SHARES,
      self.cost_basis / MAX_SHARE_PRICE,
      self.total_shares_sold / MAX_NUM_SHARES,
      self.total_sales_value / (MAX_NUM_SHARES * MAX_SHARE_PRICE),
    ]], axis=0)
    return obs

  def step(self, action):
    # Execute one time step within the environment
    self._take_action(action)
    self.current_step += 1
    if self.current_step > len(self.df.loc[:, 'Open'].values) - 6:
      self.current_step = 0
    delay_modifier = (self.current_step / MAX_STEPS)
    
    reward = self.balance * delay_modifier
    done = self.net_worth <= 0
    next_states = self._next_observation()

    profit = self.net_worth - PRINCIPAL

    return next_states, reward, done, {}, profit
  
  def _take_action(self, action):
    # Set the current price to a random price within the time step
    current_price = random.uniform(
      self.df.loc[self.current_step, "Open"], self.df.loc[self.current_step, "Close"])

    if action == 2:
      # Buy amount % of balance in shares
      total_possible = self.balance / current_price
      shares_bought = total_possible * 0.05
      prev_cost = self.cost_basis * self.shares_held
      additional_cost = shares_bought * current_price

      self.balance -= additional_cost
      self.cost_basis = (prev_cost + additional_cost) / (self.shares_held + shares_bought)
      self.shares_held += shares_bought
    elif action == 0:
      # Sell amount % of shares held
      shares_sold = self.shares_held * 0.05
      self.balance += shares_sold * current_price
      self.shares_held -= shares_sold
      self.total_shares_sold += shares_sold
      self.total_sales_value += shares_sold * current_price

    self.net_worth = self.balance + self.shares_held * current_price

    if self.net_worth > self.max_net_worth:
      self.max_net_worth = self.net_worth

    if self.shares_held == 0:
      self.cost_basis = 0
      
  def render(self, mode='human', close=False):
    # Render the environment to the screen
    profit = self.net_worth - PRINCIPAL
    print(f'Step: {self.current_step}')
    print(f'Balance: {self.balance}')
    print(f'Shares held: {self.shares_held} (Total sold: {self.total_shares_sold})')
    print(f'Avg cost for held shares: {self.cost_basis} (Total sales value: {self.total_sales_value})')
    print(f'Net worth: {self.net_worth} (Max net worth: {self.max_net_worth})')
    print(f'Profit: {profit}')
