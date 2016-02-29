from sys import version_info
import sys
from player import *
import operator


class gameplay:

    def __init__(self):
        self.totalPlayers = []
        self.playerDict = {}
        self.winner = ""

    def addPlayer(self, name, dealer="NULL", userRight=False):
        playerObj = player(name, dealer, userRight)
        self.playerDict[playerObj.name] = playerObj
        self.totalPlayers.append(playerObj)

        print ("Player " + playerObj.name + " is added to the game.")

    def removePlayer(self, obj):
        if obj in self.totalPlayers:
            self.totalPlayers.remove(obj)

    def startGame(self, deck):
        print("\n**** Game Start! ****\n")
        for i in range (2):
            for j in self.totalPlayers:
                j.drawCard(deck)

        for k in self.totalPlayers:
            temp = str(k.totalOnHand)
            print("%s cards adds up to be %s" % (k.name, temp))

    def checkMatch(self,deck):
        compareValue = {}
        for i in self.totalPlayers:
            while (i.totalOnHand < 15 and i.userRight == False):
                i.drawCard(deck)
            if i.totalOnHand > 21:
                i.cardBurst = True
            else:
                compareValue[i.name] = i.totalOnHand

        if len(compareValue)!=0:
                sorted_x = sorted(compareValue.items(), key=operator.itemgetter(1), reverse=True)
                print (sorted_x)
                self.winner = ((sorted_x)[0])[0]
                self.playerDict[self.winner].winner = True
        else:
            self.winner = ""

        print (self.winner)


        # play = input("Play Ultimate BlackJack? \nInput anything to continue OR Input 'no' to quit game: ")
        #
        # if (play.lower()!="no"):
        #     print("Game Start!")
        #     for i in range (2):
        #         for j in self.totalPlayers:
        #             j.drawCard(deck)
        #
        #     for k in self.totalPlayers:
        #         temp = str(k.totalOnHand)
        #         print("\n%s cards adds up to be %s" % (k.name, temp))
        # else:
        #     sys.exit("Quit Game")




        # py3 = version_info[0] > 2 #creates boolean value for test that Python major version > 2
        #
        # if py3:
        #   print("Game Started. \nYour cards adds up to be %" % player.totalOnHand)
        # else:
        #   print("Game Started. \nYour cards adds up to be %" % player.totalOnHand)
