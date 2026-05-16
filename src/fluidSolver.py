import numpy as np
import math as mt
import matplotlib.pyplot as plt
import biotSavart as bs
from biotSavart import cache, n_samples
import tracing
from tracing import trace_file

# inits the arrays and params
time = 1

frameheatmap = np.zeros((64, 64))
framef2 = np.zeros((64, 64))
# generates a frame for heatmap

def frameCreate():
    for x in range(64):
        for y in range(64):
            iteration = np.array((x, y))

            print(iteration, "<---")
            frameheatmap[x][y] = bs.monteCarloEstimator(iteration, time)


def frameCreate2():
    for x in range(64):
        for y in range(64):
            iteration = np.array((x, y))

            print(iteration, "<---")
            framef2[x][y] = bs.monteCarloEstimator(iteration, 2)

frameCreate()
frameCreate2()
#plt.imshow(frameheatmap, cmap='coolwarm', origin='lower')
plt.imshow(framef2 - frameheatmap, cmap='coolwarm', origin='lower')
plt.show()

with open('cache_dump.txt', 'w') as f:
    for key in sorted(cache.keys()):
        f.write(f"{key}: {cache[key]}\n")
print("Success Finally")

