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

app = Flask(__name__)


def select_aristocrats(game: Game):
    selected_files = list("".join(map(str, aristocrat.cost)) for aristocrat in
                          game.board.aristocrats)
    return [
        url_for("static", filename=f"components/aristocrats/{file}.png")
        for file in selected_files
    ]


game = Game()

image2build = {  # to be wired
    "image9": game.all_moves[23],
    "image10": game.all_moves[24],
    "image11": game.all_moves[25],
    "image12": game.all_moves[26],
    "image36": game.all_moves[29],
    "image14": game.all_moves[19],
    "image15": game.all_moves[20],
    "image16": game.all_moves[21],
    "image17": game.all_moves[22],
    "image37": game.all_moves[28],
    "image19": game.all_moves[15],
    "image20": game.all_moves[16],
    "image21": game.all_moves[17],
    "image22": game.all_moves[18],
    "image38": game.all_moves[27],
}

image2reserve = {  # to be wired
    "image9": game.all_moves[38],
    "image10": game.all_moves[39],
    "image11": game.all_moves[40],
    "image12": game.all_moves[41],
    "image13": game.all_moves[44],
    "image14": game.all_moves[34],
    "image15": game.all_moves[35],
    "image16": game.all_moves[36],
    "image17": game.all_moves[37],
    "image18": game.all_moves[43],
    "image19": game.all_moves[30],
    "image20": game.all_moves[31],
    "image21": game.all_moves[32],
    "image22": game.all_moves[33],
    "image23": game.all_moves[42],
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


@app.route('/click', methods=['POST'])
def click():
    global grabbed_resources, game
    data = request.json
    image_class = data.get('class')
    right_click = data.get('clickType') == "right"
    if image_class in image2build:
        if right_click:
            action = image2reserve[image_class]
        else:
            action = image2build[image_class]
        if not action.is_valid(game) or astuple(grabbed_resources):
            return jsonify(success=False)
        game = perform_move(game, action)
        return jsonify(success=True, turn_finished=True)
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


if __name__ == "__main__":
    app.run(debug=True)
