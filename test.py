from cards import *
from gameplay import *
from player import player

def main():
    dealer = cards()
    deck = dealer.generateDeck()
    dealer.shuffleDeck(deck)

    game = gameplay()
    game.addPlayer('Jack', dealer='dealer')
    game.addPlayer('James')
    game.addPlayer('Bob')
    game.startGame(deck)

    game.checkMatch(deck)


if __name__ == "__main__": main()