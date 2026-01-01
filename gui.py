from time import sleep
import random

import PyGem
import cards
import gui_game_bank
from PyGem import GameMaster, GameMasterError
import gui_assets, gui_cards, gui_player_board
import flet as ft



def gui(page: ft.Page):
    page.title = "PyGem"
    page.fonts = {"lobster" : "/fonts/Lobster-Regular.ttf"}
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    # page.window.height = 870
    # page.window.width = 1020
    page.window.maximized=True

    game = GameMaster(['Jorge', 'Alejandra'])

    market = gui_cards.CardMarket(game)
    game_bank = gui_game_bank.GameBank(game)
    player_board = gui_player_board.PlayerBank(game.get_current_player())
    player_reserved = gui_player_board.PlayerReserved(game.get_current_player())
    market_and_player_board = ft.Column(controls=[market.gui_obj, player_board.gui_obj, player_reserved.gui_obj], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)
    page.add(ft.Row(controls=[market_and_player_board, game_bank.gui_obj], spacing=30, vertical_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER))



def test_player_bank_values(game, player_board):
    sleep(2)
    test_player = game.get_current_player()
    test_player.deposit_bank('gold')
    test_player._player_bank = 'w3b0g2r2n0'
    test_player._player_dado = 'w4b1g2r1n2'
    player_board.update_player_bank_values()
def test_player_new_reserved(game: PyGem.GameMaster, market, player_reserved):
    sleep(2)
    reserved_card = test_new_card(game, market)
    test_player = game.get_current_player()
    test_player.add_to_reserved(reserved_card)
    player_reserved.update_player_reserved_cards()
def test_new_card(game, market=None):
    sleep(2)
    old = game.get_visible_cards(1)[1]
    old: cards.Card
    old.set_visible(False)
    next = game.get_next_card(1)
    next: cards.Card
    next.set_visible(True)
    market.update_market_grid()
    return old

ft.app(gui, assets_dir="assets")

