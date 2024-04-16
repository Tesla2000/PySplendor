from itertools import pairwise, starmap

import numpy as np
from torch import nn, Tensor

from Config import Config


class Agent(nn.Module):
    _input_size_dictionary = {
        2: 211,
    }

    def __init__(
        self,
        n_players: int,
        hidden_size: tuple = Config.hidden_size,
        n_moves: int = Config.n_actions,
    ):
        super().__init__()
        self.tanh = nn.Tanh()
        self.softmax = nn.Softmax(dim=1)
        first_size = self._get_size(n_players)
        sizes = first_size, *hidden_size
        self.layers = nn.ModuleList(starmap(nn.Linear, pairwise(sizes)))
        self.trained = True
        self.fc_v = nn.Linear(sizes[-1], 1)
        self.fc_p = nn.Linear(sizes[-1], n_moves)
        self._n_moves = n_moves

    def _get_size(self, n_players: int) -> int:
        return self._input_size_dictionary[n_players]

    def forward(self, state: Tensor):
        if not self.training and not self.trained:
            return self.softmax(Tensor(np.random.random((1, self._n_moves)))), Tensor(
                np.random.uniform(-1, 1, (1, 1))
            )
        self.trained = True
        for layer in self.layers:
            state = layer(state)
        return self.softmax(self.fc_p(state)), self.tanh(self.fc_v(state))
