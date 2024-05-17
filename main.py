import random

from src.Game import Game


def main():
    print(len(Game().get_state()) - 45)
    print(len(Game(n_players=3).get_state()) - 45)
    print(len(Game(n_players=4).get_state()) - 45)
    game = Game()
    # while not game.is_terminal():
    #     actions = game.get_possible_actions()
    #     action = random.choice(actions)
    #     game = game.perform(action)


if __name__ == "__main__":
    main()
