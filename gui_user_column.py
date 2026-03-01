# column on the left side of the card market/player board which serves as the space for messages to the user and various
# buttons like the "commit button" which commits the turn for the user and switches to the next user
import flet as ft

import gui_cards
import gui_functions


class UserColumn:
    def __init__(self, game, back_func, end_turn_func):
        self.game = game
        self.end_turn_button = ft.Button(content='End Turn', on_click=end_turn_func)
        self.back_button = ft.Button(content='Go Back', on_click = back_func)
        self.buy_button = ft.Button(content='Buy Card')
        self.reserve_button = ft.Button(content='Reserve Card')
        self.user_message = ft.Text(text_align=ft.TextAlign.CENTER)
        self.gui_obj = ft.Container(width = 155, height = 350, content=ft.Column(controls=[self.user_message],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN, intrinsic_width=True))
        self.initial_message()

    def update_user_column(self):
        self.gui_obj.update()

    def initial_message(self):
        self.gui_obj.content.controls = [self.user_message]
        self.user_message.value = ('Click any card to reserve or buy (if you can afford it)\nor'
                                   '\nClick any gem in the bank to begin gem taking action')



    def reserve_card_only(self, card_container):
        card_obj = card_container.data.card_obj
        # a tuple that contains the 2 args for the event handler [0] and [1], plus an event handler [2]
        event_payload = (card_obj, self.game, self.ready_to_end_turn)  # to be called by on_click handler
        self.gui_obj.content.controls.insert(0, card_container)
        self.gui_obj.content.controls.append(self.reserve_button)
        self.gui_obj.content.controls.append(ft.Text('or', text_align=ft.TextAlign.CENTER))
        self.gui_obj.content.controls.append(self.back_button)

        self.user_message.value = "Reserve card and receive one gold"
        self.reserve_button.data = event_payload # "tucking" payload into the control so it can be used by the handler
        self.reserve_button.on_click = gui_functions.gui_reserve_card

    def reserve_or_buy_card(self, card_container):
        card_obj = card_container.data.card_obj
        self.gui_obj.content.controls.insert(0, card_container)

    def ready_to_end_turn(self, last_move):
        self.gui_obj.content.controls = [
            ft.Text('End turn to move on to next player', text_align=ft.TextAlign.CENTER),
            self.end_turn_button
        ]
        print(last_move)
