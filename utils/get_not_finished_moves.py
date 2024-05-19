from itertools import dropwhile

from Config import Config
from agent.entities import GameMovePairs


def get_not_finished_moves(player_id: int, game_sequence: GameMovePairs):
    player_moves = filter(lambda game_state: game_state.game.current_player.id == player_id and game_state.move,
                          game_sequence)
    return dropwhile(
        lambda game_state: game_state.game.current_player.points >= Config.min_n_points_to_finish,
        player_moves)
