#Include some standard libraries
from __future__ import print_function

import numpy as np
import random
#import argparse


#Just a test for custom input arguments
def argumentTest():

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                      help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                     const=sum, default=max,
                    help='sum the integers (default: find the max)')

    args = parser.parse_args()
    frequencyExchange = args.integers


    #print(args.accumulate(args.integers))


def frequencyFunction(basevalue, exchangeValue):
    currentvalue = basevalue + exchangeValue
    # Setup correct sign depending on input
    if exchangeValue > 0:
        sign = "+"
    else:
        sign = ""
    status = "Current frequency %s, change of %s%s; resulting frequency %s" % (
    basevalue, sign, exchangeValue,
    currentvalue)
    print(status)
    return currentvalue



def frequencyFunctionList(basevalue, integerList):
    currentvalue = basevalue

    for i in range(len(integerList)):
        basevalue = currentvalue
        currentvalue = basevalue + integerList[i]
        # Setup correct sign depending on input
        if frequencyExchange > 0:
            sign = "+"
        else:
            sign = "-"
        status = "Current frequency %s, change of %s%s; resulting frequency %s" % (
        basevalue, sign, integerList[i],
        currentvalue)
        print(status)
    return basevalue
# Current frequency  0, change of +1; resulting frequency  1.

def isInt(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def file_len(filename):
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def frequencyTest():
    baseValue = 0
    filepath = "input.txt"
    file = open(filepath, 'r')
    lengthOfFile = file_len(filepath)
    print(lengthOfFile)

    with open("input.txt") as fp:
        for cnt in range(lengthOfFile):
            line = fp.readline()
            print("Line {}: {}".format(cnt, line.strip()))
            intStatus = True
            value = ""
            startIndex = 1
            while intStatus == True:
                if isInt(line[startIndex]):
                    value = value + line[startIndex]
                    startIndex = startIndex +1
                    intStatus = isInt(line[startIndex])
            # Check sign
            if line[0] == "+":
                exchangeValue = float(value)
            else:
                exchangeValue = -1*float(value)
            # Update the value
            baseValue =frequencyFunction(baseValue,exchangeValue)

            #print(float(line))
            cnt += 1
    finalStatus = "The final result is %s" % baseValue
    print(finalStatus)


def frequencyTwiceTest():
    baseValue = 0
    filepath = "input.txt"
    file = open(filepath, 'r')
    lengthOfFile = file_len(filepath)

    # Create a list with a big amount of available objects from -100k to 100k
    listsize = 500000
    twiceList = np.zeros(listsize)
    twiceStatus = False
    # start at 0
    half = listsize/2
    twiceList[half] = 1

    #loop the data as many times as needed

    while twiceStatus is False:

        with open(filepath) as fp:
            for cnt in range(lengthOfFile):
                line = fp.readline()
                print("Line {}: {}".format(cnt, line.strip()))
                intStatus = True
                value = ""
                startIndex = 1
                while intStatus == True:
                    if isInt(line[startIndex]):
                        value = value + line[startIndex]
                        startIndex = startIndex + 1
                        intStatus = isInt(line[startIndex])
                # Check sign
                if line[0] == "+":
                    exchangeValue = float(value)

                else:
                    exchangeValue = -1 * float(value)
                # Update the value
                baseValue = frequencyFunction(baseValue, exchangeValue)

                twiceList[half + int(baseValue)] = twiceList[half + int(baseValue)] + 1
                if twiceList[half + int(baseValue)] == 2:
                    status = "First twice value is %s" % baseValue
                    print(status)
                    twiceStatus = True
                # Check sign and update the twice list

                if twiceStatus is True:
                    break
                # print(float(line))
                cnt += 1

def lentest():
    result = file_len("input.txt")
    print(result)

#lentest()
#frequencyTest()
frequencyTwiceTest()

