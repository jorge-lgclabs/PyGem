class PlayerException(Exception):
    """Exceptions pertaining to the Player"""
    pass

class Player:
    """
    Models the player, who possesses the following:
    a bank: the tokens they have, a string in the format 'w3b1g0r1n0'
    dado: permanent resources gained by purchasing cards, a string in the format 'w3b1g0r1n0'
    gold: how many gold tokens they have, an integer
    hand: the cards the player has purchased, a list with Card objects
    reserved: the cards the player has reserved, a list with Card objects
    """
    def __init__(self, player_name: str, player_number: int):
        """Initializes the names and values of the player's resources"""
        self._player_name = player_name
        self._player_number = player_number
        self._player_bank = 'w0b0g0r0n0'
        self._player_dado = 'w0b0g0r0n0'
        self._gold = 0
        self._hand = []
        self._reserved = []
        self.points = 0

    def bank_lookup(self, color):
        """Receives a string of a color and returns the location of that bank resource"""
        bank_lookup = {'white': self._player_bank[1],
                       'blue': self._player_bank[3],
                       'green': self._player_bank[5],
                       'red': self._player_bank[7],
                       'noir': self._player_bank[9],
                       'gold': self._gold
                       }
        return bank_lookup[color]

    def dado_lookup(self, color):
        """Receives a string of a color and returns the location of that bank resource"""
        dado_lookup = {'white': self._player_dado[1],
                       'blue': self._player_dado[3],
                       'green': self._player_dado[5],
                       'red': self._player_dado[7],
                       'noir': self._player_dado[9]
                       }
        return dado_lookup[color]

    def get_player_name(self) -> str:
        """Returns a string of the Player's name"""
        return self._player_name

    def get_player_number(self) -> int:
        """Returns the Player's number"""
        return self._player_number

    def get_player_bank(self) -> str:
        """Returns a string of the player's bank (tokens) in 'w3b1g0r1n0' format"""
        return self._player_bank

    def get_player_dado(self) -> str:
        """Returns a string of the player's dado (permanent resources/discount) in 'w3b1g0r1n0' format"""
        return self._player_dado

    def get_player_hand(self):
        """Returns a list of Card objects (the cards the player has purchased)"""
        return self._hand

    def get_player_reserved(self):
        """Returns a list of Card objects (the cards the player has reserved)"""
        return self._reserved

    def get_player_tender(self) -> tuple:
        """Returns a tuple containing the player's bank in 'w3b1g0r1n0' format including all dado (their total tender), and an integer of how many gold they have"""
        player_total = str()
        for color in ['white', 'blue', 'green', 'red', 'noir']:
            player_total += color[0] + str(int(self.bank_lookup(color)) + int(self.dado_lookup(color)))
        return player_total, self._gold

    def get_player_bank_length(self) -> int:
        """Returns the total number of tokens the player has"""
        result = 0
        for index in [1,3,5,7,9]:
            result += int(self._player_bank[index])
        return result

    def mutate_balance(self, balance: str, color: str, modifier: int) -> str:
        """
        Receives a string balance in the 'w3b1g0r1n0' format, a string of a color and either 1 or -1
        then modifies the balance by either incrementing or decrementing that resource
        """
        target_index = {'white':1,'blue':3,'green':5,'red':7,'noir':9}[color]
        new_balance = str()
        for index in range(10):
            char = balance[index]
            if index == target_index:
                char = str(int(char) + modifier)
            new_balance += char

        return new_balance

    def deposit_bank(self, color):
        """Receives the name of a color and increments that resource in the player's bank (player receives token)"""
        if color == 'gold':
            self._gold += 1
            return

        self._player_bank = self.mutate_balance(self._player_bank, color, 1)

    def deposit_dado(self, color):
        """Receives the name of a color and increments that resource in the player's dado (player buys card with dado)"""
        self._player_dado = self.mutate_balance(self._player_dado, color, 1)

    def withdraw(self, color):
        """Receives the name of a color and decrements that resource from player bank (player puts token back onto pile)"""
        if color == 'gold':
            self._gold -= 1
            return

        self._player_bank = self.mutate_balance(self._player_bank, color, -1)

    def add_to_hand(self, incoming_card: object):
        """Receives a Card object and adds it to hand"""
        self._hand.append(incoming_card)

    def add_to_reserved(self, incoming_card: object):
        """receives a Card object and add its to reserved"""
        self._reserved.append(incoming_card)

    def remove_from_reserved(self, outgoing_card: object):
        """Receives a Card object and removes it from reserve (if it exists)"""
        if outgoing_card in self._reserved:
            self._reserved.remove(outgoing_card)


    def show_status(self):
        """Prints out the players 'status' which is their hand (what cards they own) their reserved cards, their nobles, what tokens and dado they have and their point score"""
        print('\n')
        print((f'Player {self._player_number} - {self._player_name}'),
              (f'\nCards owned (including Nobles earned): {self._hand}'),
              (f'\nCards reserved: {self._reserved}'),
              (f'\nWhite - tokens: {self.bank_lookup('white')} - dado: {self.dado_lookup('white')}'),
              (f'\nBlue - tokens: {self.bank_lookup('blue')} - dado: {self.dado_lookup('blue')}'),
              (f'\nGreen - tokens: {self.bank_lookup('green')} - dado: {self.dado_lookup('green')}'),
              (f'\nRed - tokens: {self.bank_lookup('red')} - dado: {self.dado_lookup('red')}'),
              (f'\nNoir - tokens: {self.bank_lookup('noir')} - dado: {self.dado_lookup('noir')}'),
              (f'\nGold: {self._gold}'),
              (f'\nPoints: {self.points}'))
        input('Press enter to continue')