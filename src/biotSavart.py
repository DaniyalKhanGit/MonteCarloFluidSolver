import numpy as np
import math as mt

frame_size = 64
time_step = 1
cache = np.zeros(frame_size, frame_size)

def initVor(x: int, y: int) -> int: 
    return x + y

# advection, biot-savart MC solver

def biotSavartSolver(x: np.array[2], time: int, n_samples: int) -> int:
    for i in range(n_samples):
        y_i = np.random(0, frame_size, size=(n_samples,2))

        if (time == 0):
            nth_vorticity = initVor(y_i[0], y_i[1])
        else:
            nth_vorticity = recursiveSolver(y_i, (time - time_step), n_samples)

        diff = x - y_i
        G = diff / (2*mt.pi*diff^2) + mt.exp(-100)
        crossprod = (-nth_vorticity * G[1], nth_vorticity * G[0])
        summation += crossprod
    return summation / n_samples

def recursiveSolver(x: np.array[2], time: int, n_samples: int) -> np.array[2]:
    ntime = time - time_step
    if (time == 0):
        return initVor(x[0], x[1])
    
    nposition = x - time_step*biotSavartSolver(x, ntime, n_samples)
    return nposition


# caching handled here
# return of 0 means unsuccessful, anything else is good

def cachingSolver(x: np.array[2], time: int) -> int:
    
    if (cache[x[0]][x[1]] == 0):
        cache[x[0]][x[1]] = [x, time]
        return 1
    
    if (cache[x[0]][x[1]][1] < time):
        cache[x[0]][x[1]] = [x, time]
        return 1
    
    return 0


def cachingHelper(x, time) -> np.array[any]:
