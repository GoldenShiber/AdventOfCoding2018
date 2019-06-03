from __future__ import print_function
import string
import timeit
import re
import operator

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from usefulFunctions import *


class Elf:
    def __init__(self):
        self.mark = 0
        self.score = 0
        self.markSign =""

    def movement(self, map):
        move = self.score + 1
        #print(" The mark was previously at:" + str(self.mark))
        if self.mark + move > len(map)-1:
            #print("it is too long")
            self.mark += move % len(map)
            if self.mark >= len(map):
                self.mark -= len(map)
        else:
            self.mark += move
        #print("The move is :" +str(move))
        #print("The total map looks like: "+ map)
        #print("The new location of the recept is at:" +str(map[self.mark]))
        self.score = int(map[self.mark])


def sumElf(elves):
    sum = 0
    for i in range(len(elves)):
        sum += elves[i].score
    return str(sum)


def step(elves, map):
    map += sumElf(elves)
    for i in range(len(elves)):
        elves[i].movement(map)
    return map

def printMap(elves, map):
    if elves[0].mark < elves[1].mark:
        [first, last] = [0, 1]
    else:
        [first, last] = [1, 0]
    mapString = map[0:elves[first].mark] + elves[first].markSign[0] + map[elves[first].mark:elves[first].mark +1] +\
                    elves[first].markSign[1] + map[elves[first].mark +1:elves[last].mark] +\
                    elves[last].markSign[0] + map[elves[last].mark:elves[last].mark+1] + elves[last].markSign[1] +\
                    map[elves[last].mark+1:len(map)]
    print(mapString)


def printSumScore(cursor, map):
    print("The sum after recept "+str(cursor) + " is: " + map[cursor:cursor+10])


def findScore(score, map):
    state = False
    for i in range(len(map)):
        if state is False:
            if map[i] is score[0]:
                for j in range(1, len(score)):
                    if map[i+j] is not score[j]:
                        break
                    if j == len(score)-1:
                        state = True
                if state is True:
                    print(map[i:i+j])
        else:
            break
    print("The score: " +score + " is found after "+str(i -1) + " recept")



def setupData():
    elf1 = Elf()
    elf2 = Elf()
    [elf1.mark, elf1.score, elf1.markSign] = [0, 3, "()"]
    [elf2.mark, elf2.score, elf2.markSign] = [1, 7, "[]"]
    map = str(elf1.score) + str(elf2.score)
    elves = [elf1, elf2]

    for i in range(10000000):
        map = step(elves, map)
        #printMap(elves, map)
        if i % 100000 == 0:
            print("Currently at:[" +str(i) + "/" + str(10000000))
    printSumScore(5, map)
    printSumScore(18, map)
    printSumScore(939601, map)

    file = open('Information.txt', 'w')
    file.write(map)
    file.close()

def findRecept():
    lengthOfFile = file_len("Information.txt")
    map = ""
    with open("Information.txt") as fp:
        for cnt in range(lengthOfFile):
            map = fp.readline()
            #self.map.append(line)
    printSumScore(939601, map)

    findScore("51589", map)
    findScore("01245", map)
    findScore("92510", map)
    findScore("59414", map)
    findScore("939601", map)


'''

For part 2 we need a big data solution, since it takes millions of recepts to reach the goal.
BY using yield we can quickly yield the string together.

'''

def myGenerator(state, amount):
    post =[0, 1]
    for x in state:
        yield x

    for i in range(amount):
        score = [int(c) for c in str(state[post[0]] + state[post[1]])]
        state.extend(score)
        # Update positions
        for j in range(len(post)):
            post[j] = (post[j] + 1 + state[post[j]]) % len(state)
        # Then save the score to be added.
        for x in score:
            yield x

def solveWithEffectiveMethod(state, amount, target):

    intTarget = int(target)
    # Make a map
    targetList = list(map(int, str(target)))

    arr = []
    # Then generate the combinations
    for i, x in enumerate(myGenerator(state, amount)):
        arr.append(x)
        if i +1 -10 == intTarget:
            print("The sum for part 1 is: ", ''.join(map(str, arr[-10:])))
        if arr[-len(targetList):] == targetList:
            print('The amount of recepts created at part 2 is: ', i + 1 - len(targetList))
            break


solveWithEffectiveMethod([3, 7], 100000000, 939601)
