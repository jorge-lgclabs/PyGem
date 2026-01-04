import flet as ft

import PyGem
import cards

from gui_assets import RED, GREEN, BLUE, WHITE, NOIR
from gui_assets import RED_GEM, GREEN_GEM, BLUE_GEM, WHITE_GEM, NOIR_GEM, GEM_LOOKUP
from gui_assets import FILLED_WITH_STROKE
from gui_assets import CELL_SIZE, CARD_HEIGHT, CARD_WIDTH, CARD_ROUNDING_RADIUS, SHADE_OPACITY, GRID_SPACING
from gui_assets import CircleWithNum, NumWithStrokeCenter

class GameCard:
    def __init__(self, card_obj: cards.Card):
        self.lookup = GEM_LOOKUP
        self.card_obj = card_obj

        letter = card_obj.get_dado()
        level = card_obj.get_level()
        color_string = self.lookup[letter][2]
        bg_num = card_obj.bg_num

        self.card_cost = card_obj.get_cost()
        self.gem = self.lookup[letter][1]
        self.color = self.lookup[letter][0]
        self.points = card_obj.get_points()

        self.size = CELL_SIZE
        self.shade_container = self.set_shade(self.color)
        self.grid_container = self.create_card_grid()
        self.bg_img = self.set_bg(level, bg_num, color_string)
        self.gui_obj = ft.Stack(controls=[self.bg_img, self.shade_container, self.grid_container])
        self.build_card_contents()


    def create_card_grid(self):
        self.row_lists = []
        self.row_objects = []
        for i in range (4):
            row_list = []
            for j in range (3):
                row_list.append(ft.Container(width=self.size, height=self.size))
            self.row_lists.append(row_list)
            self.row_objects.append(ft.Row(controls=row_list, alignment=ft.MainAxisAlignment.CENTER, spacing=GRID_SPACING))
        column = ft.Column(controls=self.row_objects, alignment=ft.MainAxisAlignment.CENTER, spacing=GRID_SPACING)
        return ft.Container(
            content=column,
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
            border_radius=CARD_ROUNDING_RADIUS,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            shadow=ft.BoxShadow(
                blur_radius=CARD_ROUNDING_RADIUS / 2,
                spread_radius=0,
                offset=ft.Offset(0, (CARD_ROUNDING_RADIUS / 2)),
                color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK)
            ),
            alignment=ft.alignment.Alignment.CENTER)

    def set_bg(self, level, bg_num, gem_string):
        return ft.Image(src=f"/images/{gem_string}{level}-{bg_num}.png", border_radius=ft.border_radius.all(CARD_ROUNDING_RADIUS), fit=ft.BoxFit.COVER, width=CARD_WIDTH, height=CARD_HEIGHT)

    def set_shade(self, color):
        return ft.Container(
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
            border_radius=CARD_ROUNDING_RADIUS,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            bgcolor=color,
            opacity=SHADE_OPACITY,
            alignment=ft.alignment.Alignment.CENTER)

    def insert_cost_circle(self, color, price, count):
        if count == 0:
            self.row_lists[3][0].content = CircleWithNum(price, self.size * (28/50), color).gui_obj
        elif count == 1:
            self.row_lists[2][0].content = CircleWithNum(price, self.size * (28 / 50), color).gui_obj
        elif count == 2:
            self.row_lists[3][1].content = CircleWithNum(price, self.size * (28 / 50), color).gui_obj
        else:
            self.row_lists[2][1].content = CircleWithNum(price, self.size * (28 / 50), color).gui_obj


    def build_card_contents(self):
        # 'w3b0g2r2n0'
        count = 0
        index = 1
        while count < 4 and index <= 9:
            letter = self.card_cost[index-1]
            color = self.lookup[letter][0]
            if int(self.card_cost[index]) > 0:
                self.insert_cost_circle(color, int(self.card_cost[index]), count)
                count += 1
            index += 2

        if self.points > 0:
            self.row_lists[0][0].content = NumWithStrokeCenter(self.points, self.size * .8).gui_obj

        self.row_lists[0][2].content = self.gem

