from time import sleep

import flet as ft
import cards
import gui_player_board
from gui_assets import CARD_ROUNDING_RADIUS
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