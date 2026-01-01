import flet as ft

RED = '#E84D6F'
BLUE = '#5EB3E2'
GREEN = '#7CC454'
WHITE = '#D3EFFC'
NOIR = '#241C18'

# Card constants
GRID_SPACING = 1
CELL_SIZE = 40
CARD_HEIGHT = CELL_SIZE * 4.17
CARD_WIDTH = CARD_HEIGHT * .8
CARD_ROUNDING_RADIUS = CELL_SIZE * .32
SHADE_OPACITY = 0.2

# PlayerBoard constants
PLAYER_BANK_CELL_SIZE = CELL_SIZE * 1.086
PLAYER_BANK_HEIGHT = PLAYER_BANK_CELL_SIZE * 2.75
PLAYER_BANK_WIDTH = CARD_WIDTH * 5.35
PLAYER_BANK_ROUNDING_RADIUS = PLAYER_BANK_CELL_SIZE * .32


GEM_COLORS = [RED, BLUE, GREEN, WHITE, NOIR]

RED_GEM = ft.Image(src="/icons/ruby-red-diamond-inline.svg", fit=ft.ImageFit.CONTAIN)
BLUE_GEM = ft.Image(src="/icons/sapphire-octagon-inline.svg", fit=ft.ImageFit.CONTAIN)
GREEN_GEM = ft.Image(src="/icons/emerald-square-inline.svg", fit=ft.ImageFit.CONTAIN)
WHITE_GEM = ft.Image(src="/icons/diamond-blue-inline.svg", fit=ft.ImageFit.CONTAIN)
NOIR_GEM = ft.Image(src="/icons/obsidian-rectangle-inline.svg", fit=ft.ImageFit.CONTAIN)
GOLD_COIN = ft.Image(src="/icons/gold-coin-inline.svg", fit=ft.ImageFit.CONTAIN)
GEM_ICONS = [RED_GEM, BLUE_GEM, GREEN_GEM, WHITE_GEM, NOIR_GEM, GOLD_COIN]

GEM_LOOKUP = {"g" : (GREEN, GREEN_GEM, 'green'), "r" : (RED, RED_GEM, 'red'), "b" : (BLUE, BLUE_GEM, 'blue'), "w" : (WHITE, WHITE_GEM, 'white'), "n" : (NOIR, NOIR_GEM, 'noir')}




FG_WHITE = ft.Colors.WHITE
BG_BLACK = ft.Colors.BLACK38


FILLED_WITH_STROKE = ft.TextStyle(
    weight=ft.FontWeight.BOLD,
    foreground=ft.Paint(  # paint fill explicitly
        style=ft.PaintingStyle.FILL,
        color=FG_WHITE,
    ),
    shadow=[
        ft.BoxShadow(blur_radius=0, offset=ft.Offset(-1.25, 0), color=ft.Colors.BLACK),
        ft.BoxShadow(blur_radius=0, offset=ft.Offset( 1.25, 0), color=ft.Colors.BLACK),
        ft.BoxShadow(blur_radius=0, offset=ft.Offset( 0,-1.25), color=ft.Colors.BLACK),
        ft.BoxShadow(blur_radius=0, offset=ft.Offset( 0, 1.25), color=ft.Colors.BLACK),
    ]
)

class CircleWithNum:
    def __init__(self, num: int, size, color):
        self.num_text = ft.Text(str(num), font_family="lobster", style=FILLED_WITH_STROKE)
        self.gui_obj = ft.CircleAvatar(content=self.num_text, bgcolor=color)
        self.set_size(size)

    def set_size(self, new_size: int):
        self.gui_obj.radius = new_size
        self.num_text.size = new_size * 1.2
        if self.gui_obj.parent is not None:
            self.gui_obj.update()
        if self.num_text.parent is not None:
            self.num_text.update()

    def set_num(self, new_num: int):
        self.num_text.value = str(new_num)
        if self.gui_obj.parent is not None:
            self.gui_obj.update()

class NumWithStrokeCenter:
    def __init__(self, num: int, size):
        self.gui_obj = ft.Text(str(num), font_family="lobster", style=FILLED_WITH_STROKE, size=size*.75, width=size, height=size, text_align=ft.TextAlign.CENTER)

    def set_num(self, new_num: int):
        self.gui_obj.value = str(new_num)
        if self.gui_obj.parent is not None:
            self.gui_obj.update()