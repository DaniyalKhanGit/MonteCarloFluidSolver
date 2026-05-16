import numpy as np
import math as mt

frame_size = 64
time_step = 1
cache = np.zeros((frame_size, frame_size))
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
    # check the cache if theres any entry (ill do this after basic implement)
    # fetchedCache = cacheFetch(x)
    # if (fetchedCache != 0):
    #     if (fetchedCache[1] == time - time_step):
    #         newX = fetchedCache[0]

    y = np.random.uniform(0, frame_size, size=(1, 2)).flatten()
    # print(y, "random sampled point")
    newX = x - (time_step * integralEstimation(y, time - time_step))
    # print(x)
    # print(newX)

    # once we find this newX we have to insert it into the cache accordingly

    # cachingSolver(newX, time - time_step)

    return monteCarloEstimator(newX,
                               (time - time_step))

# caching rewrite on the way

# caching handled here
# return of 0 means unsuccessful, anything else is good
# updates the cache with a newer entry
'''
def cachingSolver(x: np.ndarray, time: int) -> int:

    print(type(x), x, "cachingSolver")
    print(type(time), time, "cachingSolverTIME")
    
    if (cache[int(x[0]), int(x[1])] == 0):
        cache[int(x[0]), int(x[1])] = [x, time]
        return 1
    
    if (cache[int(x[0]), int(x[1])][1] < time):
        cache[int(x[0]), int(x[1])] = [x, time]
        return 1
    
    return 0
'''

def cacheSolver(x: np.ndarray, time: int) -> int:
    pass

def nearestCoord(x: np.ndarray) -> np.ndarray:

    print(type(x), x, "nearestcoord")
    
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

    nearCoord = np.array([nearestX, nearestY])
    return nearCoord

# fetches the nearest adjacent position from the cache
def cacheFetch(x: np.ndarray) -> np.ndarray:

    print(type(x), x, "cachefetch")
    
    gridPos = nearestCoord(x)
    return cache[gridPos[0],gridPos[1]]