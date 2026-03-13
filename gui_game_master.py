import cards
import gui_cards, gui_player_board, gui_game_bank, gui_functions
import gui_user_column
from PyGem import GameMaster
import flet as ft

from gui_assets import CARD_ROUNDING_RADIUS, GEM_LOOKUP


class GuiGameMaster:
    def __init__(self, game: GameMaster, page: ft.Page, start_func):
        self.game = game
        self.page = page
        self.start_func = start_func
        self.gui_players = [gui_player_board.GuiPlayer(player) for player in game._players]
        self.update_current_gui_player()
        self.market = gui_cards.CardMarket(game)
        self.nobles = gui_cards.NobleMarket(game)
        self.game_bank = gui_game_bank.GameBank(game)
        #self.test_moves()
        self.test_flag = 0
        self.user_column = gui_user_column.UserColumn(game, self.go_back_from_move, self.end_turn_change_player, self.refresh_gui, self.token_giveback_handler)
        self.last_move = ''
        self.token_take_cache = []
        self.token_bank_cache = {}
        self.token_giveback_cache = int()
        self.token_player_cache = {}



    def test_moves(self):
        # testing bank
        for _ in range(3):
            self.game._bank.withdraw('red')
            self.current_player.player_obj.deposit_bank('red')

        for _ in range(2):
            self.game._bank.withdraw('blue')
            self.current_player.player_obj.deposit_bank('blue')

        self.current_player.player_obj.deposit_dado('green')
        self.current_player.player_obj.deposit_dado('green')
        self.current_player.player_obj.deposit_dado('green')
        self.current_player.player_obj.deposit_dado('green')

        self.current_player.player_obj.deposit_dado('red')
        self.current_player.player_obj.deposit_dado('red')
        self.current_player.player_obj.deposit_dado('red')

        self.current_player.player_obj.deposit_dado('blue')
        self.current_player.player_obj.deposit_dado('blue')
        #self.current_player.player_obj.deposit_dado('red')



        self.game._bank.withdraw('green')
        self.current_player.player_obj.deposit_bank('green')
        self.game._bank.withdraw('white')
        self.current_player.player_obj.deposit_bank('white')

        gui_functions.highlight_buyable_cards(self.market.get_all_containers(), self.current_player)
        self.current_player.player_bank.update_player_bank_values()
        self.game_bank.update_game_bank_values()


    def update_current_gui_player(self):
        for player in self.gui_players:
            if self.game.get_current_player() == player.player_obj:
                self.current_player = player

    def load_initial_gui(self):
        self.market_and_player_board = ft.Column(controls=[
            self.nobles.gui_obj,
            self.market.gui_obj,
            self.current_player.player_label,
            self.current_player.player_bank.gui_obj,
            self.current_player.player_reserved.gui_obj
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)
        gui_functions.make_cards_clickable(self.market.get_all_containers(), self.card_click_handler)
        self.game_bank.make_bank_color_containers_clickable(token_taker_handler=self.token_click_handler)

        return ft.Row(controls=[self.user_column.gui_obj, self.market_and_player_board, self.game_bank.gui_obj], spacing=30,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)

    def refresh_gui(self):
        self.current_player.player_reserved.update_player_reserved_cards()
        self.current_player.player_bank.update_player_bank_values()
        self.current_player.update_player_points()
        self.market.update_market_grid()
        self.nobles.refresh_nobles_row()
        self.game_bank.update_game_bank_values()
        self.user_column.update_user_column()

    def go_back_from_move(self, e):
        e.control.parent.controls.clear()
        gui_functions.make_cards_clickable(self.market.get_all_containers(), self.card_click_handler)
        gui_functions.highlight_buyable_cards(self.market.get_all_containers(), self.current_player)
        gui_functions.highlight_and_make_clickable_reserved_cards(self.current_player.get_buyable_reserved_containers(), self.card_click_handler)
        self.game_bank.make_bank_color_containers_clickable(token_taker_handler=self.token_click_handler)
        self.token_bank_cache = {}
        self.token_take_cache = []
        self.market.update_market_grid()
        self.user_column.initial_message()
        self.user_column.update_user_column()

    def end_turn_change_player(self, e):
        self.last_move = e.control.data
        has_won = self.game.end_turn(self.last_move, is_gui=True)

        if has_won:
            player_scores = []
            for player in self.gui_players:
                player_scores.append((player.player_obj.get_player_name(), player.player_obj.points))
            gui_functions.winning_screen(player_scores, self.page, self.start_func)
            return

        self.update_current_gui_player()

        for _ in range(3):
            self.market_and_player_board.controls.pop()

        self.market_and_player_board.controls.append(self.current_player.player_label)
        self.market_and_player_board.controls.append(self.current_player.player_bank.gui_obj)
        self.market_and_player_board.controls.append(self.current_player.player_reserved.gui_obj)

        gui_functions.unhighlight_and_make_unclickable_reserved_cards(self.current_player.get_buyable_reserved_containers())
        gui_functions.unhighlight_all_cards(self.market.get_all_containers())
        gui_functions.highlight_buyable_cards(self.market.get_all_containers(), self.current_player)
        gui_functions.make_cards_clickable(self.market.get_all_containers(), self.card_click_handler)
        gui_functions.highlight_and_make_clickable_reserved_cards(self.current_player.get_buyable_reserved_containers(), self.card_click_handler)
        self.game_bank.make_bank_color_containers_clickable(token_taker_handler=self.token_click_handler)
        self.token_bank_cache = {}
        self.token_take_cache = []

        self.refresh_gui()
        self.user_column.initial_message()

    def card_click_handler(self, e):
        gui_functions.make_cards_unclickable(self.market.get_all_containers())
        gui_functions.unhighlight_all_cards(self.market.get_all_containers())
        gui_functions.unhighlight_and_make_unclickable_reserved_cards(self.current_player.get_buyable_reserved_containers())
        self.game_bank.make_bank_color_containers_clickable(token_taker_handler=self.token_click_handler, which_colors=[])

        container_data = e.control.data


        if type(container_data) == str:  # if the card clicked has a string data, it is the top of a deck and not a card
            card_obj = str(len(container_data))  # text in the container either 'I', 'II', or 'III'
        else:
            card_obj = container_data.card_obj

        if isinstance(card_obj, cards.Card) and gui_functions.gui_can_afford(card_obj, self.current_player):
            self.user_column.reserve_or_buy_card(card_obj, can_buy=True)
        else:
            self.user_column.reserve_or_buy_card(card_obj, can_buy=False)

        self.refresh_gui()

    def token_click_handler(self, e):
        gui_functions.make_cards_unclickable(self.market.get_all_containers())
        gui_functions.unhighlight_all_cards(self.market.get_all_containers())

        clicked_color = GEM_LOOKUP[e.control.data][2]

        if len(self.token_take_cache) == 0: # first token-taking action
            # subsection for calculating whether eventually the player will have to give back tokens (more than 10)
            self.token_giveback_cache = (self.current_player.player_obj.get_player_bank_length() +
                                         self.current_player.player_obj.get_player_tender()[1] +
                                         1)

            available_colors = self.game_bank.bank.get_available_tokens()
            for color in available_colors:
                self.token_bank_cache[color] = self.game_bank.bank.get_token_num(color)
            self.token_take_cache = [clicked_color]
            self.token_bank_cache[clicked_color] -= 1
            self.user_column.token_taking_messages(first_take=self.token_take_cache[0])
        elif len(self.token_take_cache) == 1: # second token-taking action
            self.token_giveback_cache += 1
            self.token_take_cache.append(clicked_color)
            if self.token_take_cache[0] == self.token_take_cache[1]: # if the player took two of the same color
                self.token_giveback_cache -= 10
                if self.token_giveback_cache <= 0:
                    self.token_giveback_cache = 0
                self.game_bank.make_bank_color_containers_clickable(self.token_click_handler, which_colors=[]) # make all tokens unclickable
                self.user_column.token_taking_messages(
                    first_take=self.token_take_cache[0],
                    second_take=self.token_take_cache[1],
                    end=True,
                    giveback=self.token_giveback_cache
                )
                return # end here since this is the last move if 2 of the same color are taken
            else: # if the player took another color other than the first, necessitating a third taking action
                self.token_bank_cache[clicked_color] -= 1
                self.user_column.token_taking_messages(
                    first_take=self.token_take_cache[0],
                    second_take=self.token_take_cache[1])
                if self.token_take_cache[0] in self.token_bank_cache.keys():
                    self.token_bank_cache.pop(self.token_take_cache[0])
                self.token_bank_cache.pop(self.token_take_cache[1])

        else: # third token-taking action
            self.token_giveback_cache += 1
            self.token_giveback_cache -= 10
            if self.token_giveback_cache <= 0:
                self.token_giveback_cache = 0

            self.token_take_cache.append(clicked_color)
            self.game_bank.make_bank_color_containers_clickable(self.token_click_handler, which_colors=[])  # make all tokens unclickable
            self.user_column.token_taking_messages(
                first_take=self.token_take_cache[0],
                second_take=self.token_take_cache[1],
                third_take=self.token_take_cache[2],
                end=True,
                giveback=self.token_giveback_cache)
            return # final move
        remaining_colors = []
        to_remove = []

        for key in self.token_bank_cache.keys():
            if self.token_bank_cache[key] == 0:  # remove those colors which have been expended
                to_remove.append(key)
            elif key == self.token_take_cache[0] and self.token_bank_cache[key] < 3: # remove color that violates "take 2 only if 3 or more of it" rule
                to_remove.append(key)
            else:
                remaining_colors.append(key[0])  # otherwise, leave color as remaining choice

        for color in to_remove:
            self.token_bank_cache.pop(color)
        self.game_bank.make_bank_color_containers_clickable(token_taker_handler=self.token_click_handler, which_colors=remaining_colors)

    def token_giveback_handler(self, e, giveback=None, last_move=None):
        if e is None:  # means this is the first call, the setup to the giveback loop
            self.refresh_gui()
            self.token_giveback_cache = giveback
            self.last_move = last_move
            self.token_take_cache = []
            for color in ['red', 'blue', 'white', 'green', 'noir']:
                if int(self.current_player.player_obj.bank_lookup(color)) > 0:
                    self.token_player_cache[color] = int(self.current_player.player_obj.bank_lookup(color))
            self.user_column.token_giveback_messages(self.token_player_cache.keys(), 1)
        else:
            # means this is the first, second, or third giveback click
            clicked_color = e.control.data

            self.current_player.player_obj.withdraw(clicked_color)
            self.game_bank.bank.deposit(clicked_color)
            self.refresh_gui()

            self.token_take_cache.append(clicked_color)
            self.token_player_cache[clicked_color] -= 1
            if self.token_player_cache[clicked_color] == 0:
                self.token_player_cache.pop(clicked_color)
            # if this is the last token to give back, end turn
            if len(self.token_take_cache) == self.token_giveback_cache:
                self.user_column.ready_to_end_turn(f'{self.last_move} and gave back {self.token_take_cache}')
            else:  # otherwise, ask for more tokens back
                if self.token_giveback_cache - len(self.token_take_cache) == 1:
                    iteration = self.token_giveback_cache
                else:
                    iteration = 2
                self.user_column.token_giveback_messages(self.token_player_cache.keys(), iteration)





















# def test_player_bank_values(game, player_board):
#     sleep(2)
#     test_player = game.get_current_player()
#     test_player.deposit_bank('gold')
#     test_player._player_bank = 'w3b0g2r2n0'
#     test_player._player_dado = 'w4b1g2r1n2'
#     player_board.update_player_bank_values()
# def test_player_new_reserved(game: PyGem.GameMaster, market, player_reserved):
#     sleep(2)
#     reserved_card = test_new_card(game, market)
#     test_player = game.get_current_player()
#     test_player.add_to_reserved(reserved_card)
#     player_reserved.update_player_reserved_cards()
# def test_new_card(game, market=None):
#     sleep(2)
#     old = game.get_visible_cards(1)[1]
#     old: cards.Card
#     old.set_visible(False)
#     next = game.get_next_card(1)
#     next: cards.Card
#     next.set_visible(True)
#     market.update_market_grid()
#     return old