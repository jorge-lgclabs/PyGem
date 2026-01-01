
from PyGem import GameMaster, GameMasterError
import tkinter as tk



CARD_WIDTH = 100
CARD_HEIGHT = 140
PADDING = 10

class PyGemGUI:
    """Object that encompasses the GUI"""
    def __init__(self, root):
        self.root = root
        self.root.title("PyGem GUI")

        # Initialize game logic
        self.gm = GameMaster(gui=True)

        # Container frames
        self.board_frame = tk.Frame(root)
        self.board_frame.pack(padx=10, pady=10)
        self.action_frame = tk.Frame(root)
        self.action_frame.pack(padx=10, pady=5)
        self.status_frame = tk.Frame(root)
        self.status_frame.pack(padx=10, pady=5)

        # Action buttons
        self.create_action_buttons(['Buy a card', 'Reserve a card', 'Take tokens'], self.action_click_handler)
        self.draw_board()
        self.update_status()

    def draw_board(self):
        """Draws and re-draws the board of cards in the board_frame"""
        # Clear previous board
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        # Draw rows of cards (levels 3, 2, 1)
        for level in [3, 2, 1]:
            row_frame = tk.Frame(self.board_frame)
            row_frame.pack(pady=5)
            visible_cards = self.gm.get_visible_cards(level)
            for card in visible_cards:
                canvas = tk.Canvas(
                    row_frame,
                    width=CARD_WIDTH,
                    height=CARD_HEIGHT,
                    highlightthickness=1,
                    highlightbackground='black'
                )
                canvas.pack(side=tk.LEFT, padx=5)
                self.draw_card(canvas, card)


        # Display bank tokens
        tokens = ['white', 'blue', 'green', 'red', 'noir', 'gold']
        token_string = "Bank: "
        for color in tokens:
            token_string = token_string + '   ' + color.capitalize() + ': ' + str(self.gm._bank.get_token_num(color))
        tk.Label(self.board_frame, text=token_string).pack(pady=5)

    def draw_card(self, canvas, card):
        """Draws each individual card based on how many resources it costs, its dado, and how many points it gives"""
        # Create canvas rectangle (card)
        canvas.create_rectangle(0, 0, CARD_WIDTH, CARD_HEIGHT, fill='white', outline='black')

        # Set proper color name for dado circle
        dado_color = card.get_dado()
        if dado_color == 'w':
            dado_color = 'white'
        elif dado_color == 'b':
            dado_color = 'blue'
        elif dado_color == 'g':
            dado_color = 'green'
        elif dado_color == 'r':
            dado_color = 'red'
        else:
            dado_color = 'black'

        radius = 10  # set the radius for all ovals

        canvas.create_oval(   # create the oval representing the dado color in the top left
            PADDING, PADDING,
            PADDING + 2 * radius, PADDING + 2 * radius,
            fill=dado_color,
            outline='black'
        )

        # Create the points label in the top right
        points = card.get_points()
        if points > 0:
            canvas.create_text(
                CARD_WIDTH - PADDING, PADDING,
                text=str(points), anchor='ne'
            )

        # Create a list of just those resources that are part of the cost, and their cost
        cost_str = card.get_cost()
        cost_lookup = {1: 'white', 3: 'blue', 5: 'green', 7: 'red', 9: 'black'}
        costs = []
        for index, color in cost_lookup.items():
            amount = int(cost_str[index])
            if amount > 0:
                costs.append((color, amount))
        number_of_resources = len(costs)  # how many resources are in the cost

        # Placing the cost circles
        if number_of_resources == 1:  # when its just one resource, lower left corner
            color, price = costs[0]
            x = PADDING + radius
            y = CARD_HEIGHT - (2 * radius + 2)
            self.draw_cost_circle(canvas, x, y, radius, color, price)
        elif number_of_resources == 2:  # when its two resources, two stacked on top of each other lower left corner
            for index in [0, 1]:
                color, price = costs[index]
                x = PADDING + radius
                y = CARD_HEIGHT - (2 - index) * (2 * radius + 2)
                self.draw_cost_circle(canvas, x, y, radius, color, price)
        elif number_of_resources == 3:  # when its three resources, three stacked on top of each other, lower left corner
            for index in [0, 1, 2]:
                color, price = costs[index]
                x = PADDING + radius
                y = CARD_HEIGHT - (3 - index) * (2 * radius + 2)
                self.draw_cost_circle(canvas, x, y, radius, color, price)
        elif number_of_resources == 4:  # when its four resources, 2 stacks of 2, next to each other, lower left corner
            for index in [0, 1, 2, 3]:
                color, price = costs[index]
                col_offset = 0 if index < 2 else 1
                row_offset = index % 2
                x = PADDING + col_offset * (2 * radius + 5) + radius
                y = CARD_HEIGHT - (2 - row_offset) * (2 * radius + 2)
                self.draw_cost_circle(canvas, x, y, radius, color, price)

    def draw_cost_circle(self, canvas, x, y, r, color, price):
        """Helper function that draws the individual costs circles of the cost poriton of the card"""
        outline = 'black'
        canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline=outline)
        # Set text to white if the color of the circle is black (for visibility)
        text_fill = 'white' if color == 'black' else 'black'
        canvas.create_text(x, y, text=str(price), fill=text_fill)

    def create_action_buttons(self, labels: list, handler: object):
        """Receives a list of labels and a callable function which will be the "handler" of each distinct action, as represented by its label"""
        for label in labels:
            button = tk.Button(
                self.action_frame,
                text=label,
                command=lambda action=label: handler(action)  # lambda is used so that the call is not executed until the button is pressed, the action=label definition is to overcome the "late binding" issue
            )
            button.pack(side=tk.LEFT, padx=5)

    def action_click_handler(self, label):
        """Helper function that receives the button clicks of the different actions (buy, reserve, tokens)"""
        print(label)  # where the actions would be handled, to be implemented


    def update_status(self):
        """Draws and re-draws the information in the status_frame, which shows the current players status"""
        for widget in self.status_frame.winfo_children():
            widget.destroy() # clear status frame
        player = self.gm.get_current_player()
        status = (
            f" Player {player.get_player_number()} {player.get_player_name()}  | Points: {player.points}\n "
            f" White: tokens = {player.bank_lookup('white')} | dado = {player.dado_lookup('white')} | total = {int(player.bank_lookup('white')) + int(player.dado_lookup('white'))}\n"
            f" Blue: tokens = {player.bank_lookup('blue')} | dado = {player.dado_lookup('blue')} | total = {int(player.bank_lookup('blue')) + int(player.dado_lookup('blue'))}\n"
            f" Green: tokens = {player.bank_lookup('green')} | dado = {player.dado_lookup('green')} | total = {int(player.bank_lookup('green')) + int(player.dado_lookup('green'))}\n"
            f" Red: tokens = {player.bank_lookup('red')} | dado = {player.dado_lookup('red')} | total = {int(player.bank_lookup('red')) + int(player.dado_lookup('red'))}\n"
            f" Noir: tokens = {player.bank_lookup('noir')} | dado = {player.dado_lookup('noir')} | total = {int(player.bank_lookup('noir')) + int(player.dado_lookup('noir'))}\n"
            f" Gold = {player._gold}"
        )
        tk.Label(self.status_frame, text=status).pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = PyGemGUI(root)
    root.mainloop()
