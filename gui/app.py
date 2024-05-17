from flask import Flask, render_template, request, jsonify, url_for

from Config import Config
from src.Game import Game

game = Game()
app = Flask(__name__, template_folder=Config.templates)


@app.route('/')
def home():
    image_path_0 = url_for('static', filename='components/tier_2.png')
    return render_template('new_index.html', image_path_0=image_path_0)


@app.route('/click', methods=['POST'])
def click():
    data = request.json
    image_class = data.get('class')
    # Process the data as needed
    print(f"Clicked image class: {image_class}")
    return jsonify(success=True)


if __name__ == '__main__':
    app.run(debug=True)
