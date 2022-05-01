from Table import Table
import pandas as pd
import random

def getFitness(tableSize,  genes, numHands):
    table = Table(tableSize, genes)
    players = table.table[:-1]
    dealer = table.table[-1]

    handsPlayed = 0
    while handsPlayed < numHands:
        table.deal()
        print()
        print('Hands Dealt:')
        print(table.hands())
        #print(table.deck.deck)'''

        #check for if Dealer has Blackjack
        table.checkBlackjack()
        if table.blackjacks[-1] == True:
            for i in range(len(players)):
                if table.blackjacks[:-1][i] == True:
                    table.payout[i] = [0] #push
                else:
                    table.payouts[i] = [-1]

        #if no dealer backjack check for if all players have blackjack
        # if all players have black jack then immediately payout dealer doesnt draw
        elif (False not in table.blackjacks[:-1]):
            #payout all players
            for i in range(len(players)):
                table.payouts[i] = [1.5]

        #if no dealer backjack or not all players blackjack then continue
        else:
            #players play
            for player in players:
                player.play()

            # check for busts if at least one hand still active, dealer plays
            table._getPlayerBusts()
            if table.checkActive():
                dealer.play()
            table.getPayouts()

        table.payout()
        print('Chips:', table.getChips())

        print('After Play')
        print(table.hands())
        print(table.getValues())

        if table.deck.shuffle:
            table.deck.shuffle()
            print("The Deck has been shuffled")
        
        table.clearHands()

        handsPlayed += 1

actions = ['H', 'S', 'D', 'Sp']
data = []
for i in range(24):
    row = []
    for j in range(10):
        row.append(random.choice(actions[:-1]))
    data.append(row)
for i in range(10):
    row = []
    for j in range(10):
        row.append(random.choice(actions))
    data.append(row)

df = pd.DataFrame(data)
df.columns = [2, 3, 4, 5, 6, 7, 8, 9, 10, "A"]
df.index = [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5,
            'A, 9', 'A, 8', 'A, 7', 'A, 6', 'A, 5', 'A, 4', 'A, 3', 'A, 2', 'A, A',
            '10, 10', '9, 9', '8, 8', '7, 7', '6, 6', '5, 5', '4, 4', '3, 3', '2, 2']
print(df)
getFitness(tableSize = 1, genes = df, numHands = 10)
