# column on the left side of the card market/player board which serves as the space for messages to the user and various
# buttons like the "commit button" which commits the turn for the user and switches to the next user
import flet as ft

class UserColumn:
    def __init__(self, game):
        self.game = game

        self.end_turn_button = ft.Button(visible = False, content='End Turn')
        self.back_button = ft.Button(visible = False, content='Back')
        self.buy_button = ft.Button(visible = False, content='Buy Card')
        self.reserve_button = ft.Button(visible=False, content='Reserve Card')
        self.user_message = ft.Text(text_align=ft.TextAlign.CENTER)
        self.gui_obj = ft.Container(width = 155, height = 300, content=ft.Column(controls=[self.user_message],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN, intrinsic_width=True))
        self.initial_message()

    def update_user_column(self):
        self.gui_obj.update()

    def initial_message(self):
        self.end_turn_button.visible=False
        self.back_button.visible=False
        self.buy_button.visible=False
        self.reserve_button.visible=False

        self.user_message.value = ('Click any card to reserve or buy (if you can afford it)\nor'
                                   '\nClick any gem in the bank to begin gem taking action')