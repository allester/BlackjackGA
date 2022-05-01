# Player.py

import pandas as pd

'''
This file contains the Player and Dealer Class
'''

class Player:
    def __init__(self, deck = None, genes = None):
        self.deck = deck
        self.genes = genes
        self.upcard = None #dealer's upcard
        self.hand = [[]]
        self.isHard = [True]
        self.value = [0]
        self.isBust = [False]
        self.isDouble = [False]
        self.chipCount = 0

    def hit(self, i):
        self.hand[i].append(self.deck.draw())
        self.value[i] = self.getValue(i)
        if self.value[i] > 21:
            self.isBust[i] = True

    def canSplit(self, i):
        if len(self.hand[i]) == 2:
            return self.hand[i][0] == self.hand[i][1]
        return False

    def split(self, i):
        self.hand.append([self.hand[i].pop(-1)])
        self.isHard.append(True)
        self.value[i] = self.getValue(i)
        self.value.insert(i+1, self.getValue(i))
        self.isBust.append(False)
        self.isDouble.append(False)

    def double(self, i):
        if len(self.hand[i]) == 2:
            self.hit(i)
            self.isDouble[i] = True
        else:
            self.hit(i)

    def getHands(self):
        return self.hand

    def getHand(self, i):
        return self.hand[i]

    def getValue(self, i):
        value = 0
        aces = 0

        for card in self.hand[i]:
            if card == 'A':
                aces += 1
                continue
            value += card

        isHard = True
        while value < 21 and aces > 0:
            if value <= 10:
                value += 11
                isHard = False
            else:
                value += 1
            aces -= 1
        self.isHard[i] = isHard
        
        return value

    def isBust(self, i):
        isBust = False
        if self.getValue(i) > 21:
            isBust = True
        return isBust

    def isBlackjack(self, i):
        if len(self.hand[i]) == 2 and self.value[i] == 21:
            return True
        return False

    def getAction(self, i):
        upcard = self.upcard
        if len(self.hand[i]) == 1:
            return 'H'

        if self.canSplit(i): # for split cases
            card = self.hand[i][0]
            row = str(card) + ', ' + str(card) # 'A, A' 

        elif 'A' in self.hand[i] and self.isHard[i] == False: # for soft aces cases
            noAceValue = self.value[i] - 11
            row = 'A, ' + str(noAceValue)

        else: # for hard cases
            row = self.value[i]

        #print(row)
        #print(upcard)
        return self.genes.loc[row, upcard]

    def play(self):
        upcard = self.upcard
        if upcard == 'A':
            upcard = 11
        n = len(self.hand)
        i = 0
        while i < n :
            while self.value[i] < 21:
                if len(self.hand[i]) == 1:
                    self.hit(i)
                    continue

                action = self.getAction(i)

                if action == 'Sp':
                    self.split(i)
                    print('Sp')
                    if self.hand[i][0] == 'A':
                        self.hit(i)
                        self.hit(i+1)
                        break
                    n += 1

                elif action == 'H':
                    print('H')
                    self.hit(i)

                elif action == 'D':
                    print('D')
                    self.double(i)
                    break

                else: # 'S'
                    print('S')
                    break
            #next hand 
            i += 1
    def pay(self, payout, minBet = 1):
        self.chipCount += payout * minBet

class Dealer(Player):
    def play(self):
        while self.getValue(0) < 17:
            self.hit(0)

    def upcard(self):
        return self.hand[0][0]
