import random
from flask import Flask, render_template, url_for
import csv
from collections import Counter
import os

app = Flask(__name__)

# TODO
"""
Hejka naklejka, wydaje mi się, że przygotowałam już z GUI to co trzeba, tam jeszcze chyba Patrycja robie ekran
startowy, aczkolwiek:

    > Jest ten ekran główny, który ma jeden board główny i dwie plaszne graczy - na dole dla naszego użytkownika
    a na górze dla AI (mam nadzieje ze jest tak okej, mozemy powiedziec ze w przyszlosci mozemy umozliwiwc multiplayer
    czy coś jesli się spodoba)
    
    > Są po lewej losowani arystokraci - nie ma do nich logiki ofc kiedy się zabiera arystokrate
    
    > Są karty - karty są na poczatku shufflowane i odkrywane sa 4 w każdym tierze, nie ma znowu logiki zabierania czy
    rezerwowania tych kart, ale jeśli kliknie się na kartę to pojawia się modal -> do you want to buy this card
    
    > Na rewersach widać poziom trudności i ile kart zostało z danego (again nie am logiki zabierania)
    
    > Coinsy - wydaje mi się że w grze na 2 osoby jest po 7 z każdego koloru oprócz złotego - nie pamiętam ile jego.
    Tu nie zrobiłam nic do tych coinsów oprócz tego że patrze ile ma jeden i drugi gracz i odejmuje (ale nie korzystam
    z twoich klas niestety wiec trzeba bedzie to pozmieniać). Nie ma jakiejś logiki zabierania
    
    > Co do paneli graczy to widać na nich różne rzeczy - ile kart z danego gatunku ma gracz, ile coinsów i ile 
    łącznie ma na razie punktów tylko trzeba to na twoje klasy pozmieniać
    
    > Karty zarezerwowane wyświetlam po lewej (trzeba te logike 3 max zaaplikowac), jak nacisniesz na karte z 
    rezerwacji (swoja nie SI) to sie zapyta czy chcesz kupić

Dodatkowe rzeczy to:

    > w folderze custom znajdziesz kilka fajnych modali które zrobiłam:
        * pusty (można cos dodac, czczionka to ten ITC coś tam - jest w custom-fonts.css
        * koniec tury 'end-turn'
        * start gry 'game-start'
        * przegrana 'loser'
        * wygrana 'winner'
        * powiadomienie o tym że można max 3 karty zarezerwować 'max-reserved'
        * 'next-turn' to początek tury
        * i dodatkowo modal od zadań specjalnych - zaokrglony prostokąt XD
        
        * teraz jak mysle przydalyby sie jeszcze dwa modale - jeden to jak ma sie max monet i trzeba albo 
        kupic albo wyienic 3 + jak nie moze sie kupic karty to tez by sie przydalo powiadomienie, daj mi znac to dorobie
        
          
GDZIE CO JEST MNIEJ WIECEJ:

    > png do monet w folderze 'chips' - kto by sie spodziewał
    > png do arystokratów w aristocrats
    > png do tła w background (wowowowowowo coooo)
    > png do kart w cards (i reversy w cards-rev)
    > fonty są w custom-fonts.css w folderze css
    > korzystałam z stylów w deafult_style.css
    > i jeden skrypcik script.js
    > a karty musiałąm do GUI skopiować bo kurde mi ich nie widział i nie chciało mi sie z tym meczyc wiec sa w 
    cards.csv
    
To tyle! Dobra, mam nadzieje ze jest w miare, spedzilam nad tym z 30 godzin przez te 2 dni kurła, layout nie jest 
najlepszy - mógłby pewnie być bardziej responsywny ale nie jestem królową css'a, starałam sie jak mogłam, jakby co 
to wyświetlimy u mnie bo się ładnie u mnie prezentuje <3 wgl jak ta apka sie odpala to mów Mac prawie odlatuje takze 

PZDR

Julia hehe  
"""

