from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)


class Card:
    suits = ['Soldier', 'Noble', 'Warrior', 'Siege Engine']
    values = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
    factions = ['Ironclad Legion', 'Shadowblade Syndicate', 'Stormforge Alliance', 'Eclipse Dominion']

    faction_powers = {
        'Ironclad Legion': 'Fortitude: Reduces damage taken by 20%',
        'Shadowblade Syndicate': 'Stealth: Increases evasion by 25%',
        'Stormforge Alliance': 'Elemental Fury: Adds 15% to attack power',
        'Eclipse Dominion': 'Arcane Might: Increases spell power by 20%'
    }

    suit_powers = {
        'Soldier': 'Tactical Advantage: Increases attack power by 10%',
        'Noble': 'Commanding Presence: Increases effectiveness of adjacent cards by 10%',
        'Warrior': 'Battle Hardened: Reduces damage taken by 10%',
        'Siege Engine': 'Destructive Force: Ignores 15% of enemy defense'
    }

    value_powers = {
        '1': 'Weak Strike: Basic attack, minimal impact',
        '2': 'Quick Jab: Slightly higher impact than 1',
        '3': 'Steady Blow: Average impact',
        '4': 'Guarded Strike: Attack with slight defense boost',
        '5': 'Focused Attack: Increased accuracy',
        '6': 'Double Strike: Two quick attacks with reduced damage',
        '7': 'Heavy Hit: Higher damage',
        '8': 'Fortified Assault: Moderate defense boost',
        '9': 'Precision Strike: High accuracy, critical hit chance',
        '10': 'Brutal Blow: Very high damage',
        '11': 'Unyielding Force: High damage with slight defense boost',
        '12': 'Savage Assault: Ignores some enemy defense',
        '13': 'Ultimate Strike: Maximum damage with added effects'
    }

    base_health_values = {
        '1': 10, '2': 15, '3': 20, '4': 25, '5': 30, '6': 35, '7': 40,
        '8': 45, '9': 50, '10': 55, '11': 60, '12': 65, '13': 70
    }

    base_attack_values = {
        '1': 5, '2': 10, '3': 15, '4': 20, '5': 25, '6': 30, '7': 35,
        '8': 40, '9': 45, '10': 50, '11': 55, '12': 60, '13': 70
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
        return f"{self.value} of {self.suit} ({self.faction}, Power: {self.power}, Health: {self.health}, Attack: {self.attack})"

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

    def select_cards(self, player_hand):
        print(f"Your hand: {player_hand}")
        selected_cards = []
        while len(selected_cards) < 3:
            try:
                choice = int(input(f"Select card {len(selected_cards)+1} by index (0 to {len(player_hand)-1}): "))
                if choice < 0 or choice >= len(player_hand):
                    print("Invalid index. Try again.")
                else:
                    selected_cards.append(player_hand.pop(choice))
            except ValueError:
                print("Invalid input. Please enter a number.")
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

    def play_game(self):
        self.deal_cards()

        print("\nPlayer 1's turn to select cards:")
        self.player1_field = self.select_cards(self.player1_hand)

        print("\nPlayer 2's turn to select cards:")
        self.player2_field = self.select_cards(self.player2_hand)

        print("\nPlayer 1 Field:")
        for card in self.player1_field:
            print(f"{card} - {card.get_faction_power()}, {card.get_suit_power()}, {card.get_value_power()}")

        print("\nPlayer 2 Field:")
        for card in self.player2_field:
            print(f"{card} - {card.get_faction_power()}, {card.get_suit_power()}, {card.get_value_power()}")

        # Players take turns attacking each other's cards
        for turn in range(3):
            attacker = self.player1_field[turn]
            defender = self.player2_field[turn]

            damage, defeated = self.combat(attacker, defender)
            print(f"Player 1's {attacker} attacks Player 2's {defender} and deals {damage:.2f} damage.")
            if defeated:
                print(f"Player 2's {defender} is defeated!")

            attacker = self.player2_field[turn]
            defender = self.player1_field[turn]

            damage, defeated = self.combat(attacker, defender)
            print(f"Player 2's {attacker} attacks Player 1's {defender} and deals {damage:.2f} damage.")
            if defeated:
                print(f"Player 1's {defender} is defeated!")

        player1_defeated = sum(1 for card in self.player1_field if card.health <= 0)
        player2_defeated = sum(1 for card in self.player2_field if card.health <= 0)

        if player1_defeated > player2_defeated:
            print("Player 2 wins the game!")
        elif player2_defeated > player1_defeated:
            print("Player 1 wins the game!")
        else:
            print("The game is a tie!")

# Start the game
if __name__ == "__main__":
    game = WarGame()
    game.play_game()
