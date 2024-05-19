from abc import abstractmethod, ABC
from collections import deque
from operator import attrgetter

from Config import Config
from agent.entities import GameMovePairs
from src.Game import Game
from utils.get_not_finished_moves import get_not_finished_moves


class TrainingBufferExtender(ABC):
    @abstractmethod
    def append_to_buffer(self, train_buffer: deque, game_sequence: GameMovePairs):
        pass


class TrainingBufferExtenderBothPlayers(TrainingBufferExtender):
    def append_to_buffer(self, train_buffer: deque, game_sequence: GameMovePairs):
        player_ids = list(map(attrgetter("id"), game_sequence[0][0].players))
        for player_id in player_ids:
            not_finished_moves = get_not_finished_moves(player_id, game_sequence)
            for turns_till_end, (game, move) in enumerate(not_finished_moves):
                train_buffer.append((game.get_state(), turns_till_end, Game.all_moves.index(move)))


class TrainingBufferExtenderBestPlayer(TrainingBufferExtender):
    def append_to_buffer(self, train_buffer: deque, game_sequence: GameMovePairs):
        players = game_sequence[0].game.players
        winner = players[-1].id if players[-1].points >= Config.min_n_points_to_finish else players[0].id
        not_finished_moves = get_not_finished_moves(winner, game_sequence)
        for turns_till_end, (game, move) in enumerate(not_finished_moves):
            train_buffer.append((game.get_state(), turns_till_end, Game.all_moves.index(move)))
