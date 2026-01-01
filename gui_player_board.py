import flet as ft
import player


from gui_assets import GEM_LOOKUP, RED_GEM, WHITE_GEM, BLUE_GEM, GREEN_GEM, NOIR_GEM, GOLD_COIN
from gui_assets import CARD_HEIGHT, CARD_WIDTH
from gui_assets import PLAYER_BANK_CELL_SIZE, PLAYER_BANK_HEIGHT, PLAYER_BANK_WIDTH, PLAYER_BANK_ROUNDING_RADIUS, SHADE_OPACITY
from gui_assets import CircleWithNum, NumWithStrokeCenter
from gui_cards import GameCard


class PlayerBank:
    def __init__(self, player_obj: player.Player):
        self.lookup = GEM_LOOKUP
        self.size = PLAYER_BANK_CELL_SIZE
        self.player_obj = player_obj

        self.player_gold = player_obj.bank_lookup('gold')

        self.red_text_objs = (NumWithStrokeCenter(0, self.size),
                              NumWithStrokeCenter(0, self.size), 'r')
        self.green_text_objs = (NumWithStrokeCenter(0, self.size),
                              NumWithStrokeCenter(0, self.size), 'g')
        self.white_text_objs = (NumWithStrokeCenter(0, self.size),
                                NumWithStrokeCenter(0, self.size), 'w')
        self.blue_text_objs = (NumWithStrokeCenter(0, self.size),
                                NumWithStrokeCenter(0, self.size), 'b')
        self.noir_text_objs = (NumWithStrokeCenter(0, self.size),
                                NumWithStrokeCenter(0, self.size), 'n')
        self.gold_text_obj = NumWithStrokeCenter(0, self.size)
        self.text_obj_tuples = [self.white_text_objs, self.blue_text_objs, self.green_text_objs, self.red_text_objs, self.noir_text_objs]

        self.update_player_bank_values()
        self.shade_container = self.set_shade()
        self.grid_container = self.create_bank_and_dado_grid()
        self.gui_obj = ft.Container(content=ft.Stack(controls=[self.shade_container, self.grid_container], alignment=ft.alignment.center))

    def update_player_bank_values(self):
        index_offset = 1
        for obj_tuple in self.text_obj_tuples:
            bank_text_obj, dado_text_obj, letter = obj_tuple
            bank_value = int(self.player_obj.get_player_bank()[index_offset])
            dado_value = int(self.player_obj.get_player_dado()[index_offset])

            bank_text_obj.set_num(bank_value)
            dado_text_obj.set_num(dado_value)

            index_offset += 2

        gold_value = self.player_obj.bank_lookup('gold')
        self.gold_text_obj.set_num(gold_value)



    def create_bank_and_dado_grid(self):
        bank_and_dado_row = []
        gem_icon_row = []

        for obj_tuple in self.text_obj_tuples:
            bank_text_obj, dado_text_obj, letter = obj_tuple

            bank_container = ft.Container(content=bank_text_obj.gui_obj, width=self.size, height=self.size,
                                          alignment=ft.alignment.center)
            dado_container = ft.Container(border_radius=PLAYER_BANK_ROUNDING_RADIUS,
                                          shadow=ft.BoxShadow(
                                              blur_radius=PLAYER_BANK_ROUNDING_RADIUS / 8,
                                              spread_radius=0,
                                              offset=ft.Offset(0, (PLAYER_BANK_ROUNDING_RADIUS / 8)),
                                              color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK)),
                                          clip_behavior=ft.ClipBehavior.ANTI_ALIAS,bgcolor=ft.Colors.with_opacity(SHADE_OPACITY, ft.Colors.GREY_100),
                                          content=dado_text_obj.gui_obj, width=self.size, height=self.size,
                                          alignment=ft.alignment.center)
            mini_row = ft.Row(spacing=1 , width=self.size * 2.1, height=self.size *1.05, controls=[bank_container, dado_container])
            bank_dado_container = ft.Container(border_radius=PLAYER_BANK_ROUNDING_RADIUS, alignment=ft.alignment.center, height=self.size*1.5,
                                          clip_behavior=ft.ClipBehavior.ANTI_ALIAS, content=mini_row, width=self.size*2.5,
                                          bgcolor=ft.Colors.with_opacity(.99, self.lookup[letter][0]))
            gem_icon_container = ft.Container(border_radius=PLAYER_BANK_ROUNDING_RADIUS, alignment=ft.alignment.center, height=self.size*.75,
                                          clip_behavior=ft.ClipBehavior.ANTI_ALIAS, content=self.lookup[letter][1], width=self.size*2.5)
            bank_and_dado_row.append(bank_dado_container)
            gem_icon_row.append(gem_icon_container)

        #  gold section
        gold_icon_container = ft.Container(border_radius=PLAYER_BANK_ROUNDING_RADIUS, alignment=ft.alignment.center, height=self.size*.75,
                                          clip_behavior=ft.ClipBehavior.ANTI_ALIAS, content=GOLD_COIN, width=self.size*2.5)
        gem_icon_row.append(gold_icon_container)

        gold_value_text_container =  ft.Container(content=self.gold_text_obj.gui_obj, width=self.size, height=self.size,
                                          alignment=ft.alignment.center)
        gold_value_container = ft.Container(border_radius=PLAYER_BANK_ROUNDING_RADIUS, alignment=ft.alignment.center, height=self.size*1.5,
                                          clip_behavior=ft.ClipBehavior.ANTI_ALIAS, content=gold_value_text_container, width=self.size*2.5,
                                          bgcolor=ft.Colors.with_opacity(.39, ft.Colors.GREY_50))
        bank_and_dado_row.append(gold_value_container)


        bank_and_dado_row_obj = ft.Row(controls=bank_and_dado_row, vertical_alignment=ft.alignment.center, alignment=ft.MainAxisAlignment.CENTER)
        gem_bank_row_obj = ft.Row(controls=gem_icon_row, vertical_alignment=ft.alignment.center, alignment=ft.MainAxisAlignment.CENTER)
        both_col = ft.Column(spacing=1, controls=[gem_bank_row_obj, bank_and_dado_row_obj], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
        return ft.Container(
            content=both_col,
            width=PLAYER_BANK_WIDTH,
            height=PLAYER_BANK_HEIGHT,
            border_radius=PLAYER_BANK_ROUNDING_RADIUS,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            shadow=ft.BoxShadow(
                blur_radius=PLAYER_BANK_ROUNDING_RADIUS / 2,
                spread_radius=0,
                offset=ft.Offset(0, (PLAYER_BANK_ROUNDING_RADIUS / 2)),
                color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK)
            ),
            alignment=ft.alignment.center)

    def set_shade(self):
        return ft.Container(
            width=PLAYER_BANK_WIDTH,
            height=PLAYER_BANK_HEIGHT,
            border_radius=PLAYER_BANK_ROUNDING_RADIUS,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            bgcolor=ft.Colors.GREY_50,
            opacity=SHADE_OPACITY,
            alignment=ft.alignment.center)

class PlayerReserved:
    def __init__(self, player_obj: player.Player):
        self.player_obj = player_obj
        self.container_row = [ft.Container(
            content=None,
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
            border_radius=PLAYER_BANK_ROUNDING_RADIUS,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            bgcolor=ft.Colors.with_opacity(.3, ft.Colors.GREY_50),
            alignment=ft.alignment.center) for _ in range(3)]

        self.row = ft.Row(controls=self.container_row, vertical_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.alignment.center)
        self.gui_obj = ft.Container(content=self.row, alignment=ft.alignment.center, width= CARD_WIDTH * 3.15)

    def update_player_reserved_cards(self):
        player_reserved_list = self.player_obj.get_player_reserved()

        if len(player_reserved_list) > 0:
            for card in player_reserved_list:
                for container in self.container_row:
                    if container.content is None:
                        container.content = GameCard(card).gui_obj
                        container.update()
                        break






