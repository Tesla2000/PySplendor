import torch

from ai_move_service import AiMoveDifferential, VeryEasyAI, EasyAI
from src.Game import Game
from src.entities.BasicResources import BasicResources
from src.moves import Move, GrabTwoResource

move_performer = EasyAI()


@torch.no_grad()
def perform_move(game: Game, move: Move) -> Game:
    print("Player move", move)
    game = game.perform(move)
    print("performing move AI")
    game = move_performer.perform_move(game)
    return game


if __name__ == '__main__':
    game = Game()
    perform_move(game, GrabTwoResource(BasicResources(black=2)))
