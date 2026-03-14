# column on the left side of the card market/player board which serves as the space for messages to the user and various
# buttons like the "commit button" which commits the turn for the user and switches to the next user
import flet as ft
from flet.controls.border_radius import horizontal

import PyGem
import cards
import gui_cards
import gui_functions
import gui_game_master
import player
from gui_assets import GEM_LOOKUP, CARD_ROUNDING_RADIUS, MessageToken, CircleWithNum, SquareWithNum, GOLD_COIN, \
    SHADE_OPACITY


class PlayerBankBar:
    def __init__(self, player_obj: player.Player):
        self.player_obj = player_obj
        self.dado_row = ft.Row(vertical_alignment=ft.CrossAxisAlignment.START,
                               alignment=ft.MainAxisAlignment.SPACE_EVENLY)
        self.dado_container = ft.Container(content=self.dado_row, height=14)
        self.tokens_row = ft.Row(vertical_alignment=ft.CrossAxisAlignment.START,
                               alignment=ft.MainAxisAlignment.SPACE_EVENLY)
        self.tokens_container = ft.Container(content=self.tokens_row, height=19)
        self.dado_token_column = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                           alignment=ft.MainAxisAlignment.START, spacing=.2,
                                           controls=[self.dado_container, self.tokens_container])
        self.player_label = ft.Text(text_align=ft.TextAlign.LEFT, size=15)
        self.full_column = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                     alignment=ft.MainAxisAlignment.START,
                                     controls=[self.player_label, self.dado_token_column])
        self.gui_obj = ft.Container(content=self.full_column, border_radius=CARD_ROUNDING_RADIUS,
                                    bgcolor=ft.Colors.with_opacity(.1, ft.Colors.GREY_50))
        self.fill_player_bank_bar()

    def fill_player_bank_bar(self):
        name = self.player_obj.get_player_name()
        score = self.player_obj.points
        self.player_label.value=f'{name} - Points: {score}'
        colors = ['white', 'blue', 'green', 'red', 'noir']
        for color in colors:
            dado_num = self.player_obj.dado_lookup(color)
            dado_circle = SquareWithNum(dado_num, 8, color)
            self.dado_row.controls.append(dado_circle.gui_obj)
            bank_num = self.player_obj.bank_lookup(color)
            self.tokens_row.controls.append(ft.Text(bank_num, size=15))

        self.dado_row.controls.append(ft.Container(content=GOLD_COIN, height=12, width=12, alignment=ft.Alignment.CENTER))
        self.tokens_row.controls.append(ft.Text(self.player_obj.bank_lookup('gold'), size=15))

    def refresh_player_bank_bar(self):
        self.dado_row.controls.clear()
        self.tokens_row.controls.clear()
        self.fill_player_bank_bar()



