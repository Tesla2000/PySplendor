from itertools import pairwise, starmap

import numpy as np
from torch import nn, Tensor


class Agent(nn.Module):
    _input_size_dictionary = {
        2: 205,
    }

    def __init__(
        self,
        n_players: int,
        hidden_sizes: tuple = (256, 128, 64, 32),
        n_moves: int = 46,
    ):
        super().__init__()
        self.relu = nn.ReLU()
        self.tanh = nn.Tanh()
        self.softmax = nn.Softmax(dim=1)
        first_size = self._get_size(n_players)
        sizes = first_size, *hidden_sizes
        self.layers = tuple(starmap(nn.Linear, pairwise(sizes)))
        for index, layer in enumerate(self.layers):
            setattr(self, f"layer_{index}", layer)
        self.fc_v = nn.Linear(hidden_sizes[-1], 1)
        self.fc_p = nn.Linear(hidden_sizes[-1], n_moves)
        self._n_moves = n_moves
        self._trained = False

    def _get_size(self, n_players: int) -> int:
        return self._input_size_dictionary[n_players]

    def forward(self, state: Tensor):
        if not self.training and not self._trained:
            return self.softmax(Tensor(np.random.random((1, self._n_moves)))), Tensor(
                np.random.uniform(-1, 1, (1, 1))
            )
        self._trained = True
        for layer in self.layers:
            state = layer(state)
            state = self.relu(state)
        return self.softmax(self.fc_p(state)), self.tanh(self.fc_v(state))
