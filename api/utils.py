import os
import pickle

import pandas as pd

RESOURCE_FOLDER = "./res"
MODELS_FOLDER = "./models"
RESULTS_FOLDER = "./results"
SVM_RESULTS_FOLDER = "./svm-results"
SVM_RESULTS_FOLDER_DATA = "data"
SVM_RESULTS_FOLDER_GRAPHICS = "graphics"

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
        print(
            f"Invalid Option. Your Option [{opt}] does not exists in option choices: {valid_options}\n\n")
        opt = get_option(msg, convert_to_int)

    return opt


def get_boolchar(msg):
    valid_boolchars = ["y", "n"]
    opt = get_option(f"{msg} (Y/N): ", False)

    while opt.lower() not in valid_boolchars:
        print(
            f"Invalid Option. Your Option [{opt}] does not exists in option choices: {valid_boolchars}\n\n")
        opt = get_option(f"{msg} (Y/N): ", False)

    if opt == valid_boolchars[0]:
        return True
    else:
        return False


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
    except Exception as err:
        print(f"Error while saving file! {err}")
        return False


def interval_save_pickle(data, file_dir, i, interval=100):
    if i == interval:
        save_pickle(data, file_dir)
        return 0

    return i + 1


def get_res_directory_map(debug=False):
    directory_map = {}
    for f in os.listdir(RESOURCE_FOLDER):
        directory_map[f] = True

    if debug:
        print(f"\n\nDirectory Map:\n{directory_map}")

    return directory_map


def get_models_directory_map(debug=False):
    directory_map = {}
    for f in os.listdir(MODELS_FOLDER):
        directory_map[f] = True

    if debug:
        print(f"\n\nDirectory Map:\n{directory_map}")

    return directory_map


def check_file_in_res_directory(file_name):
    try:
        return get_res_directory_map()[file_name]
    except:
        return False


def check_file_in_models_directory(file_name):
    try:
        return get_models_directory_map()[file_name]
    except:
        return False


def evaluate_trends(data, debug=False):
    data_with_trend = []

    for i, candle in enumerate(data):
        if i == len(data)-1:
            break  # loop is finished, erase the final row

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


def generate_rewards_profits_dataframe(episode_rewards, profits):
    if len(episode_rewards) != len(profits):
        raise Exception(
            "Length of episode_rewards should equal to length of profits")

    compiled_data = []

    for i in range(len(episode_rewards)):
        data = [i, episode_rewards[i], profits[i]]
        compiled_data.append(data)

    return pd.DataFrame(compiled_data, columns=["Episode #", "Rewards", "Profits"])


def generate_profits_dataframe(profits):
    compiled_data = []
    accumulated_profits = 0

    for i in range(len(profits)):
        accumulated_profits += profits[i]
        data = [i, profits[i], accumulated_profits]
        compiled_data.append(data)

    return pd.DataFrame(compiled_data, columns=["Episode #", "Profits", "Accumulative Profits"])


def mini_batch_train(env, agent, max_episodes, max_steps, batch_size):
    episode_rewards = []
    profits = []

    print("\n=== START TESTING ===")

    for episode in range(max_episodes):
        state = env.reset()
        episode_reward = 0
        total_profit = 0

        for step in range(max_steps):
            action = agent.get_action(state)

            action = action % 3

            next_state, reward, done, _, profit = env.step(action)
            agent.replay_buffer.push(state, action, reward, next_state, done)
            episode_reward += reward
            total_profit += profit

            if len(agent.replay_buffer) > batch_size:
                agent.update(batch_size)

            if done or step == max_steps-1:
                episode_rewards.append(episode_reward)
                profits.append(total_profit)
                print(
                    f"Episode {episode}\t|\tTotal Rewards: {episode_reward:.10f}\t|\tTotal Profit: {total_profit}")
                break

            state = next_state

    return episode_rewards, profits
