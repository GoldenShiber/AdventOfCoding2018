'''

THIS IS WORK IN PROGRESS; IT WORKS FOR SMALLER DUNGEONS, but still needs to be optimsed and FIXED
CONSIDER THIS WHILE LOOKING AT THIS CODE

'''

from __future__ import print_function
import string
import timeit
import re
import operator

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from usefulFunctions import *

filledMap = []

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
            self.unitList[i].enemyList = []
            for j in range(len(self.unitList)):
                if self.unitList[i].Class is not self.unitList[j].Class:
                    self.unitList[i].enemyList.append(self.unitList[j])
                else:
                    self.unitList[i].friendList.append(self.unitList[j])
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
        global filledMap
        filledMap = []
        mapMax = 30
        self.orderList()
        for unit in self.unitList:
            if len(filledMap) > 0:
                if filledMap[unit.position[0]][unit.position[1]].dist is not mapMax:
                    doAction = False
                    print(" A move is not needed ")
                else:
                    doAction = True
            else:
                doAction = True
            if doAction:
                if unit.isInBattle(self.map) or unit.isReachableUnits(self.map) is False:
                    #print("unit is in battle or enemies are occupied")
                    i = []
                else:
                    distMap = DistanceMap(self.map, unit)
                    distMap.setup()
                    while distMap.finished is False:
                        distMap.step()
                    unit.position = [unit.position[0]+distMap.potentialMove[0], unit.position[1]+distMap.potentialMove[1]]
                [state, battleUnit] = unit.battle()
                if state is True:
                    if battleUnit.health <= 0:
                        self.removeUnit(battleUnit)
                        self.setEnemies()
                        #self.orderList()
                    ##if battleUnit.health <= 0:
                    ##   self.removeUnit(battleUnit)
                self.updateMap()

            #self.printMap()

    def gameEnd(self):
        state = False
        loserType = ""
        types = ["G", "E"]
        for type in types:
            sum = 0
            for unit in self.unitList:
                if unit.Class is type:
                    sum += 1
                    break
            if sum is 0:
                state = True
                loserType = type
                break
        return [state, loserType]

    def countPoints(self, turn):
        sum = 0
        for unit in self.unitList:
            sum += unit.health
        sum = turn*sum
        return sum

    def removeUnit(self, sacrifice):
        newList = []
        index = self.unitList.index(sacrifice)
        for i in range(len(self.unitList)):
            if i is not index:
                newList.append(self.unitList[i])
        self.unitList = newList

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
        self.friendList = []
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

    def isReachableUnits(self, map):
        state = False
        for enemy in self.enemyList:
            if enemy.isReachable(map):
                state = True
                break
        return state

    def isPassableNode(self, map, coordinates):
        sign = map[coordinates[0]][coordinates[1]]
        if sign in [".", self.Class]:
            if sign is ".":
                return True
            else:
                friendTarget = []
                for friend in self.friendList:
                    if friend.position[0] == coordinates[0] and friend.position[1] == coordinates[1]:
                        friendTarget = friend
                        break
                if friendTarget.isInBattle(map):
                    return False
                else:
                    return True
                #index = self.friendList.index(sacrifice)

    def battle(self):
        attackpattern = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        lowestHP = 999
        targetEnemy =[]
        state = False
        for x in attackpattern:
            attack = [x[0] + self.position[0], x[1]+self.position[1]]
            #print("The attack is:" + str(attack))
            for y in self.enemyList:

                if attack[0] is y.position[0] and attack[1] is y.position[1] and y.health <= lowestHP:
                    #print("It is a hit!")
                    lowestHP = y.health
                    if state is False:
                        targetEnemy = y
                    else:
                        targetEnemy = prioTarget([targetEnemy, y])
                    state = True
        if state:
            targetEnemy.health -= self.damage
            return [state, targetEnemy]
        else:
            return[state, self]


class Arrow:
    def __init__(self, location, originalMove):
        self.location = location
        self.originalMove = originalMove
        self.dist = 30

    def arrowExpansion(self, arrowList, map, dist, countMap, friendlyClass):
        moveSets = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        for move in moveSets:
            if map[self.location[0] + move[0]][self.location[1] + move[1]] not in ["#", "x"] and \
                    dist < countMap[self.location[0] + move[0]][self.location[1] + move[1]].dist:
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
        #print(self.startUnit.position)

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
        global filledMap
        newArrowList = []
        for arrow in self.tempArrows:
            newArrowList.append(arrow)
        self.tempArrows = []
        if len(newArrowList) > 0:
            for arrow in newArrowList:
                ##if self.map[arrow.location[0]][arrow.location[1]] is "." \
                  ##      and self.countMap[arrow.location[0]][arrow.location[1]].dist >= self.dist:
                    ##self.tempArrows = arrow.arrowExpansion(self.tempArrows, self.map, (self.dist + 1), self.countMap, self.startUnit.Class)
                if self.startUnit.isPassableNode(self.map, arrow.location) \
                    and self.countMap[arrow.location[0]][arrow.location[1]].dist >= self.dist:
                    self.tempArrows = arrow.arrowExpansion(self.tempArrows, self.map, (self.dist + 1), self.countMap, self.startUnit.Class)
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
                #if self.dist > 30:
                    #self.finished = True
                    #break
            #if self.dist > 30 and len(self.tempArrows) is 0:
        else:
        #if len(self.tempArrows) is 0 and self.finished:
            self.finished = True
            self.potentialMove = [0, 0]
            filledMap = self.countMap
            print("We reached an end")


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
        #for arrow in self.tempArrows:
         #   print(arrow.originalMove)

    def step(self):
        if self.finished is False:
            self.dist += 1
            self.arrowAction()
            self.updateDistMap()
            #self.printDistanceMap()
        else:
            #print("The potential move is: "+str(self.potentialMove))
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


def prioTarget(unitList):
    order = []
    for unit in unitList:
        order.append([unit.health, unit.position[0], unit.position[1], unit])
    order = sorted(order, key=operator.itemgetter(0, 1, 2))
    return order[0][3]

def test(filepath):
    initMap = Map()
    initMap.importMap(filepath)
    initMap.setup()
    initMap.printMap()
    initMap.printBase()

    #distMap = DistanceMap(initMap, initMap.unitList[0])
    #distMap.setup()
    # print(distMap.startUnit.position)
    n = 48
    i = 0
    gamestate = False
    while gamestate is False:
        print("Time for mambo number :" + str(i))
        [gamestate, loser] = initMap.gameEnd()
        if gamestate:
            print("Game has ended!")
            points = initMap.countPoints(i)
            print("The type of :"+loser+": lost with "+str(points)+ " points!")
            initMap.printMap()
            for unit in initMap.unitList:
                print("The class is "+unit.Class + " and the health is now "+str(unit.health))
        #print("Number of alive units are: " +str(len(initMap.unitList)))
	initMap.step()
        i += 1



test("day15/test2.txt")
#test("day15/input.txt")
