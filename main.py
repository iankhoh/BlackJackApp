import tkinter as tk   # python
from tkinter import *
from gameplay import *
from player import *

TITLE_FONT = ("Helvetica", 25, "bold")

class BlackJackApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.minsize(self, 400, 400)

        self.title("BlackJack App | created by Ian Khoh")
        self.geometry("500x550")

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

    def gridContainerInit(self, *args, **kwargs):
        self.container.pack_forget()
        self.container.grid_rowconfigure(10, weight=1)
        self.container.grid_columnconfigure(10, weight=1)
        self.container.grid()

    # Show a frame for the given page name
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def closeApp(self):
        self.destroy()

    def replayGame(self, controller):
        controller.once = "1"
        self.refrehGamePage(controller)

    def settingsGame(self, controller):
        self.show_frame("SetUpPage")

    def okButton(self, controller, name, var):
        self.name = str(name.get())
        self.option = str(var.get())
        self.gridContainerInit(controller)
        self.once = "1"

        self.refrehGamePage(controller)

    def hitMeButton(self, controller):
        user = controller.game.playerDict[controller.name]
        user.drawCard(controller.deck)

        self.refrehGamePage(controller)

    def doneButton(self, controller):
        controller.game.checkMatch(controller.deck)

        self.showCard = True
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
            self.gameInit(controller)
        self.guiInit(controller)

### ====== Add Players for the first init ====== ###
    def gameInit(self, controller):
        controller.once = "0"
        controller.showCard = False
        userName = controller.name
        option = controller.option

        # Add players to the game - depending on "Select Players" input
        game = gameplay()
        game.addPlayer("Dealer", "D")
        if option == "2":
            game.addPlayer("Player2")
        elif option == "3":
            game.addPlayer("Player2")
            game.addPlayer("Player3")

        game.addPlayer(userName, "NULL", True)

        # Get a deck of cards, shuffle them!
        host = cards()
        deck = host.generateDeck()
        host.shuffleDeck(deck)

        # game.startGame makes players draw 2 cards to begin with, including dealer
        game.startGame(deck)

        controller.passVal2controller(controller, game, deck)

### ====== GUI display settings ====== ###

    def guiInit(self, controller):
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
        if dealer.winner == False:
            dealerLabel = tk.Label(self, text=dealerName, font=TITLE_FONT, fg="red")
        elif dealer.winner == True:
            dealerLabel = tk.Label(self, text=dealerName, font=TITLE_FONT, fg="green")
        else:
            dealerLabel = tk.Label(self, text=dealerName, font=TITLE_FONT)

        dealerLabel.grid(row=2, column=0)

        for i in range (0, len(dealerOnHand)):
            if controller.showCard == True:
                dealerCards = tk.Label(self, text=dealerOnHand[i], bg="black", fg="white")
            else:
                dealerCards = tk.Label(self, text=dealerOnHand[i], bg="black", fg="black")
            dealerCards.grid(row=3, column=1+i, padx=(0,5), ipadx=5, ipady=15)


        # If user choose 2 players - add 1 more players (including himself)
        if option == "2":
            if p2.winner == False:
                p2 = tk.Label(self, text=p2name, font=TITLE_FONT, fg="red")
            elif p2.winner == True:
                p2 = tk.Label(self, text=p2name, font=TITLE_FONT, fg="green")
            else:
                p2 = tk.Label(self, text=p2name, font=TITLE_FONT)

            p2.grid(row=4, column=0)

            for i in range (0, len(p2OnHand)):
                if controller.showCard == True:
                    p2Cards = tk.Label(self, text=p2OnHand[i], bg="black", fg="white")
                else:
                    p2Cards = tk.Label(self, text=p2OnHand[i], bg="black", fg="black")
                p2Cards.grid(row=5, column=1+i, padx=(0,5), ipadx=5, ipady=15)


        # If user choose 3 players - add 2 more players (including himself)
        elif option == "3":
            # ===== Player 2 Display ===== #
            if p2.winner == False:
                p2 = tk.Label(self, text=p2name, font=TITLE_FONT, fg="red")
            elif p2.winner == True:
                p2 = tk.Label(self, text=p2name, font=TITLE_FONT, fg="green")
            else:
                p2 = tk.Label(self, text=p2name, font=TITLE_FONT)

            p2.grid(row=4, column=0)

            for i in range (0, len(p2OnHand)):
                if controller.showCard == True:
                    p2Cards = tk.Label(self, text=p2OnHand[i], bg="black", fg="white")
                else:
                    p2Cards = tk.Label(self, text=p2OnHand[i], bg="black", fg="black")
                p2Cards.grid(row=5, column=1+i, padx=(0,5), ipadx=5, ipady=15)



            # ===== Player 3 Display ===== #
            if p3.winner == False:
                p3 = tk.Label(self, text=p3name, font=TITLE_FONT, fg="red")
            elif p3.winner == True:
                p3 = tk.Label(self, text=p3name, font=TITLE_FONT, fg="green")
            else:
                p3 = tk.Label(self, text=p3name, font=TITLE_FONT)

            p3.grid(row=6, column=0)

            for i in range (0, len(p3OnHand)):
                if controller.showCard == True:
                    p3Cards = tk.Label(self, text=p3OnHand[i], bg="black", fg="white")
                else:
                    p3Cards = tk.Label(self, text=p3OnHand[i], bg="black", fg="black")
                p3Cards.grid(row=7, column=1+i, padx=(0,5), ipadx=5, ipady=15)

        # ===== Line ===== #

        line = tk.Label(self, text="_______________________________", font=TITLE_FONT)
        line.grid(row=19, column=0, pady=(5), columnspan=10)

        # ===== User Display ===== #
        if user.winner == False:
            userLabel = tk.Label(self, text=userName, font=TITLE_FONT, fg="red")
        elif user.winner == True:
            userLabel = tk.Label(self, text=userName, font=TITLE_FONT, fg="green")
        else:
            userLabel = tk.Label(self, text=userName, font=TITLE_FONT)

        userLabel.grid(row=20, column=0)

        for i in range (0, len(userOnHand)):
            userCards = tk.Label(self, text=userOnHand[i], bg="black", fg="white")
            userCards.grid(row=21, column=1+i, padx=(0,5), ipadx=5, ipady=15)

        # ===== Buttons Display ===== #
        hitMe = tk.Button(self, text="Hit Me",
                          command=lambda: controller.hitMeButton(controller))
        done = tk.Button(self, text="Stay",
                          command=lambda: controller.doneButton(controller))
        replayButton = tk.Button(self, text="Replay?",
                            command=lambda: controller.replayGame(controller))
        settingsButton = tk.Button(self, text="Settings",
                            command=lambda: controller.settingsGame(controller))
        closeButton = tk.Button(self, text="Quit",
                            command=lambda: controller.closeApp())

        hitMe.grid(row=22, column=1, pady=(25, 0))
        done.grid(row=22, column=2, pady=(25, 0))
        replayButton.grid(row=23, column=1, pady=(3,0))
        settingsButton.grid(row=23, column=2, pady=(3,0))
        closeButton.grid(row=24, column=1, columnspan=2, pady=(5,0))


if __name__ == "__main__":
    app = BlackJackApp()
    app.mainloop()