# Przykładowe rozłożenie TODO: trzeba to zastąpić tymi klasami
total_chips = {"black": 7, "white": 7, "green": 7, "blue": 7, "red": 7, "gold": 5}
player_chips = {"black": 2, "white": 1, "green": 0, "blue": 1, "red": 2, "gold": 1}
si_chips = {"black": 1, "white": 0, "green": 2, "blue": 3, "red": 1, "gold": 0}

card_1 = {"production": "red", "gain": 1}
card_2 = {"production": "blue", "gain": 0}
card_3 = {"production": "red", "gain": 1}
card_4 = {
    "production": "black",
    "gain": 3,
    "cost": {"green": 1, "blue": 0, "red": 3, "black": "1", "white": 1},
}
card_4a = {
    "production": "black",
    "gain": 3,
    "cost": {"green": 1, "blue": 0, "red": 0, "black": "1", "white": 1},
}
card_4b = {
    "production": "black",
    "gain": 3,
    "cost": {"green": 1, "blue": 0, "red": 3, "black": "1", "white": 1},
}
card_4c = {
    "production": "black",
    "gain": 2,
    "cost": {"green": 1, "blue": 0, "red": 3, "black": "1", "white": 1},
}
card_5 = {"production": "white", "gain": 0}
card_6 = {"production": "green", "gain": 0}
card_7 = {"production": "black", "gain": 2}

player_cards = [card_1, card_2, card_3, card_5, card_6, card_7]
player_cards_reserved = [card_4]
si_cards_reserved = [card_4b, card_4c, card_4a]
si_cards = [card_5, card_6, card_7]


def calculate_card_data(cards):
    card_count = Counter()
    total_points = 0

    for card in cards:
        card_count[card["production"]] += 1
        total_points += card["gain"]

    return card_count, total_points


def load_cards(filename):
    cards = {"1": [], "2": [], "3": []}
    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cards[row["tier"]].append(row)

    cards_count = {tier: len(cards[tier]) for tier in cards}

    for tier in cards:
        random.shuffle(cards[tier])
        cards[tier] = cards[tier][:4]
        cards_count[
            tier
        ] -= 4  # TODO: Tutaj trzeba bedzie jakas logike odejmowania tych kart, na razie odejmuje 4 bo tyle wykladam na poczatku

    return cards, cards_count


def calculate_chips_left(
        total_chips, player1_chips, player2_chips
):  # TODO: zastąpić prawdziwą logiką liczenia ile zostało coinsów
    chips_left = {}
    for color in total_chips:
        total = total_chips[color]
        player1 = player1_chips.get(color, 0)
        player2 = player2_chips.get(color, 0)
        left = total - player1 - player2
        chips_left[color] = left if left > 0 else 0  # Ensure non-negative count
    return chips_left


def select_aristocrats():
    aristocrats_folder = os.path.join(app.static_folder, "components/aristocrats")
    all_files = [f for f in os.listdir(aristocrats_folder) if f.endswith(".png")]
    selected_files = random.sample(all_files, 3)
    return [
        url_for("static", filename=f"components/aristocrats/{file}")
        for file in selected_files
    ]


@app.route("/")
def index():
    chips_left = calculate_chips_left(total_chips, player_chips, si_chips)
    player_card_count, player_total_points = calculate_card_data(player_cards)
    si_card_count, si_total_points = calculate_card_data(si_cards)
    cards, cards_left = load_cards("cards.csv")
    aristocrats_urls = select_aristocrats()
    return render_template(
        "index.html",
        cards=cards,
        cards_left=cards_left,
        chips_left=chips_left,
        player_cards=player_cards,
        player_card_count=player_card_count,
        player_total_points=player_total_points,
        player_chips=player_chips,
        si_card_count=si_card_count,
        si_total_points=si_total_points,
        si_chips=si_chips,
        si_cards_reserved=si_cards_reserved,
        player_cards_reserved=player_cards_reserved,
        aristocrats_urls=aristocrats_urls,
    )


if __name__ == "__main__":
    app.run(debug=True)