class UserColumn:
    def __init__(self, game, back_func, end_turn_func, refresh_gui_func, giveback_func):
        self.game: PyGem.GameMaster = game
        self.refresh_gui = refresh_gui_func
        self.giveback_func = giveback_func
        self.end_turn_button = ft.Button(content='End Turn', on_click=end_turn_func)
        self.back_button = ft.Button(content='Go Back', on_click = back_func)
        self.buy_button = ft.Button(content='Buy Card', on_click = gui_functions.gui_buy_card)
        self.reserve_button = ft.Button(content='Reserve Card', on_click = gui_functions.gui_reserve_card)
        self.message_column = ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    alignment=ft.MainAxisAlignment.SPACE_EVENLY, intrinsic_width=True)
        self.top_spacer = ft.Container(width=155, height=133)
        self.message_container = ft.Container(width=155, height=500, content=self.message_column)
        self.middle_spacer = ft.Container(width=155, height=60)
        self.player_scores_column = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    alignment=ft.MainAxisAlignment.START, spacing=7, intrinsic_width=True)
        self.player_scores_container = ft.Container(width=155, height=290, content=self.player_scores_column)
        self.full_column = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    alignment=ft.MainAxisAlignment.START, intrinsic_width=True,
                                     controls=[
                                         self.top_spacer, self.message_container, self.middle_spacer, self.player_scores_container
                                     ])
        self.gui_obj = ft.Container(width = 155, height = 1010, content=self.full_column)
        self.initial_message()
        self.fill_player_scores()

    def update_user_column(self):
        self.refresh_player_scores()
        self.gui_obj.update()

    def initial_message(self):
        self.message_column.controls = [ft.Text(value=('Click any card to reserve or buy (if you can afford it)\nor'
                                   '\nClick any gem in the bank to begin gem taking action'), text_align=ft.TextAlign.CENTER)]

    def fill_player_scores(self):
        self.player_score_objs = []
        for player in self.game._players:
            player_score_obj = PlayerBankBar(player)
            self.player_score_objs.append(player_score_obj)
            self.player_scores_column.controls.append(player_score_obj.gui_obj)

    def refresh_player_scores(self):
        for bar in self.player_score_objs:
            bar.refresh_player_bank_bar()

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
        self.message_column.controls = [
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
        for element in self.message_column.controls:
            element.visible = True
        self.message_column.controls[6].value = 'or' # change last message back to 'or'

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
            self.message_column.controls[6].value = 'No moves available'
        for index in index_to_be_invisible:
            self.message_column.controls[index].visible = False

    def token_taking_messages(self, first_take, second_take=None, third_take=None, end=False, giveback=0):
        self.message_column.controls = [
            ft.Text(f'First gem taken:', text_align=ft.TextAlign.CENTER),
            MessageToken(first_take).gui_obj
        ]
        if second_take:
            self.message_column.controls.extend([
                ft.Text(f'Second gem taken:', text_align=ft.TextAlign.CENTER),
                MessageToken(second_take).gui_obj]
            )
        if third_take:
            self.message_column.controls.extend([
                ft.Text(f'Third gem taken:', text_align=ft.TextAlign.CENTER),
                MessageToken(third_take).gui_obj]
            )
        if not end:
            self.message_column.controls.append(
                ft.Text(f'Click another gem to continue gem-taking action', text_align=ft.TextAlign.CENTER)
            )
        else:
            final_move_tuple = (first_take, second_take)
            if third_take:
                final_move_tuple += (third_take,)

            if giveback > 0:
                event_payload = [final_move_tuple, giveback, self.game.take_tokens, self.giveback_func]
                self.message_column.controls.extend([
                    ft.Text(f"Warning: you will have to return {giveback} tokens to the bank after committing", text_align=ft.TextAlign.CENTER),
                    ft.Button(content='Commit move', data=event_payload, on_click=gui_functions.gui_commit_token_take_and_giveback)
                ])
            else:
                event_payload = [final_move_tuple, self.game.take_tokens, self.ready_to_end_turn]
                self.message_column.controls.append(
                    ft.Button(content='Commit move', data=event_payload, on_click=gui_functions.gui_commit_token_take)
            )
        self.message_column.controls.extend([
            ft.Text('or', text_align=ft.TextAlign.CENTER),
            self.back_button]
        )

    def token_giveback_messages(self,giveback_options, iteration=3):
        column = self.message_column.controls
        column.clear()
        iter_text = {1 : 'first', 2 : 'second', 3 : 'third'}
        column.append(ft.Text(f'Select your {iter_text[iteration]} gem to give back to the bank:', text_align=ft.TextAlign.CENTER))
        buttons = []
        for color in giveback_options:
            button = MessageToken(color).gui_obj
            button.data = color
            button.on_click = self.giveback_func
            buttons.append(button)

        column.extend(buttons)


    def ready_to_end_turn(self, last_move):
        self.refresh_gui()
        self.end_turn_button.data = last_move
        self.message_column.controls = [
            ft.Text('End turn to move on to next player', text_align=ft.TextAlign.CENTER),
            self.end_turn_button
        ]
