#Blackjack.py
import random

class Deck:
    def __init__(self, numDecks = 6):
        self.shuffle = False
        self.deck = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4 * numDecks
        self.played = 0
        random.shuffle(self.deck)

    def draw(self):
        if len(self.deck) < 52 * 1.5:
            self.shuffle = True
        return self.deck.pop(-1)

    def shuffle(self):
        random.shuffle(self.deck)
        
    def getLength(self):
        return len(self.deck)

class Player:
    def __init__(self, deck):
        self.deck = deck
        self.hand = [[]]
        self.isHard = [True]
        self.value = [0]
        self.isBust = [False]
        self.isDouble = [False]
        self.isSplit = False

    def hit(self, i):
        self.hand[i].append(self.deck.draw())
        self.value[i] = self.getValue(i)
        if self.value[i] > 21:
            self.isBust[i] = True

    def split(self, i):
        self.hand.append([self.hand[i].pop(-1)])
        self.isHard.append(True)
        self.value[i] = self.getValue(i)
        self.value.insert(i+1, self.getValue(i))
        self.isBust.append(False)
        self.isDouble.append(False)
        self.isSplit = True
        print(self.hand)
        print(self.value)

    def double(self, i):
        self.hit(i)
        self.isDouble[i] = True

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

    def contents(self):
        return([self.value, self.isHard])


class Dealer(Player):
    def play(self):
        while self.getValue(0) < 17:
            self.hit(0)

    def upcard(self):
        return self.hand[0][0]

class Strategy(Player):
    def play(self):
        upcard = self.upcard
        if upcard == 'A':
            upcard = 11
        n = len(self.hand)
        i = 0
        while i < n:
            if self._split(i, upcard):
                n += 1
                j = 0
                if self.hand[i][0] == 'A':
                    self.hit(i)
                    i += 1
                    continue
            self._play(i, upcard)
            i += 1
        
    
    def _split(self, i, upcard):
        # when split is possible, chunk 4
        if len(self.hand[i]) == 2:
            if self.hand[i][0] == self.hand[i][1]:
                split = self.hand[i][0]
                if split == 'A' or split == 8:
                    self.split(i)
                    return True
                elif split == 10:
                    pass
                elif split == 9:
                    if upcard == 7 or upcard >= 10:
                        pass
                    else:
                        self.split(i)
                        return True
                elif split == 7:
                    if upcard <= 7:
                        self.split(i)
                        return True
                    elif upcard == 10:
                        pass
                    else:
                        self.hit(i)
                elif split == 6:
                    if upcard <= 6:
                        self.split(i)
                        return True
                    else:
                        self.hit(i)
                elif split == 5:
                    if upcard <= 9:
                        self.double(i)
                    else:
                        self.hit(i)
                elif split == 4:
                    if upcard == 5 or upcard == 6:
                        self.double(i)
                    else:
                        self.hit(i)
                elif split == 3:
                    if upcard >= 4 and upcard <=7:
                        self.split(i)
                        return True
                    else:
                        self.hit(i)
                elif split == 2:
                    if upcard >= 3 and upcard <= 7:
                        self.split(i)
                        return True
                    else:
                        self.hit(i)
        return False

    def _play(self, i, upcard):
        
        while self.value[i] < 21 and not self.isDouble[i]:
            #print(self.value[i])
            
            # if theres and ace in hand
            if 'A' in self.hand[i] and self.isHard[i] == False:
                if self.value[i] == 20:
                    break
                elif self.value[i] == 19:
                    if  upcard == 6:
                        self.double(i)
                    else:
                        break

                elif self.value[i] == 18:
                    if upcard >= 3 and upcard <= 6:
                        self.double(i)
                    elif upcard == 9 or upcard == 10:
                        self.hit(i)
                    else:
                        break

                elif self.value[i] == 17:
                    if upcard <= 6:
                        self.double(i)
                    else:
                        self.hit(i)

                elif self.value[i] <= 16:
                    if upcard == 4 or upcard == 5 or upcard == 6:
                        self.double(i)
                    else:
                        self.hit(i)

            # when hand is hard, chunk 1 and 2
            elif self.isHard[i] == True:
                if self.value[i] >= 17:
                    break

                elif self.value[i] >= 13:
                    if upcard <= 6:
                        break
                    else:
                        self.hit(i)

                elif self.value[i] == 12:
                    if upcard <= 3:
                        self.hit(i)
                    elif upcard <= 6:
                        break
                    else:
                        self.hit(i)

                elif self.value[i] == 11:
                    self.double(i)
                
                elif self.value[i] == 10:
                    if upcard <= 9:
                        self.double(i)
                    else:
                        self.hit(i)

                elif self.value[i] == 9:
                    if upcard <= 6:
                        self.double(i)
                    else:
                        self.hit(i)

                elif self.value[i] == 8:
                    if upcard == 5 or upcard == 6:
                        self.double(i)
                    else:
                        self.hit(i)
                
                else:
                    self.hit(i)
        return self.value[i]

class Table:
    def __init__(self, numPlayers = 5):
        self.deck = Deck()
        self.table = []
        while numPlayers > 0:
            #self.table.append(Player(self.deck))
            self.table.append(Strategy(self.deck))
            numPlayers -= 1
        self.table.append(Dealer(self.deck))

    def deal(self):
        n = 2
        while n > 0:
            for player in self.table:
                player.hit(0)
            n -= 1

        for player in self.table:
            player.upcard = self.upcard()

    def hands(self):
        hands = []
        for player in self.table:
            hands.append(player.hand)
        return hands

    def upcard(self):
        return self.table[-1].upcard()

    def checkBlackjack(self): #check for blackjack after deal
        self.blackjacks = []
        for player in self.table:
            if player.value[0] == 21:
                self.blackjacks.append(True)
            else:
                self.blackjacks.append(False)

    def _getPlayerBusts(self): # check for player busts
        self.busts = []
        for player in self.table[:-1]:
                self.busts.append(player.isBust)
    
    def checkActive(self):
        anyActive = False
        for playerBusts in self.busts:
            for busts in playerBusts:
                if busts == False:
                    anyActive = True
        return anyActive

    def getValues(self):
        values = []
        for player in self.table:
            values.append(player.value)
        return values


table = Table(1)
players = table.table[:-1]
dealer = table.table[-1]
table.deal()
print()
print('Hands Dealt:')
print(table.hands())
#print(table.deck.deck)
#check for dealerblackjack
table.checkBlackjack()
if table.blackjacks[-1] == True:
    for i in range(len(players)):
        if table.blackjacks[:-1][i] == True:
            #push
            pass
        else:
            #lose
            pass

#if no dealer backjack check for if all players have blackjack
# if all players have black jack then immediately payout dealer doesnt draw
elif (False not in table.blackjacks[:-1]):
    #payout all players
    pass
#if no dealer backjack or not all players blackjack then continue
else:
    #players play
    for player in players:
        player.play()

    # check for busts if at least one hand still active, dealer plays
    table._getPlayerBusts()
    print(table.busts)
    if table.checkActive():
        dealer.play()

print('After Play')
print(table.hands())
print(table.getValues())
#print(table.deck.deck)

'''
table.table[0].hit(table.deck)
table.table[0].hit(table.deck)
for player in table.table:
    print(player.getHand())
    print(player.contents())
'''

