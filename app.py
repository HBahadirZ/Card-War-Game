from flask import Flask, render_template, request
import random

app = Flask(__name__)


class Card:
    suits = ['Soldier', 'Noble', 'Warrior', 'Siege Engine']
    values = [
        'Apprentice', 'Squire', 'Footman', 'Sentinel', 'Knight', 'Captain',
        'Champion', 'Warlord', 'General', 'Hero', 'Vanguard', 'Conqueror',
        'Legend'
    ]
    factions = [
        'Ironclad Legion', 'Shadowblade Syndicate', 'Stormforge Alliance',
        'Eclipse Dominion'
    ]

    faction_powers = {
        'Ironclad Legion': 'Fortitude: Reduces damage taken by 20%',
        'Shadowblade Syndicate': 'Stealth: Increases evasion by 25%',
        'Stormforge Alliance': 'Elemental Fury: Adds 15% to attack power',
        'Eclipse Dominion': 'Arcane Might: Increases spell power by 20%'
    }

    suit_powers = {
        'Soldier Class': 'Tactical Advantage: Increases attack power by 10%',
        'Noble Class':
        'Commanding Presence: Increases effectiveness of adjacent cards by 10%',
        'Warrior Class': 'Battle Hardened: Reduces damage taken by 10%',
        'Siege Engine Class': 'Destructive Force: Ignores 15% of enemy defense'
    }

    value_powers = {
        'Apprentice': 'Weak Strike: Basic attack, minimal impact',
        'Squire': 'Quick Jab: Slightly higher impact than 1',
        'Footman': 'Steady Blow: Average impact',
        'Sentinel': 'Guarded Strike: Attack with slight defense boost',
        'Knight': 'Focused Attack: Increased accuracy',
        'Captain': 'Double Strike: Two quick attacks with reduced damage',
        'Champion': 'Heavy Hit: Higher damage',
        'Warlord': 'Fortified Assault: Moderate defense boost',
        'General': 'Precision Strike: High accuracy, critical hit chance',
        'Hero': 'Brutal Blow: Very high damage',
        'Vanguard': 'Unyielding Force: High damage with slight defense boost',
        'Conqueror': 'Savage Assault: Ignores some enemy defense',
        'Legend': 'Ultimate Strike: Maximum damage with added effects'
    }

    base_health_values = {
        'Apprentice': 10,
        'Squire': 15,
        'Footman': 20,
        'Sentinel': 25,
        'Knight': 30,
        'Captain': 35,
        'Champion': 40,
        'Warlord': 45,
        'General': 50,
        'Hero': 55,
        'Vanguard': 60,
        'Conqueror': 65,
        'Legend': 70
    }

    base_attack_values = {
        'Apprentice': 5,
        'Squire': 10,
        'Footman': 15,
        'Sentinel': 20,
        'Knight': 25,
        'Captain': 30,
        'Champion': 35,
        'Warlord': 40,
        'General': 45,
        'Hero': 50,
        'Vanguard': 55,
        'Conqueror': 60,
        'Legend': 70
    }

    def __init__(self, suit, value, power, faction):
        self.suit = suit
        self.value = value
        self.power = power
        self.faction = faction
        self.health = self.calculate_health()
        self.attack = self.calculate_attack()

    def get_faction_power(self):
        return Card.faction_powers[self.faction]

    def get_suit_power(self):
        return Card.suit_powers[self.suit]

    def get_value_power(self):
        return Card.value_powers[self.value]

    def calculate_health(self):
        base_health = Card.base_health_values[self.value]
        if self.faction == 'Ironclad Legion':
            return base_health * 1.5
        else:
            return base_health

    def calculate_attack(self):
        base_attack = Card.base_attack_values[self.value]
        attack_multiplier = 1.0

        if self.faction == 'Stormforge Alliance':
            attack_multiplier *= 1.15
        elif self.faction == 'Eclipse Dominion':
            base_attack += 10

        if self.suit == 'Soldier':
            attack_multiplier *= 1.1
        elif self.suit == 'Noble':
            base_attack += 5
        elif self.suit == 'Siege Engine':
            # We'll handle this special case in combat calculation
            pass

        return base_attack * attack_multiplier

    def __repr__(self):
        return (
            f"{self.value} of {self.suit} ({self.faction}) - "
            f"Power: {self.power}, Health: {self.health:.2f}, Attack: {self.attack:.2f}\n"
            f"Faction Power: {self.get_faction_power()}, Suit Power: {self.get_suit_power()}, Value Power: {self.get_value_power()}"
        )


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

    def combat(self, attacker, defender):
        attack_value = attacker.attack
        defense_multiplier = 1.0

        if defender.suit == 'Warrior':
            defense_multiplier = 0.9
        elif attacker.suit == 'Siege Engine':
            # Ignore 15% of the defender's defense
            defense_multiplier *= 0.85

        damage_dealt = attack_value * defense_multiplier

        defender.health -= damage_dealt
        return damage_dealt, defender.health <= 0  # Return damage dealt and whether the defender is defeated


@app.route('/')
def index():
    game = WarGame()
    game.deal_cards()
    return render_template('index.html',
                           player1_hand=game.player1_hand,
                           player2_hand=game.player2_hand)


@app.route('/play', methods=['POST'])
def play():
    game = WarGame()
    player1_choices = [int(i) for i in request.form.getlist('player1_choices')]
    player2_choices = [int(i) for i in request.form.getlist('player2_choices')]
    game.player1_field = game.select_cards(game.player1_hand, player1_choices)
    game.player2_field = game.select_cards(game.player2_hand, player2_choices)

    results = []
    for turn in range(3):
        attacker1, defender1 = game.player1_field[turn], game.player2_field[
            turn]
        damage1, defeated1 = game.combat(attacker1, defender1)
        results.append((attacker1, defender1, damage1, defeated1))

        attacker2, defender2 = game.player2_field[turn], game.player1_field[
            turn]
        damage2, defeated2 = game.combat(attacker2, defender2)
        results.append((attacker2, defender2, damage2, defeated2))

    return render_template('result.html',
                           results=results,
                           player1_field=game.player1_field,
                           player2_field=game.player2_field)


if __name__ == '__main__':
    app.run(debug=True)
