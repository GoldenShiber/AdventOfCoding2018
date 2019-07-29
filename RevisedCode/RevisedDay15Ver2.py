from __future__ import print_function
import string
import timeit
import re
import operator

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from usefulFunctions import *


'''
First create a map, which contains all the units involved in the problem.
The map contains:
    - the game map
    - the amount of units 
    - a filtered map with only borders and dots
'''

class Map:
    def __init__(self):
        self.map = []
        self.unitList = []
        self.baseMap = []

    def importMap(self, filepath):
        lengthOfFile = file_len(filepath)
        self.map = []
        with open(filepath) as fp:
            for cnt in range(lengthOfFile):
                line = fp.readline()
                self.map.append(line)

    def filterMap(self):
        for i in range(len(self.map)):
            self.baseMap.append(self.map[i].replace('G', '.').replace('E', '.'))

    def printMap(self):
        print("Current map is:\n", end=" ")
        for i in range(len(self.map)):
            print(self.map[i], end=" ")

    def printBase(self):
        print("Map with only borders looks like:\n", end=" ")
        for i in range(len(self.baseMap)):
            print(self.baseMap[i], end=" ")

    def findUnits(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                sign = self.map[i][j]
                if sign is "G" or sign is "E":
                    self.unitList.append(Unit(sign, [i, j]))

    def setEnemies(self):
        for i in range(len(self.unitList)):
            for j in range(len(self.unitList)):
                if self.unitList[i].Class is not self.unitList[j].Class:
                    self.unitList[i].enemyList.append(self.unitList[j])
    def orderList(self):
        order = []
        for unit in self.unitList:
            order.append([unit.position[0], unit.position[1], unit])
        order = sorted(order, key=operator.itemgetter(0, 1))
        #print(order)
        unitOrder = []
        for x in order:
            unitOrder.append(x[2])
        self.unitList = unitOrder

    def setup(self):
        self.filterMap()
        self.findUnits()
        self.setEnemies()

    def step(self):
        self.orderList()
        for unit in self.unitList:
            if unit.isInBattle(self.map):
                print("unit is in battle ")
            else:
                distMap = DistanceMap(self.map, unit)
                distMap.setup()
                while distMap.finished is False:
                    distMap.step()
                unit.position = [unit.position[0]+distMap.potentialMove[0], unit.position[1]+distMap.potentialMove[1]]
            self.updateMap()
            self.printMap()

    def updateMap(self):
        testMap = []
        for maps in self.baseMap:
            testMap.append(maps)
        for unit in self.unitList:
            #print(unit.position)
            testString = list(testMap[unit.position[0]])
            testString[unit.position[1]] = unit.Class
            testString = "".join(testString)
            testMap[unit.position[0]] = testString

            #[unit.position[1]] = unit.Class
        self.map = testMap

class Unit:
    def __init__(self, Class, position):
        self.Class = Class
        self.position = position
        self.health = 200
        self.enemyList = []
        #self.enemyCoords = []
        self.turnorder = 0
        self.damage = 3
        self.phantomList = []

        if Class == "E":
            self.enemyType = "G"
        else:
            self.enemyType = "E"

    def isInBattle(self, map):
        neighbours = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        state = False
        for y in neighbours:
            neighPos = [y[0] + self.position[0], y[1] + self.position[1]]
            if map[neighPos[0]][neighPos[1]] is self.enemyType:
                state = True
                break
        return state

    def isReachable(self, map):
        neighbours = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        state = False
        for y in neighbours:
            neighPos = [y[0]+self.position[0], y[1] + self.position[1]]
            if map[neighPos[0]][neighPos[1]] is ".":
                state = True
        return state

class Arrow:
    def __init__(self, location, originalMove):
        self.location = location
        self.originalMove = originalMove
        self.dist = 9

    def arrowExpansion(self, arrowList):
        moveSets = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        for move in moveSets:
            arrowList.append(Arrow([self.location[0] + move[0], self.location[1] + move[1]], self.originalMove))
        return arrowList

'''
A distance map is generated while choosing the path for a unit, we save evert distance in steps.
Stop conditions: If after the timestep an enemy was reached, choose direction for the unit. 
'''

class DistanceMap:
    def __init__(self, map, startUnit):
        self.map = map
        self.startUnit = startUnit
        self.dist = 0
        self.arrows = []
        self.countMap = []
        self.tempArrows = []
        self.distMap = []
        self.finished = False
        self.potentialMove = []
        print(self.startUnit.position)

    def makeDist(self):
        for i in range(len(self.map)):
            #self.countMap.append(self.map[i].replace('G', '.').replace('E', '.'))
            self.distMap.append(self.map[i].replace('G', '.').replace('E', '.'))
        #self.distMap[self.startUnit.position[0]][self.startUnit.position[1]] = "0"

    def createCountMap(self):
        for i in range(len(self.map)):
            self.countMap.append([])
            distString = ""
            for j in range(len(self.map[i])):
                if self.startUnit.position[0] is i and self.startUnit.position[1] is j:
                    self.countMap[i].append(Arrow([i,j], [0, 0]))
                    self.countMap[i][j].dist = 0
                    distString += str(0)
                else:
                    self.countMap[i].append(Arrow([i, j], [0, 0]))
                    distString += str(9)
            self.distMap.append(distString)

    def updateDistMap(self):
        self.distMap = []
        for i in range(len(self.map)):
            distString = ""
            for j in range(len(self.map[i])):
                distString += str(self.countMap[i][j].dist)
            self.distMap.append(distString)

    def arrowAction(self):
        newArrowList = []
        for arrow in self.tempArrows:
            newArrowList.append(arrow)
        self.tempArrows = []
        for arrow in newArrowList:
            if self.map[arrow.location[0]][arrow.location[1]] is "." \
                    and self.countMap[arrow.location[0]][arrow.location[1]].dist >= self.dist:
                self.tempArrows = arrow.arrowExpansion(self.tempArrows)
                #self.tempArrows = arrowExpansion([arrow.location[0], arrow.location[1]], self.tempArrows)
                self.countMap[arrow.location[0]][arrow.location[1]] = arrow
                self.countMap[arrow.location[0]][arrow.location[1]].dist = self.dist
            elif self.countMap[arrow.location[0]][arrow.location[1]].dist >= self.dist:
                self.countMap[arrow.location[0]][arrow.location[1]] = arrow
                self.countMap[arrow.location[0]][arrow.location[1]].dist = self.dist
                self.countMap[arrow.location[0]][arrow.location[1]].originalMove =\
                    compareMovements(self.countMap[arrow.location[0]][arrow.location[1]].originalMove,
                                     arrow.originalMove)
                if self.map[arrow.location[0]][arrow.location[1]] is self.startUnit.enemyType:
                    self.finished = True
                    self.potentialMove = compareMovements(self.potentialMove, arrow.originalMove)


    def printDistanceMap(self):
        print("Map with only borders looks like:\n", end=" ")
        for i in range(len(self.distMap)):
            print(self.distMap[i]+"\n", end=" ")

    def setup(self):
        self.createCountMap()
        self.makeDist()
        startX = self.startUnit.position[0]
        startY = self.startUnit.position[1]
        moveSets = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        for move in moveSets:
            if self.map[startX + move[0]][startY + move[1]] is ".":
                self.tempArrows.append(Arrow([startX + move[0], startY + move[1]], move))
        for arrow in self.tempArrows:
            print(arrow.originalMove)

    def step(self):
        if self.finished is False:
            self.dist += 1
            self.arrowAction()
            self.updateDistMap()
            #self.printDistanceMap()
        else:
            print("The potential move is: "+str(self.potentialMove))
            print("The closest distance is found")


def compareMovements(oldMove, compare):
    if len(oldMove) <= 0:
        return compare
    else:
        #print(oldMove)
        tempList = []
        tempList.append(oldMove)
        tempList.append(compare)
        tempList = sorted(tempList, key=operator.itemgetter(0, 1))
        return tempList[0]


def test(filepath):
    initMap = Map()
    initMap.importMap(filepath)
    initMap.setup()
    initMap.printMap()
    initMap.printBase()

    #distMap = DistanceMap(initMap, initMap.unitList[0])
    #distMap.setup()
    # print(distMap.startUnit.position)
    n = 3
    for i in range(n):
        print("Time for mambo number :" +str(i+1))
        initMap.step()




test("day15/test.txt")
