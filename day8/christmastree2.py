# Include some standard libraries
from __future__ import print_function
import string
import timeit

filepath = "input.txt"
#filepath = "example3.txt"
#filepath = "example2.txt"

# letterList = string.ascii_uppercase + string.ascii_lowercase


with open(filepath) as fp:
    line = fp.readline()
numData = line.split(" ")

# Fix the last newline import
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


    def rootSumReal(self):
        self.counter = 0
        self.rootSum = 0
        #while self.counter <= int(self.maxChild)+2:
        while self.counter <= len(self.value):
            try:
                #print(self.value)
                print('Currently working with index:', int(self.value[self.counter]), ' and the name:',self.name )
                if int(self.children[int(self.value[self.counter])-1].maxChild) != 0:
                    self.rootSum += self.children[int(self.value[self.counter])-1].rootSumReal()
                    print('Counter is at:', self.counter,' With the name :', self.name)
                    self.counter += 1
                    print('Counter moved to:', self.counter, ' With the name :', self.name)
                #elif self.children[iterations].maxChild == 0:
                elif int(self.children[int(self.value[self.counter])-1].maxChild) == 0:
                    self.rootSum += sumStringList(self.children[int(self.value[self.counter])-1].value)
                    print('We have met a child end.')
                    print('Current rootSum is:', self.rootSum)
                    self.counter += 1
                    print('Counter moved to:', self.counter, ' With the name :', self.name)
            except:
                try:
                    print('We have met a dead end, metavalue does not point to an available child')
                    print('The meta data is :', self.value, ' with the pointer:', )
                    self.rootSum = sumStringList(self.children[int(self.value[self.counter])-1].value)
                    print('The sum is:', self.rootSum)
                    print('Counter is at:', self.counter,' With the name :', self.name)

                except:
                    print('Bad end!')
                    self.rootSum += 0
                self.counter += 1
                print('Counter moved to:', self.counter, ' With the name :', self.name)
        #print(self.children[0].rootSum)
        return self.rootSum


def sumStringList(numList):
    value = 0
    for i in range(len(numList)):
        value = int(numList[i]) + value
    if value is None:
        value = 0
    return value


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
                print("hej")
                rootvalues = rootMult
            # else:
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
            #print('what is happening with metamax',self.value)
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
    print(root.name)
    print(type(root.name))
    print(root.name[0])
    print(type(root.name[0]))
    if root.name[0] == "Root":
        print("hej")
    childrenStatus(root)
    print(totalSum)
    root.rootSumReal()
    print(root.rootSum)


def test():
    for i in range(4):
        print(i)


# test()
treeRun()







