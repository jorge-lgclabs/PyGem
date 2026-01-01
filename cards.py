import random

from player import Player

level1_cards_db = {
    'w0b3g0r0n0': [1, 0, 'w', 1],
    'w0b0g0r2n1': [1, 0, 'w', 2],
    'w0b1g1r1n1': [1, 0, 'w', 1],
    'w0b2g0r0n2': [1, 0, 'w', 2],
    'w0b1g2r1n1': [1, 0, 'w', 1],
    'w0b2g2r0n1': [1, 0, 'w', 2],
    'w3b1g0r0n1': [1, 0, 'w', 1],
    'w0b0g4r0n0': [1, 1, 'w', 2],
    'w0b0g0r0n3': [1, 0, 'b', 1],
    'w1b0g0r0n2': [1, 0, 'b', 2],
    'w1b0g1r1n1': [1, 0, 'b', 1],
    'w0b0g2r0n2': [1, 0, 'b', 2],
    'w1b0g1r2n1': [1, 0, 'b', 1],
    'w1b0g2r2n0': [1, 0, 'b', 2],
    'w0b1g3r1n0': [1, 0, 'b', 1],
    'w0b0g0r4n0': [1, 1, 'b', 2],
    'w0b0g0r3n0': [1, 0, 'g', 1],
    'w2b1g0r0n0': [1, 0, 'g', 2],
    'w1b1g0r1n1': [1, 0, 'g', 1],
    'w0b2g0r2n0': [1, 0, 'g', 2],
    'w1b1g0r1n2': [1, 0, 'g', 1],
    'w0b1g0r2n2': [1, 0, 'g', 2],
    'w1b3g1r0n0': [1, 0, 'g', 1],
    'w0b0g0r0n4': [1, 1, 'g', 2],
    'w3b0g0r0n0': [1, 0, 'r', 1],
    'w0b2g1r0n0': [1, 0, 'r', 2],
    'w1b1g1r0n1': [1, 0, 'r', 1],
    'w2b0g0r2n0': [1, 0, 'r', 2],
    'w2b1g1r0n1': [1, 0, 'r', 1],
    'w2b0g1r0n2': [1, 0, 'r', 2],
    'w1b0g0r1n3': [1, 0, 'r', 1],
    'w4b0g0r0n0': [1, 1, 'r', 2],
    'w0b0g3r0n0': [1, 0, 'n', 1],
    'w0b0g2r1n0': [1, 0, 'n', 2],
    'w1b1g1r1n0': [1, 0, 'n', 1],
    'w2b0g2r0n0': [1, 0, 'n', 2],
    'w1b2g1r1n0': [1, 0, 'n', 1],
    'w2b2g0r1n0': [1, 0, 'n', 2],
    'w0b0g1r3n1': [1, 0, 'n', 1],
    'w0b4g0r0n0': [1, 1, 'n', 2]}

level2_cards_db = {
    'w0b0g0r5n0': [2, 2, 'w', 1],
    'w6b0g0r0n0': [2, 3, 'w', 2],
    'w0b0g3r2n2': [2, 1, 'w', 1],
    'w0b0g1r4n2': [2, 2, 'w', 2],
    'w2b3g0r3n0': [2, 1, 'w', 1],
    'w0b0g0r5n3': [2, 2, 'w', 2],
    'w0b5g0r0n0': [2, 2, 'b', 1],
    'w0b6g0r0n0': [2, 3, 'b', 2],
    'w0b2g2r3n0': [2, 1, 'b', 1],
    'w2b0g0r1n4': [2, 2, 'b', 2],
    'w5b3g0r0n0': [2, 2, 'b', 1],
    'w0b0g5r0n0': [2, 2, 'g', 2],
    'w0b0g6r0n0': [2, 3, 'g', 1],
    'w2b3g0r0n2': [2, 1, 'g', 2],
    'w3b0g2r2n0': [2, 1, 'g', 1],
    'w4b2g0r0n1': [2, 2, 'g', 1],
    'w0b5g3r0n0': [2, 2, 'g', 2],
    'w0b0g0r0n5': [2, 2, 'r', 1],
    'w0b0g0r6n0': [2, 3, 'r', 2],
    'w2b0g0r2n3': [2, 1, 'r', 1],
    'w1b4g2r0n0': [2, 2, 'r', 2],
    'w0b3g0r2n3': [2, 1, 'r', 1],
    'w3b0g0r0n5': [2, 2, 'r', 2],
    'w0b0g0r0n5': [2, 2, 'n', 1],
    'w0b0g0r0n6': [2, 3, 'n', 2],
    'w3b2g2r0n0': [2, 1, 'n', 1],
    'w0b1g4r2n0': [2, 2, 'n', 2],
    'w3b0g3r0n2': [2, 1, 'n', 1],
    'w0b0g5r3n0': [2, 2, 'n', 2]}

level3_cards_db = {
    'w0b0g0r0n7': [3, 4, 'w', 1],
    'w3b0g0r0n7': [3, 5, 'w', 2],
    'w3b0g0r3n6': [3, 4, 'w', 1],
    'w0b3g3r5n3': [3, 3, 'w', 2],
    'w7b0g0r0n0': [3, 4, 'b', 1],
    'w7b3g0r0n0': [3, 5, 'b', 2],
    'w6b3g0r0n3': [3, 4, 'b', 1],
    'w3b0g3r3n5': [3, 3, 'b', 2],
    'w0b7g0r0n0': [3, 4, 'g', 1],
    'w0b7g3r0n0': [3, 5, 'g', 2],
    'w3b6g3r0n0': [3, 4, 'g', 1],
    'w5b3g0r3n3': [3, 3, 'g', 2],
    'w0b0g7r0n0': [3, 4, 'r', 1],
    'w0b0g7r3n0': [3, 5, 'r', 2],
    'w0b3g6r3n0': [3, 4, 'r', 1],
    'w3b5g3r0n3': [3, 3, 'r', 2],
    'w0b0g0r7n0': [3, 4, 'n', 1],
    'w0b0g0r7n3': [3, 5, 'n', 2],
    'w0b0g3r6n3': [3, 4, 'n', 1],
    'w3b3g5r3n0': [3, 3, 'n', 2]}

