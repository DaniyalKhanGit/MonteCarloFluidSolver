import numpy as np
import math as mt
import tracing
from tracing import trace_file, trace

outofFrameRecursion = False 

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
# biot-savart 
def integralEstimation(x: np.ndarray, time: int) -> np.ndarray:
    integral_samples = np.random.uniform(0, frame_size, size=(n_samples, 2))
    diff = x - integral_samples
    
    vorticities = np.array([monteCarloEstimator(s, time) for s in integral_samples])
    #print(type(vorticities), vorticities, "vorticity")
    
    kernel = diff / ((2*mt.pi*abs((np.linalg.norm(diff, axis=1, keepdims=True)**2))) + mt.exp(-100))
    # print(np.mean(kernel, axis=0), "mean of kernel")
    cross_product = vorticities[:, np.newaxis] * np.column_stack((-kernel[:, 1], kernel[:, 0]))
    # print(cross_product)
    trace(x, time, "starter val")
    trace(np.mean(cross_product, axis=0), "integral estimation answer and time:", time)
    return (np.mean(cross_product, axis=0) * frame_size**2)

def monteCarloEstimator(x: np.ndarray, time: int) -> int:

    if (time == 0):
        return initVor(x)

    if (not outofFrameRecursion and not 0 < x[0] < 64 and not 0 < x[1] < 64):
        return 0

    fetchedCache = cacheFetch(x)
    if (fetchedCache != 0 and fetchedCache[1] == time):
        vorticity = fetchedCache[2]
    # to prevent us from throwing away values and making it ironically slower
    elif (fetchedCache != 0 and fetchedCache[3] == time):
        vorticity = fetchedCache[4]
    else:
        # changes to be made here
        newX = x - (time_step * integralEstimation(x, time - time_step))
        vorticity = monteCarloEstimator(newX, time - time_step)
        cacheSolver(x, time, vorticity)

    # trace(x - newX, "difference between x and newX")
    return vorticity

# All cache related below -------------------------------------------------------

# updates the cache with a newer entry
# this is for input to cache
# returns 1 if success, 0 otherwise (this is just for tracing/error handling)
def cacheSolver(x: np.ndarray, time: int, vorticity: int) -> int:
    # now that the cache is a dictionary, we can go about a new way of inputting values
    
    gridCoord = nearestCoord(x)

    if (not outofFrameRecursion):
        if (gridCoord[0] >= 64): return 0
        elif (gridCoord[0] < 0): return 0
        if (gridCoord[1] >= 64): return 0
        elif (gridCoord[1] < 0): return 0

    if tuple(gridCoord) in cache:
        # handling
        if (cache[tuple(gridCoord)][1] < time):
            # update case
            timePrevious = cache[tuple(gridCoord)][1]
            vorticityPrevious = cache[tuple(gridCoord)][2]
            insert = (x, time, vorticity, timePrevious, vorticityPrevious)
            cache.update({tuple(gridCoord): insert})
            return 1
        return 0

    else:
        insert = (x, time, vorticity, 0, 0)
        cache.update({tuple(gridCoord): insert})
        return 1


# hard coded fineness for now, so its just flipping you to an int basically each time
def nearestCoord(x: np.ndarray) -> np.ndarray:
    
    if (x[0] % 1 >= 0.5):
        nearestX = int(mt.ceil(x[0]))
    else:
        nearestX = int(mt.floor(x[0]))

    if (x[1] % 1 >= 0.5):
        nearestY = int(mt.ceil(x[1]))
    else:
        nearestY = int(mt.floor(x[1]))

    nearCoord = np.array([nearestX, nearestY])
    return nearCoord

# fetches the nearest adjacent position from the cache
def cacheFetch(x: np.ndarray) -> np.ndarray:

    # trace(type(x), x, "cachefetch")
    
    gridPos = nearestCoord(x)
    if tuple(gridPos) in cache:
        return cache[tuple(gridPos)]
    else:
        return 0