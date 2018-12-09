
#Include some standard libraries
from __future__ import print_function
import string
import timeit

filepath = "input.txt"

#letterList = string.ascii_uppercase + string.ascii_lowercase


with open(filepath) as fp:
    line = fp.readline()
numData = line.split(" ")

# Fix the last newline import
numData[len(numData)-1]=(numData[len(numData)-1])[0]
rootMult = numData[len(numData) - 11:len(numData)]
letterList=["hej"]*len(numData)
letterList[0]="Root"
i = 0
letterIndex = 0
totalSum = 0
Rootsum = 0
previousleaf = ""
rootvalues =[]
leafIndex = 0
rootSum = 0

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
    def add_child(self, obj):
        self.children.append(obj)
        self.childAmount =int(self.childAmount)+1

# root = Node("A",[2,3,4])
# root.name = "A"
# >>> root.value
# [2, 3, 4]


def sumStringList(numList):
    value = 0
    for i in range(len(numList)):
        value = int(numList[i]) + value
    return value


def childrenStatus(self ):
    global i
    global letterIndex
    global totalSum
    global rootSum
    global previousleaf
    global rootvalues
    while i < len(numData):
        if int(self.childAmount) < int(self.maxChild):
            previousleaf = self.name[0]
            if previousleaf == "Root":
                print("hej")
                rootvalues = rootMult
            else:
                rootvalues = self.value
            letterIndex = letterIndex + 1
            childname = letterList[letterIndex]
            i = i + 2
            nodevalues = [childname, numData[i], numData[i+1] ]
            node = Node(nodevalues[0],nodevalues[2], int(nodevalues[1]))
            self.add_child(node)
            status = "Adding child %s to  parent %s" %(letterList[letterIndex], self.name)
            #print(status)
            childrenStatus(self.children[int(self.childAmount)-1])
        else:
            i = i + 2
            metamax = i + int(self.value)
            self.value = numData[i:metamax]
            totalSum = totalSum + sumStringList(self.value)
            i = metamax -2
            status = "Child %s has metavalue %s" %(self.name, self.value)
            rootvalues = self.value
            if previousleaf is "Root":
                print(leafIndex)
                #rootSum = multiplyByindex(str(leafIndex), rootMult, sumStringList(self.value))+ rootSum
            break


def treeRun():
    global rootvalues
        # First two numbers represent <amount of children> <metadata>
        # After that is the children with similiar structure
    children = numData[i]
    metasize = int(numData[i+1])
    letter = [letterList[letterIndex]]
    rootvalues = [[letterList[letterIndex]],numData[i], numData[i+1], ]
    root = Node(rootvalues[0],rootvalues[2], rootvalues[1])
    print(root.name)
    print(type(root.name))
    print(root.name[0])
    print(type(root.name[0]))
    if root.name[0] == "Root":
        print("hej")
    #rootBase = numData[len(numData)-:len(numData)]
    childrenStatus(root)
    print(totalSum)
    print(rootMult)


def test():
    for i in range(4):
        print(i)

#test()
treeRun()







