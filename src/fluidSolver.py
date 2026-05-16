import numpy as np
import math as mt
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import biotSavart as bs
from biotSavart import cache, n_samples
import tracing
from tracing import trace_file

# inits the arrays and params
max_time = 5
frames = []

frameheatmap = np.zeros((64, 64))
framef2 = np.zeros((64, 64))
# generates a frame for heatmap
"""
def frameCreate():
    for x in range(64):
        for y in range(64):
            iteration = np.array((x, y))

            print(iteration, "<---")
            frameheatmap[x][y] = bs.monteCarloEstimator(iteration, time)
"""

for t in range(max_time):
    frame = np.zeros((64, 64))
    for x in range(64):
        for y in range(64):
            iteration = np.array((x, y))
            print(iteration, "t =", t, "<---")
            frame[x][y] = bs.monteCarloEstimator(iteration, t)
    frames.append(frame.copy())
    print(f"Frame {t} done")


fig, ax = plt.subplots()
im = ax.imshow(frames[0], cmap='coolwarm', origin='lower')
plt.colorbar(im)

def update(i):
    im.set_data(frames[i])
    ax.set_title(f"t = {i}")
    return [im]

#frameCreate()
#frameCreate2()
#plt.imshow(frameheatmap, cmap='coolwarm', origin='lower')
#plt.imshow(framef2 - frameheatmap, cmap='coolwarm', origin='lower')


animation = ani.FuncAnimation(fig, update, frames=len(frames), interval=500)
plt.show()

with open('cache_dump.txt', 'w') as f:
    for key in sorted(cache.keys()):
        f.write(f"{key}: {cache[key]}\n")
print("Success Finally")

