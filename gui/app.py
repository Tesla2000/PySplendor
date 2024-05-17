from dataclasses import astuple

from flask import Flask, render_template, request, jsonify, url_for

from Config import Config
from src.Game import Game
from src.entities.AllResources import AllResources
from src.entities.BasicResources import BasicResources
from src.entities.Card import Card
from src.moves import GrabThreeResource, GrabTwoResource

game = Game()
app = Flask(__name__, template_folder=Config.templates)


def get_building_name(tier: int, building: Card) -> str:
    prod2str = {
        BasicResources(red=1): "RED",
        BasicResources(green=1): "GREEN",
        BasicResources(blue=1): "BLUE",
        BasicResources(black=1): "BROWN",
        BasicResources(white=1): "WHITE",
    }
    return str(tier) + prod2str[building.production] + "".join(map(str, astuple(building.cost)))


images = {}


@app.route('/')
def home():
    images.update({
        'image_path_0': url_for('static', filename='components/resource/red.png'),
        'image_path_1': url_for('static', filename='components/resource/green.png'),
        'image_path_2': url_for('static', filename='components/resource/blue.png'),
        'image_path_3': url_for('static', filename='components/resource/brown.png'),
        'image_path_4': url_for('static', filename='components/resource/white.png'),
        'image_path_5': url_for('static', filename='components/resource/gold.png'),
        'image_path_6': url_for('static',
                                filename=f'components/aristocrats/{"".join(map(str, astuple(game.board.aristocrats[0].cost)))}.png'),
        'image_path_7': url_for('static',
                                filename=f'components/aristocrats/{"".join(map(str, astuple(game.board.aristocrats[1].cost)))}.png'),
        'image_path_8': url_for('static',
                                filename=f'components/aristocrats/{"".join(map(str, astuple(game.board.aristocrats[2].cost)))}.png'),
        'image_path_9': url_for('static',
                                filename=f'components/buildings/{get_building_name(3, game.board.tiers[2].visible[0])}.png'),
        'image_path_10': url_for('static',
                                 filename=f'components/buildings/{get_building_name(3, game.board.tiers[2].visible[1])}.png'),
        'image_path_11': url_for('static',
                                 filename=f'components/buildings/{get_building_name(3, game.board.tiers[2].visible[2])}.png'),
        'image_path_12': url_for('static',
                                 filename=f'components/buildings/{get_building_name(3, game.board.tiers[2].visible[3])}.png'),
        'image_path_13': url_for('static', filename='components/tier_3.png'),
        'image_path_14': url_for('static',
                                 filename=f'components/buildings/{get_building_name(2, game.board.tiers[1].visible[0])}.png'),
        'image_path_15': url_for('static',
                                 filename=f'components/buildings/{get_building_name(2, game.board.tiers[1].visible[1])}.png'),
        'image_path_16': url_for('static',
                                 filename=f'components/buildings/{get_building_name(2, game.board.tiers[1].visible[2])}.png'),
        'image_path_17': url_for('static',
                                 filename=f'components/buildings/{get_building_name(2, game.board.tiers[1].visible[3])}.png'),
        'image_path_18': url_for('static', filename='components/tier_2.png'),
        'image_path_19': url_for('static',
                                 filename=f'components/buildings/{get_building_name(1, game.board.tiers[0].visible[0])}.png'),
        'image_path_20': url_for('static',
                                 filename=f'components/buildings/{get_building_name(1, game.board.tiers[0].visible[1])}.png'),
        'image_path_21': url_for('static',
                                 filename=f'components/buildings/{get_building_name(1, game.board.tiers[0].visible[2])}.png'),
        'image_path_22': url_for('static',
                                 filename=f'components/buildings/{get_building_name(1, game.board.tiers[0].visible[3])}.png'),
        'image_path_23': url_for('static', filename='components/tier_1.png'),
        'image_path_24': url_for('static', filename='components/resource/red.png'),
        'image_path_25': url_for('static', filename='components/resource/green.png'),
        'image_path_26': url_for('static', filename='components/resource/blue.png'),
        'image_path_27': url_for('static', filename='components/resource/brown.png'),
        'image_path_28': url_for('static', filename='components/resource/white.png'),
        'image_path_29': url_for('static', filename='components/resource/gold.png'),
        'image_path_30': url_for('static', filename='components/resource/red.png'),
        'image_path_31': url_for('static', filename='components/resource/green.png'),
        'image_path_32': url_for('static', filename='components/resource/blue.png'),
        'image_path_33': url_for('static', filename='components/resource/brown.png'),
        'image_path_34': url_for('static', filename='components/resource/white.png'),
        'image_path_35': url_for('static', filename='components/resource/gold.png'),
        'image_path_36': url_for('static', filename=f'components/buildings/{get_building_name(1, game.current_player.reserve[0])}.png'),
        'image_path_37': url_for('static', filename=f'components/buildings/{get_building_name(1, game.current_player.reserve[1])}.png'),
        'image_path_38': url_for('static', filename=f'components/buildings/{get_building_name(1, game.current_player.reserve[2])}.png'),
    })
    return render_template('new_index.html', **images)


