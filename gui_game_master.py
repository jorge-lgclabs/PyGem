import gui_cards, gui_player_board, gui_game_bank
import flet as ft

class GuiGameMaster:
    def __init__(self, game):
        self.game = game
        self.market = gui_cards.CardMarket(game)
        self.game_bank = gui_game_bank.GameBank(game)
        self.player_board = gui_player_board.PlayerBank(game.get_current_player())
        self.player_reserved = gui_player_board.PlayerReserved(game.get_current_player())

    def load_full_gui(self):
        market_and_player_board = ft.Column(controls=[self.market.gui_obj, self.player_board.gui_obj, self.player_reserved.gui_obj],
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            alignment=ft.MainAxisAlignment.CENTER)
        return ft.Row(controls=[market_and_player_board, self.game_bank.gui_obj], spacing=30,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)






















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