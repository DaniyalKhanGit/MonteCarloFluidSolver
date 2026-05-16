import numpy as np
import math as mt

frame_size = 64
time_step = 1
cache = {}
n_samples = 100


# gaussian blob
def initVor(x: np.ndarray) -> int: 
    cx = 32
    cy = 32
    r = 10

    value = 0
    value += np.exp(-((x[0] - (cx-r))**2 + (x[1]-(cy+r))**2) / 50)
    value -= np.exp(-((x[0] - (cx+r))**2 + (x[1]-(cy+r))**2) / 50)
    value -= np.exp(-((x[0] - (cx-r))**2 + (x[1]-(cy-r))**2) / 50)
    value += np.exp(-((x[0] - (cx+r))**2 + (x[1]-(cy-r))**2) / 50)
    return value




# advection, biot-savart MC solver


# EVERYTHING NEEDS TO BE REFACTORED
# Plan:
# -scrap biot-savart and all relevant calculations and remake
# once those confirmed to work then focus on additional functions for this
# then WoS method finally
# we entirely redoing the way that the biot-savart is calculated

# Kernel rn bugging, need to debug urgently

def integralEstimation(x: np.ndarray, time: int) -> np.ndarray:

    # print(type(x), x, "integralEstimator")
    # print(type(time), time, "IE")

    integral_samples = np.random.uniform(0, frame_size, size=(n_samples, 2))
    diff = x - integral_samples
    # changed to montecarloestimator, though subject to change more
    vorticities = np.array([monteCarloEstimator(s, time) for s in integral_samples])
    # print(type(vorticities), vorticities, "vorticity")
    
    kernel = diff / (2*mt.pi*(np.linalg.norm(diff, axis=1, keepdims=True)**2) + mt.exp(-100))
    # print(np.mean(kernel, axis=0), "mean of kernel")
    cross_product = vorticities[:, np.newaxis] * np.column_stack((-kernel[:, 1], kernel[:, 0]))
    # print(cross_product)


    # print(np.mean(cross_product, axis=0), "integral estimation answer")
    # print(type(time), time, "TIME")

    return (np.mean(cross_product, axis=0) * frame_size**2)

def monteCarloEstimator(x: np.ndarray, time: int) -> int:

    # print(type(x), x, "MC estimator")
    # print(type(time), time, "TIME")

    if (time == 0):
        return initVor(x)

    fetchedCache = cacheFetch(x)
    if (fetchedCache != 0 and fetchedCache[1] == time - time_step):
        newX = fetchedCache[0]
    else:
        y = np.random.uniform(0, frame_size, size=(1, 2)).flatten()
        newX = x - (time_step * integralEstimation(y, time - time_step))
        cacheSolver(newX, time - time_step)
    # print(y, "random sampled point")
    # print(x)
    # print(newX)
    return monteCarloEstimator(newX,
                               (time - time_step))

# All cache related below -------------------------------------------------------

# updates the cache with a newer entry
# this is for input to cache
# returns 1 if success, 0 otherwise (this is just for tracing/error handling)
def cacheSolver(x: np.ndarray, time: int) -> int:
    # now that the cache is a dictionary, we can go about a new way of inputting values
    
    gridCoord = nearestCoord(x)

    if (gridCoord[0] >= 64): return 0
    elif (gridCoord[0] < 0): return 0
    if (gridCoord[1] >= 64): return 0
    elif (gridCoord[1] < 0): return 0

    insert = (x, time)

    if tuple(gridCoord) in cache:
        # handling
        if (cache[tuple(gridCoord)][1] < time):
            # update case
            cache.update({tuple(gridCoord): insert})
            return 1
        return 0

    else:
        cache.update({tuple(gridCoord): insert})
        return 1


# hard coded fineness for now, so its just flipping you to an int basically each time
def nearestCoord(x: np.ndarray) -> np.ndarray:
    
    if (x[0] % 1 >= 0.5):
        nearestX = mt.ceil(x[0])
    else:
        nearestX = mt.floor(x[0])

    if (x[1] % 1 >= 0.5):
        nearestY = mt.ceil(x[1])
    else:
        nearestY = mt.floor(x[1])

    nearCoord = np.array([nearestX, nearestY])
    return nearCoord

# fetches the nearest adjacent position from the cache
def cacheFetch(x: np.ndarray) -> np.ndarray:

    print(type(x), x, "cachefetch")
    
    gridPos = nearestCoord(x)
    if tuple(gridPos) in cache:
        return cache[tuple(gridPos)]
    else:
        return 0