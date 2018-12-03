#Include some standard libraries
from __future__ import print_function

import numpy as np

# #1238 @ 665,330: 13x13

def isAreaone(matrix, x,y,interval):
    trueMatrix = (matrix[x:x+interval,y:y+interval]==1)
    status = True
    for i in range(interval):
        for j in range(interval):
            if trueMatrix[i][j] == False:
                status = False
            if status == False:
                break
        if status == False:
            break
    return status


def makeRectangle(paintedMap, x, y):
    xmin = x
    xhigh = x
    i = x
    ymin = y
    ymax = y
    j = y
    # check the next value at the map
    xstatus = False
    ystatus = False
    while xstatus == False:
        if paintedMap[i+1][j] == 1:
            i = i + 1
        else:
            xhigh = i
            xstatus = True
    while ystatus == False:
        k = xmin
        while k <= xhigh:
            if paintedMap[k][j+1]!=1:
                ystatus = True
                ymax = j
                break
            elif k == xhigh:
                j = j+1
                k = xmin
            else:
                k = k + 1
    size =(xhigh-xmin)*(ymax-ymin)
    return ymin, ymax, xmin, xhigh, size

def checkRectExists(rectList,x,y):
    status = True
    for i in range(len(rectList)):
        #print(rectList)
        #print(x)
        #print(y)
        if rectList[i][0]<= x <= rectList[i][1] and rectList[i][2] <= y <= rectList[i][3]:
            status = False
            break
    #print(status)

    return status





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

def testFabric(filepath):
    lengthOfFile = file_len(filepath)
    pixelCount = 0
    # Create register matrix for the input data
    registerMatrix = np.zeros(shape=(lengthOfFile, 5))
    # Create work matrix, which is painted with the input in mind, let's make it really big
    paintMatrix = np.zeros(shape=(3000, 3000))

    # loop the data as many times as needed
    with open(filepath) as fp:
        for cnt in range(lengthOfFile):
            line = fp.readline()
            #print("Line {}: {}".format(cnt, line.strip()))
            registerlimit = [1, findIndex(line, "@")-1]
            registerMatrix[cnt][0] = line[registerlimit[0]:registerlimit[1]]
            registerinchLimit1 = [findIndex(line, "@") +1, findIndex(line, ",")]
            registerMatrix[cnt][1] = line[registerinchLimit1[0]:registerinchLimit1[1]]
            registerinchLimit2 = [findIndex(line, ",") + 1, findIndex(line, ":")]
            registerMatrix[cnt][2] = line[registerinchLimit2[0]:registerinchLimit2[1]]
            registerPaintLimit1 = [findIndex(line, ":") + 2, findIndex(line, "x")]
            registerMatrix[cnt][3] = line[registerPaintLimit1[0]:registerPaintLimit1[1]]
            registerPaintLimit2 = [findIndex(line,"x") +1, len(line)]
            registerMatrix[cnt][4] = line[registerPaintLimit2[0]:registerPaintLimit2[1]]

            #print(registerMatrix[cnt])

    # Now let's fill in the painting the data in mind!
    for cnt in range(lengthOfFile):
        inch1 = int(registerMatrix[cnt][1])
        inch2 = int(registerMatrix[cnt][2])
        paint1 = int(registerMatrix[cnt][3])
        paint2 = int(registerMatrix[cnt][4])
        paintx = [inch1, inch1+paint1]
        painty = [inch2,paint2+inch2]
        paintMatrix[paintx[0]:paintx[1],painty[0]:painty[1]] = paintMatrix[paintx[0]:paintx[1],painty[0]:painty[1]] +1
        status = "Paints at x coordinates from %s : %s in x coordinates and %s : %s in y coordinates" % (paintx[0]
        , paintx[1], painty[0], painty[1])
        #print(status)

    # Make a more refined matrix
    registerMatrixClean = np.zeros(shape=(lengthOfFile, 5))
    for cnt in range(lengthOfFile):
        registerMatrixClean[cnt][0] = registerMatrix[cnt][0]
        registerMatrixClean[cnt][1] = registerMatrix[cnt][1]
        registerMatrixClean[cnt][2] = registerMatrix[cnt][2]
        registerMatrixClean[cnt][3] = registerMatrix[cnt][1]+ registerMatrix[cnt][3] -1
        registerMatrixClean[cnt][4] = registerMatrix[cnt][2] + registerMatrix[cnt][4] -1


    # The painting is now filled, let's find every index that has a value of 2 or more

    for i in range(3000):
        for j in range(3000):
            if paintMatrix[i][j] >=2:
                pixelCount = pixelCount +1

    #print(pixelCount)

    # Now figure out where only one claim is alone
    uniqueMatrix = np.zeros(shape=(500, 4))
    uniqueMatrix[0,:]=[9999,10000, 9999, 10000]
    size = 1
    i = 0
    iteration = 1
    while i < 2500:
        j = 0
        while j < 2500:
            #use recangle and check triangle function
                if paintMatrix[i][j] == 1:
                    recInfo = makeRectangle(paintMatrix, i, j)
                    if checkRectExists(uniqueMatrix,i,j) and recInfo[4]>350:
                        status = "currently workng on %s and %s" % (i,j)
                        #print(status)
                        uniqueMatrix[iteration,:] = [ recInfo[2], recInfo[3], recInfo[0], recInfo[1]]
                       # uniqueMatrix=np.vstack([uniqueMatrix, [recInfo[2], recInfo[3], recInfo[0], recInfo[1]]])
                        status = "saved data is for x coordinates [%s,%s] and y coordinates [%s,%s]" % (recInfo[2]
                                                                            , recInfo[3],recInfo[0], recInfo[1])
                        print(status)

                        iteration = iteration + 1
                j = j+1
        i = i +1
    #print(iteration)

    #print(uniqueMatrix[0:10])

    uniqueXvalue = uniqueMatrix[0][0]
    uniqueYvalue = uniqueMatrix[0][1]
    # if 10000 <= number <= 30000:
    # Now find the correct ID
    ID = ""
    for cnt in range(lengthOfFile):
        for i in range(iteration):
            #print(i)
            if int(registerMatrixClean[cnt][1]) == int(uniqueMatrix[i][0]) and int(registerMatrixClean[cnt][3])\
                    == int(uniqueMatrix[i][1])\
                    and int(registerMatrixClean[cnt][2]) == int(uniqueMatrix[i][2]) and\
                    int(registerMatrixClean[cnt][4]) == int(uniqueMatrix[i][3]):

                ID = registerMatrix[cnt][0]
                break
    print(ID)

testFabric("input.txt")


