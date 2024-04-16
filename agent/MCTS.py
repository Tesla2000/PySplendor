import numpy as np
import torch
from torch import Tensor

from Config import Config
from agent.Agent import Agent
from agent.Node import Node
from src.Game import Game


class MCTS:
    def __init__(self, game: Game, model: Agent, c: float = Config.c, dirichlet_epsilon: float = Config.dirichlet_epsilon, dirichlet_alpha: float = Config.dirichlet_alpha):
        self.game = game
        self.c = c
        self.dirichlet_epsilon = dirichlet_epsilon
        self.dirichlet_alpha = dirichlet_alpha
        self.model = model

    @torch.no_grad()
    def search(self, state: np.array | tuple):
        root = Node(self.game, self.c, state, visit_count=1)

        policy, _ = self.model(
            torch.tensor(Tensor(state), device=self.model.device).unsqueeze(0)
        )
        policy = torch.softmax(policy, axis=1).squeeze(0).cpu().numpy()
        policy = (1 - self.dirichlet_epsilon) * policy + self.dirichlet_epsilon \
                 * np.random.dirichlet([self.dirichlet_alpha] * self.game.action_size)

        valid_moves = self.game.get_possible_actions()
        policy *= valid_moves
        policy /= np.sum(policy)
        root.expand(policy)

        for search in range(Config.n_simulations):
            node = root

            while node.is_fully_expanded():
                node = node.select()

            value, is_terminal = self.game.get_value_and_terminated(node.action_taken)
            value = -value

            if not is_terminal:
                policy, value = self.model(
                    torch.tensor(Tensor(node.state), device=self.model.device).unsqueeze(0)
                )
                policy = torch.softmax(policy, axis=1).squeeze(0).cpu().numpy()
                valid_moves = self.game.get_possible_actions()
                policy *= valid_moves
                policy /= np.sum(policy)

                value = value.item()

                node.expand(policy)

            node.backpropagate(value)

        action_probs = np.zeros(self.game.action_size)
        for child in root.children:
            action_probs[child.action_taken] = child.visit_count
        action_probs /= np.sum(action_probs)
        return action_probs
