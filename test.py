import matplotlib.pyplot as plt
import numpy as np
import random


for i in range(50):
    y = random.random()
    plt.scatter(i, y)
    plt.pause(.0001)
