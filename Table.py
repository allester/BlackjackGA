from Player import Player, Dealer
from Deck import Deck

class Table:
    def __init__(self, numPlayers = 1, genes = None):
        self.deck = Deck()
        self.numPlayers = numPlayers
        self.table = []
        self.payouts = []
        for i in range(numPlayers):
            self.payouts.append([0])
        self.genes = genes
        for i in range(numPlayers):
            self.table.append(Player(self.deck, genes))
            self.payouts.append([0])

        self.table.append(Dealer(self.deck))

    def deal(self):
        for i in range(2):
            for player in self.table:
                player.hit(0)

        for player in self.table:
            player.upcard = self.table[-1].hand[0][0]

    def clearHands(self):
        for player in self.table:
            player.upcard = None #dealer's upcard
            player.hand = [[]]
            player.isHard = [True]
            player.value = [0]
            player.isBust = [False]
            player.isDouble = [False]
    

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

    def getPayouts(self): # writes new payout and overwrite self.payout to update with new values and splits
        dealer = self.table[-1]
        dealerValue = dealer.value[0]
        players = self.table[:-1]
        payouts = []
        for player in players:
            playerPayouts = []
            # we already checked for no black jack on dealer
            for i in range(len(player.hand)):

                # if player has black jack 
                if player.isBlackjack(i):
                    playerPayouts.append(1.5)

                # if player busts
                elif player.isBust[i]:
                    playerPayouts.append(-1)

                # is dealer bust and player is not bust
                elif (dealer.isBust[0] and not player.isBust[i]):
                    playerPayouts.append(1)

                # if player and dealer is not bust and player has higher value
                elif player.getValue(i) > dealerValue and not dealer.isBust[0]:
                    playerPayouts.append(1)

                # if player has less than dealer
                elif (not player.isBust[i] and player.getValue(i) < dealerValue and not dealer.isBust[0]):
                    playerPayouts.append(-1)

                # if player has equal value to dealer
                elif (not player.isBust[i] and player.getValue(i) == dealerValue and not dealer.isBust[0]):
                    playerPayouts.append(0)

                print('Doubled down: ', player.isDouble[i])
                # if player doubled down on hand
                if player.isDouble[i]:
                    playerPayouts[i] = playerPayouts[i] * 2

            payouts.append(playerPayouts)
        self.payouts = payouts
        print('Payout: ', self.payouts)

    def payout(self):
        for i in range(self.numPlayers):
            for payout in self.payouts[i]:
                self.table[i].pay(payout)

    def getChips(self):
        chips = []
        for player in self.table[:-1]:
            chips.append(player.chipCount)
        return chips
