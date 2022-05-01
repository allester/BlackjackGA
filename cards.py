# cards.py
import random

class Card:

    def __init__(self, rank = None, suit = None):
        self.rank = rank
        self.suit = suit
        self.ranks = {
            2 : 2,
            3 : 3,
            4 : 4,
            5 : 5,
            6 : 6,
            7 : 7,
            8 : 8,
            9 : 9,
            10 : 10,
            "J" : 10,
            "Q" : 10,
            "K" : 10,
            "A" : 11 # or 1 this is accounted for in Hand class
        }
        self.suits = {
            'C' : 1,
            'D' : 2,
            'H' : 3,
            'S' : 4
        }

    def getRank(self):
        return self.rank
    
    def getSuit(self):
        return self.suit

class Deck:

    def __init__(self, n = 1):
        self.n = n
        self.ranks = {
            2 : 2,
            3 : 3,
            4 : 4,
            5 : 5,
            6 : 6,
            7 : 7,
            8 : 8,
            9 : 9,
            10 : 10,
            "J" : 10,
            "Q" : 10,
            "K" : 10,
            "A" : 11 # or 1 this is accounted for in Hand class
        }
        self.suits = {
            'C' : 1,
            'D' : 2,
            'H' : 3,
            'S' : 4
        }
        self.fullDeck = []
        for suit in self.suits:
            for rank in self.ranks:
                self.fullDeck.append(Card(rank,suit))
        self.currState = self.fullDeck
        self.deck = self.deck * n
        self.length = len(self.deck)
    
    def pop(self, i = -1):
        return self.currState.pop(i)

    def shuffle(self):
        indices = range(self.length)
        indices = random.sample(indices, self.length)
        self.currState = []
        for i in indices:
            self.currState.append(self.fullDeck[i])
        return self.currState


class Hand:

    def __init__(self):
        self.hand = []
        self.aces = 0

    def addCard(self, card):
        cardValue = card.ranks[card.getRank()]
        self.hand.append(card.getRank())
        if cardValue == 11:
            self.aces += 1

    def getValue(self):
        aces = self.aces
        value = sum(self.hand)
        if value > 21 and aces > 0:
            value -= 10
            aces -= 1
        return value

        
class Player:
    
    def __init__(self, numHands = 1):
        self.numHands = numHands
        self.hands = [Hand()] * numHands

    def getHands(self):
        return self.hands


class Table:

    def __init__(self, numPlayers = 1, numDecks = 6):
        self.numPlayers = numPlayers
        self.players = [Player()] * numPlayers
        self.deck = Deck(numDecks).shuffle()
    
    def play

    def deal(self):
        n = 2
        while n > 0:
            for player in self.players:
                for hand in player.getHands():
                    hand.addCard(self.deck.pop(-1))
            n -= 1

    def p