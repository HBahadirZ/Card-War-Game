from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)


class Card:
    suits = ['Soldier', 'Noble', 'Warrior', 'Siege Engine']
    values = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'
    ]
    factions = [
        'Ironclad Legion', 'Shadowblade Syndicate', 'Stormforge Alliance',
        'Eclipse Dominion'
    ]

    def __init__(self, suit, value, power, faction):
        self.suit = suit
        self.value = value
        self.power = power
        self.faction = faction

    def __repr__(self):
        return f"{self.value} of {self.suit} ({self.faction}, Power: {self.power})"


class Deck:

    def __init__(self):
        self.cards = self.create_deck()
        random.shuffle(self.cards)

    def create_deck(self):
        deck = []
        for suit in Card.suits:
            for value in Card.values:
                power = random.randint(
                    1, 10)  # Assign a random power value between 1 and 10
                faction = random.choice(
                    Card.factions)  # Assign a random faction
                deck.append(Card(suit, value, power, faction))
        return deck

    def deal(self):
        return self.cards.pop() if self.cards else None


class WarGame:

    def __init__(self):
        self.deck = Deck()
        self.player1_hand = []
        self.player2_hand = []
        self.player1_field = []
        self.player2_field = []

    def deal_cards(self):
        for _ in range(10):
            self.player1_hand.append(self.deck.deal())
            self.player2_hand.append(self.deck.deal())

    def select_cards(self, player_hand, choices):
        selected_cards = [player_hand.pop(choice) for choice in choices]
        return selected_cards

    def calculate_power(self, field):
        total_power = 0
        faction_streak = 0
        current_faction = None

        for card in field:
            if card.faction == current_faction:
                faction_streak += 1
            else:
                faction_streak = 1
                current_faction = card.faction

            multiplier = 1 + 0.1 * (faction_streak - 1)
            total_power += card.power * multiplier

        return total_power

    def play_round(self, player1_choices, player2_choices):
        self.player1_field = self.select_cards(self.player1_hand,
                                               player1_choices)
        self.player2_field = self.select_cards(self.player2_hand,
                                               player2_choices)

        player1_power = self.calculate_power(self.player1_field)
        player2_power = self.calculate_power(self.player2_field)

        result = {
            'player1_power':
            player1_power,
            'player2_power':
            player2_power,
            'winner':
            'Player 1' if player1_power > player2_power else
            'Player 2' if player1_power < player2_power else 'Tie',
            'player1_field':
            self.player1_field,
            'player2_field':
            self.player2_field
        }
        return result


game = WarGame()
game.deal_cards()


@app.route('/')
def index():
    return render_template('index.html',
                           player1_hand=game.player1_hand,
                           player2_hand=game.player2_hand)


@app.route('/play', methods=['POST'])
def play():
    player1_choices = [int(i) for i in request.form.getlist('player1_choices')]
    player2_choices = [int(i) for i in request.form.getlist('player2_choices')]
    result = game.play_round(player1_choices, player2_choices)
    return render_template('result.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
