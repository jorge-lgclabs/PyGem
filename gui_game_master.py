import cards
import gui_cards, gui_player_board, gui_game_bank, gui_functions
import gui_user_column
from PyGem import GameMaster
import flet as ft

from gui_assets import CARD_ROUNDING_RADIUS, GEM_LOOKUP


class GuiGameMaster:
    def __init__(self, game: GameMaster):
        self.game = game
        self.gui_players = [gui_player_board.GuiPlayer(player) for player in game._players]
        self.update_current_gui_player()
        #self.test_moves()
        self.market = gui_cards.CardMarket(game)
        self.nobles = gui_cards.NobleMarket(game)
        self.game_bank = gui_game_bank.GameBank(game)
        self.user_column = gui_user_column.UserColumn(game, self.go_back_from_move, self.end_turn_change_player, self.refresh_gui)
        self.last_move = ''
        self.token_take_cache = []
        self.token_bank_cache = {}

        # not meant to be done at the outset, only here for testing purposes
        #gui_functions.highlight_buyable_cards(self.market.get_all_containers(), self.current_player)
        #self.current_player.player_bank.update_player_bank_values()

    def test_moves(self):
        # testing bank
        for _ in range(3):
            self.game._bank.withdraw('red')
            self.current_player.player_obj.deposit_bank('red')

        for _ in range(2):
            self.game._bank.withdraw('blue')
            self.current_player.player_obj.deposit_bank('blue')

        self.game._bank.withdraw('green')
        self.current_player.player_obj.deposit_bank('green')
        self.game._bank.withdraw('white')
        self.current_player.player_obj.deposit_bank('white')


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
        self.game.end_turn(self.last_move)
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
            available_colors = self.game_bank.bank.get_available_tokens()
            for color in available_colors:
                self.token_bank_cache[color] = self.game_bank.bank.get_token_num(color)
            self.token_take_cache.append(clicked_color)
            self.token_bank_cache[clicked_color] -= 1
            self.user_column.token_taking_messages(first_take=self.token_take_cache[0])
        elif len(self.token_take_cache) == 1: # second token-taking action
            self.token_take_cache.append(clicked_color)
            if self.token_take_cache[0] == self.token_take_cache[1]: # if the player took two of the same color
                self.game_bank.make_bank_color_containers_clickable(self.token_click_handler, which_colors=[]) # make all tokens unclickable
                self.user_column.token_taking_messages(
                    first_take=self.token_take_cache[0],
                    second_take=self.token_take_cache[1],
                    end=True)
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
            self.token_take_cache.append(clicked_color)
            self.game_bank.make_bank_color_containers_clickable(self.token_click_handler, which_colors=[])  # make all tokens unclickable
            self.user_column.token_taking_messages(
                first_take=self.token_take_cache[0],
                second_take=self.token_take_cache[1],
                third_take=self.token_take_cache[2],
                end=True)
            return # final move
        remaining_colors = []
        to_remove = []

        for key in self.token_bank_cache.keys():
            if self.token_bank_cache[key] == 0:  # remove those colors which have been expended
                to_remove.append(key)
            elif key == self.token_take_cache[0] and self.token_bank_cache[key] < 2: # remove color that violates "take 2 only if 3 or more of it" rule
                to_remove.append(key)
            else:
                remaining_colors.append(key[0])  # otherwise, leave color as remaining choice

        for color in to_remove:
            self.token_bank_cache.pop(color)
        self.game_bank.make_bank_color_containers_clickable(token_taker_handler=self.token_click_handler, which_colors=remaining_colors)






















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