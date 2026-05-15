import numpy as np
import math as mt
import matplotlib.pyplot as plt
import biotSavart as bs
from biotSavart import cache, n_samples

# inits the arrays
time = 1

U = np.array((64, 64))
V = np.array((64, 64))
X = np.array((64, 0))
Y = np.array((0, 64))


# generates a frame for quiver
for x in range(64):
    for y in range(64):
        iteration = np.array((x, y))
        # tracing
        print(type(iteration), iteration, "iterate")


        gridentry = bs.monteCarloEstimator(iteration, time)
        U[x][y] = gridentry[0]
        V[x][y] = gridentry[1]



plt.quiver(X, Y, U, V)
plt.show

