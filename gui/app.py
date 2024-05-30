import logging
from dataclasses import asdict, astuple
from itertools import count

from flask import Flask, render_template, url_for, request, jsonify

from perform_move import perform_move
from src.Game import Game
from src.entities.AllResources import AllResources
from src.entities.BasicResources import BasicResources
from src.entities.Card import empty_card
from src.moves import GrabThreeResource, GrabTwoResource
from app_utils import card_to_dict
from src.moves.BuildBoard import BuildBoard
from src.moves.BuildReserve import BuildReserve

app = Flask(__name__)


def select_aristocrats(game: Game):
    selected_files = list("".join(map(str, aristocrat.cost)) for aristocrat in
                          game.board.aristocrats)
    return [
        url_for("static", filename=f"components/aristocrats/{file}.png")
        for file in selected_files
    ]


game = Game()

# TODO: Nie mam pojecia czy to dobrze, looknij tez w index w miejsca gdzie jest todo
image2build = {  # to be wired
    "tier1_index1": BuildBoard(tier_index=1, index=1),
    "tier1_index2": BuildBoard(tier_index=1, index=2),
    "tier1_index3": BuildBoard(tier_index=1, index=3),
    "tier1_index4": BuildBoard(tier_index=1, index=4),
    "tier2_index1": BuildBoard(tier_index=2, index=1),
    "tier2_index2": BuildBoard(tier_index=2, index=2),
    "tier2_index3": BuildBoard(tier_index=2, index=3),
    "tier2_index4": BuildBoard(tier_index=2, index=3),
    "tier3_index1": BuildBoard(tier_index=3, index=1),
    "tier3_index2": BuildBoard(tier_index=3, index=2),
    "tier3_index3": BuildBoard(tier_index=3, index=3),
    "tier3_index4": BuildBoard(tier_index=3, index=4),
    "reserved_index1": BuildReserve(1),
    "reserved_index2": BuildReserve(2),
    "reserved_index3": BuildReserve(3),
}

image2reserve = {  # to be wired
    "tier1_index1": BuildBoard(tier_index=1, index=1),
    "tier1_index2": BuildBoard(tier_index=1, index=2),
    "tier1_index3": BuildBoard(tier_index=1, index=3),
    "tier1_index4": BuildBoard(tier_index=1, index=4),
    "tier2_index1": BuildBoard(tier_index=2, index=1),
    "tier2_index2": BuildBoard(tier_index=2, index=2),
    "tier2_index3": BuildBoard(tier_index=2, index=3),
    "tier2_index4": BuildBoard(tier_index=2, index=3),
    "tier3_index1": BuildBoard(tier_index=3, index=1),
    "tier3_index2": BuildBoard(tier_index=3, index=2),
    "tier3_index3": BuildBoard(tier_index=3, index=3),
    "tier3_index4": BuildBoard(tier_index=3, index=4),
}

image2resource = {
    "resource_red": BasicResources(red=1),
    "resource_green": BasicResources(green=1),
    "resource_blue": BasicResources(blue=1),
    "resource_black": BasicResources(black=1),
    "resource_white": BasicResources(white=1),
}
grabbed_resources = BasicResources()


@app.route("/")
def index():
    aristocrats_urls = select_aristocrats(game)
    return render_template(
        "index.html",
        cards=dict(zip(map(str, count(1)), map(lambda tier: list(map(card_to_dict, tier.visible)),
                                               game.board.tiers))),
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


@app.route('/click_resource', methods=['POST'])
def click_resource():
    global grabbed_resources, game
    data = request.json
    image_class = data.get('class')
    right_click = data.get('clickType') == "right"
    if image_class in image2resource:
        chosen_resource = image2resource[image_class]

        if right_click:
            new_resources = AllResources(*grabbed_resources) - chosen_resource
            if new_resources.lacks():
                return jsonify(success=False)
            grabbed_resources = new_resources.get_basic()
        else:
            grabbed_resources += chosen_resource
        if sum(grabbed_resources) == 3:
            game = perform_move(game, GrabThreeResource(grabbed_resources))
            return jsonify(success=True, turn_finished=True)
        if max(grabbed_resources) == 2 and game.board.resources[
            astuple(grabbed_resources).index(max(grabbed_resources))
        ] < 2:
            return jsonify(success=False)
        if max(grabbed_resources) == 2 and sum(grabbed_resources) == 3:
            return jsonify(success=False)
        if max(grabbed_resources) == 2 and sum(grabbed_resources) != 3:
            game = perform_move(game, GrabTwoResource(grabbed_resources))
            return jsonify(success=True, turn_finished=True)

        return jsonify(success=True, turn_finished=False)

    return jsonify(success=False)


@app.route('/click_card', methods=['POST'])
def click_card():
    global grabbed_resources, game
    data = request.json
    card_id = data.get('card_id')
    action = data.get('action')

    # Determine the appropriate action based on the card_id and action
    # TODO: Checknij czy tam ma być
    if action == 'buy':
        if card_id in image2build:
            action = image2build[card_id]
            print(action)
        else:
            return jsonify(success=False)
    elif action == 'reserve':
        if card_id in image2reserve:
            action = image2reserve[card_id]
            print(action)
        else:
            return jsonify(success=False)

    if not action.is_valid(game):
        return jsonify(success=False)

    game = perform_move(game, action)
    return jsonify(success=True, turn_finished=True)


if __name__ == "__main__":
    app.run(debug=True)
