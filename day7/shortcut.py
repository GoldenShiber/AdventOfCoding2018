from __future__ import print_function
import string
import timeit

def findIndex(word, letter):
    lengthOfFile = len(word)
    index = 0
    for i in range(lengthOfFile):
        if word[i] == letter:
            index = i
            break
    return index

def file_len(filename):
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def findMax(list):
    maxValue = max(list)
    for i in range(len(list)):
        if list[i] == maxValue:
            index = i
            break
    return maxValue, index

def createRuleMatrix(filepath):
    letterList = string.ascii_uppercase
    size = len(letterList)
    ruleMap = [[None for x in range(size)] for z in range(size)]
    return ruleMap

def insertRules(rulemap, filepath):
    letterList = string.ascii_uppercase
    lengthOfFile = file_len(filepath)
    with open(filepath) as fp:
        for cnt in range(lengthOfFile):
            line = fp.readline()
            req = line[5]
            reqIndex = findIndex(letterList,req)
            node =line[36]
            nodeIndex = findIndex(letterList, node)
            rulemap[nodeIndex][reqIndex] = 0
    return rulemap

def isLetterReady(rulematrix, letter):
    state = True
    letterList = string.ascii_uppercase
    index = findIndex(letterList, letter)
    for i in range(len(rulematrix)):
        if rulematrix[index][i] == 1:
            state = True
        elif rulematrix[index][i] == 0:
            state = False
            break
    return state

def updateList(rulematrix, letter):
    letterList = string.ascii_uppercase
    index = findIndex(letterList, letter)
    for i in range(len(rulematrix)):
        if rulematrix[i][index] == 0:
            rulematrix[i][index] = 1
    return rulematrix

def nextLetter(progress, rulematrx):
    letterList = string.ascii_uppercase
    for i in range(len(letterList)):
        if progress[i] == 0 and isLetterReady(rulematrx, letterList[i]):
            progress[i] = 1
            break
    return progress, letterList[i]

def updateWorker(workList,rulematrix, elfList):
    # The worker list is defined by three conditions
    #First what letter it is
    #Second is if someone is working on it.
    #Third is time left

    # Start string is empty ""
    doneString=""
    workString =""

    letterList = string.ascii_uppercase

    time = 0
    while len(doneString) < len(letterList):

        # check if index is empty and if that is the case, add a worker to it with the included
        for i in range(len(workList[0])):
            if workList[0][i] is None:

                newLetter = ""
                threshold = 999
                # First find the avialble letters for the current worker progress
                for l in range(len(letterList)):
                    if letterList[l] not in doneString and isLetterReady(rulematrix, letterList[l]) and letterList[l] not in workString:
                            if threshold > ord(letterList[l]):
                                newLetter = letterList[l]
                                threshold = ord(newLetter)

                if newLetter is not "":
                    workString = workString + newLetter
                    workList[0][i] = newLetter
                    for j in range(len(elfList)):
                        if elfList[j][1] == 0:
                            workList[1][i] = elfList[j][0]
                            elfList[j][1] = 1
                            break
                    workList[2][i] = ord(workList[0][i])-64+60

                    statusWork = "Current Letters are%s\nCurrent workers are %s\nCurrent time is %s\n and time taken is %s\n" \
                         % (workList[:][0], workList[:][1], workList[:][2], time)


        #Take away finished progresses and reduce time
        for k in range(len(workList[0])):
            if isLetterReady(rulematrix, workList[0][k]) and workList[0][k] is not None: #and workList[2][k] is not None:
                workList[2][k] = workList[2][k] -1
                if workList[2][k] == 0:
                    doneString = doneString + workList[0][k]
                    rulematrix = updateList(rulematrix, workList[0][k])
                    workList[0][k] = None
                    elfList[workList[1][k]-1][1] = 0
                    workList[1][k] = None
                    workList[2][k] = None

        time = time + 1
    print(doneString)
    print(time)
    return workList

def testRun(filepath):
    start = timeit.default_timer()
    stringorder = ""
    rulemap = createRuleMatrix(filepath)
    rulemap = insertRules(rulemap, filepath)
    letterList = string.ascii_uppercase
    progress = [0] * len(letterList)

    while sum(progress) < len(letterList):
        [progress, letter] = nextLetter(progress, rulemap)
        rulemap = updateList(rulemap, letter)
        stringorder = stringorder + letter
    print(stringorder)

    stop = timeit.default_timer()
    part1Time = stop - start

    # Now for part 2 we use parallel elf working force
    # We know the string order.

    start = timeit.default_timer()

    # Create a time list needed for each letter

    rulemap = createRuleMatrix(filepath)
    rulemap = insertRules(rulemap, filepath)

    timeCost = [0] * len(letterList)
    for i in range(len(stringorder)):
       timeCost[i]= ord(stringorder[i]) - 64 + 60
    print(timeCost)

    letterIndex = 0
    workMap = [[None for x in range(5)] for z in range(3)]
    # Workers defined by the numbers 1 to 4, second column checks if they work
    elfList = [[0 for x in range(2)] for z in range(5)]
    elfList[0][0] = 1
    elfList[1][0] = 2
    elfList[2][0] = 3
    elfList[3][0] = 4
    elfList[4][0] = 5

    updateWorker(workMap, rulemap, elfList)

    stop = timeit.default_timer()
    part2Time = stop - start

    print('Time for part 1 is: ', part1Time, "s")
    print('Time for part 2 is: ', part2Time, "s")


testRun("input.txt")