image2build = {
    "image9": game.all_moves,
    "image10": lambda: game.board.tiers[2].visible[1],
    "image11": lambda: game.board.tiers[2].visible[2],
    "image12": lambda: game.board.tiers[2].visible[3],
    "image13": lambda: game.board.tiers[2].hidden[0],
    "image14": lambda: game.board.tiers[1].visible[0],
    "image15": lambda: game.board.tiers[1].visible[1],
    "image16": lambda: game.board.tiers[1].visible[2],
    "image17": lambda: game.board.tiers[1].visible[3],
    "image18": lambda: game.board.tiers[1].hidden[0],
    "image19": lambda: game.board.tiers[0].visible[0],
    "image20": lambda: game.board.tiers[0].visible[1],
    "image21": lambda: game.board.tiers[0].visible[2],
    "image22": lambda: game.board.tiers[0].visible[3],
    "image23": lambda: game.board.tiers[0].hidden[3],
}


image2reserve = {
    "image9": lambda: game.board.tiers[2].visible[0],
    "image10": lambda: game.board.tiers[2].visible[1],
    "image11": lambda: game.board.tiers[2].visible[2],
    "image12": lambda: game.board.tiers[2].visible[3],
    "image13": lambda: game.board.tiers[2].hidden[0],
    "image14": lambda: game.board.tiers[1].visible[0],
    "image15": lambda: game.board.tiers[1].visible[1],
    "image16": lambda: game.board.tiers[1].visible[2],
    "image17": lambda: game.board.tiers[1].visible[3],
    "image18": lambda: game.board.tiers[1].hidden[0],
    "image19": lambda: game.board.tiers[0].visible[0],
    "image20": lambda: game.board.tiers[0].visible[1],
    "image21": lambda: game.board.tiers[0].visible[2],
    "image22": lambda: game.board.tiers[0].visible[3],
    "image23": lambda: game.board.tiers[0].hidden[3],
}

image2resource = {
    "image24": BasicResources(red=1),
    "image25": BasicResources(green=1),
    "image26": BasicResources(blue=1),
    "image27": BasicResources(black=1),
    "image28": BasicResources(white=1),
}
grabbed_resources = BasicResources()


@app.route('/click', methods=['POST'])
def click():
    global grabbed_resources
    data = request.json
    image_class = data.get('class')
    right_click = data.get('clickType') == "right"
    if image_class in image2build:

        return jsonify(success=True)
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
            game.perform(GrabThreeResource(grabbed_resources))
        if max(grabbed_resources) == 2 and sum(grabbed_resources) == 3:
            return jsonify(success=False)
        if max(grabbed_resources) == 2 and sum(grabbed_resources) != 3:
            game.perform(GrabTwoResource(grabbed_resources))
        return jsonify(success=True)

    return jsonify(success=False)


if __name__ == '__main__':
    app.run(debug=True)
