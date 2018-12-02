#Include some standard libraries
from __future__ import print_function
import re
#To make sure you didn't miss any, you scan the likely candidate boxes again, counting the number that have an ID
# containing exactly two of any letter and then separately counting those with exactly three of any letter.
#  You can multiply those two counts together to get a rudimentary checksum and compare it to what your device predicts.

#For example, if you see the following box IDs:

#abcdef contains no letters that appear exactly two or three times.
#bababc contains two a and three b, so it counts for both.
#abbcde contains two b, but no letter appears exactly three times.
#abcccd contains three c, but no letter appears exactly two times.
#aabcdd contains two a and two d, but it only counts once.
#abcdee contains two e.
#ababab contains three a and three b, but it only counts once.

#Of these box IDs, four of them contain a letter which appears exactly twice, and three of them contain a letter which
#appears exactly three times. Multiplying these together produces a checksum of 4 * 3 = 12.


def lettercheck(id):
    saveID = id
    twocount = 0
    threecount = 0
    # Create Lists for occurrence and the letter
    letterlist = [None] * 100
    occurrencelist = [None] * 100
    startIndex = 0
    while len(saveID) is not 0:
        checkletter = saveID[0]
        countlist = checkIndexes(checkletter, saveID)
        letterlist[startIndex] = checkletter
        occurrencelist[startIndex] = len(countlist)
        if len(countlist) == 2:
            twocount =1
        elif len(countlist) == 3:
            threecount = 1
        status = "Currently used letter is %s and occurs %s times, found from %s" % (checkletter,
                                                                                     len(countlist), saveID)
        saveID = re.sub(checkletter, '', saveID)
        #print(status)
    return twocount, threecount



def checkIndexes(letter, id):
    idlength = len(id)
    indexlist = [None] * 1
    for i in range(idlength):
        if id[i]==letter:
            if len(indexlist)==1:
                if indexlist[0] is None:
                    indexlist[0] = i
                else:
                    indexlist.append(i)
            else:
                indexlist.append(i)
    return indexlist

def file_len(filename):
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def findcommonletters(word1, word2):
    # Create a dummy string, as well as a miss counter
    wordlength = len(word1)
    dummystring = ""
    count = 0
    for i in range(wordlength):
        if word1[i] == word2[i]:
            dummystring = dummystring + word1[i]
        else:
            count = count +1
    return dummystring, count



def testrunsum(filepath):
    baseValue = [0,0]
    lengthOfFile = file_len(filepath)

    # loop the data as many times as needed
    with open(filepath) as fp:
        for cnt in range(lengthOfFile):
            line = fp.readline()
            print("Line {}: {}".format(cnt, line.strip()))
            occurence = lettercheck(line)
            # Update the occurrence
            baseValue[0] = baseValue[0] + occurence[0]
            baseValue[1] = baseValue[1] + occurence[1]
    sum = baseValue[0]*baseValue[1]
    print(baseValue[0])
    print(baseValue[1])
    print(sum)


def testruncommon(filepath):
    basestrings = ["", 100]
    beststrings = basestrings
    lengthOfFile = file_len(filepath)
    # Create a list to be filled with all the IDs
    Idlist = ["hohoho"]*lengthOfFile
    # loop the data as many times as needed
    with open(filepath) as fp:
        for cnt in range(lengthOfFile):
            line = fp.readline()
            #fill the list
            Idlist[cnt] = line

    for j in range(lengthOfFile):
        for k in range(j,lengthOfFile):
            if j is not k:
                teststring = findcommonletters(Idlist[j], Idlist[k])
                #print(teststring)
                if teststring[1]<beststrings[1]:
                    beststrings = teststring
    print(beststrings)


#test3()
#testrunsum("input.txt")
testruncommon("input.txt")

