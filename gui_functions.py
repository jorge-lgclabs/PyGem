from time import sleep

import flet as ft
import cards
import gui_player_board
from gui_assets import CARD_ROUNDING_RADIUS, CARD_WIDTH
from PyGem import GameMaster

def gui_reserve_card(e):
    card_to_reserve, game, ready_end_turn = e.control.data
    player = game.get_current_player()

    ready_end_turn(game.reserve_card(player=player, is_gui=True, incoming_card=card_to_reserve))

def gui_buy_card(e):
    card_to_buy, game, ready_end_turn = e.control.data
    player = game.get_current_player()

    ready_end_turn(game.buy_card(player=player, is_gui=True, incoming_card_obj=card_to_buy))


def gui_can_afford(card_obj: cards.Card, gui_player: gui_player_board.GuiPlayer):
    return card_obj.can_afford(gui_player.player_obj.get_player_tender())

def highlight_buyable_cards(market_containers, gui_player):
    for row in market_containers:
        for card in row:
            card_container = card
            if card_container.data in ['I', 'II', 'III']:  # if card is top-of-deck, ignore it
                continue
            card_obj = card_container.data.card_obj
            if gui_can_afford(card_obj, gui_player):
                card_container.border = ft.border.all(3, ft.Colors.GREEN_500)
                card_container.border_radius = CARD_ROUNDING_RADIUS

def unhighlight_all_cards(market_containers):
    for row in market_containers:
        for card in row:
            card_container = card
            card_container.border = None
            # card_container.border_radius = CARD_ROUNDING_RADIUS

def make_cards_clickable(market_containers, handler_func):
    for row in market_containers:
        for card_container in row:
            card_container.on_click = handler_func
            if card_container.parent is not None:
                card_container.update()


def make_cards_unclickable(market_containers):
    for row in market_containers:
        for card_container in row:
            card_container.on_click = None
            card_container.update()

def highlight_and_make_clickable_reserved_cards(reserved_containers, handler_func):
    for card_container in reserved_containers:
        card_container.on_click = handler_func
        card_container.border = ft.border.all(3, ft.Colors.GREEN_500)
        card_container.border_radius = CARD_ROUNDING_RADIUS

def unhighlight_and_make_unclickable_reserved_cards(reserved_containers):
    for card_container in reserved_containers:
        card_container.on_click = None
        card_container.border = None

def gui_commit_token_take(e):
    to_take_tuple, take_token_func, end_turn_func = e.control.data
    to_take_list = list(to_take_tuple)
    move = take_token_func(is_gui=True, to_take=to_take_list)
    end_turn_func(last_move=move)

def gui_commit_token_take_and_giveback(e):
   to_take_tuple, giveback, take_token_func, giveback_func = e.control.data
   to_take_list = list(to_take_tuple)
   move = take_token_func(is_gui=True, to_take=to_take_list)
   giveback_func(e=None, giveback=giveback, last_move=move)

def opening_screen(start_game_func):

    def start_handler(e):
        menu_column = e.control.parent
        player_list = []
        for element in menu_column.controls:
            if isinstance(element, ft.TextField):
                name = element.value.strip()
                if name == '':
                    name = element.label[17:]
                player_list.append(name)
        start_game_func(player_list)

    def select_handler(e):
        selected_value = e.control.value
        menu_column = e.control.parent
        to_remove = []
        for element in menu_column.controls:
            if isinstance(element, ft.TextField):
                to_remove.append(element)
        for element in to_remove:
            menu_column.controls.remove(element)


        for x in range(1,int(selected_value)+1):
            insert_pos = x+2
            menu_column.controls.insert(insert_pos, ft.TextField(label=f'Enter the name of player {x}'))

        menu_column.update()

    container = ft.Container()
    column = ft.Column(alignment=ft.MainAxisAlignment.START,
                       horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                       width=CARD_WIDTH * 2,
                       height=800,
                       spacing=40)
    container.content = column
    column.controls.append(ft.Container(height=200))
    column.controls.append(ft.Text("Select the number of players:", text_align=ft.TextAlign.CENTER))
    dropdown = ft.Dropdown(autofocus=True,
                       options=[
                           ft.DropdownOption(key='2', text='2'),
                           ft.DropdownOption(key='3', text='3'),
                           ft.DropdownOption(key='4', text='4')
                       ],
                        value='2',
                        on_select=select_handler)
    column.controls.append(dropdown)
    column.controls.append(ft.TextField(label='Enter the name of Player 1'))
    column.controls.append(ft.TextField(label='Enter the name of Player 2'))
    column.controls.append(ft.Button("Start Game", on_click=start_handler))

    return container

def winning_screen(player_scores: list, page, start_func):
    def restart_game(page, start_func):
        page.controls.clear()
        page.overlay.clear()
        page.add(opening_screen(start_func))

    def score_sort(e):
        return e[1]

    results = ''
    player_scores.sort(key=score_sort)
    winner = player_scores[0][0]

    for score in player_scores:
        results += f'{score[0]} = {score[1]}\n'

    container = ft.Container(height=500, width=650, bgcolor=ft.Colors.GREY_800, alignment=ft.Alignment.CENTER, border_radius=40)
    winner_text = ft.Text(f'{winner} has won!',
                   text_align=ft.TextAlign.CENTER, size=40)
    result_text = ft.Text(f'{results}', text_align=ft.TextAlign.CENTER, size=25)
    button = ft.Button('Play again', on_click=lambda: restart_game(page, start_func))


    container.content = ft.Column([winner_text, result_text, button], alignment=ft.MainAxisAlignment.SPACE_EVENLY, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    full_page_container = ft.Container(alignment=ft.Alignment.CENTER, content=container, width=page.width, height=page.height)
    page.overlay.append(full_page_container)
    page.update()