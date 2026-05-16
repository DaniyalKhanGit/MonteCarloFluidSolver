import numpy as np
import math as mt
import matplotlib.pyplot as plt
import biotSavart as bs
from biotSavart import cache, n_samples

# inits the arrays
time = 2

frameheatmap = np.zeros((64, 64))

# generates a frame for quiver
for x in range(64):
    for y in range(64):
        iteration = np.array((x, y))
        # tracing
        # print(type(iteration), iteration, "iterate")


        frameheatmap[x][y] = bs.monteCarloEstimator(iteration, time)




plt.imshow(frameheatmap, cmap='coolwarm', origin='lower')
plt.show()
print("Success Finally")

