import math
from typing import Self, Literal

import numpy as np

from src.Game import Game
from src.moves import NullMove


class Node:
    def __init__(self, game: Game, c: float, state: np.array, parent: Self = None, action_taken: int = None,
                 prior: int = 0, visit_count: int = 0):
        self.game = game
        self.c = c
        self.state = state
        self.parent = parent
        self.action_taken = action_taken
        self.prior = prior

        self.children = []

        self.visit_count = visit_count
        self.value_sum = 0

    def is_fully_expanded(self) -> bool:
        return len(self.children) > 0

    def select(self) -> Self:
        best_ucb = -np.inf

        for child in self.children:
            ucb = self.get_ucb(child)
            if ucb > best_ucb:
                best_child = child
                best_ucb = ucb

        return best_child

    def get_ucb(self, child: Self) -> float:
        if child.visit_count == 0:
            q_value = 0
        else:
            q_value = 1 - ((child.value_sum / child.visit_count) + 1) / 2
        return q_value + self.c * (math.sqrt(self.visit_count) / (child.visit_count + 1)) * child.prior

    def expand(self, policy: np.array) -> Self:
        for action_index, prob in enumerate(policy):
            if prob > 0:
                action = self.game.all_moves[action_index]
                child_game = action.perform(self.game)

                child = Node(child_game, self.c, child_game.get_state(), self, action_index, prob)
                self.children.append(child)
        if not self.children:
            action = self.game.null_move
            child_game = action.perform(self.game)
            child = Node(child_game, self.c, child_game.get_state(), self)
            self.children.append(child)
        return child

    def backpropagate(self, value: float):
        self.value_sum += value
        self.visit_count += 1

        value = -value
        if self.parent is not None:
            self.parent.backpropagate(value)
