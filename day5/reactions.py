#Include some standard libraries
from __future__ import print_function
import string

def rule(letter1, letter2):
    status = ""
    # First check if they are of the same type
    if letter1.lower()==letter2.lower():
        if letter1.islower() and letter2.isupper():
            status = "pop"
        elif letter1.isupper() and letter2.islower():
            status = "pop"
        else:
            status = "continue"
    else:
        status = "continue"
    return status


def filtertype(text,letter):
    i = 0
    while i < len(text):
        if text[i].lower() == letter and i+1 < len(text):
            start = text[0:i]
            end = text[i+1:len(text)]
            text = start + end
        elif text[i].lower() == letter and i+1 == len(text):
            text = text[0:i-1]
            break
        else:
            i = i + 1
    return text



def pop(indexes, genelist):
    try:
        start = genelist[0:indexes[0]]
        end = genelist[indexes[1]+1:len(genelist)]
        newstring = start + end
    except:
        errStatus = "String out of range with withinn indexes %s, and a total length%s" \
                    % (indexes, len(genelist))
        print(errStatus)
    return newstring, genelist[indexes[0]], genelist[indexes[1]]

def testPop(text):
    index = [0, 1]
    i = 1
    while i < 10:
        status = rule(text[index[0]], text[index[1]])
        if status == "pop":
            state = "pop at %s and %s" % (index[0], index[1])
            text = pop(index, text)
            print(text)
        else:
            if (index[1]+1) == len(text):
                index = [0, 1]
            else:
                index[0] = index[0] + 1
                index[1] = index[1] + 1


def testrun(filepath):
    index=[0,1]

    # Save the string in the input file in a line
    with open(filepath) as fp:
        line = fp.readline()
        iter = 0
    while iter < 1000:
        #print(index[0])
        #print(index[1])

        status = rule(line[index[0]],line[index[1]])
        if status == "pop":

            [line, pop1, pop2] = pop(index,line)
            state = "pop at %s and %s the letters popped are [%s and %s] at new location lies [%s and %s]" \
                    % (index[0], index[1], pop1, pop2, line[index[0]], line[index[1]])
            print(state)
            #line = lineData[0]
            #checkIndex = lineData[1]
            #index = [checkIndex, checkIndex +1]
        else:

            if (index[1]+1) == len(line):
                index = [0, 1]
                state = "length of line is %s, new check is from [%s, %s]" % (len(line), index[0] , index[1] )
                #print(state)
                iter = iter +1
            else:
                state = "length of line is %s, new check is from [%s, %s]" % (len(line), index[0]+1, index[1]+1)
                #print(state)
                index[0] = index[0] + 1
                index[1] = index[1] + 1


    print(len(line))
    with open("resultFile.txt", 'w') as file_handler:
        for item in line:
            file_handler.write("{}".format(item))
    #print(len(line))

def testrun2(filepath):
    bestunit = ""
    bestcomplexity = 99999
    # Open the base file
    with open(filepath) as fp:
        baseString = fp.readline()

    letterList = string.ascii_lowercase
    for i in range(len(letterList)):
        status = "working on letter %s" % letterList[i]
        print(status)
        tempString = filtertype(baseString,letterList[i])
        repeat = 0
        oldValue = len(tempString)
        index = [0,1]
        while repeat == 0:
            try:
                status = rule(tempString[index[0]], tempString[index[1]])
            except:
                errStatus = "String out of range with letter %s, withing indexes %s, and a total length %s" \
                            % (letterList[i], index, len(tempString))
                print(errStatus)

            if status == "pop":

                [tempString, pop1, pop2] = pop(index, tempString)
                if index[1] == len(tempString):
                    index[0] = index[0]-1
                    index[1] = index[1]-1
            else:

                if (index[1] + 1) == len(tempString):
                    index = [0, 1]
                    if len(tempString) == oldValue:
                        repeat = 1
                    oldValue = len(tempString)
                else:
                    index[0] = index[0] + 1
                    index[1] = index[1] + 1

        # Now check if the letter is better
        if len(tempString) < bestcomplexity:
            bestcomplexity = len(tempString) -1
            bestunit = letterList[i]
            status = "New record! %s take the lead with %s reactions" % (bestunit, bestcomplexity)
            print(status)

    status = "Best reactions is given by removing %s with a %s amount of reactions" % (bestunit, bestcomplexity)
    print(status)

testrun2("input.txt")