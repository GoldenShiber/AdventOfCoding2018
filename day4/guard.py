#Include some standard libraries
from __future__ import print_function

import numpy as np
import operator
import pickle


def sort_table(table, cols):
    """ sort a table by multiple columns
        table: a list of lists (or tuple of tuples) where each inner list
               represents a row
        cols:  a list (or tuple) specifying the column numbers to sort by
               e.g. (1,0) would sort by column 1, then by column 0
    """
    for col in reversed(cols):
        table = sorted(table, key=operator.itemgetter(col))
    return table


def file_len(filename):
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def findIndex(word, letter):
    lengthOfFile = len(word)
    index = 0
    for i in range(lengthOfFile):
        if word[i] == letter:
            index = i
            break
    return index


# First gather the data, and collect it in a good order.


def seperateInformation(line):
    dateStart = findIndex(line, "[")+1
    dateEnd = findIndex(line, "]")
    date = line[dateStart:dateEnd]
    messageStart = dateEnd +2
    messageEnd = len(line)
    message = line[messageStart:messageEnd]
    return date, message


def dateParser(timeString):
    # A time string determined by year, month day
    # example 1518-11-17 00:50
    year = timeString[0:4]
    month = timeString[5:7]
    day = timeString[8:10]
    hours = timeString[11:13]
    minutes = timeString[14:16]
    return year, month, day, hours, minutes

def createSortedListDate(filepath, newfile):
    # Create information matrix
    lengthOfFile = file_len(filepath)
    dataInfo = [[0 for x in range(6)] for z in range(lengthOfFile)]
    stringCollection = [None] * lengthOfFile
    with open(filepath) as fp:
        for cnt in range(lengthOfFile):
            line = fp.readline()
            stringVector = seperateInformation(line)
            dateInfo = dateParser(stringVector[0])

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
        timematrix[id:id+1,oldTime:minutes] = timematrix[id:id+1,oldTime:minutes] +1
        previousTime = minutes
    elif indexStatus == "f":
        previousTime = minutes
    elif indexStatus == "G":
        id = int(fetchGuardID(status))
        previousTime = minutes

    return  previousTime, id


def guardTest(filepath):
    lengthOfFile = file_len(filepath)
    pixelCount = 0
    # Create register matrix for the input data, big amount of ID, 60 minutes
    registerMatrix = np.zeros(shape=(5000, 60))
    sumMatrix = np.zeros(shape=(5000, 1))
    id = 1
    oldTime = 0
    minutes = 0

    with open(filepath) as fp:
        for cnt in range(lengthOfFile):
            line = fp.readline()
            seperateData = seperateInformation(line)
            dateInfo = dateParser(seperateData[0])
            minutes = int(dateInfo[4])
            if cnt == 0:
                oldState = guardStates(line, oldTime, minutes, id, registerMatrix)
            else:
                oldState = guardStates(line,oldState[0],minutes,oldState[1],registerMatrix)

    # Find the max value in the register
    guardMax = np.sum(registerMatrix, axis=1)
    maxIndex = np.argmax(guardMax)
    maxValue = np.argmax(registerMatrix[maxIndex])
    status = "Guard with ID %s rest at minute %s for a total of the score %s" % (maxIndex, maxValue, maxIndex*maxValue)
    print(status)

    # Part 2
    #Find the right index
    maxFreq = np.argmax(registerMatrix.all)
    ind = np.unravel_index(np.argmax(registerMatrix, axis=None), registerMatrix.shape)
    status = "Guard with ID %s rest most at minute %s for a total of %s times for a total of the score %s" % (
    ind[0], ind[1],registerMatrix[ind[0],ind[1]], ind[0] * ind[1])
    print(status)

#createSortedListDate("input.txt","sortedInput.txt")

guardTest("sortedInput.txt")