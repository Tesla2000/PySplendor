import random
from flask import Flask, render_template
import csv

app = Flask(__name__)


def load_cards(filename):
    cards = {'1': [], '2': [], '3': []}
    with open(filename, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cards[row['tier']].append(row)

    # Shuffle and select first 4 cards for each tier
    for tier in cards:
        random.shuffle(cards[tier])
        cards[tier] = cards[tier][:4]

    return cards


@app.route('/')
def index():
    cards = load_cards('cards.csv')
    return render_template('index.html', cards=cards)


if __name__ == '__main__':
    app.run(debug=True)

