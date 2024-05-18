from agent.services.game_end_checker import EndOnSecondPlayer
from agent.train_to_go_fast import get_shortest_game
from src.Game import Game


def test_get_completion_times():
    game = Game()
    game_end_checker = EndOnSecondPlayer(game)
    for game_state in get_shortest_game((game, None,), 10, game_end_checker):
        pass
    # game = game.perform(GrabTwoResource(BasicResources(black=2)))
    # next_states = tuple(game.perform(valid_move) for valid_move in game.get_possible_actions())
    # return max(next_states,
    #            key=lambda state: (completion_time := get_game_sequences([GameState(state)], 10)).get(
    #                game.current_player.id, 0) / completion_time.get(game.players[-1].id, 1))


if __name__ == '__main__':
    test_get_completion_times()
