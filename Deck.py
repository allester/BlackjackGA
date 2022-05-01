import random

class Deck:
    def __init__(self, numDecks = 6):
        self.numDecks = numDecks
        self.shuffle = False
        self.deck = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4 * self.numDecks
        self.played = 0
        random.shuffle(self.deck)

    def draw(self):
        if len(self.deck) < 52 * 1.5:
            self.shuffle = True
        return self.deck.pop(-1)

    def shuffleDeck(self):
        self.deck = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4 * self.numDecks
        random.shuffle(self.deck)
        self.shuffle = False
        
    def getLength(self):
        return len(self.deck)