from PySplendor.data.Card import empty_card
from PySplendor.processing.GamePrototype import GamePrototype
from PySplendor.processing.moves.Reserve import Reserve


class ReserveTop(Reserve):
    def perform(self, game: GamePrototype) -> None:
        tier = game.board.tiers[self.tier_index]
        card = tier.hidden.pop()
        self.reserve_card(game, card)

    def is_valid(self, game: GamePrototype) -> bool:
        tier = game.board.tiers[self.tier_index]
        return bool(tier.hidden) and empty_card in game.current_player.reserve
