import torch.nn as nn

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