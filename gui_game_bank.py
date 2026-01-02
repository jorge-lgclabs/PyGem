import flet as ft

import PyGem
import player


from gui_assets import GEM_LOOKUP, RED_GEM, WHITE_GEM, BLUE_GEM, GREEN_GEM, NOIR_GEM, GOLD_COIN
from gui_assets import CARD_HEIGHT, CARD_WIDTH
from gui_assets import PLAYER_BANK_CELL_SIZE, PLAYER_BANK_HEIGHT, PLAYER_BANK_WIDTH, PLAYER_BANK_ROUNDING_RADIUS, SHADE_OPACITY
from gui_assets import CircleWithNum, NumWithStrokeCenter
from gui_cards import GameCard


class GameBank:
    def __init__(self, game: PyGem.GameMaster):
        self.lookup = GEM_LOOKUP
        #self.page = page
        self.size = PLAYER_BANK_CELL_SIZE
        self.game = game
        self.bank = self.game._bank

        #self.player_gold = player_obj.bank_lookup('gold')

        self.red_text_objs = (NumWithStrokeCenter(0, self.size), 'r')
        self.green_text_objs = (NumWithStrokeCenter(0, self.size), 'g')
        self.white_text_objs = (NumWithStrokeCenter(0, self.size), 'w')
        self.blue_text_objs = (NumWithStrokeCenter(0, self.size), 'b')
        self.noir_text_objs = (NumWithStrokeCenter(0, self.size), 'n')
        self.gold_text_obj = NumWithStrokeCenter(0, self.size)
        self.text_obj_tuples = [self.white_text_objs, self.blue_text_objs, self.green_text_objs, self.red_text_objs, self.noir_text_objs]

        self.update_game_bank_values()
        self.shade_container = self.set_shade()
        self.grid_container = self.create_game_bank_grid()
        self.gui_obj = ft.Container(content=ft.Stack(controls=[self.shade_container, self.grid_container], alignment=ft.alignment.Alignment.CENTER))

    def update_game_bank_values(self):
        for obj_tuple in self.text_obj_tuples:
            bank_text_obj, letter = obj_tuple

            bank_value = self.bank.get_token_num(self.lookup[letter][2])
            bank_text_obj.set_num(bank_value)

        gold_value = self.bank.get_token_num('gold')
        self.gold_text_obj.set_num(gold_value)



    def create_game_bank_grid(self):
        bank_column = []
        #gem_icon_row = []

        for obj_tuple in self.text_obj_tuples:
            bank_text_obj, letter = obj_tuple

            bank_text_container = ft.Container(content=bank_text_obj.gui_obj, width=self.size, height=self.size,
                                          alignment=ft.alignment.Alignment.CENTER)
            bank_color_container = ft.Container(border_radius=PLAYER_BANK_ROUNDING_RADIUS,
                                                alignment=ft.alignment.Alignment.CENTER, height=self.size * 1.35,
                                                clip_behavior=ft.ClipBehavior.ANTI_ALIAS, content=bank_text_container,
                                                width=self.size * 1.35,
                                                bgcolor=ft.Colors.with_opacity(.99, self.lookup[letter][0]))
            gem_icon_container = ft.Container(border_radius=PLAYER_BANK_ROUNDING_RADIUS, alignment=ft.alignment.Alignment.CENTER,
                                              height=self.size * .75,
                                              clip_behavior=ft.ClipBehavior.ANTI_ALIAS, content=self.lookup[letter][1],
                                              width=self.size * 2.5)
            mini_column = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, spacing=8 , width=self.size * 2, height=self.size * 2, controls=[gem_icon_container, bank_color_container])


            bank_column.append(mini_column)
            #gem_icon_row.append(gem_icon_container)

        #  gold section
        gold_icon_container = ft.Container(border_radius=PLAYER_BANK_ROUNDING_RADIUS, alignment=ft.alignment.Alignment.CENTER, height=self.size*.75,
                                          clip_behavior=ft.ClipBehavior.ANTI_ALIAS, content=GOLD_COIN, width=self.size*2.5)

        gold_value_text_container =  ft.Container(content=self.gold_text_obj.gui_obj, width=self.size, height=self.size,
                                          alignment=ft.alignment.Alignment.CENTER)
        gold_value_container = ft.Container(border_radius=PLAYER_BANK_ROUNDING_RADIUS, alignment=ft.alignment.Alignment.CENTER, height=self.size*1.35,
                                          clip_behavior=ft.ClipBehavior.ANTI_ALIAS, content=gold_value_text_container, width=self.size*1.35,
                                          bgcolor=ft.Colors.with_opacity(.39, ft.Colors.GREY_50))
        gold_mini_column = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, spacing=8 , width=self.size * 2, height=self.size * 2, controls=[gold_icon_container, gold_value_container])
        bank_column.append(gold_mini_column)


        game_bank_obj = ft.Column(spacing=25, controls=bank_column, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)
        #gem_bank_row_obj = ft.Row(controls=gem_icon_row, vertical_alignment=ft.alignment.Alignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)
        #both_col = ft.Column(spacing=1, controls=[gem_bank_row_obj, bank_and_dado_row_obj], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
        return ft.Container(
            content=game_bank_obj,
            width=PLAYER_BANK_HEIGHT,
            height=PLAYER_BANK_WIDTH,
            border_radius=PLAYER_BANK_ROUNDING_RADIUS,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            shadow=ft.BoxShadow(
                blur_radius=PLAYER_BANK_ROUNDING_RADIUS / 2,
                spread_radius=0,
                offset=ft.Offset(0, (PLAYER_BANK_ROUNDING_RADIUS / 2)),
                color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK)
            ),
            alignment=ft.alignment.Alignment.CENTER)

    def set_shade(self):
        return ft.Container(
            width=PLAYER_BANK_HEIGHT,
            height=PLAYER_BANK_WIDTH,
            border_radius=PLAYER_BANK_ROUNDING_RADIUS,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            bgcolor=ft.Colors.GREY_50,
            opacity=SHADE_OPACITY,
            alignment=ft.alignment.Alignment.CENTER)




