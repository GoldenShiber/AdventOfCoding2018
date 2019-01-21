#Include some standard libraries
from __future__ import print_function
import string
import timeit

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from usefulFunctions import *

letterList = string.ascii_lowercase

def manhattanDistance(node, nodelist, area):
    distanceColletion = [None] * len(nodelist)
    crosscheck = 0
    for i in range(len(nodelist)):
        distanceColletion[i] = abs(nodelist[i][0]-node[0]) + abs(nodelist[i][1] -node[1])
    minValue = min(distanceColletion)
    for j in range(len(distanceColletion)):
        if minValue == distanceColletion[j]:
            charIndex = nodelist[j][2]
            crosscheck += 1
    if crosscheck > 1:
        area[node[0]][node[1]] = "Nope"
    else:
        area[node[0]][node[1]] = charIndex
    return area


def createNodeList(filepath):
    lengthOfFile = file_len(filepath)
    letterindex = 0
    iteration = 0
    # Create a list matrix for the nodes
    nodeList = [[None for x in range(3)] for z in range(lengthOfFile)]
    with open(filepath) as fp:
        for cnt in range(lengthOfFile):
            line = fp.readline()
            splitline = line.split(",")
            coordinates = cleanIntList(splitline)
            nodeList[cnt][0] = int(coordinates[0])
            nodeList[cnt][1] = int(coordinates[1])
            if letterindex < len(letterList) and iteration == 0:
                nodeList[cnt][2] = letterList[letterindex]
                letterindex += 1
            elif letterindex == len(letterList):
                letterindex = 0
                iteration = 1
                nodeList[cnt][2] = letterList[letterindex] + str(iteration)
                letterindex += 1
            else:
                nodeList[cnt][2] = letterList[letterindex] + str(iteration)
                letterindex += 1
    return nodeList


def createPlayMat(size):
    nodeMap = [[None for x in range(size)] for z in range(size)]
    return nodeMap


def existOnBoundary(area, node):
    maxNode = len(area)
    minNode = 0
    state = False
    for i in range(maxNode):
        if i == minNode or i == (maxNode-1):
            for j in range(maxNode):
                if area[i][j] == node:
                    state = True
        else:
            if area[i][minNode] == node or area[i][maxNode-1] == node:
                state = True
    return state


def filterPotentialList(area, nodelist):
    candidateList =[None] * 0
    for i in range(len(nodelist)):
        if existOnBoundary(area, nodelist[i][2]):
            status = "Type %s goes to infinity" % nodelist[i]
            #print(status)
        else:
            candidateList.append(nodelist[i])
    return candidateList


def fillPlayMat(nodeList, size):
    playmat = createPlayMat(size)
    for i in range(len(nodeList)):
        playmat[(nodeList[i][0])][(nodeList[i][1])] = nodeList[i][2]
    return playmat


def countArea(playmat, nodelist):
    maxsize = len(playmat)
    countList = [0] * len(nodelist)
    for i in range(maxsize):
        for j in range(maxsize):
            for k in range(len(nodelist)):
                if playmat[i][j] == nodelist[k][2]:
                    countList[k] += 1
    result = findMax(countList)
    status = "The type %s has the max distance that is not infinity with the distance of %s" % \
             (nodelist[result[1]][2], result[0])
    print(status)

    regionSize = 0
    for l in range(len(countList)):
        if countList[l] < 10000:
            regionSize += countList[l]


def totalDistance(nodelist, threshold):
    maxsize = 500
    legalSum = 0
    for i in range(maxsize):
        for j in range(maxsize):
            nodedistance = 0
            for k in range(len(nodelist)):
                nodedistance = nodedistance + abs(nodelist[k][0]-i) + abs(nodelist[k][1] -j)
            if nodedistance < threshold:
                legalSum += 1
    status = "The total nodes within a %s distance threshold is %s" %(threshold, legalSum)
    print(status)



def test(filepath, size):
    start = timeit.default_timer()
    nodeList = createNodeList(filepath)
    playmat = fillPlayMat(nodeList, size)
    for i in range(size):
        for j in range(size):
            manhattanDistance([i, j], nodeList, playmat)
    candidateList = filterPotentialList(playmat, nodeList)
    stop = timeit.default_timer()
    prepTime = stop - start
    start = timeit.default_timer()
    countArea(playmat, candidateList)
    stop = timeit.default_timer()
    part1Time = stop - start
    start = timeit.default_timer()
    totalDistance(nodeList, 10000)
    stop = timeit.default_timer()
    part2Time = stop - start

    print('Time for preparation is: ', prepTime, "s")
    print('Time for part 1 is: ', part1Time, "s")
    print('Time for part 2 is: ', part2Time, "s")





test("../day6/input.txt", 500)