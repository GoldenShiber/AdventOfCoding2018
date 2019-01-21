from __future__ import print_function
#from ..usefulFunctions import *
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from usefulFunctions import *

import timeit



def letterCounter(id):
    checkList = [0,0]
    letterList = [None]*0
    counterList = [int]*0
    idLength = len(id)
    for i in range(idLength):
        if id[i] in letterList:
            letterIndex = findIndex(letterList, id[i])
            counterList[letterIndex] += 1
        else:
            letterList.append(id[i])
            counterList.append(1)
    if 3 in counterList:
        checkList[1] = 1
    if 2 in counterList:
        checkList[0] = 1
    return checkList


def findcommonletters(word1, word2):
    # Create a dummy string, as well as a miss counter
    wordlength = len(word1)
    dummystring = ""
    count = 0
    for i in range(wordlength):
        if word1[i] == word2[i]:
            dummystring += word1[i]
        else:
            count += 1
    return dummystring, count


def main(filepath):
    lengthOfFile = file_len(filepath)

    start = timeit.default_timer()
    # Save the IDs into a last, as well as initialising sum counters
    beststrings = ["", 100]
    IDList = ["hohoho"] * lengthOfFile

    sumCounter = [0,0]
    with open(filepath) as fp:
        for cnt in range(lengthOfFile):
            line = fp.readline()
            IDList[cnt] = line
            counter = letterCounter(line)
            sumCounter[0] += counter[0]
            sumCounter[1] += counter[1]
    sum = sumCounter[0]*sumCounter[1]
    info = "The checksum of the packages is %s" % sum
    print(info)
    stop = timeit.default_timer()
    part1Time = stop - start
    print('Time for part 1 is: ', part1Time, "s")

    # Now find the closest packages
    start = timeit.default_timer()
    for j in range(lengthOfFile):
        for k in range(j,lengthOfFile):
            if j is not k:
                teststring = findcommonletters(IDList[j], IDList[k])
                if teststring[1]<beststrings[1]:
                    beststrings = teststring
    info = "Most common letters are %s" % beststrings[0]
    print(info)
    stop = timeit.default_timer()
    part2Time = stop - start
    print('Time for part 2 is: ', part2Time, "s")


main("../day2/input.txt")