import random
from collections import deque

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

import utils as u

SVM_SAMPLE_SIZE = 200000
SVM_KERNEL_TYPE = "rbf"
class BasicBuffer:

  def __init__(self, max_size):
    self.max_size = max_size
    self.buffer = deque(maxlen=max_size)

  def push(self, state, action, reward, next_state, done):
    experience = (state, action, np.array([reward]), next_state, done)
    self.buffer.append(experience)

  def sample(self, batch_size):
    state_batch = []
    action_batch = []
    reward_batch = []
    next_state_batch = []
    done_batch = []

    batch = random.sample(self.buffer, batch_size)

    for experience in batch:
      state, action, reward, next_state, done = experience
      state_batch.append(state)
      action_batch.append(action)
      reward_batch.append(reward)
      next_state_batch.append(next_state)
      done_batch.append(done)

    return (state_batch, action_batch, reward_batch, next_state_batch, done_batch)

  def __len__(self):
    return len(self.buffer)

class SupportVectorClassifier:
  def __init__(self, data_source):
    df = data_source
    df = df.drop(["Timestamp"], axis=1)
    df = df.head(SVM_SAMPLE_SIZE)

    x = df.drop(["Trend"], axis=1)
    x = x.values
    y = df["Trend"]
    
    x_train, self.x_test, y_train, self.y_test = train_test_split(x, y, test_size = 0.20)

    model_file_name = f"SVC_{SVM_KERNEL_TYPE}-{SVM_SAMPLE_SIZE}.model"
    model_file_dir = f"{u.MODELS_FOLDER}/{model_file_name}"


    if u.check_file_in_models_directory(model_file_name):
      print("Model Data Found! Using Cached Model.")
      self.classifier = u.load_pickle(model_file_dir)
    else:
      print("No Model Found! Constructing Model...")
      self.classifier = SVC(kernel=SVM_KERNEL_TYPE)
      self.classifier.fit(x_train, y_train)
      u.save_pickle(self.classifier, model_file_dir)

    self.evaluate_classifier()
  
  def predict(self, env):
    return self.classifier.predict(env)
  
  def evaluate_classifier(self):
    predictions = self.predict(self.x_test)
    print(f"Accuracy -> {accuracy_score(self.y_test, predictions)*100} %")

def mini_batch_train(env, agent, max_episodes, max_steps, batch_size):
  episode_rewards = []
  profits = []

  for episode in range(max_episodes):
    state = env.reset()
    episode_reward = 0

    for step in range(max_steps):
      action = agent.get_action(state)
      next_state, reward, done, _, profit = env.step(action)
      agent.replay_buffer.push(state, action, reward, next_state, done)
      episode_reward += reward

      if len(agent.replay_buffer) > batch_size:
        agent.update(batch_size)   

      if done or step == max_steps-1:
        episode_rewards.append(episode_reward)
        profits.append(profit)
        print(f"\nEpisode {episode} Rewards: {episode_reward}")
        env.render()
        break

      state = next_state

  return episode_rewards, profits

class DQN(nn.Module):
    
  def __init__(self, input_dim, output_dim):
    super(DQN, self).__init__()
    self.input_dim = input_dim
    self.output_dim = output_dim
    
    self.fc = nn.Sequential(
      nn.Linear(self.input_dim[0], 128),
      nn.ReLU(),
      nn.Linear(128, 256),
      nn.ReLU(),
      nn.Linear(256, self.output_dim)
    )

  def forward(self, state):
    qvals = self.fc(state)
    return qvals


class DQNSVCAgent:

  def __init__(self, env, data_source, learning_rate=3e-4, gamma=0.99, tau=0.01, buffer_size=10000):
    self.env = env
    self.learning_rate = learning_rate
    self.gamma = gamma
    self.tau = tau
    self.replay_buffer = BasicBuffer(max_size=buffer_size)

    self.device = torch.device("cpu")

    self.model = DQN(env.observation_space.shape, env.action_space.n).to(self.device)
    self.target_model = DQN(env.observation_space.shape, env.action_space.n).to(self.device)
    
    # hard copy model parameters to target model parameters
    for target_param, param in zip(self.model.parameters(), self.target_model.parameters()):
      target_param.data.copy_(param)

    self.optimizer = torch.optim.Adam(self.model.parameters())

    self.classifier = SupportVectorClassifier(data_source)
      
      
  def get_action(self, state, eps=0.20):
    state_tensor = torch.FloatTensor(state).float().unsqueeze(0).to(self.device)
    qvals = self.model.forward(state_tensor)
    action = np.argmax(qvals.cpu().detach().numpy())
    
    if(np.random.randn() < eps):
      predictions = self.classifier.predict(state)
      latest_prediction = predictions[-1] # get the latest element
      return latest_prediction

    return action

  def compute_loss(self, batch):     
    states, actions, rewards, next_states, dones = batch

    # converting to numpy array (for faster performance)
    states = np.array(states)
    rewards = np.array(rewards)
    next_states = np.array(next_states)

    states = torch.FloatTensor(states).to(self.device)
    actions = torch.LongTensor(actions).to(self.device)
    rewards = torch.FloatTensor(rewards).to(self.device)
    next_states = torch.FloatTensor(next_states).to(self.device)
    dones = list(map(int, dones)) # converts [True, False, True, ...] to [1, 0, 1, ...]
    dones = torch.FloatTensor(dones)

    # resize tensors
    actions = actions.view(actions.size(0), 1, 1)
    dones = dones.view(dones.size(0), 1, 1)
    rewards = rewards.view(rewards.size(0), 1, 1)
    states = states.view(states.size(), -1)
    next_states = states.view(next_states.size(), -1)

    action = actions[0].item()
    if action > 2:
      action = 1

    # compute loss
    curr_Q = self.model.forward(states)[0][0][action]
    next_Q = self.target_model.forward(next_states)
    max_next_Q = torch.max(next_Q, 1)[0]
    max_next_Q = max_next_Q.view(96, 1)
    expected_Q = rewards + (1 - dones) * self.gamma * max_next_Q
    
    loss = F.mse_loss(curr_Q, expected_Q.detach())
    
    return loss

  def update(self, batch_size):
    batch = self.replay_buffer.sample(batch_size)
    loss = self.compute_loss(batch)

    self.optimizer.zero_grad()
    loss.backward()
    self.optimizer.step()
    
    # target network update
    for target_param, param in zip(self.target_model.parameters(), self.model.parameters()):
      target_param.data.copy_(self.tau * param + (1 - self.tau) * target_param)
