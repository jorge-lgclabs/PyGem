from time import sleep

from PyGem import GameMaster, GameMasterError
from gui_game_master import GuiGameMaster
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
    gui_game = GuiGameMaster(game)
    page.add(gui_game.load_full_gui())
    #gui_game.market.grid_1_0.on_click = gui_game.test_reserve
    gui_game.test_selecting_card()


ft.run(gui, assets_dir="assets")

