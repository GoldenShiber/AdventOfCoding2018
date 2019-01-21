#Include some standard libraries
from __future__ import print_function
import string
import timeit

'''
Rules for the reactions
'''

def rule(letter1, letter2):
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

'''
Pop mechanics
'''


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

'''
Filter text functions, while removing a letter type
'''

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
            i += 1
    return text


'''
The reaction function for the polymer problem
'''


def reactions(polymerstring):
    index=[0,1]
    line = polymerstring
    # Save the string in the input file in a line
    repeat = 0
    oldValue = len(line)
    while repeat == 0:
        status = rule(line[index[0]], line[index[1]])
        if status == "pop":

            [line, pop1, pop2] = pop(index, line)
            if index[1] == len(line):
                index[0] -= 1
                index[1] -= 1
        else:
            if (index[1] + 1) == len(line):
                index = [0, 1]
                if len(line) == oldValue:
                    repeat = 1
                oldValue = len(line)
            else:
                index[0] += 1
                index[1] += 1
    return line



def test(filepath):
    with open(filepath) as fp:
        line = fp.readline()
    start = timeit.default_timer()
    part1Poly = reactions(line)
    status = "The length after the reaction of the polymer is %s." % (len(part1Poly)-1)
    print(status)

    stop = timeit.default_timer()
    part1Time = stop - start
    print('Time for part 1 is: ', part1Time, "s")
    # Part 2 looks for the best genome to remove for shortest total polymer after reactions
    start = timeit.default_timer()
    bestunit = ""
    bestcomplexity = 99999
    letterList = string.ascii_lowercase
    for i in range(len(letterList)):
        status = "working on letter %s" % letterList[i]
        #print(status)
        tempString = filtertype(line, letterList[i])

        tempString = reactions(tempString)
        # Now check if the letter is better
        if len(tempString) < bestcomplexity:
            bestcomplexity = len(tempString)
            bestunit = letterList[i]
            status = "New record! %s take the lead with %s reactions" % (bestunit, bestcomplexity-1)
            print(status)


    status = "Best reactions is given by removing %s with a %s amount of reactions" % (bestunit, bestcomplexity-1)
    print(status)
    stop = timeit.default_timer()
    part2Time = stop - start
    print('Time for part 2 is: ', part2Time, "s")


test("../day5/input.txt")