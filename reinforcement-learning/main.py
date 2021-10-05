from Agent import Agent
from utils import *
import sys

stock_name = input("Stock .csv: ")
window_size = input("Window Size: ")
episode_count = input("Episode Count: ")
stock_name = str(stock_name)
window_size = int(window_size)
episode_count = int(episode_count)
agent = Agent(window_size)
data = get_stock_data_vector(stock_name)
l = len(data) - 1
batch_size = 32
for e in range(episode_count + 1):
    print("Episode " + str(e) + "/" + str(episode_count))
    state = get_state(data, 0, window_size + 1)
    total_profit = 0
    agent.inventory = []
    for t in range(l):
        print(f"Iteration {t}: ", end='')
        action = agent.act(state)
        # sit
        next_state = get_state(data, t + 1, window_size + 1)
        reward = 0
        if action == 1: # buy
            agent.inventory.append(data[t])
            print("Buy: " + format_price(data[t]))
        elif action == 2 and len(agent.inventory) > 0: # sell
            bought_price = window_size_price = agent.inventory.pop(0)
            reward = max(data[t] - bought_price, 0)
            total_profit += data[t] - bought_price
            print("Sell: " + format_price(data[t]) + " | Profit: " + format_price(data[t] - bought_price))
        else:
            print("Holding...")
        done = True if t == l - 1 else False
        agent.memory.append((state, action, reward, next_state, done))
        state = next_state
        if done:
            print("--------------------------------")
            print("Total Profit: " + format_price(total_profit))
            print("--------------------------------")
        if len(agent.memory) > batch_size:
            agent.exp_replay(batch_size)
    if e % 10 == 0:
        agent.model.save(str(e))
