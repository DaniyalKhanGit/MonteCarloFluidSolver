import numpy as np
import math as mt
import matplotlib.pyplot as plt
import biotSavart as bs
from biotSavart import cache, n_samples
import tracing
from tracing import trace_file

# inits the arrays
time = 1

frameheatmap = np.zeros((64, 64))

# generates a frame for heatmap

def frameCreate():
    for x in range(64):
        for y in range(64):
            iteration = np.array((x, y))

            frameheatmap[x][y] = bs.monteCarloEstimator(iteration, time)



frameCreate()
plt.imshow(frameheatmap, cmap='coolwarm', origin='lower')
plt.show()
print("Success Finally")

