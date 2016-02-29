import math
from cards import *

class player:

    def __init__(self, name, dealer="NULL", userRight=False):
        self.name = name
        self.dealer = dealer
        self.onHand = []
        self.totalOnHand = 0
        self.userRight = userRight
        self.cardBurst = False
        self.winner = False

    def drawCard(self, deck):
        drawnCard = deck.pop(0)
        self.onHand.append(drawnCard)
        cardNum = int(cards.numbersRep['%s' % drawnCard[0]])
        self.totalOnHand += cardNum
