#Include some standard libraries
from __future__ import print_function
import operator

'''
Check if a char is of the integer type
'''

def isInt(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


'''
Find the amount of rows in a txt file
'''

def file_len(filename):
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

'''
With the time format of 1518-11-17 00:50 , the dateParser functions fetch the year, month
day,hours and minute of the string defining the time.
'''

def dateParser(timeString):
    # A time string determined by year, month day
    # example 1518-11-17 00:50
    year = timeString[0:4]
    month = timeString[5:7]
    day = timeString[8:10]
    hours = timeString[11:13]
    minutes = timeString[14:16]
    return year, month, day, hours, minutes

def dateParser2(timeString):
    # A time string determined by year, month day
    # example 1518-11-17 00:50
    timeSplit = timeString.split(" ")
    date = timeSplit[0].split("-")
    time = timeSplit[1].split(":")
    year = date[0]
    month = date[1]
    day = date[2]
    hours = time[0]
    minutes = time[1][0:2]
    return year, month, day, hours, minutes


''' 
    sort a table by multiple columns
        
    table: a list of lists (or tuple of tuples) where each inner list
    represents a row
    cols:  a list (or tuple) specifying the column numbers to sort by
    e.g. (1,0) would sort by column 1, then by column 0
'''

def sort_table(table, cols):
    for col in reversed(cols):
        table = sorted(table, key=operator.itemgetter(col))
    return table

'''
Find the index of a letter in a string, the first time it appears
'''

def findIndex(word, letter):
    lengthOfWord = len(word)
    index = 0
    for i in range(lengthOfWord):
        if word[i] == letter:
            index = i
            break
    return index


'''
Find max value in a list, as well as its index.
'''

def findMax(list):
    maxValue = max(list)
    for i in range(len(list)):
        if list[i] == maxValue:
            index = i
            break
    return maxValue, index


'''
Find min value in a list, as well as its index.
'''

def findMin(list):
    minValue = min(list)
    for i in range(len(list)):
        if list[i] == minValue:
            index = i
            break
    return minValue, index


'''
Cleans the string of any non integers
'''

def cleanIntString(line):

    lineProduct = ""
    for i in range(len(line)):
        if isInt(line[i]):
            lineProduct += line[i]
    return lineProduct
