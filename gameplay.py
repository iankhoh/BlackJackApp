from player import *

class gameplay:

    def __init__(self):
        self.totalPlayers = []
        self.playerDict = {}
        self.winner = ""

    def addPlayer(self, name, dealer="NULL", userRight=False):
        playerObj = player(name, dealer, userRight)
        self.playerDict[playerObj.name] = playerObj
        self.totalPlayers.append(playerObj)

        print ("Player '%s' is added to the game." % playerObj.name)

    def removePlayer(self, obj):
        if obj in self.totalPlayers:
            self.totalPlayers.remove(obj)

    def startGame(self, deck):
        print("\n**** Game Start! ****\n")
        cards.numbersRep['A'] = 11
        for i in range (2):
            for j in self.totalPlayers:
                j.drawCard(deck)


        for k in self.totalPlayers:
            if (self.playerDict[k.name].userRight != False):
                temp = str(k.totalOnHand)
                print("%s's cards adds up to be %s" % (k.name, temp))

    def checkMatch(self,deck):
        print ("\n** Results **")

        # Players who has card value lower than 16, will keep drawing until totalOnHand >= 16.
        for i in self.totalPlayers:
            while (i.totalOnHand < 16 and i.userRight == False):
                i.drawCard(deck)

        # Gets dealer's totalOnHand card value to compare with players
        dealer = self.playerDict["Dealer"]
        dealerOnHand = dealer.totalOnHand
        print ("Dealer: %s" % dealerOnHand)


        # If dealer has more than 21, players gets
        # tied by having > 21
        # or win by having < 21
        if dealerOnHand > 21:
            dealer.cardBurst = True
            for i in self.totalPlayers:
                if (i.dealer == "NULL"):
                    if i.totalOnHand > 21:
                        i.cardBurst = True
                        i.winner = "Tie"
                        print ("%s: %s - TIE! (card burst)" % (i.name, i.totalOnHand))

                    else:
                        i.winner = True
                        print ("%s: %s - WON!" % (i.name, i.totalOnHand))

        # If dealer does not exceed 21, validate players
        # Win, Lose, or Tie
        else:
            for i in self.totalPlayers:
                if (i.dealer == "NULL"):
                    if i.totalOnHand > 21:
                        i.winner = False
                        print ("%s: %s - LOST! (card burst)" % (i.name, i.totalOnHand))
                    elif i.totalOnHand > dealerOnHand:
                        i.winner = True
                        print ("%s: %s - WON!" % (i.name, i.totalOnHand))
                    elif i.totalOnHand == dealerOnHand:
                        i.winner = "Tie"
                        print ("%s: %s - TIED!" % (i.name, i.totalOnHand))
                    else:
                        i.winner = False
                        print ("%s: %s - LOST!" % (i.name, i.totalOnHand))


        print ("________________________\n")