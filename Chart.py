import pandas as pd
import random

def generateGenes(generation):
    if 
    actions = ['H', 'S', 'D', 'Sp']

    data = []
    for i in range(34):
        row = []
        for j in range(10):
            row.append(random.choice(actions))
        data.append(row)

    df = pd.DataFrame(data)

    df.columns = [2, 3, 4, 5, 6, 7, 8, 9, 10, "A"]
    df.index = [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5,
            'A, 9', 'A, 8', 'A, 7', 'A, 6', 'A, 5', 'A, 4', 'A, 3', 'A, A', 'A, 2',
            '10, 10', '9, 9', '8, 8', '7, 7', '6, 6', '5, 5', '4, 4', '3, 3', '2, 2']

    print(df)
    print(df.loc[10,9])

