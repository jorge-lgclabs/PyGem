import cards
import bank
import json
import copy
from tkinter import simpledialog, messagebox


from player import Player

COLORS = ['white', 'blue', 'green', 'red', 'noir']

class GameMasterError(Exception):
    """If something goes wrong"""
    pass

class GameMaster:
    """
    The object which creates, controls and ends the game.
    """
    def __init__(self, player_names: list):
        """Initializes the game and its data"""
        self._num_players = len(player_names)
        self._players = []

        for index, name in enumerate(player_names):
            self._players.append(Player(name, index+1))

        self._current_player = self._players[0]
        self._level_1_deck, self._level_2_deck, self._level_3_deck = cards.get_cards()
        self._nobles_deck = cards.get_nobles(self._num_players)
        self._bank = bank.GameBank(self._num_players)
        self._deck_pointer_1 = self._deck_pointer_2 = self._deck_pointer_3 = 4  # starts at the first face-down card at the top of deck after making 4 visible
        self._turn = 1
        self._log = []
        self.initialize_visible_cards()

    def prompt_user(self, message: str, required_type: str, int_range=None):
        """
        Receives a string message and the string ('int'|'color'|'color2'|'action'|'yesno'|'card') and an optional tuple of two ints
        prints message and prompts user for input, checks user input against required_type and prompts again if wrong type
        'int' = answer requires a number
        'color' = answer requires one of the 5 resource colors (ie not Gold)
        'color2' = answer requires any of the 6 token colors, including Gold
        'action' = answer requires one of 3 actions ['buy','reserve','tokens']
        'yesno' = answer requires yes or no in the format of string 'y' or 'n'
        'card' = answer requires a string in the 'w3b1g0r1n0' format

        param message: a string which explains to the user what is required
        param required_type: a string representing what are the valid forms of response (see above)
        param int_range: optional, only if required_type is int, a tuple of two integers representing the range required, exclusive

        return: the user's response once they enter a valid response
        """


        user_input = input(message)

        if user_input == 'back':
            return 'back'
        if required_type == 'int':
            try:
                user_input = int(user_input) + 1
                user_input -= 1
                if user_input not in range(int_range[0], int_range[1]):
                    print("The number must be be between",int_range[0], "and", int_range[1]-1, "please try again")
                    return self.prompt_user(message, required_type, int_range)
            except ValueError:
                print("You must enter a number, please try again")
                return self.prompt_user(message, required_type, int_range)
            return user_input
        elif required_type == 'color':
            if user_input not in ['white', 'blue', 'green', 'red', 'noir']:
                print("You must enter a color (white, blue, green, red, or noir), please try again")
                return self.prompt_user(message, required_type)
            return user_input
        elif required_type == 'color2':
            if user_input not in ['white', 'blue', 'green', 'red', 'noir', 'gold']:
                print("You must enter a color (white, blue, green, red, noir, or gold), please try again")
                return self.prompt_user(message, required_type)
            return user_input
        elif required_type == 'action':
            if user_input not in ['buy', 'reserve', 'tokens','status']:
                print("You must enter an action: 'buy' a card, 'reserve' a card, or take 'tokens', please try again")
                return self.prompt_user(message, required_type)
            return user_input
        elif required_type == 'yesno':
            if user_input not in ['y', 'n']:
                print("You must enter y (yes) or n (no), please try again")
                return self.prompt_user(message, required_type)
            return user_input
        elif required_type == 'card':
            for index, char in enumerate(['w',0,'b',0,'g',0,'r',0,'n',0]):
                if type(char) == str:
                    if char != user_input[index]:
                        print("You must enter a card in 'w0b0g0r0n0' format, please try again")
                        return self.prompt_user(message, required_type)
                if char == 0 and int(user_input[index]) not in range(0,8):
                    print("You must enter a card in 'w0b0g0r0n0' format, please try again")
                    return self.prompt_user(message, required_type)
            return user_input
        else:
            raise GameMasterError

    def take_an_action(self, player: Player, action: str):
        if action == 'buy':
            print("start the buy card action")
            self.buy_card(player)
        elif action == 'reserve':
            print("start the reserve card action")
            self.reserve_card(player)
        elif action == 'status':
            self.get_current_player().show_status()
        elif action == 'back':
            return
        else:
            print("start the token taking action")
            self.take_tokens(player)

    def end_turn(self, message: str):
        """Called by every of the available actions (take_tokens, buy_card, reserve_card) at the end of their execution, receives a message describing the action which just took place"""
        # Construct the full log line and add it to the log
        log_line = "Turn " + str(self._turn) + ": Player " + str(self.get_current_player().get_player_number()) + " " + self.get_current_player().get_player_name() + " took the following action: " + message
        print(log_line)
        self._log.append(log_line)

        # Check if any nobles have been earned
        for noble in self._nobles_deck:
            if noble.can_afford((self.get_current_player().get_player_dado(), 0)):
                # the player who just took their turn has now earned a noble tile
                # mechanism representing the player taking the noble tile from the table and earning its points
                self.get_current_player().add_to_hand(noble)
                self.get_current_player().points += noble.get_points()
                self._nobles_deck.remove(noble)

        # check if Player has now won
        if self.get_current_player().points >= 15:
            input(f'{self.get_current_player().get_player_name()} has won the game! Press enter for log')
            for line in self._log:
                print(line)
            return

        self.change_to_next_player()
        self._turn += 1


    def take_tokens(self, player=None):
        """Method representing the in-game action of a player taking tokens. In Splendor a player can either take a single gem of 3 different kinds, or 2 of a single kind, barring there are less than 3 total of that kind"""
        if player is None:  # for the sake of the GUI implementation can call without getting current player
            player = self.get_current_player()
        def commit_tokens():
            """Internal helper function to execute once the turn has been committed to"""
            # if the code has reached this point, every token action is valid so it can be committed to
            for color in taken:
                self._bank.withdraw(color)  # withdraw from the real bank this time
                player.deposit_bank(color)  # deposit the real tokens into the real players bank

            self.end_turn(("took tokens " + str(taken)))

            return True

        take = 0  # how many tokens the player has taken
        taken = [] # a list of the color taken at each take

        # For this action, we will first have the player take the actions against a simulacra of the current bank,
        # only committing to taking the actions on the real bank once the whole move has been confirmed. This gives the player
        # the opportunity to back out of any token taking actions they don't want to commit to

        fake_bank = copy.deepcopy(self._bank)

        # The first token taking action: the only restriction is what is available
        while take == 0:
            first_take = self.prompt_user(("Which gem would you like to take " + str(fake_bank.get_available_tokens()) + "? (or 'back' to start turn again): "), 'color')
            if first_take == 'back':
                return 'back'
            if first_take not in fake_bank.get_available_tokens():
                print(f"There are no", first_take, "available, please try again.")
                continue
            else:
                take += 1

        # The mechanism representing taking a token from the bank, but in this case not on the real bank yet
        fake_bank.withdraw(first_take)
        taken.append(first_take)

        # the second token taking action: restricted to only those that are available and only those that have more than 1 if it is first_take
        available_colors = fake_bank.get_available_tokens()
        if first_take in available_colors:
            if fake_bank.get_token_num(first_take) < 2:
                available_colors.remove(first_take)

        while take == 1:
            second_take = self.prompt_user(("Which gem would you like to take " + str(available_colors) + "?: (or 'back' to start turn again): "), 'color')
            if second_take == 'back':
                return 'back'
            if second_take not in available_colors:
                print("That is not an available color, please try again.")
                continue
            else:
                take += 1

        # Once again, the mechanism of the player taking that token from the bank, but against the fake bank (at first)
        fake_bank.withdraw(second_take)
        taken.append(second_take)

        # the third token taking action: only happens if the player hasn't already taken 2 of the same color, restricted to only those that haven't already been taken
        if taken[0] == taken[1]:
            if commit_tokens() is True: # jumps to committing the move
                return
        else:
            available_colors = fake_bank.get_available_tokens()
            for color in taken:
                if color in available_colors:
                    available_colors.remove(color)

        while take == 2:
            third_take = self.prompt_user(("Which gem would you like to take " + str(available_colors) + "?: (or 'back' to start turn again): "), 'color')
            if third_take == 'back':
                return 'back'
            if third_take not in available_colors:
                print("That is not an available color, please try again.")
                continue
            else:
                take += 1

            # The third and final mechanism of the third token being taken from the fake bank
            fake_bank.withdraw(third_take)
            taken.append(third_take)
            if commit_tokens() is True: # jumps to committing the move
                return

    def initialize_visible_cards(self):
        """Starts the mechanism which maintains the visible cards (those that are on the table and in play)"""
        for deck in [self._level_1_deck, self._level_2_deck, self._level_3_deck]:
            for index in range(4):
                deck[index].set_visible(True)

    def get_visible_cards(self, row: int):
        """Receives an integer which is the row (same as deck) and returns all the visible cards of that row (cards on the table)"""
        result_list = []
        if row == 1:
            result_list += [card for card in self._level_1_deck if card.is_visible()]
        elif row == 2:
            result_list += [card for card in self._level_2_deck if card.is_visible()]
        else:
            result_list += [card for card in self._level_3_deck if card.is_visible()]

        return result_list

    def get_next_card(self, deck_or_card):
        """
        Receives a param which is either a number a Card object:
        when it is a number, it is which deck to get the next card from
        when it is a Card object, it calculates which deck it is from and sets that as the deck number
        Returns Card object which is the next face-down card (top of the deck) of that deck
        """
        if deck_or_card == 1:
            result = self._level_1_deck[self._deck_pointer_1]
            self._deck_pointer_1 += 1
        elif deck_or_card == 2:
            result = self._level_2_deck[self._deck_pointer_2]
            self._deck_pointer_2 += 1
        elif deck_or_card == 3:
            result = self._level_3_deck[self._deck_pointer_3]
            self._deck_pointer_3 += 1
        else:
            if deck_or_card in self._level_1_deck:
                result = self._level_1_deck[self._deck_pointer_1]
                self._deck_pointer_1 += 1
            elif deck_or_card in self._level_2_deck:
                result = self._level_2_deck[self._deck_pointer_2]
                self._deck_pointer_2 += 1
            else:
                result = self._level_3_deck[self._deck_pointer_3]
                self._deck_pointer_3 += 1
        return result


    def buy_card(self, player=None):
        """Method representing the in-game action of a player buying a card. In Splendor a player can buy a card if they have enough tokens and/or dado to pay its price, they then take the card from the table and place it in their hand"""
        if player is None:  # for the sake of the GUI implementation can call without getting current player
            player = self.get_current_player()

        available_cards = []
        player_tender = player.get_player_tender()

        # iterate through every card and filter it down to only those cards the player can afford
        for row in range (1,4):
            available_cards += [card for card in self.get_visible_cards(row) if card.can_afford(player_tender)]

        # add any cards the player has reserved that they can afford
        available_cards += [card for card in player.get_player_reserved() if card.can_afford(player_tender)]

        if self._is_gui is True:
            return available_cards  # exit point where the code diverges for the GUI version

        # get the card from player
        found = False
        while not found:
            card_to_buy = self.prompt_user(("Which card would you like to buy?: " + str([card.get_cost() for card in available_cards]) + "(or 'back' to start turn again): "), 'card')
            if card_to_buy == 'back':
                return 'back'
            for card in available_cards:
                if card.get_cost() == card_to_buy:
                    card_to_buy = card # here the string entered by the user is being transmutated into the Card object itself of that card
                    found = True
                    break
            if found:
                break
            # this only executes if the card was not found among available_cards
            print("That card is not purchasable, please try again")

        # at this point the card_to_buy should contain a card that is fully valid for player to buy

        # mechanism representing the removing of the card from row, placing it into the hand of player and replacing the card in the row (buying)
        card_to_buy.set_visible(False)  # make the bought card not visible anymore (remove from table)
        card_to_buy.set_owner(player)  # set the card's owner to the current player
        player.add_to_hand(card_to_buy)  # add it to their hand
        self.get_next_card(card_to_buy).set_visible(True)  # make the next card in that deck visible (place it on table)
        player.remove_from_reserved(card_to_buy)  # removes the card from player's reserve (if that is where they got it from)
        card_to_buy.set_reserved_by(None)  # set Card as not being reserved by anyone

        # giving the player the dado they have earned
        if card_to_buy.get_dado() == 'w':
            player.deposit_dado('white')
        elif card_to_buy.get_dado() == 'b':
            player.deposit_dado('blue')
        elif card_to_buy.get_dado() == 'g':
            player.deposit_dado('green')
        elif card_to_buy.get_dado() == 'r':
            player.deposit_dado('red')
        else:
            player.deposit_dado('noir')

        # if the card has points, player earns them
        player.points += card_to_buy.get_points()

        # mechanism representing the paying for the card by taking the appropriate tokens from the player and returning them to the game bank (paying)
        cost_string = card_to_buy.get_cost()
        lookup = {1:'white', 3:'blue', 5:'green', 7:'red', 9:'noir'}
        # Iterate through each gem and calculate what must be paid
        for index, color in lookup.items():
            # get the player's amount of that gem and calculate how much is needed after factoring in the discount given by dado
            player_amount = int(player.bank_lookup(color))
            gem_cost = int(cost_string[index]) - int(player.dado_lookup(color))
            if gem_cost > 0:
                # if the players tokens are not enough to cover the cost of this gem, calculate gold
                if gem_cost - player_amount > 0:
                    gold_needed = gem_cost - player_amount
                    gem_needed = player_amount
                    # withdraw needed gold from Player's bank and deposit into GameBank
                    for _ in range(gold_needed):
                        player.withdraw('gold')
                        self._bank.deposit('gold')
                    # withdraw all of Player's tokens of that gem and deposit into GameBank
                    for _ in range(gem_needed):
                        player.withdraw(color)
                        self._bank.deposit(color)
                # otherwise, just withdraw that many tokens from Player's bank and deposit into GameBank
                else:
                    for _ in range (gem_cost):
                        player.withdraw(color)
                        self._bank.deposit(color)

        self.end_turn(("bought card " + str(card_to_buy)))

    def reserve_card(self, player=None):
        """Method representing the in-game action of a player reserving a card, receives a Player object and allows that player to reserve any visible Card or the next_card of any row and receive a gold token"""
        # all visible cards are available
        available_cards = self.get_visible_cards(1) + self.get_visible_cards(2) + self.get_visible_cards(3)

        if player is None:  # for the sake of the GUI implementation can call without getting current player
            player = self.get_current_player()

        # The unique input needs of this function require using a custom user prompt rather than using the prompt_user method, combining the 'card' requirement with the numbers [1,2,3]
        while True:
            card_to_reserve = input(f"Which card would you like to reserve? the top of the deck for row [1, 2, 3] or {str([card.get_cost() for card in available_cards])}  (or 'back' to start turn again): ")
            if card_to_reserve == 'back':
                return 'back'
            if len(card_to_reserve) == 1 and card_to_reserve in ['1','2','3']:
                break
            else:
                for index, char in enumerate(['w', 0, 'b', 0, 'g', 0, 'r', 0, 'n', 0]):
                    if type(char) == str:
                        if char != card_to_reserve[index]:
                            print("Please enter a valid value (1,2,3 or a card)")
                            return self.reserve_card(player)
                    if char == 0 and int(card_to_reserve[index]) not in range(0, 8):
                        print("Please enter a valid value (1,2,3 or a card)")
                        return self.reserve_card(player)
        # if the code has reached this part, it is a valid input
            break
        if len(card_to_reserve) > 1:
            valid = False
            for card in available_cards:  # determine whether the requested card is a valid card
                if card.get_cost() == card_to_reserve:
                    card_to_reserve = card  # here the string entered by the user is being transmutated into the Card object itself of that card
                    valid = True
                    break
            if not valid:
                print("That card is not available to reserve, please try again") # if the code reaches here, that means the card was not valid
                return self.reserve_card(player)

        # if the code has reached this part, it is a valid action

        # if the input was a number (simulates the player reserving the top face-down card of that row's deck)
        if type(card_to_reserve) == str:
            card_to_reserve = self.get_next_card(int(card_to_reserve))  # here the integer is being translated into the appropriate next face-down card from the deck

        # if the code has reached this part, then card_to_reserve now must contain the Card object of the card to reserved

        # mechanism with simulates the player taking the card and placing it in their reserve pile
        card_to_reserve.set_reserved_by(player) # set the cards 'reserved by' property to the current player
        card_to_reserve.set_visible(False)  # make the reserved not visible (take it from table)
        self.get_next_card(card_to_reserve).set_visible(True)  # take the next face-down card of that deck and make it visible (place it on table)
        player.add_to_reserved(card_to_reserve)  # add card to the player's 'reserved' property
        # taking a gold token
        self._bank.withdraw('gold')
        player.deposit_bank('gold')
        self.end_turn(("reserved card " + str(card_to_reserve)))
        return

    def get_current_player(self) -> Player:
        """Returns the current player"""
        return self._current_player

    def change_to_next_player(self):
        current_index = self._current_player.get_player_number()-1
        if current_index + 1 == self._num_players:
            current_index = -1
        self._current_player = self._players[current_index+1]

    def draw_board(self):
        self.print_row_of_cards(self.get_visible_cards(3))
        self.print_row_of_cards(self.get_visible_cards(2))
        self.print_row_of_cards(self.get_visible_cards(1))

        print(f"Bank: white = {self._bank.get_token_num('white')}  blue = {self._bank.get_token_num('blue')}  green = {self._bank.get_token_num('green')}  red = {self._bank.get_token_num('red')}  noir = {self._bank.get_token_num('noir')}  gold = {self._bank.get_token_num('gold')}\n")

    def print_row_of_cards(self, row_of_cards: list):
        w1 = row_of_cards[0].get_cost()[1]
        w2 = row_of_cards[1].get_cost()[1]
        w3 = row_of_cards[2].get_cost()[1]
        w4 = row_of_cards[3].get_cost()[1]
        b1 = row_of_cards[0].get_cost()[3]
        b2 = row_of_cards[1].get_cost()[3]
        b3 = row_of_cards[2].get_cost()[3]
        b4 = row_of_cards[3].get_cost()[3]
        g1 = row_of_cards[0].get_cost()[5]
        g2 = row_of_cards[1].get_cost()[5]
        g3 = row_of_cards[2].get_cost()[5]
        g4 = row_of_cards[3].get_cost()[5]
        r1 = row_of_cards[0].get_cost()[7]
        r2 = row_of_cards[1].get_cost()[7]
        r3 = row_of_cards[2].get_cost()[7]
        r4 = row_of_cards[3].get_cost()[7]
        n1 = row_of_cards[0].get_cost()[9]
        n2 = row_of_cards[1].get_cost()[9]
        n3 = row_of_cards[2].get_cost()[9]
        n4 = row_of_cards[3].get_cost()[9]
        d1 = row_of_cards[0].get_dado()
        d2 = row_of_cards[1].get_dado()
        d3 = row_of_cards[2].get_dado()
        d4 = row_of_cards[3].get_dado()
        p1 = ' '
        p2 = ' '
        p3 = ' '
        p4 = ' '
        if row_of_cards[0].get_points() != 0:
            p1 = row_of_cards[0].get_points()
        if row_of_cards[1].get_points() != 0:
            p2 = row_of_cards[1].get_points()
        if row_of_cards[2].get_points() != 0:
            p3 = row_of_cards[2].get_points()
        if row_of_cards[3].get_points() != 0:
            p4 = row_of_cards[3].get_points()

        print(f" __________    __________    __________    __________  ")
        print(f"| w {w1}    {d1} |  | w {w2}    {d2} |  | w {w3}    {d3} |  | w {w4}    {d4} | ")
        print(f"| b {b1}    {p1} |  | b {b2}    {p2} |  | b {b3}    {p3} |  | b {b4}    {p4} | ")
        print(f"| g {g1}      |  | g {g2}      |  | g {g3}      |  | g {g4}      | ")
        print(f"| r {r1}      |  | r {r2}      |  | r {r3}      |  | r {r4}      | ")
        print(f"| n {n1}      |  | n {n2}      |  | n {n3}      |  | n {n4}      | ")
        print(f" __________    __________    __________    __________  ")




if __name__ == "__main__":
    game = GameMaster()
    while True:
        game.draw_board()
        print(f"Player {game.get_current_player().get_player_number()} {game.get_current_player().get_player_name()}, please take an action:")
        game.take_an_action(player=game.get_current_player(), action=game.prompt_user("'buy' a card\n'reserve' a card\ntake 'tokens'\nsee your 'status' (cards, tokens, points)\ntake an action:", 'action'))


