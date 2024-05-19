from dataclasses import astuple

from flask import Flask, render_template, request, jsonify, url_for

from Config import Config
from gui.get_building_name import get_building_name
from gui.perform_move import perform_move
from src.Game import Game
from src.entities.AllResources import AllResources
from src.entities.BasicResources import BasicResources
from src.moves import GrabThreeResource, GrabTwoResource

game = Game()
app = Flask(__name__, template_folder=Config.templates)


images = {}


@app.route('/')
def home():
    images.update({
        'image_path_0': url_for('static', filename=f'components/resource/red{game.players[-1].resources.red}.png'),
        'image_path_1': url_for('static', filename=f'components/resource/green{game.players[-1].resources.green}.png'),
        'image_path_2': url_for('static', filename=f'components/resource/blue{game.players[-1].resources.blue}.png'),
        'image_path_3': url_for('static', filename=f'components/resource/black{game.players[-1].resources.black}.png'),
        'image_path_4': url_for('static', filename=f'components/resource/white{game.players[-1].resources.white}.png'),
        'image_path_5': url_for('static', filename=f'components/resource/gold{game.players[-1].resources.gold}.png'),
        'image_path_6': url_for('static',
                                filename=f'components/aristocrats/{"".join(map(str, astuple(game.board.aristocrats[0].cost)))}.png'),
        'image_path_7': url_for('static',
                                filename=f'components/aristocrats/{"".join(map(str, astuple(game.board.aristocrats[1].cost)))}.png'),
        'image_path_8': url_for('static',
                                filename=f'components/aristocrats/{"".join(map(str, astuple(game.board.aristocrats[2].cost)))}.png'),
        'image_path_9': url_for('static',
                                filename=f'components/{get_building_name(game.board.tiers[2].visible[0])}.png'),
        'image_path_10': url_for('static',
                                 filename=f'components/{get_building_name(game.board.tiers[2].visible[1])}.png'),
        'image_path_11': url_for('static',
                                 filename=f'components/{get_building_name(game.board.tiers[2].visible[2])}.png'),
        'image_path_12': url_for('static',
                                 filename=f'components/{get_building_name(game.board.tiers[2].visible[3])}.png'),
        'image_path_13': url_for('static', filename='components/tier_3.png'),
        'image_path_14': url_for('static',
                                 filename=f'components/{get_building_name(game.board.tiers[1].visible[0])}.png'),
        'image_path_15': url_for('static',
                                 filename=f'components/{get_building_name(game.board.tiers[1].visible[1])}.png'),
        'image_path_16': url_for('static',
                                 filename=f'components/{get_building_name(game.board.tiers[1].visible[2])}.png'),
        'image_path_17': url_for('static',
                                 filename=f'components/{get_building_name(game.board.tiers[1].visible[3])}.png'),
        'image_path_18': url_for('static', filename='components/tier_2.png'),
        'image_path_19': url_for('static',
                                 filename=f'components/{get_building_name(game.board.tiers[0].visible[0])}.png'),
        'image_path_20': url_for('static',
                                 filename=f'components/{get_building_name(game.board.tiers[0].visible[1])}.png'),
        'image_path_21': url_for('static',
                                 filename=f'components/{get_building_name(game.board.tiers[0].visible[2])}.png'),
        'image_path_22': url_for('static',
                                 filename=f'components/{get_building_name(game.board.tiers[0].visible[3])}.png'),
        'image_path_23': url_for('static', filename='components/tier_1.png'),
        'image_path_24': url_for('static', filename=f'components/resource/red{game.board.resources.red}.png'),
        'image_path_25': url_for('static', filename=f'components/resource/green{game.board.resources.green}.png'),
        'image_path_26': url_for('static', filename=f'components/resource/blue{game.board.resources.blue}.png'),
        'image_path_27': url_for('static', filename=f'components/resource/black{game.board.resources.black}.png'),
        'image_path_28': url_for('static', filename=f'components/resource/white{game.board.resources.white}.png'),
        'image_path_29': url_for('static', filename=f'components/resource/gold{game.board.resources.gold}.png'),
        'image_path_30': url_for('static', filename=f'components/resource/red{game.current_player.resources.red}.png'),
        'image_path_31': url_for('static',
                                 filename=f'components/resource/green{game.current_player.resources.green}.png'),
        'image_path_32': url_for('static',
                                 filename=f'components/resource/blue{game.current_player.resources.blue}.png'),
        'image_path_33': url_for('static',
                                 filename=f'components/resource/black.{game.current_player.resources.black}png'),
        'image_path_34': url_for('static',
                                 filename=f'components/resource/white{game.current_player.resources.white}.png'),
        'image_path_35': url_for('static',
                                 filename=f'components/resource/gold{game.current_player.resources.gold}.png'),
        'image_path_36': url_for('static',
                                 filename=f'components/{get_building_name(game.current_player.reserve[0])}.png'),
        'image_path_37': url_for('static',
                                 filename=f'components/{get_building_name(game.current_player.reserve[1])}.png'),
        'image_path_38': url_for('static',
                                 filename=f'components/{get_building_name(game.current_player.reserve[2])}.png'),
        'points_current_player': game.current_player.points,
        'points_other_player': game.players[-1].points,
    })
    return render_template('new_index.html', **images)


image2build = {
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

image2reserve = {
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
    "image24": BasicResources(red=1),
    "image25": BasicResources(green=1),
    "image26": BasicResources(blue=1),
    "image27": BasicResources(black=1),
    "image28": BasicResources(white=1),
}
grabbed_resources = BasicResources()


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


if __name__ == '__main__':
    app.run(debug=True)
