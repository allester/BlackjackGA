import pandas as pd
import random

def geneticAlgorithm(POP_SIZE = 500, NUM_HANDS = 100000, TABLE_SIZE = 1, GROUP_SIZE = 2):
    pass

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

def generateGenes(generation):
    pass