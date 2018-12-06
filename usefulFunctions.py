#Include some standard libraries
from __future__ import print_function


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


def dateParser(timeString):
    # A time string determined by year, month day
    # example 1518-11-17 00:50
    year = timeString[0:4]
    month = timeString[5:7]
    day = timeString[8:10]
    hours = timeString[11:13]
    minutes = timeString[14:16]
    return year, month, day, hours, minutes


def sort_table(table, cols):
    """ sort a table by multiple columns
        table: a list of lists (or tuple of tuples) where each inner list
               represents a row
        cols:  a list (or tuple) specifying the column numbers to sort by
               e.g. (1,0) would sort by column 1, then by column 0
    """
    for col in reversed(cols):
        table = sorted(table, key=operator.itemgetter(col))
    return table


def findIndex(word, letter):
    lengthOfFile = len(word)
    index = 0
    for i in range(lengthOfFile):
        if word[i] == letter:
            index = i
            break
    return index


def findMax(list):
    maxValue = max(list)
    for i in range(len(list)):
        if list[i] == maxValue:
            index = i
            break
    return maxValue, index


def findMin(list):
    minValue = min(list)
    for i in range(len(list)):
        if list[i] == minValue:
            index = i
            break
    return minValue, index