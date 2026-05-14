import numpy as np
import math as mt
import matplotlib.pyplot as plt
import biotSavart as bs
from biotSavart import cach

time = 1
n_samples = 100
U = np.array[64][64]
V = np.array[64][64]
X = np.array[64][0]
Y = np.array[0][64]

for x in range(64):
    for y in range(64):
        temp = np.array[x, y]
        U[x - 1][y - 1] = bs.recursiveSolver(temp, time, n_samples)[0]
        V[x - 1][y - 1] = bs.recursiveSolver(temp, time, n_samples)[1]



plt.quiver(X, Y, U, V)
plt.show

