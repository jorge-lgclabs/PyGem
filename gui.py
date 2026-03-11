from time import sleep

import gui_functions
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

    def start_game(player_names: list):
        game = GameMaster(player_names)
        gui_game = GuiGameMaster(game)
        page.controls.clear()
        page.add(gui_game.load_initial_gui())
        page.update()

    page.add(gui_functions.opening_screen(start_game))


ft.run(gui, assets_dir="assets")

