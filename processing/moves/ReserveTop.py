from splendor.data.Card import empty_card
from splendor.processing._Game import _Game
from splendor.processing.moves.Reserve import Reserve


class ReserveTop(Reserve):
    def perform(self, game: _Game) -> None:
        tier = game.board.tiers[self.tier_index]
        card = tier.hidden.pop()
        self.reserve_card(game, card)

    def is_valid(self, game: _Game) -> bool:
        tier = game.board.tiers[self.tier_index]
        return bool(tier.hidden) and empty_card in game.current_player.reserve.cards
