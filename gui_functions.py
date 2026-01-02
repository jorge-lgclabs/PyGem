from time import sleep

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
    game.end_turn(("reserved card " + str(card_to_reserve)))
    return