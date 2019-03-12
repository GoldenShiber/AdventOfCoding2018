from __future__ import print_function
import string
import timeit
import re
import numpy as np

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from usefulFunctions import *

'''
Calculate the power level!
'''

def powerLevel(x, y, serialNumb):
    rackID = x+10
    power = rackID * y
    power += serialNumb
    power *= rackID
    try:
        power = int(str(power)[len(str(power))-3])
    except:
        power = 0
    power -= 5
    return power

'''
Power cell collector in an area!
'''

def collectPowerLevel(x,y, matrix, size):
    power = 0
    mLen = np.size(matrix,1)
    for i in range(x,x+size):
        for j in range(y,y+size):
            if i+size < mLen  and j + size < mLen:
                     power += matrix[i][j]
    return power

'''
The main method
'''

def powerSearcher(serialNum, size, collectSize):
    start = timeit.default_timer()
    powerMatrix = np.zeros((size,size))
    for i in range(len(powerMatrix)):
        for j in range(len(powerMatrix)):
            powerMatrix[i][j] = powerLevel(i, j, serialNum)

    powerMatrix3 = np.zeros((size,size))
    for i in range(0,len(powerMatrix)-1):
        for j in range(0,len(powerMatrix)-1):
            powerMatrix3[i][j] = collectPowerLevel(i,j,powerMatrix,collectSize)
    print(powerMatrix3.max())
    coordinates = np.where(powerMatrix3 == 29)
    print("The Coordinates for part 1 are: "+str(coordinates[0][0])+","+str(coordinates[1][0])+\
          " with the size: "+ str(collectSize))
    stop = timeit.default_timer()
    Time1 = stop - start

    # Now check for all the potential sizes to find a max value.
    start = timeit.default_timer()
    noImprovement = 0
    initialSize = 1
    intialPower = 0
    initialCoord = [0, 0]

    for k in range(1,size/2):
        testPowerMatrix = np.zeros((size, size))
        for l in range(1, size+1):
            for m in range(1, size+1):
                if l + k < size and m + k < size:
                    testPowerMatrix[l][m] = collectPowerLevel(l, m, powerMatrix, k)
        power = testPowerMatrix.max()
        if power >= intialPower:
            intialPower = power
            coordinates = np.where(testPowerMatrix == power)
            initialSize = k
            initialCoord = [coordinates[0][0], coordinates[1][0]]
            #print("New record with power of: " + str(power) + " with the size: " + str(k) +
                  #" and the Coordinates for the max power are: " + str(initialCoord[0]) +
                  #"," + str(initialCoord[1]))
            # Then check if no improvements has been done for a while... about 8
        else:
            noImprovement += 1
            if noImprovement > 8:
                break
    print("The Coordinates for the max power are probably at: " + str(initialCoord[0]) + "," + str(initialCoord[1]) + \
          " with the size: " + str(initialSize)+ ", and the power of: " + str(intialPower))
    stop = timeit.default_timer()
    Time2 = stop - start

    print("Time taken for part 1 is is: " + str(Time1) + " seconds!")
    print("Time taken for part 2 is is: " + str(Time2) + " seconds!")



powerSearcher(6548,300,3)