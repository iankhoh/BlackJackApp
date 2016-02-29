import tkinter as tk   # python
from gameplay import *
from player import *

TITLE_FONT = ("Helvetica", 25, "bold")

class BlackJackApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.minsize(self, 350, 350)

        self.title("BlackJack App | created by Ian Khoh")
        self.geometry("500x500")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (WelcomePage, SetUpPage):
            page_name = F.__name__
            frame = F(self.container, self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomePage")

    # Show a frame for the given page name
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def closeApp(self):
        self.destroy()

    def replayGame(self, controller):
        controller.once = "1"
        self.refrehGamePage(controller)

    def okButton(self, controller, name, var):
        self.name = str(name.get())
        self.option = str(var.get())
        self.once = "1"

        self.refrehGamePage(controller)

    def hitMeButton(self, controller):
        user = controller.game.playerDict[controller.name]
        user.drawCard(controller.deck)

        self.refrehGamePage(controller)

    def doneButton(self, controller):
        controller.game.checkMatch(controller.deck)

        self.refrehGamePage(controller)

    def refrehGamePage(self, controller):
        page_name = GamePage.__name__
        frame = GamePage(self.container, controller)
        self.frames[page_name] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        controller.show_frame("GamePage")

    def passVal2controller(self, controller, game, deck):
        self.game = game
        self.deck = deck

class WelcomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to Ultimate BlackJack!", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=30)


        button1 = tk.Button(self, text="Start Game", bg="blue",
                            command=lambda: controller.show_frame("SetUpPage"))
        button2 = tk.Button(self, text="Quit",
                            command=lambda: controller.closeApp())
        button1.pack(ipadx=50, ipady=40)
        button2.pack(pady=10)

        button1.config(font=('copper black', 20, 'bold'))

class SetUpPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="What is your name?", font=TITLE_FONT)
        name = tk.Entry(self, bd =5)

        label.pack(side="top", fill="x", pady=10)
        name.pack(ipadx=10, pady=5)

        #######

        label = tk.Label(self, text="Select Player(s)", font=TITLE_FONT)

        var = tk.StringVar()
        var.set("1") # initial value

        option = tk.OptionMenu(self, var, "1", "2", "3")

        label.pack(fill="x", pady=10)
        option.pack()

        ########

        button = tk.Button(self, text="OK",
                           command=lambda: controller.okButton(controller, name, var))
        button.pack(pady=40)


class GamePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # 'controller.once' determines if it's the first init.
        # If it is (="1"), add players + generate card decks + draw cards,
        # or else continue with the game with existing players and cards
        if controller.once == "1":
            self.addPlayer(controller)
        self.gameInit(controller)

### ====== Add Players for the first init ====== ###
    def addPlayer(self, controller):
        controller.once = "0"
        userName = controller.name
        option = controller.option

        # Add players to the game - depending on "Select Players" input
        game = gameplay()
        game.addPlayer("Dealer", "D")
        game.addPlayer(userName, "NULL", True)
        if option == "2":
            game.addPlayer("Player2")
        elif option == "3":
            game.addPlayer("Player2")
            game.addPlayer("Player3")

        # Get a deck of cards, shuffle them!
        host = cards()
        deck = host.generateDeck()
        host.shuffleDeck(deck)

        # game.startGame makes players draw 2 cards to begin with, including dealer
        game.startGame(deck)

        controller.passVal2controller(controller, game, deck)

### ====== GUI display settings ====== ###

    def gameInit(self, controller):
        userName = controller.name
        option = controller.option

        game = controller.game
        deck = controller.deck

        dealer = game.playerDict["Dealer"]
        dealerName = dealer.name
        dealerOnHand = dealer.onHand

        user = game.playerDict[userName]
        userOnHand = user.onHand

        if option == "2":
            p2 = game.playerDict["Player2"]
            p2name = p2.name
            p2OnHand = p2.onHand

        elif option == "3":
            p2 = game.playerDict["Player2"]
            p2name = p2.name
            p2OnHand = p2.onHand
            p3 = game.playerDict["Player3"]
            p3name = p3.name
            p3OnHand = p3.onHand

        # Default display - Dealer and User display
        # ===== Dealer Display ===== #
        if dealer.cardBurst == True:
            dealerLabel = tk.Label(self, text=dealerName, font=TITLE_FONT, fg="red")
        elif dealer.winner == True:
            dealerLabel = tk.Label(self, text=dealerName, font=TITLE_FONT, fg="green")
        else:
            dealerLabel = tk.Label(self, text=dealerName, font=TITLE_FONT)

        dealerCards = tk.Label(self, text=dealerOnHand)

        # ===== User Display ===== #
        if user.cardBurst == True:
            userLabel = tk.Label(self, text=userName, font=TITLE_FONT, fg="red")
        elif user.winner == True:
            userLabel = tk.Label(self, text=userName, font=TITLE_FONT, fg="green")
        else:
            userLabel = tk.Label(self, text=userName, font=TITLE_FONT)

        userCards = tk.Label(self, text=userOnHand)


        dealerLabel.pack(side="top", fill="x")
        dealerCards.pack(fill="x")


        # If user choose 2 players - add 1 more players (including himself)
        if option == "2":
            if p2.cardBurst == True:
                p2 = tk.Label(self, text=p2name, font=TITLE_FONT, fg="red")
            elif p2.winner == True:
                p2 = tk.Label(self, text=p2name, font=TITLE_FONT, fg="green")
            else:
                p2 = tk.Label(self, text=p2name, font=TITLE_FONT)

            p2Cards = tk.Label(self, text=p2OnHand)

            p2.pack(fill="x")
            p2Cards.pack(fill="x")


        # If user choose 3 players - add 2 more players (including himself)
        elif option == "3":
            # ===== Player 2 Display ===== #
            if p2.cardBurst == True:
                p2 = tk.Label(self, text=p2name, font=TITLE_FONT, fg="red")
            elif p2.winner == True:
                p2 = tk.Label(self, text=p2name, font=TITLE_FONT, fg="green")
            else:
                p2 = tk.Label(self, text=p2name, font=TITLE_FONT)

            p2Cards = tk.Label(self, text=p2OnHand)

            p2.pack(fill="x")
            p2Cards.pack(fill="x")

            # ===== Player 3 Display ===== #
            if p3.cardBurst == True:
                p3 = tk.Label(self, text=p3name, font=TITLE_FONT, fg="red")
            elif p3.winner == True:
                p3 = tk.Label(self, text=p3name, font=TITLE_FONT, fg="green")
            else:
                p3 = tk.Label(self, text=p3name, font=TITLE_FONT)

            p3Cards = tk.Label(self, text=p3OnHand)

            p3.pack(fill="x")
            p3Cards.pack(fill="x")


        # ===== Buttons Display ===== #

        hitMe = tk.Button(self, text="Hit Me",
                          command=lambda: controller.hitMeButton(controller))
        done = tk.Button(self, text="Done",
                          command=lambda: controller.doneButton(controller))
        replayButton = tk.Button(self, text="Replay?",
                            command=lambda: controller.replayGame(controller))
        closeButton = tk.Button(self, text="Quit",
                            command=lambda: controller.closeApp())


        userLabel.pack(fill="x", pady=(50, 0))
        userCards.pack(fill="x")

        hitMe.pack(pady=(20, 0))
        done.pack()
        replayButton.pack()
        closeButton.pack()


if __name__ == "__main__":
    app = BlackJackApp()
    app.mainloop()