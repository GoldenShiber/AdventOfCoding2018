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
First introduce the unit class, which can be either a goblin or and elf.
'''


class Unit:
    def __init__(self, Class, position):
        self.Class = Class
        self.position = position
        self.health = 200
        self.enemyList = []
        self.turnorder = 0
        self.damage = 3

    # The distance will be defined with the manhattan distance from targets

    def distanceUnits(self, target):
        dist = 0
        #print(self.position)
        for i in range(2):
            dist += abs(self.position[i] - target.position[i])
        return dist


    def chooseTarget(self, map):
        dist = 100
        targetList = []
        #print(self.enemyList)
        for enemy in self.enemyList:
            #print(self.distanceUnits(enemy))
            if self.distanceUnits(enemy) < dist and enemy.isReachable(map):
                dist = self.distanceUnits(enemy)
                targetList = []
                targetList.append([enemy.position[0], enemy.position[1], enemy])
            elif self.distanceUnits(enemy) == dist: #and targetNotBlocked(map, self.position, enemy.position):
                targetList.append([enemy.position[0], enemy.position[1], enemy])

            if len(targetList) is 0:
                #if self.distanceUnits(enemy) < dist and targerNotBlocked(map, self.position, enemy.position):
                if targetNotBlocked(map, self.position, enemy.position):
                    dist = self.distanceUnits(enemy)
                    targetList = []
                    targetList.append([enemy.position[0], enemy.position[1], enemy])
        sortedEnemy = sorted(targetList, key=operator.itemgetter(0, 1, 2))
        return sortedEnemy[0][2], dist


    def isReachable(self, map):
        neighbours = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        state = False
        for y in neighbours:
            neighPos = [y[0]+self.position[0], y[1] + self.position[1]]
            if map[neighPos[0]][neighPos[1]] is ".":
                state = True
        return state


    def potentialMove(self, target, map):
        moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        potMoves = []
        for x in moves:
            #print(type(self.position[0]))
            move = [x[0] + self.position[0], x[1]+self.position[1]]
            if map[move[0]][move[1]] is ".":
                potMoves.append(move)
        #print(type(target))
        potDist = []
        dist = 100
        for y in potMoves:
            #if distance(y, target.position) < distance(self.position, target.position):
            #if map[y[0]][y[1]] is "." and distance(y, target.position) < distance(self.position, target.position)\
                    #and targetNotBlocked(map, y, target.position):
            if map[y[0]][y[1]] is "." and targetNotBlocked(map, y, target.position):
                potDist.append([distance(y, target.position), y[0], y[1]])
        print("The potential list is:" + str(potDist))
        moveList = sorted(potDist, key=operator.itemgetter(0, 1, 2))
        #print(oveList)
        if len(potDist) == 0:
            return self.position
        else:
            print("The chosen potential move is:" + str([moveList[0][1], moveList[0][2]]))
            return [moveList[0][1], moveList[0][2]]

    def battle(self):
        attackpattern = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        for x in attackpattern:
            attack = [x[0] + self.position[0], x[1]+self.position[1]]
            #print("The attack is:" + str(attack))
            for y in self.enemyList:
                if attack[0] is y.position[0] and attack[1] is y.position[1]:
                    #print("It is a hit!")
                    y.health -= self.damage
    # The decision is made by the shortest distance and order


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

    # We need to identify the units on the map

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

    def step(self):
        self.orderList()
        #print(self.orderList())
        for unit in self.unitList:

            [enemy, dist] = unit.chooseTarget(self.map)
            #print("The distance is: " +str (dist))
            if dist != 1:
                unit.position = unit.potentialMove(enemy, self.map)
            unit.battle()
            self.updateMap()
            self.printMap()


    def setup(self):
        self.filterMap()
        self.findUnits()
        self.setEnemies()

    def updateMap(self):
        testMap = []
        for maps in self.baseMap:
            testMap.append(maps)
        for unit in self.unitList:
            testString = list(testMap[unit.position[0]])
            testString[unit.position[1]] = unit.Class
            testString = "".join(testString)
            testMap[unit.position[0]] = testString

            #[unit.position[1]] = unit.Class
        self.map = testMap

    def printMap(self):
        for i in range(len(self.map)):
            print(self.map[i], end=" ")
    def printBase(self):
        for i in range(len(self.baseMap)):
            print(self.baseMap[i], end=" ")


class distanceMap:
    def __init__(self, map):
        self.map = map
        self.distList = []
        self.moves = [[0,1], [0,-1], [1, 0], [-1, 0]]

#def rules(initialMove, previousMove):
 #   if initialMove == [0, 1]:


def distance(user, target):
    dist = 0
    for i in range(2):
        dist += abs(user[i] - target[i])
    return dist


def targetNotBlocked(map, unit, target):
    state = True
    xpos = [unit[0], target[0]]
    xpos = [min(xpos), max(xpos)]

    ypos = [unit[1], target[1]]
    ypos = [min(ypos), max(ypos)]

    for i in range(xpos[0], xpos[1]):
        if map[i][unit[1]] is not ".":
            state = False
            break
    for j in range(ypos[0], ypos[1]):
        if map[unit[0]][j] is not ".":
            state = False
            break
    return state


def priority(list):
    list = sorted(list, key=operator.itemgetter(0, 1))
    return list


def test(filepath):
    initMap = Map()
    initMap.importMap(filepath)
    initMap.setup()
    #print(len(initMap.unitList))

    print("Now it begins")
    initMap.printMap()
    #initMap.printBase()
    for i in range(1):
        initMap.step()
        print("The next step! WOOP WOOP------------------------- AT ROUND" + str(i))
        initMap.printMap()
        #for unit in initMap.unitList:
            #print("The class is "+unit.Class + " and the health is now "+str(unit.health))
test("day15/test.txt")
