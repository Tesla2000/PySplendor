from agent.train_to_go_fast import get_expected_completion_times, GameState
from src.Game import Game
from src.entities.BasicResources import BasicResources
from src.moves import GrabTwoResource


def test_get_completion_times():
    game = Game()
    game = game.perform(GrabTwoResource(BasicResources(black=2)))
    next_states = tuple(game.perform(valid_move) for valid_move in game.get_possible_actions())
    return max(next_states,
               key=lambda state: (completion_time := get_expected_completion_times([GameState(state)], 10)).get(
                   game.current_player.id, 0) / completion_time.get(game.players[-1].id, 1))


if __name__ == '__main__':
    test_get_completion_times()
