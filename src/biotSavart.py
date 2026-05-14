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
            if (cacheFetch(x, time) != 0):
                nth_vorticity = cacheFetch(x, time)
            else:
                nth_vorticity = recursiveSolver(y_i, (time - time_step), n_samples)

        diff = x - y_i
        G = diff / (2*mt.pi*diff^2) + mt.exp(-100)
        crossprod = (-nth_vorticity * G[1], nth_vorticity * G[0])
        summation += crossprod
    return summation / n_samples

def recursiveSolver(x: np.array[1], time: int, n_samples: int) -> np.array[1]:
    ntime = time - time_step
    if (time == 0):
        return initVor(x[0], x[1])
    
    nposition = x - time_step*biotSavartSolver(x, ntime, n_samples)
    return nposition


# caching handled here
# return of 0 means unsuccessful, anything else is good

def cachingSolver(x: np.array[1], time: int) -> int:
    
    if (cache[x[0]][x[1]] == 0):
        cache[x[0]][x[1]] = [x, time]
        return 1
    
    if (cache[x[0]][x[1]][1] < time):
        cache[x[0]][x[1]] = [x, time]
        return 1
    
    return 0


def nearestCoord(x) -> np.array[1]:
    
    if (x[0] % 1 >= 0.5):
        nearestX = mt.ceil(x[0])
    else:
        nearestX = mt.floor(x[0])

    if (x[1] % 1 >= 0.5):
        nearestY = mt.ceil(x[1])
    else:
        nearestY = mt.floor(x[1])

    if (nearestX >= 64): nearestX = 63
    elif (nearestX < 0): nearestX = 0

    if (nearestY >= 64): nearestY = 63
    elif (nearestY < 0): nearestY = 0

    nearCoord = np.array(nearestX, nearestY)
    return nearCoord


def cacheFetch(x, time) -> np.array[1]:
    
    gridPos = nearestCoord(x)
    return cache[gridPos[0],gridPos[1]]