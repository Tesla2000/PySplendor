from dataclasses import asdict

from flask import Flask, render_template, url_for

from src.Game import Game
from src.entities.BasicResources import BasicResources
from src.entities.Card import empty_card, Card

app = Flask(__name__)


def select_aristocrats(game: Game):
    selected_files = list("".join(map(str, aristocrat.cost)) for aristocrat in
                          game.board.aristocrats)
    return [
        url_for("static", filename=f"components/aristocrats/{file}.png")
        for file in selected_files
    ]


game = Game()


def card_to_dict(card: Card):
    prod2str = {
        BasicResources(red=1): "RED",
        BasicResources(green=1): "GREEN",
        BasicResources(blue=1): "BLUE",
        BasicResources(black=1): "BLACK",
        BasicResources(white=1): "WHITE",
    }
    return dict(**asdict(card.cost), production=prod2str[card.production])


@app.route("/")
def index():
    aristocrats_urls = select_aristocrats(game)
    return render_template(
        "index.html",
        cards=dict(enumerate(map(lambda tier: list(map(asdict, tier.visible)),
                                 game.board.tiers), 1)),
        cards_left=list(map(lambda tier: len(tier.hidden), game.board.tiers)),
        chips_left=asdict(game.board.resources),
        player_card_count=asdict(game.current_player.production),
        player_total_points=game.current_player.points,
        player_chips=asdict(game.current_player.resources),
        si_card_count=asdict(game.players[-1].production),
        si_total_points=game.players[-1].points,
        si_chips=asdict(game.players[-1].resources),
        si_cards_reserved=list(
            filter(lambda card: card != empty_card, game.players[-1].reserve)),
        player_cards_reserved=list(filter(lambda card: card != empty_card,
                                          game.current_player.reserve)),
        aristocrats_urls=aristocrats_urls,
    )


if __name__ == "__main__":
    app.run(debug=True)
