from itertools import pairwise, starmap

from torch import nn, Tensor

from Config import Config


class Agent(nn.Module):
    device = Config.device
    _input_size_dictionary = {
        2: 256,
    }

    def __init__(
        self,
        n_players: int = Config.n_players,
        hidden_size: tuple = Config.hidden_size,
        n_moves: int = Config.n_actions,
    ):
        super().__init__()
        self.tanh = nn.Tanh()
        self.softmax = nn.Softmax(dim=1)
        first_size = self._get_size(n_players)
        self.hidden_sizes = hidden_size
        sizes = first_size, *hidden_size
        self.layers = nn.ModuleList(starmap(nn.Linear, pairwise(sizes)))
        self.fc_p = nn.Linear(sizes[-1], n_moves)
        self._n_moves = n_moves
        self.relu = nn.LeakyReLU()

    def _get_size(self, n_players: int) -> int:
        return self._input_size_dictionary[n_players]

    def forward(self, state: Tensor):
        for layer in self.layers:
            state = layer(state)
            state = self.relu(state)
        return self.fc_p(state)
