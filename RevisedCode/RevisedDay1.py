#Include some standard libraries
from __future__ import print_function
import numpy as np
import timeit


if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from usefulFunctions import *


def main(file_path):
    start = timeit.default_timer()
    length_of_file = file_len(filepath)
    sum = 0
    # Create register list for the frequency
    listSize = 1000000
    twiceList = np.zeros(listSize)
    twiceList[listSize / 2] = 1
    # loop the data as many times as needed
    finished = False
    while finished is False:
        with open(file_path) as fp:
            for cnt in range(length_of_file):
                line = fp.readline()
                sum += float(line)
                twiceList[listSize/2 + int(sum)] += 1

                if twiceList[listSize/2 + int(sum)] == 2:
                    info = "Frequency %s happen twice" % sum
                    print(info)
                    finished = True
                    break
    stop = timeit.default_timer()
    total_time = stop - start
    print('Time for part 2 is: ', total_time, "s")

main("../day1/input.txt")