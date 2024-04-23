import math
from typing import Self

import numpy as np
from numba import jit

from src.Game import Game


class Node:
    def __init__(self, game: Game, c: float, parent: Self = None, action_taken: int = None,
                 prior: int = 0, visit_count: int = 0):
        self.game = game
        self.c = c
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
        return _get_ucb(child.visit_count, child.value_sum, child.prior, self.c, self.visit_count)
        # if child.visit_count == 0:
        #     q_value = 0
        # else:
        #     q_value = 1 - ((child.value_sum / child.visit_count) + 1) / 2
        # return q_value + self.c * (math.sqrt(self.visit_count) / (child.visit_count + 1)) * child.prior

    def expand(self, policy: np.array) -> Self:
        for action_index, prob in enumerate(policy):
            if prob > 0:
                action = self.game.all_moves[action_index]
                child_game = action.perform(self.game)

                child = Node(child_game, self.c, self, action_index, prob)
                self.children.append(child)
        if not self.children:
            action = self.game.null_move
            child_game = action.perform(self.game)
            child = Node(child_game, self.c, self)
            self.children.append(child)
        return child

    def backpropagate(self, value: float):
        self.value_sum += value
        self.visit_count += 1

        value = -value
        if self.parent is not None:
            self.parent.backpropagate(value)


@jit(nopython=True)
def _get_ucb(child_visit_count: int, child_value_sum: int, child_prior: float, c: float, visit_count: int):
    if child_visit_count == 0:
        q_value = 0
    else:
        q_value = 1 - ((child_value_sum / child_visit_count) + 1) / 2
    return q_value + c * (math.sqrt(visit_count) / (child_visit_count + 1)) * child_prior
