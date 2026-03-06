# column on the left side of the card market/player board which serves as the space for messages to the user and various
# buttons like the "commit button" which commits the turn for the user and switches to the next user
import flet as ft

import PyGem
import cards
import gui_cards
import gui_functions


class UserColumn:
    def __init__(self, game, back_func, end_turn_func, refresh_gui_func):
        self.game: PyGem.GameMaster = game
        self.refresh_gui = refresh_gui_func
        self.end_turn_button = ft.Button(content='End Turn', on_click=end_turn_func)
        self.back_button = ft.Button(content='Go Back', on_click = back_func)
        self.buy_button = ft.Button(content='Buy Card', on_click = gui_functions.gui_buy_card)
        self.reserve_button = ft.Button(content='Reserve Card', on_click = gui_functions.gui_reserve_card)
        self.gui_obj = ft.Container(width = 155, height = 500, content=ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    alignment=ft.MainAxisAlignment.SPACE_EVENLY, intrinsic_width=True))
        self.initial_message()

    def update_user_column(self):
        self.gui_obj.update()

    def initial_message(self):
        self.gui_obj.content.controls = ft.Text(value=('Click any card to reserve or buy (if you can afford it)\nor'
                                   '\nClick any gem in the bank to begin gem taking action'), text_align=ft.TextAlign.CENTER)

    def reserve_or_buy_card(self, card_obj, can_buy: bool):
        # Either render the card if it is a card or simply display top-of-deck message
        if card_obj in ['1', '2', '3']:
            cost_text = ''
            dado_text = ''
            display_card = ft.Text(f'Top of level {card_obj} deck', text_align=ft.TextAlign.CENTER)
        else:
            display_card = gui_cards.GameCard(card_obj).gui_obj
            cost_text = card_obj.get_cost()
            dado_text = card_obj.get_dado()

        # a tuple that contains the 2 args for the event handler [0] and [1], plus an event handler [2]
        event_payload = (card_obj, self.game, self.ready_to_end_turn)  # to be called by on_click handler
        self.reserve_button.data = event_payload  # "tucking" payload into the control so it can be used by the handler

        if can_buy:
            self.buy_button.data = event_payload # tucking payload for buying

        # fill column then conditionally make elements invisible if they are not available moves
        self.gui_obj.content.controls = [
            display_card,
            ft.Text('Reserve card and receive one gold', text_align=ft.TextAlign.CENTER),
            self.reserve_button,
            ft.Text('or', text_align=ft.TextAlign.CENTER),
            ft.Text(f'Buy card for {cost_text} and receive one {dado_text} dado', text_align=ft.TextAlign.CENTER),
            self.buy_button,
            ft.Text('or', text_align=ft.TextAlign.CENTER),
            self.back_button
        ]

        # make all elements visible in case they were made invisible last iteration
        for element in self.gui_obj.content.controls:
            element.visible = True
        self.gui_obj.content.controls[6].value = 'or' # change last message back to 'or'

        # now conditionally make elements invisible based on available moves
        index_to_be_invisible = []
        current_reserved = self.game.get_current_player().get_player_reserved()
        # if player has reserved the max # of cards or is trying to buy an already reserved card
        if len(current_reserved) == 3 or card_obj in current_reserved:
            index_to_be_invisible.extend([0,1,2,3])

        if not can_buy:  # if player cannot buy card
            if 3 in index_to_be_invisible:
                index_to_be_invisible.extend([4,5])
            else:
                index_to_be_invisible.extend([3,4,5])

        if len(index_to_be_invisible) == 6:  # if both reserve and buy are disabled/invisible, change last 'or'
            self.gui_obj.content.controls[6].value = 'No moves available'
        for index in index_to_be_invisible:
            self.gui_obj.content.controls[index].visible = False


    def ready_to_end_turn(self, last_move):
        self.refresh_gui()
        self.end_turn_button.data = last_move
        self.gui_obj.content.controls = [
            ft.Text('End turn to move on to next player', text_align=ft.TextAlign.CENTER),
            self.end_turn_button
        ]
