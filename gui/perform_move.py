import torch

from ai_move_service import AiMoveDifferential, VeryEasyAI
from src.Game import Game
from src.entities.BasicResources import BasicResources
from src.moves import Move, GrabTwoResource

move_performer = VeryEasyAI()


@torch.no_grad()
def perform_move(game: Game, move: Move) -> Game:
    game = game.perform(move)
    game = move_performer.perform_move(game)
    print("performed move AI")
    return game


if __name__ == '__main__':
    game = Game()
    perform_move(game, GrabTwoResource(BasicResources(black=2)))
