#Include some standard libraries
from __future__ import print_function

import numpy as np
import timeit


if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from usefulFunctions import *


def createSortedListDate(filepath, newfile):
    # Create information matrix
    lengthOfFile = file_len(filepath)
    dataInfo = [[0 for x in range(6)] for z in range(lengthOfFile)]
    stringCollection = [None] * lengthOfFile
    with open(filepath) as fp:
        for cnt in range(lengthOfFile):
            line = fp.readline().strip("[]")
            #stringVector = seperateInformation(line)
            dateInfo = dateParser2(line)

            # save data in a order list which is then sorted
            dataInfo[cnt][0] = dateInfo[0]
            dataInfo[cnt][1] = dateInfo[1]
            dataInfo[cnt][2] = dateInfo[2]
            dataInfo[cnt][3] = dateInfo[3]
            dataInfo[cnt][4] = dateInfo[4]
            dataInfo[cnt][5] = cnt

            stringCollection[cnt] = line

    # Now make a new string collection in the right order, and save it as a new input file
    sortedTable = sort_table(dataInfo, (0, 1, 2, 3, 4))
    sortedTextFile = [None] * lengthOfFile
    for i in range(lengthOfFile):
        sortedTextFile[i] = stringCollection[sortedTable[i][5]]
    # Write out the result
    with open(newfile, 'w') as file_handler:
        for item in sortedTextFile:
            file_handler.write("{}".format(item))

def fetchGuardID(line):
    startID = findIndex(line,"#") +1
    endID = findIndex(line,"b")
    ID = line[startID: endID]
    return ID


def guardStates(status,oldTime, minutes, id, timematrix):
    # 3 states, w as wakes, f as falls asleep and G as new guard
    indexStatus = findIndex(status, "]")+2
    indexStatus = status[indexStatus]
    if indexStatus == "w":
        timematrix[id:id+1,oldTime:minutes] += 1
        previousTime = minutes
    elif indexStatus == "f":
        previousTime = minutes
    elif indexStatus == "G":
        id = int(fetchGuardID(status))
        previousTime = minutes

    return  previousTime, id

def test(filepath):
    start = timeit.default_timer()
    # Create register matrix for the input data, big amount of ID, 60 minutes
    registerMatrix = np.zeros(shape=(5000, 60))

    id = 1
    oldTime = 0

    lengthOfFile = file_len(filepath)
    with open(filepath) as fp:
        for cnt in range(lengthOfFile):
            line = fp.readline()
            stripLine = line.strip("[]")
            timeData = dateParser2(stripLine)
            minutes = int(timeData[4][0:2])
            if cnt == 0:
                oldState = guardStates(line, oldTime, minutes, id, registerMatrix)
            else:
                oldState = guardStates(line, oldState[0], minutes, oldState[1], registerMatrix)

            # Find the max value in the register
        guardMax = np.sum(registerMatrix, axis=1)
        maxIndex = np.argmax(guardMax)
        maxValue = np.argmax(registerMatrix[maxIndex])
        status = "Guard with ID %s rest at minute %s for a total of the score %s" % (
        maxIndex, maxValue, maxIndex * maxValue)
        print(status)
        stop = timeit.default_timer()
        part1Time = stop - start
        print('Time for part 1 is: ', part1Time, "s")

        # Part 2
        start = timeit.default_timer()
        # Find the right index
        ind = np.unravel_index(np.argmax(registerMatrix, axis=None), registerMatrix.shape)
        status = "Guard with ID %s rest most at minute %s for a total of %s times for a total of the score %s" % (
            ind[0], ind[1], registerMatrix[ind[0], ind[1]], ind[0] * ind[1])
        print(status)
        stop = timeit.default_timer()
        part2Time = stop - start
        print('Time for part 2 is: ', part2Time, "s")


test("sortedInput.txt")



#createSortedListDate("../day4/input.txt","sortedInput.txt")