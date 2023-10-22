from PySplendor.data.Card import empty_card
from PySplendor.processing._Game import _Game
from PySplendor.processing.moves.Reserve import Reserve


class ReserveVisible(Reserve):
    def __init__(self, tier_index: int, index: int):
        super().__init__(tier_index)
        self.index = index

    def perform(self, game: _Game) -> None:
        tier = game.board.tiers[self.tier_index]
        card = tier.pop(self.index)
        self.reserve_card(game, card)

    def is_valid(self, game: _Game) -> bool:
        tier = game.board.tiers[self.tier_index]
        if tier.visible[self.index] == empty_card:
            return False
        return empty_card in game.current_player.reserve
