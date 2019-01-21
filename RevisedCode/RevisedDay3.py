#Include some standard libraries

from __future__ import print_function

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from usefulFunctions import *

import numpy as np
import re
import timeit


def makeRectangle(paintedMap, x, y):
    xmin = x
    #xhigh = x
    i = x
    ymin = y
    ymax = y
    j = y
    # check the next value at the map
    xstatus = False
    ystatus = False
    while xstatus is False:
        if paintedMap[i+1][j] == 1:
            i += 1
        else:
            xhigh = i
            xstatus = True
    while ystatus is False:
        k = xmin
        while k <= xhigh:
            if paintedMap[k][j+1]!=1:
                ystatus = True
                ymax = j
                break
            elif k == xhigh:
                j += 1
                k = xmin
            else:
                k += 1
    size = (xhigh-xmin)*(ymax-ymin)
    return ymin, ymax, xmin, xhigh, size

def checkRectExists(rectList,x,y):
    status = True
    for i in range(len(rectList)):
        if rectList[i][0]<= x <= rectList[i][1] and rectList[i][2] <= y <= rectList[i][3]:
            status = False
            break
    return status

def cleanUp(infoData):
    cleanList = [0] * 5
    infoData = re.sub('[!@#$:\n]', '', infoData)
    numData = infoData.split(" ")
    offset = numData[2].split(",")
    area = numData[3].split("x")
    cleanList[0] = int(numData[0])
    cleanList[1] = int(offset[0])
    cleanList[2] = int(offset[1])
    cleanList[3] = int(area[0])
    cleanList[4] = int(area[1])

    return cleanList

def paintTheMatrix(paintMatrix,offset, area):
    # Now let's fill in the painting the data in mind!
    inch1 = int(offset[0])
    inch2 = int(offset[1])
    paint1 = int(area[0])
    paint2 = int(area[1])
    paintx = [inch1, inch1+paint1]
    painty = [inch2,paint2+inch2]
    paintMatrix[paintx[0]:paintx[1],painty[0]:painty[1]] += 1

def test(filepath):
    lengthOfFile = file_len(filepath)
    start = timeit.default_timer()
    pixelCount = 0
    # Create register matrix for the input data
    registerMatrix = np.zeros(shape=(lengthOfFile, 5))
    # Create work matrix, which is painted with the input in mind, let's make it really big
    paintMatrix = np.zeros(shape=(3000, 3000))
    with open(filepath) as fp:
        for cnt in range(lengthOfFile):
        #for cnt in range(5):
            line = fp.readline()
            registerMatrix[cnt] = cleanUp(line)
            offset = [registerMatrix[cnt][1], registerMatrix[cnt][2]]
            paint = [registerMatrix[cnt][3], registerMatrix[cnt][4]]
            paintTheMatrix(paintMatrix, offset, paint)
    # Calculate the amount of pixels
    for i in range(3000):
        for j in range(3000):
            if paintMatrix[i][j] >=2:
                pixelCount += 1

    print(pixelCount)

    stop = timeit.default_timer()
    part1Time = stop - start
    print('Time for part 1 is: ', part1Time, "s")
    # Begin to find the single claim id

    start = timeit.default_timer()
    uniqueMatrix = np.zeros(shape=(500, 4))
    #uniqueMatrix[0, :] = [9999, 10000, 9999, 10000]
    iteration = 1
    limit = 1150
    for i in range(limit):
        for j in range(limit):
            # use recangle and check triangle function
            if paintMatrix[i][j] == 1:
                recInfo = makeRectangle(paintMatrix, i, j)
                if checkRectExists(uniqueMatrix, i, j) and recInfo[4] > 350:
                    uniqueMatrix[iteration, :] = [recInfo[2], recInfo[3], recInfo[0], recInfo[1]]
                    iteration += 1

    # Now find the correct ID among the possible unique matrices
    ID = ""
    for cnt in range(lengthOfFile):
        for i in range(iteration):
            # print(i)
            if int(registerMatrix[cnt][1]) == int(uniqueMatrix[i][0]) and int(registerMatrix[cnt][1]+
                                                                              registerMatrix[cnt][3] -1) \
                    == int(uniqueMatrix[i][1]) \
                    and int(registerMatrix[cnt][2]) == int(uniqueMatrix[i][2]) and \
                    int(registerMatrix[cnt][2]+registerMatrix[cnt][4] -1) == int(uniqueMatrix[i][3]):
                ID = registerMatrix[cnt][0]
                break
    print(ID)
    stop = timeit.default_timer()
    part2Time = stop - start
    print('Time for part 2 is: ', part2Time, "s")


test("../day3/input.txt")