from time import sleep

import flet as ft
import cards
import gui_player_board
from gui_assets import CARD_ROUNDING_RADIUS
from PyGem import GameMaster
from cards import Card

def gui_reserve_card(game: GameMaster, card_to_reserve: Card):

    player = game.get_current_player()

    # mechanism with simulates the player taking the card and placing it in their reserve pile
    card_to_reserve.set_reserved_by(player._player_number)  # set the cards 'reserved by' property to the current player
    card_to_reserve.set_visible(False)  # make the reserved not visible (take it from table)
    game.get_next_card(card_to_reserve.get_level()).set_visible(
        True)  # take the next face-down card of that deck and make it visible (place it on table)
    player.add_to_reserved(card_to_reserve)  # add card to the player's 'reserved' property
    # taking a gold token
    game._bank.withdraw('gold')
    player.deposit_bank('gold')
    return "reserved card " + str(card_to_reserve)

def gui_can_afford(card_obj: cards.Card, gui_player: gui_player_board.GuiPlayer):
    return card_obj.can_afford(gui_player.player_obj.get_player_tender())

def highlight_buyable_cards(market_containers, gui_player):
    for row in market_containers:
        for card in row:
            card_container = card
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
        for card in row:
            card_container = card
            card_container.on_click = handler_func