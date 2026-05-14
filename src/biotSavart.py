import numpy as np
import math as mt

frame_size = 64
time_step = 1
cache = np.zeros((frame_size, frame_size))
n_samples = 100

def initVor(x: np.array[1]) -> int: 
    return x[0] + x[1]

# advection, biot-savart MC solver
"""
def biotSavartSolverOLD(x: np.array[1], time: int, n_samples: int) -> int:
    for i in range(n_samples):
        y_i = np.random(0, 1, size=(n_samples,2))

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

def biotSavartCalculation(x: np.array[1], time: int, n_samples: int):
    if (time == 0):
        nth_vorticity = initVor(y_i[0], y_i[1])
    else:
        if (cacheFetch(x, time) != 0):
            nth_vorticity = cacheFetch(x, time)
        else:
            nth_vorticity = recursiveSolver(y_i, (time - time_step), n_samples)

    

def biotSavartSolver(x: np.array[1], time: int, n_samples: int) -> int:
    random_samples = np.random.uniform(0, frame_size, n_samples)
    estimate = frame_size * np.mean(biotSavartCalculation(random_samples, time, n_samples))
    return estimate


def recursiveSolver(x: np.array[1], time: int, n_samples: int) -> np.array[1]:
    ntime = time - time_step
    if (time == 0):
        return initVor(x[0], x[1])
    
    nposition = x - time_step*biotSavartSolver(x, ntime, n_samples)
    # i dont care abt error handling rn
    cachingSolver(nposition, time)
    return nposition
"""

# we entirely redoing the way that the biot-savart is calculated


def integralEstimation(x: np.array[1], time: int) -> np.array[1]:

    integral_samples = np.random.uniform(0, frame_size, size=(n_samples, 2))
    diff = x - integral_samples
    # this is current fixed to only time samples 1, however likely once montecarloestimator is finished ill change it
    vorticity = initVor(integral_samples)
    kernel = diff / 2*mt.pi*np.linalg.norm(diff, axis=1)
    cross_product = np.cross(vorticity, kernel)

    return cross_product / n_samples

def monteCarloEstimator(x: np.array[1], time: int) -> int:

    fetchedCache = cacheFetch(x, time)

    if (time == 0):
        return initVor(x)
    # check the cache if theres any entry
    elif (fetchedCache != 0):
        pass

    y = np.random(0, frame_size, size=(1, 2))

    return monteCarloEstimator(x - time_step * integralEstimation(y, time - time_step),
                               (time - time_step))


# caching handled here
# return of 0 means unsuccessful, anything else is good
# updates the cache with a newer entry
def cachingSolver(x: np.array[1], time: int) -> int:
    
    if (cache[x[0]][x[1]] == 0):
        cache[x[0]][x[1]] = [x, time]
        return 1
    
    if (cache[x[0]][x[1]][1] < time):
        cache[x[0]][x[1]] = [x, time]
        return 1
    
    return 0

def nearestCoord(x: np.array[1]) -> np.array[1]:
    
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

# fetches the nearest adjacent position from the cache
def cacheFetch(x: np.array[1], time: int) -> np.array[1]:
    
    gridPos = nearestCoord(x)
    return cache[gridPos[0],gridPos[1]]