class CardMarket:
    def __init__(self,game: PyGem.GameMaster):
        self.game = game

        self.grid_0_0 = ft.Container(content=None)
        self.grid_0_1 = ft.Container(content=None)
        self.grid_0_2 = ft.Container(content=None)
        self.grid_0_3 = ft.Container(content=None)
        self.grid_1_0 = ft.Container(content=None)
        self.grid_1_1 = ft.Container(content=None)
        self.grid_1_2 = ft.Container(content=None)
        self.grid_1_3 = ft.Container(content=None)
        self.grid_2_0 = ft.Container(content=None)
        self.grid_2_1 = ft.Container(content=None)
        self.grid_2_2 = ft.Container(content=None)
        self.grid_2_3 = ft.Container(content=None)

        self.level_1_deck = self.create_level_deck(1)
        self.level_2_deck = self.create_level_deck(2)
        self.level_3_deck = self.create_level_deck(3)

        self.card_market_grid = ft.GridView(expand=1,runs_count=4,max_extent=CARD_WIDTH * 1.1,child_aspect_ratio=0.8,
                                            spacing=8,run_spacing=8, controls=
                                            [self.level_3_deck, self.grid_2_0, self.grid_2_1, self.grid_2_2,
                                             self.grid_2_3,
                                             self.level_2_deck, self.grid_1_0, self.grid_1_1, self.grid_1_2,
                                             self.grid_1_3,
                                             self.level_1_deck, self.grid_0_0, self.grid_0_1, self.grid_0_2,
                                             self.grid_0_3]
                                            )
        self.update_market_grid(first_run=True)

        self.gui_obj = ft.Container(content=self.card_market_grid, alignment=ft.alignment.Alignment.CENTER, width=CARD_WIDTH * 5.25)



    def update_market_grid(self, first_run=False):
        visible_card_grid_from_game = [[card for card in self.game.get_visible_cards(3)], [card for card in self.game.get_visible_cards(2)],
                                       [card for card in self.game.get_visible_cards(1)]]

        container_grid = [[self.grid_2_0, self.grid_2_1, self.grid_2_2, self.grid_2_3],
                          [self.grid_1_0, self.grid_1_1, self.grid_1_2, self.grid_1_3],
                          [self.grid_0_0, self.grid_0_1, self.grid_0_2, self.grid_0_3]]
        if first_run:
            for row in range(3):
                for card_pos in range(4):
                    container = container_grid[row][card_pos]
                    visible_card_obj_from_game = visible_card_grid_from_game[row][card_pos]
                    if container.data is None:
                        container.data = GameCard(visible_card_obj_from_game)
                        container.content = container.data.gui_obj
            return

        for row in range(3):
            row_from_game = visible_card_grid_from_game[row]
            container_row_from_gui = container_grid[row]
            row_from_gui = [container.data.card_obj for container in container_row_from_gui]
            if set(row_from_game) == set(row_from_gui):
                continue

            for card in row_from_game:
                if card not in row_from_gui:
                    new_card = card
            for container in container_row_from_gui:
                if container.data.card_obj not in row_from_game:
                    container.data = GameCard(new_card)
                    container.content = container.data.gui_obj
            break

    def create_level_deck(self, level: int):
        bg_img = ft.Image(src=f"/images/level-{level}-deck.png",
                 border_radius=ft.border_radius.all(CARD_ROUNDING_RADIUS), fit=ft.BoxFit.COVER, width=CARD_WIDTH,
                 height=CARD_HEIGHT, opacity=.42)
        if level == 1:
            text = "I"
        elif level == 2:
            text = "II"
        else:
            text = "III"

        text = ft.Text(value=text, size=CARD_HEIGHT * .5, text_align=ft.TextAlign.CENTER, font_family="lobster", style=FILLED_WITH_STROKE)

        return ft.Stack(controls=[bg_img, text], alignment=ft.alignment.Alignment.CENTER)

    def get_all_containers(self):
        return [[self.grid_2_0, self.grid_2_1, self.grid_2_2, self.grid_2_3],
                [self.grid_1_0, self.grid_1_1, self.grid_1_2, self.grid_1_3],
                [self.grid_0_0, self.grid_0_1, self.grid_0_2, self.grid_0_3]]
