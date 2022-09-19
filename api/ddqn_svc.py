import numpy as np
import torch
import torch.nn.functional as F

import basic_buffer as bb
import dqn
import svc


class DDQNSVCAgent:

  def __init__(self, env, data_source, learning_rate=3e-4, gamma=0.99, tau=0.01, buffer_size=10000):
    self.env = env
    self.learning_rate = learning_rate
    self.gamma = gamma
    self.tau = tau
    self.replay_buffer = bb.BasicBuffer(max_size=buffer_size)

    self.device = torch.device("cpu")

    self.model = dqn.DQN(env.observation_space.shape, env.action_space.n).to(self.device)
    self.target_model = dqn.DQN(env.observation_space.shape, env.action_space.n).to(self.device)
    
    # hard copy model parameters to target model parameters
    for target_param, param in zip(self.model.parameters(), self.target_model.parameters()):
      target_param.data.copy_(param)

    self.optimizer = torch.optim.Adam(self.model.parameters())

    self.classifier = svc.SupportVectorClassifier(data_source)
      
      
  def get_action(self, state, eps=0.20):
    state_tensor = torch.FloatTensor(state).float().unsqueeze(0).to(self.device)
    qvals = self.model.forward(state_tensor)
    action = np.argmax(qvals.cpu().detach().numpy())
    
    if(np.random.randn() < eps):
      predictions = self.classifier.predict(state)
      latest_prediction = predictions[-1] # get the latest element
      return latest_prediction%3

    return action%3

  def compute_loss(self, batch):     
    states, actions, rewards, next_states, dones = batch

    # converting to numpy array (for faster performance)
    states = np.array(states)
    rewards = np.array(rewards)
    next_states = np.array(next_states)
    dones = list(map(int, dones)) # converts [True, False, True, ...] to [1, 0, 1, ...]

    states = torch.FloatTensor(states).to(self.device)
    actions = torch.LongTensor(actions).to(self.device)
    rewards = torch.FloatTensor(rewards).to(self.device)
    next_states = torch.FloatTensor(next_states).to(self.device)
    dones = torch.FloatTensor(dones)

    # resize tensors
    actions = actions.view(actions.size(0), 1, 1)
    dones = dones.view(dones.size(0), 1, 1)
    rewards = rewards.view(rewards.size(0), 1, 1)
    states = states.view(states.size(), -1)
    next_states = states.view(next_states.size(), -1)

    action = actions[0].item()

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
