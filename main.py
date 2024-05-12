import random

from src.Game import Game


def main():
    game = Game()
    while not game.is_terminal():
        actions = game.get_possible_actions()
        action = random.choice(actions)
        game = game.perform(action)


if __name__ == "__main__":
    main()
