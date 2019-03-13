from __future__ import print_function
import string
import timeit
import re

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from usefulFunctions import *


class ruleList:
    def __init__(self):
        self.rule = []
        self.result = []

def importRulesAndState(filepath):
    lengthOfFile = file_len(filepath)
    rules = ruleList()
    initialState = ""
    with open(filepath) as fp:
        for cnt in range(lengthOfFile):
            line = fp.readline()
            # Import initial state
            if cnt < 1:
                initState =re.split(': |\n', line)
                initialState = initState[1]
            # Only import the rules, not the initial state
            if cnt >=2:
                ruleInfo = re.split(' |\n', line)
                rules.rule.append(ruleInfo[0])
                rules.result.append(ruleInfo[2])

    return rules, initialState


def checkRules(rules, testPot):
    #print(testPot)
    state = "."
    for i in range(len(rules.rule)):
        if isSameString(testPot, rules.rule[i]):
            state = rules.result[i]
            break
    if state =="0":
        print("Something is wrong at with test pot: " + testPot)
    return state

def isSameString(string1, string2):
    if string1 == string2:
        return True
    else:
        return False


def countPlantSum(plantString, buffert):
    count = 0
    for i in range(len(plantString)):
        if plantString[i] is '#':
            count += (i-buffert)
    return count


def identityTestPot(index, totalPot):
    testString = ""
    upperBound = index + 2
    lowerBound = index -2
    if upperBound < len(totalPot) and lowerBound >= 0:
        testString = totalPot[lowerBound:upperBound+1]
    elif upperBound >= len(totalPot):
        testString = totalPot[lowerBound:len(totalPot)] + totalPot[0:upperBound-len(totalPot)+1]
    else:
        testString = totalPot[len(totalPot) + lowerBound:len(totalPot)] + totalPot[0:upperBound+1]
    if len(testString) != 5:
        print( "Something is wrong at index: " +str(index))
    return testString


'''
Work in progress, don't know how zero index works...
'''

def test(filepath, timeSteps):
    plantCount = 0
    zeroIndex = 0
    [rules, initState] = importRulesAndState(filepath)
    print("The initial state is: "+initState)
    for i in range(timeSteps):
        #zeroIndex -= 2
        testState = ""
        for j in range(len(initState)):
            testPot = identityTestPot(j,initState)
            testState += checkRules(rules, testPot)

    plantCount += countPlantSum(initState, zeroIndex)

#importRulesAndState("../day12/input.txt")
#checkRules()
test("../day12/example.txt",20)
#test("../day12/input2.txt",20)