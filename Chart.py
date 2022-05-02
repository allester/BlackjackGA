from Table import Table
import matplotlib.pyplot as plt
import pandas as pd
import random
import pickle

def geneticAlgorithm(population = None, POP_SIZE = 500, NUM_HANDS = 100000, TABLE_SIZE = 1, GROUP_SIZE = 2, GENERATIONS = 250):
    #if no current population then generate a population
    if population == None:
        population = [None] * POP_SIZE
        genes = []
        for _ in range(POP_SIZE):
            genes.append(generateRandomGenes())
    bestGenes = []
    for i in range(GENERATIONS):
        print('----- BEGIN GENERATION', i,  '-----')
        for j in range(POP_SIZE):
            players = calculateFitness(tableSize = 1, genes = genes[j], numHands = 100000)
            population[j] = players[0]
            print(players[0].chipCount)
            plt.scatter(i, players[0].chipCount)

        bestInd = bestIndividual(population)
        bestGenes.append([bestInd.chipCount, bestInd.genes])
        print('Best Fitness:', bestGenes[0])
        
        selection = selectionTournament(population, GROUP_SIZE = 2)
        population = getOffspring(selection)
    

    with open("genes.pkl", 'wb') as f:
        pickle.dump(bestGenes, f)

    plt.show()
    
        
def bestIndividual(population):
    MIN = -9999999999999999
    bestIndividual = None
    for individual in population:
        if individual.chipCount > MIN:
            bestIndividual = individual.genes
            MIN = individual.chipCount
    return bestIndividual

            
def calculateFitness(tableSize,  genes, numHands):
    table = Table(tableSize, genes)
    players = table.table[:-1]
    dealer = table.table[-1]

    handsPlayed = 0
    while handsPlayed < numHands:
        table.deal()
        '''print()
        print('Hands Dealt:')
        print(table.hands())'''
        #print(table.deck.deck)'''

        #check for if Dealer has Blackjack
        table.checkBlackjack()
        if table.blackjacks[-1] == True:
            for i in range(len(players)):
                if table.blackjacks[:-1][i] == True:
                    table.payouts[i] = [0] #push
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
        '''print('Chips:', table.getChips())

        print('After Play')
        print(table.hands())
        print(table.getValues())'''

        #if table.deck.shuffle:
        # shuffle deck after every hand
        table.deck.shuffleDeck()
            #print("The Deck has been shuffled")
        
        table.clearHands()

        handsPlayed += 1

    return table.table[:-1]


def getOffspring(selection, rate = 0.5):
    offsprings = selection
    for i in range(len(selection) // 2):
        offsprings[i] , offsprings[i-1] = uniformCrossover(selection[i], selection[i-1], rate)
    return offsprings

def uniformCrossover(parent1, parent2, rate):
    #for data frame
    offspring1 = parent1.genes
    offspring2 = parent2.genes

    indexes = list(parent1.index.values)
    columns = list(parent1.columns.values)

    for index in indexes:
        for column in columns:
            if random.uniform(0,1) <= rate:
                offspring1.loc[index, column] = parent2.genes.loc[index, column]
                offspring2.loc[index, column] = parent1.genes.loc[index, column]
    
    return offspring1, offspring2
        

def selectionTournament(individuals, GROUP_SIZE = 2):
    selection = []
    for _ in range(len(individuals)):
        candidates = [random.choice(individuals) for _ in range(GROUP_SIZE)]
    selection.append(max(candidates, key = lambda candidate: candidate.chipCount))
    return selection

def generateRandomGenes():
    #used to create initial population
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
    genes = pd.DataFrame(data)
    genes.columns = [2, 3, 4, 5, 6, 7, 8, 9, 10, "A"]
    genes.index = [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5,
                'A, 9', 'A, 8', 'A, 7', 'A, 6', 'A, 5', 'A, 4', 'A, 3', 'A, 2',
                 'A, A', '10, 10', '9, 9', '8, 8', '7, 7', '6, 6', '5, 5', '4, 4', '3, 3', '2, 2']
    return genes


# main file
geneticAlgorithm(population = None, POP_SIZE = 500, NUM_HANDS = 100000, TABLE_SIZE = 1, GROUP_SIZE = 2, GENERATIONS = 250)