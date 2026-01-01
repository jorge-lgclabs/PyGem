
class GameBankException(Exception):
    """Exceptions pertaining to the GameBank (game tokens)"""
    pass

class GameBank:
    """Models the bank of resources (tokens) that the players take from"""
    def __init__(self, players: int):
        """Initializes the values of the bank according to how many players there are"""
        self._bank_balance = 'w0b0g0r0n0'
        self._gold = 5
        self._token_limit = [4,5,7][players-2]
        for color in ['white', 'blue', 'green', 'red', 'noir']:
            for token in range(self._token_limit):
                self.deposit(color)

    def get_token_num(self, color: str) -> int:
        """Receives the name of a color ('white', 'blue', 'green', 'red', 'noir', 'gold') and returns the amount of that resource in the GameBank"""
        if color == 'gold':
            return self._gold
        return int(self._bank_balance[{'white':1,'blue':3,'green':5,'red':7,'noir':9}[color]])

    def get_available_tokens(self):
        """Returns a sublist of color strings, representing the available tokens (not zero)"""
        return [color for color in ['white', 'blue', 'green', 'red', 'noir'] if (self.get_token_num(color) > 0)]

    def mutate_balance(self, color: str, modifier: int) -> str:
        """
        Receives a string of a color and either 1 or -1
        then modifies the balance by either incrementing or decrementing that resource
        """
        target_index = {'white':1,'blue':3,'green':5,'red':7,'noir':9}[color]
        new_balance = str()
        for index in range(10):
            char = self._bank_balance[index]
            if index == target_index:
                char = str(int(char) + modifier)
            new_balance += char

        return new_balance

    def deposit(self, color: str):
        """Receives the name of a color and increments that resource (returns token to pile)"""
        # if somehow too much gold is attempting to be deposited, raise an exception
        if color == 'gold':
            if self._gold + 1 > 5:
                raise GameBankException
            else:
                self._gold += 1
                return
        # if somehow too much of any other resource is attempting to be deposited, raise an exception
        if self.get_token_num(color) + 1 > self._token_limit:
            raise GameBankException
        # otherwise, increment resource
        self._bank_balance = self.mutate_balance(color, 1)

    def withdraw(self, color: str):
        """Receives the name of a color and decrements that resource (takes from the pile)"""
        # if somehow a resource is attempting to be withdrawn when there is 0, raise an exception
        if self.get_token_num(color) == 0:
            raise GameBankException
        # otherwise, decrement resource
        if color == 'gold':
            self._gold -= 1
            return
        self._bank_balance = self.mutate_balance(color, -1)



# testbank = GameBank(3)
# print(testbank._bank_balance)
#
# print(testbank.get_available_tokens())
#
# testbank.withdraw('red')
# testbank.withdraw('red')
# testbank.withdraw('red')
# testbank.withdraw('red')
# testbank.withdraw('red')
#
#
#
# print(testbank._bank_balance)
#
# print(testbank.get_available_tokens())
