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

The main class is the map, which is the whole cart system is involved, methods here inludes methods to copy a map, 
how to import the information from a txt file, how to find the carts, as well as how to update the map and carts.
With time moving forward.

'''
class map:
    def __init__(self):
        self.map = []
        self.baseMap = []

    def importMap(self, filepath):
        lengthOfFile = file_len(filepath)
        self.map = []
        with open(filepath) as fp:
            for cnt in range(lengthOfFile):
                line = fp.readline()
                self.map.append(line)

    def copyMap(self, copy):
        self.map = []
        for i in range(len(copy.map)):
            self.map.append(copy.map[i])


    def filterMap(self):
        for i in range(len(self.map)):
            self.baseMap.append(self.map[i].replace('<', '-').replace('>', '-').replace('^', '|').replace('v', '|'))


    def print(self):
        for i in range(len(self.map)):
            print(str(i)+":"+self.map[i], end=" ")

    def printBase(self):
        for i in range(len(self.baseMap)):
            print(self.baseMap[i], end=" ")

    def findCart(self):
        cartlist = []
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                sign = self.map[i][j]
                if sign is "<" or sign is ">" or sign is "v" or sign is "^":
                    cartlist.append(cart([i, j], sign))
        return cartlist

    '''
    
    Probably the most important function in this code, it based on some certain steps.
    1. Sort the current cart list in the order that they move with ticks.
    2. After that each cart that crashes with each other gets a crash mark. Which is a sign to remove them after 
       complete update.
    3. After that either the first crash is saved, or the last cart that hasn't crashed is saved for further use.
    
    '''

    def updateCartList(self, cartlist):
        # Create new cart list
        firstiter = 0
        newList = []
        for i in range(len(cartlist)):
            newList.append([cartlist[i].position[0], cartlist[i].position[1], cartlist[i].sign,
                            cartlist[i].velocity, cartlist[i].intersection])
            sortedList = sorted(newList, key=operator.itemgetter(1, 0))
        cartlist2 = []
        for j in range(len(cartlist)):
            cartlist2.append(cart([sortedList[j][0], sortedList[j][1]], sortedList[j][2]))
            cartlist2[j].intersection = sortedList[j][4]

        state = False
        position = [0, 0]
        newerList = []
        index = 0
        for i in range(len(cartlist2)):
            newerList.append(cartlist2[i])
        #while index < len(newerList) and len(newerList) > 1:
        for i in range(len(newerList)):
            newerList[i].updateCart(self.baseMap)
            for j in range(len(newerList)):
                if i != j:
                    if newerList[i].position == newerList[j].position:
                        print("Skiten crashar vid! "+str(newerList[j].position))
                        newerList[i].crash = 1
                        newerList[j].crash = 1
                        if firstiter == 0:
                            position = newerList[i].position
                            state = True
                            firstiter += 1

        filterList = []
        for i in range(len(newerList)):
            if newerList[i].crash == 0:
                filterList.append(newerList[i])
        if len(filterList) == 1:
            position = filterList[0].position

        return filterList, state, position

    def updateMap(self, cartlist):
        for i in range(len(self.map)):
            self.map[i] = self.baseMap[i]
        for i in range(len(cartlist)):
            testString = ""
            [position, sign] = [cartlist[i].position, cartlist[i].sign]
            x = position[0]
            y = position[1]
            testString = self.map[x][0:y] + sign + self.map[x][y+1:len(self.map[x])]
            self.map[x] = testString

'''

The cart is the one rolling around, and has a position, velocity, intersection ticker and a crash mark.
The cart updates by looking at the base map, without any other carts in it.

'''

class cart:
    def __init__(self, position, sign):
        self.position = position
        self.sign = sign
        self.velocity = velocitySetup(sign, [0, 0])
        self.intersection = 0
        self.crash = 0


    def updateCart(self, map):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        nextSign = map[self.position[0]][self.position[1]]
        [self.sign, self.intersection] = velocityUpdate(nextSign, self.sign, self.intersection)
        self.velocity = velocitySetup(self.sign, self.velocity)

    def printCart(self):
        print("Here is a nice cart!")
        print(self.position, end=" ")
        print(self.sign, end=" ")
        print(self.velocity)


'''

Velocity rules and update methods.

'''

def velocitySetup(sign, oldVelocity):
    if sign is "<":
        velocity = [0, -1]
    elif sign is ">":
        velocity = [0, 1]
    elif sign is "^":
        velocity = [-1, 0]
    elif sign is "v":
        velocity = [1, 0]
    else:
        velocity = oldVelocity
    return velocity


def velocityUpdate(sign, velSign, intersect):
    l = ["/", "^", "<", ">", "v", "-", "|", "+"]
    if sign is "/":
        if velSign is '<':
            velSign = "v"
        elif velSign is ">":
            velSign = "^"
        elif velSign is "v":
            velSign = "<"
        else:
            velSign = ">"

    elif sign is "+":
        if intersect % 3 == 2:
            velSign = velSign
            if velSign is ">":
                velSign = "v"
            elif velSign is "v":
                velSign = "<"
            elif velSign is "<":
                velSign = "^"
            else:
                velSign = ">"
        elif intersect % 3 == 1:
            velSign = velSign
        else:
            if velSign is ">":
                velSign = "^"
            elif velSign is "v":
                velSign = ">"
            elif velSign is "<":
                velSign = "v"
            else:
                velSign = "<"
        intersect += 1
    #elif sign is '\\':
    elif not any(substring in sign for substring in l):
        if velSign is "<":
            velSign = "^"
        elif velSign is ">":
            velSign = "v"
        elif velSign is "v":
            velSign = ">"
        else:
            velSign = "<"
    else:
        velSign = velSign
    #velSign = velSign
    return velSign, intersect


def crash(cartList):
    state = False
    position = [0, 0]
    for i in range(len(cartList)):
        for j in range(len(cartList)):
            if i != j:
                if cartList[i].position == cartList[j].position:
                    state = True
                    print("Skiten crashar!")
                    position = cartList[i].position

    return state, position





def filterMap(map):
    for i in range(len(map)):
        print(map[i])
        map[i].replace('-', '<').replace('>', '-').replace('^', '|').replace('v', '|')

def test():
    initMap = map()

    initMap.importMap("day13/input.txt")
    initMap.filterMap()
    #initMap.print()
    initMap.printBase()
    cartlist = initMap.findCart()


    firstTry = 0
    firstCrash =[0, 0]
    firstTime = 0

    for i in range(15000):
        [cartlist, state, position] = initMap.updateCartList(cartlist)
        initMap.updateMap(cartlist)
        #initMap.print()
        if state is True and firstTry == 0:
            firstCrash = position
            firstTime = i
            firstTry += 1

        if len(cartlist) <= 1:
            print("Only one remaining")
            break
        if i % 100 == 0:
            print("Current status is at time: " + str(i))
    [x, y] = position
    #print(initMap.map[position[0]][position])
    initMap.map[x]= initMap.map[x][0:y] + str(cartlist[0].sign) + initMap.map[x][y+1:len(initMap.map[x])]

    initMap.print()
    print("The first crash is at position: ["+str(firstCrash[1])+"," + str(firstCrash[0]) +
          "] at the time of "+str(firstTime))
    print("The last cart is at at position : [" + str(y) + ", " + str(x) + "]" + " at time: " + str(i))


test()




