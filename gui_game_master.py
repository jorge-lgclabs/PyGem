import gui_cards, gui_player_board, gui_game_bank, gui_functions
from PyGem import GameMaster
import flet as ft

class GuiGameMaster:
    def __init__(self, game: GameMaster):
        self.game = game
        self.market = gui_cards.CardMarket(game)
        self.game_bank = gui_game_bank.GameBank(game)
        self.gui_players = [gui_player_board.GuiPlayer(player) for player in game._players]
        self.make_cards_clickable()
        #self.refresh_player_board()

    def load_initial_gui(self):
        self.market_and_player_board = ft.Column(controls=[self.market.gui_obj],
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            alignment=ft.MainAxisAlignment.CENTER)
        for player in self.gui_players:
            if self.game.get_current_player() == player.player_obj:
                current_player = player

        self.market_and_player_board.controls.append(current_player.player_bank.gui_obj)
        self.market_and_player_board.controls.append(current_player.player_reserved.gui_obj)

        return ft.Row(controls=[self.market_and_player_board, self.game_bank.gui_obj], spacing=30,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)

    def refresh_player_board(self):
        for player in self.gui_players:
            if self.game.get_current_player() == player.player_obj:
                current_player = player
        current_player.player_reserved.update_player_reserved_cards()
        current_player.player_bank.update_player_bank_values()

    def update_all_components(self):
        self.market.update_market_grid()
        self.game_bank.update_game_bank_values()
        self.refresh_player_board()

    def make_cards_clickable(self):
        for row in self.market.get_all_containers():
            for card in row:
                card_container = card
                card_container.on_click = self.card_click_handler

    def card_click_handler(self, e):
        card_obj = e.control.data.card_obj
        gui_functions.gui_reserve_card(self.game, card_obj)
        self.update_all_components()





















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