from itertools import chain, takewhile, count

import numpy as np
import torch

from Config import Config
from agent.Agent import Agent
from agent.Node import Node
from src.Game import Game


class MCTS:
    def __init__(self, model: Agent, c: float = Config.c, dirichlet_epsilon: float = Config.dirichlet_epsilon, dirichlet_alpha: float = Config.dirichlet_alpha):
        self.c = c
        self.dirichlet_epsilon = dirichlet_epsilon
        self.dirichlet_alpha = dirichlet_alpha
        self.model = model

    @torch.no_grad()
    def search(self, game: Game):
        root = Node(game, self.c, game.get_state(), visit_count=1)

        policy, _ = self.model(
            torch.tensor(root.state, device=self.model.device).unsqueeze(0).float()
        )
        policy = torch.softmax(policy, axis=1).squeeze(0).cpu().numpy()
        policy = (1 - self.dirichlet_epsilon) * policy + self.dirichlet_epsilon \
                 * np.random.dirichlet([self.dirichlet_alpha] * root.game.action_size)

        valid_moves = np.array(tuple(map(root.game.get_possible_actions().__contains__, root.game.all_moves)))
        policy *= valid_moves
        policy /= np.sum(policy)
        root.expand(policy)

        for _ in chain.from_iterable(
            (
                range(Config.n_simulations),
                takewhile(lambda _: not all(n.visit_count for n in root.children), count())
            )
        ):
            node = root

            while node.is_fully_expanded():
                node = node.select()

            value, is_terminal = node.game.get_value_and_terminated()
            value = -value

            if not is_terminal:
                policy, value = self.model(
                    torch.tensor(node.state, device=self.model.device).unsqueeze(0).float()
                )
                policy = torch.softmax(policy, axis=1).squeeze(0).cpu().numpy()
                valid_moves = np.array(tuple(map(node.game.get_possible_actions().__contains__, Game.all_moves)))
                policy *= valid_moves
                policy /= np.sum(policy)

                value = value.item()

                node.expand(policy)

            node.backpropagate(value)

        action_probs = np.zeros(root.game.action_size)
        for child in root.children:
            action_probs[child.action_taken] = child.visit_count
        action_probs /= np.sum(action_probs)
        return action_probs
