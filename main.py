import random

from src.Game import Game

if __name__ == '__main__':
    game = Game()
    while not game.is_terminal():
        game.perform(random.choice(game.get_possible_actions()))