nobles_db = [
    'w3b3g0r0n3',
    'w0b3g3r3n0',
    'w3b0g0r3n3',
    'w0b0g4r4n0',
    'w0b4g4r0n0',
    'w0b0g0r4n4',
    'w4b0g0r0n4',
    'w3b3g3r0n0',
    'w0b0g3r3n3',
    'w4b4g0r0n0']


class Card:
    """Models a game card, with attributes and methods for accessing them"""

    def __init__(self, cost, level, points, dado, bg_num):
        """
        Initializes the Card object with its level, cost, points, and dado (given)
        cost = in the format 'w3b1g0r0n1' w = white 3 = # of w
        w = white | b = blue | g = green | r = red | n = black (noir)
        level = 1, 2, or 3
        points = # of points given to player
        dado = which resource is given (dado) by this card, 'w'|'b'|'g'|'r'|'n'
        length = the total cost of the card irrespective of which resources
        visible = is this card currently visible (on the table), the default is False
        reserved = integer (1,2,3,4) of who has the card reserved, default is 0 (no one has the card reserved)
        owner = integer (1,2,3,4) of who owns the card, default is 0 (no one owns the card)
        reserved_by = integer (1,2,3,4) of who has the card reserved, default is 0 (no one has the card reserved)
        """
        self._cost = cost
        self._level = level
        self._points = points
        self._dado = dado
        self.bg_num = bg_num
        self._length = int(self._cost[1]) + int(self._cost[3]) + int(self._cost[5]) + int(self._cost[7]) + int(self._cost[9])
        self._visible = False
        self._owner = 0
        self._reserved_by = None

    def __str__(self):
        """How a card is printed, it's 'name' is just it's cost"""
        return self._cost

    def __repr__(self):
        """How a card is represented in a list, to show its name instead of Card object"""
        return self._cost

    def get_cost(self) -> str:
        """Returns the cost of the card"""
        return self._cost

    def get_level(self) -> int:
        """Returns the level of the card"""
        return self._level

    def get_points(self) -> int:
        """Returns the points awarded by the card"""
        return self._points

    def get_dado(self) -> str:
        """Returns the resource given (dado) by the card"""
        return self._dado

    def get_length(self) -> int:
        """Returns the length (total # of resources of any kind) of the cost of the card"""
        return self._length

    def is_visible(self):
        """Returns whether the card is visible"""
        return self._visible

    def get_owner(self):
        """Returns the Player object who owns the Card or None"""
        return self._owner

    def get_reserved_by(self):
        """Returns the player (1,2,3,4) who has the Card reserved (0 for none)"""
        return self._reserved_by

    def set_visible(self, visible: bool):
        """Sets visible to True or False"""
        self._visible = visible

    def set_owner(self, owner: Player):
        """Receives the number of a player (1,2,3,4) and sets owner to that player"""
        self._owner = owner

    def set_reserved_by(self, reserved_by: int):
        """Receives the number of a player (1,2,3,4) and sets reserved_by to that player"""
        self._reserved_by = reserved_by

    def can_afford(self, tender: tuple) -> bool:
        """
        Returns True if the tender (player total + gold) is enough to afford Card, otherwise False

        Param tender: a tuple containing:
                        [0] = a string in 'w2b1g3r0n0' form representing the total resources (bank+dado) of the Player asking if they can buy the card
                        [1] = an integer representing the number of gold the Player has

        Return: True if the Player can afford to buy the card, False if they cannot
        """
        player_total, player_gold = tender
        index = 1
        # if ever the amount of a resource in the player's tender is less than the cost and less than the gold they have, return False
        while index <= 9:
            difference = int(self._cost[index]) - int(player_total[index])
            if difference > 0:
                player_gold -= difference
                if player_gold < 0:
                    return False
            index += 2
        return True

def create_cards(db: dict) -> list:
    """
    Receives a dict in card_db format and returns a list of Card objects with those values

    Param db: a database in dict format with the following structure: 'cost' : [level, points, dado]

    Return: list of Card objects in random (shuffled) order
    """
    result_list = []

    for key in db:
        cost = key
        level = db[key][0]
        points = db[key][1]
        dado = db[key][2]
        bg_num = db[key][3]

        result_list.append(Card(cost, level, points, dado, bg_num))

    random.shuffle(result_list)

    return result_list

def create_nobles(db_list: list, players: int) -> list:
    """Receives a list of costs (of each Nobles tile) and the number of players,returns a list of the respective number of Nobles objects"""
    random_nobles = random.sample(db_list, players+1)
    random_nobles = [Card(noble, 4, 3, 'x', 1) for noble in random_nobles]
    for card in random_nobles:
        card.set_visible(True)

    return random_nobles

def get_nobles(num_players: int) -> list:
    """Receives the number of players and returns a list of the respective number of Nobles tiles"""
    nobles_tiles = create_nobles(nobles_db, num_players)

    return nobles_tiles

def get_cards() -> tuple:
    """Initializes all the cards and returns them in a list"""
    level_1_deck = create_cards(level1_cards_db)
    level_2_deck = create_cards(level2_cards_db)
    level_3_deck = create_cards(level3_cards_db)

    return level_1_deck, level_2_deck, level_3_deck


