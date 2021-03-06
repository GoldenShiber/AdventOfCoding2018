# Include some standard libraries
from __future__ import print_function
import string
import timeit

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from usefulFunctions import *

filepath = "../day8/input.txt"
with open(filepath) as fp:
    line = fp.readline()
numData = line.split(" ")

# Fix some global functions, warning NOT BEAUTIFUL

numData[len(numData) - 1] = (numData[len(numData) - 1])[0]
rootMult = numData[len(numData) - 11:len(numData)]
letterList = ["hejNod"] * len(numData)
letterList[0] = "Root"
i = 0
letterIndex = 0
totalSum = 0
Rootsum = 0
previousleaf = ""
rootvalues = []
leafIndex = 0
rootSum = 0
basedRootValue = 0
class Node:

    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def PrintTree(self):
        print(self.data)


class Node(object):
    def __init__(self, name, value, maxchild):
        self.name = name
        self.value = value
        self.children = []
        self.childAmount = 0
        self.maxChild = maxchild
        self.rootSum = 0
        self.counter = 0

    def add_child(self, obj):
        self.children.append(obj)
        self.childAmount = int(self.childAmount) + 1

    '''
    Function to add the root sum to the nodes
    '''
    def rootSumReal(self):
        self.counter = 0
        self.rootSum = 0
        while self.counter <= len(self.value):
            try:
                if int(self.children[int(self.value[self.counter])-1].maxChild) != 0:
                    self.rootSum += self.children[int(self.value[self.counter])-1].rootSumReal()
                    self.counter += 1
                elif int(self.children[int(self.value[self.counter])-1].maxChild) == 0:
                    self.rootSum += sumStringList(self.children[int(self.value[self.counter])-1].value)
                    self.counter += 1
            except:
                    self.rootSum += 0
                    self.counter += 1
        return self.rootSum


def sumStringList(numList):
    value = 0
    for i in range(len(numList)):
        value = int(numList[i]) + value
    if value is None:
        value = 0
    return value


'''
Function to fill the tree from the text document
'''

def childrenStatus(self):
    global i
    global letterIndex
    global totalSum
    global previousleaf
    global rootvalues
    while i < len(numData):
        if int(self.childAmount) < int(self.maxChild):
            previousleaf = self.name[0]
            if previousleaf == "Root":
                rootvalues = rootMult
            rootvalues = self.value

            letterIndex = letterIndex + 1
            childname = letterList[letterIndex]
            i = i + 2
            nodevalues = [childname, numData[i], numData[i + 1]]
            node = Node(nodevalues[0], nodevalues[2], int(nodevalues[1]))
            self.add_child(node)
            status = "Adding child %s to  parent %s" % (letterList[letterIndex], self.name)
            # print(status)
            childrenStatus(self.children[int(self.childAmount) - 1])
        else:
            i = i + 2
            metamax = i + int(self.value)
            self.value = numData[i:metamax]
            totalSum = totalSum + sumStringList(self.value)
            i = metamax - 2
            rootvalues = self.value

            break

def treeRun():
    global rootvalues
    # First two numbers represent <amount of children> <metadata>
    # After that is the children with similiar structure
    rootvalues = [[letterList[letterIndex]], numData[i], numData[i + 1], ]
    root = Node(rootvalues[0], rootvalues[2], rootvalues[1])
    start = timeit.default_timer()
    childrenStatus(root)
    stop = timeit.default_timer()
    part1Time = stop - start
    print('The Sum of all metavalues is:', totalSum)
    start = timeit.default_timer()
    rootsum = root.rootSumReal()
    stop = timeit.default_timer()
    part2Time = stop - start
    print('The Root sum of the root is:', rootsum)


    print('Time for part 1 is: ', part1Time, "s")
    print('Time for part 2 is: ', part2Time, "s")


# test()
treeRun()







