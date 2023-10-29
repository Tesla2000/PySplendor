from PySplendor.data.Card import empty_card
from PySplendor.processing.GamePrototype import GamePrototype
from PySplendor.processing.moves.Reserve import Reserve


class ReserveVisible(Reserve):
    def __init__(self, tier_index: int, index: int):
        super().__init__(tier_index)
        self.index = index

    def perform(self, game: GamePrototype) -> GamePrototype:
        tier = game.board.tiers[self.tier_index]
        card = tier.pop(self.index)
        self.reserve_card(game, card)
        return game

    def is_valid(self, game: GamePrototype) -> bool:
        tier = game.board.tiers[self.tier_index]
        if tier.visible[self.index] == empty_card:
            return False
        return game.current_player.reserve.can_add()
