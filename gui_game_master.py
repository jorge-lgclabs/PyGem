import cards
import gui_cards, gui_player_board, gui_game_bank, gui_functions
import gui_user_column
from PyGem import GameMaster
import flet as ft

from gui_assets import CARD_ROUNDING_RADIUS


class GuiGameMaster:
    def __init__(self, game: GameMaster):
        self.game = game
        self.market = gui_cards.CardMarket(game)
        self.game_bank = gui_game_bank.GameBank(game)
        self.user_column = gui_user_column.UserColumn(game)
        self.gui_players = [gui_player_board.GuiPlayer(player) for player in game._players]
        self.update_current_gui_player()
        self.last_move = ''

        # testing bank
        self.current_player.player_obj.deposit_bank('red')
        self.current_player.player_obj.deposit_bank('red')
        self.current_player.player_obj.deposit_bank('red')
        self.current_player.player_obj.deposit_bank('blue')
        self.current_player.player_obj.deposit_bank('blue')
        self.current_player.player_obj.deposit_bank('green')
        self.current_player.player_obj.deposit_bank('white')

        gui_functions.make_cards_clickable(self.market.get_all_containers(), self.card_click_handler)
        gui_functions.highlight_buyable_cards(self.market.get_all_containers(), self.current_player)


    def update_current_gui_player(self):
        for player in self.gui_players:
            if self.game.get_current_player() == player.player_obj:
                self.current_player = player

    def load_initial_gui(self):
        self.market_and_player_board = ft.Column(controls=[
            self.market.gui_obj,
            self.current_player.player_label,
            self.current_player.player_bank.gui_obj,
            self.current_player.player_reserved.gui_obj
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)

        return ft.Row(controls=[self.user_column.gui_obj, self.market_and_player_board, self.game_bank.gui_obj], spacing=30,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)

    def refresh_gui(self):
        self.current_player.player_reserved.update_player_reserved_cards()
        self.current_player.player_bank.update_player_bank_values()
        self.market.update_market_grid()
        self.game_bank.update_game_bank_values()
        self.user_column.update_user_column()

    def end_turn_change_player(self):
        self.game.end_turn(self.last_move)
        self.update_current_gui_player()

        for _ in range(3):
            self.market_and_player_board.controls.pop()

        self.market_and_player_board.controls.append(self.current_player.player_label)
        self.market_and_player_board.controls.append(self.current_player.player_bank.gui_obj)
        self.market_and_player_board.controls.append(self.current_player.player_reserved.gui_obj)

        gui_functions.unhighlight_all_cards(self.market.get_all_containers())
        gui_functions.highlight_buyable_cards(self.market.get_all_containers(), self.current_player)

        self.refresh_gui()

    def card_click_handler(self, e):
        card_container = e.control
        card_obj: cards.Card = card_container.data.card_obj
        #self.last_move = gui_functions.gui_reserve_card(self.game, card_obj)
        self.user_column.gui_obj.content.controls.insert(0, card_container)




        if gui_functions.gui_can_afford(card_obj, self.current_player):
            print('can afford')
        else:
            print('cannot afford')

        self.user_column.user_message.value='this card?'
        self.user_column.commit_button.visible=True
        self.refresh_gui()





















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