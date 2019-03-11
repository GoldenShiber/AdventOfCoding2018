from __future__ import print_function
import string
import timeit
import re

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from usefulFunctions import *


'''
Create a player map class consisting of a 2D list, with particles and centroids in it. With functions that works
on either the list, centroids or the particles.
'''


class Playmap:
    def __init__(self, particleSize, centroidSize):
        self.playmap = [["." for x in range(1)] for z in range(1)]
        self.particleList = particleSize * [None]
        self.centroidList = centroidSize * [Centroid(0,0)]

    def print(self):
        for i in range(len(self.playmap)):
            stringOut =""
            for j in range(len(self.playmap)):
                stringOut += self.playmap[j][i]
            print(stringOut)


    '''
    Function to check the amount of close particles to the centroid.
    '''


    def countPotential(self,xRegion, yRegion):
        amount = 0
        for i in range(len(self.particleList)):
            if  xRegion[0] <= self.particleList[i].x <= xRegion[1] and \
                yRegion[0] <= self.particleList[i].y <= yRegion[1]:
                amount+=1
        return amount


    '''
    Paint the map, that we want to print later to analyze.
    '''

    def paintMap(self, xRegion, yRegion):
        proxyRegionX = [0, xRegion[1] - xRegion[0]]
        proxyRegiony = [0, yRegion[1] - yRegion[0]]
        self.playmap = [["." for x in (range(xRegion[1] - xRegion[0])*2)] for z in (range(yRegion[1] - yRegion[0])*2)]
        for i in range(len(self.particleList)):
            if xRegion[0] <= self.particleList[i].x <= xRegion[1] and\
                    yRegion[0] <= self.particleList[i].y  <= yRegion[1]\
                    and self.particleList[i].y - yRegion[0] <= proxyRegiony[1]\
            and self.particleList[i].x - xRegion[0] <= proxyRegionX[1]:
                self.playmap[self.particleList[i].x - xRegion[0]][self.particleList[i].y - yRegion[0]] = "#"

    '''
    Print centroids if we want to...
    '''

    def printCentroids(self):
        for i in range(len(self.centroidList)):
            print("Centroid number " +str(i)+ "is ["+str(self.centroidList[i].x)+", "+str(self.centroidList[i].y)+"].")


    '''
    We move the centroids through a move system, following the mean value of all close particles.
    '''

    def moveCentroid(self, xRegion, yRegion, oldCoords):
        #else:
        meanCoords = self.meanCoordinate(xRegion, yRegion, oldCoords)
        newlocation = Centroid(meanCoords[0], meanCoords[1])

        return newlocation



    def meanCoordinate(self, xRegion, yRegion, oldCoords):
        proxyRegionX = [0, xRegion[1] - xRegion[0]]
        proxyRegiony = [0, yRegion[1] - yRegion[0]]
        meanCoord = [oldCoords[0], oldCoords[1]]
        candidateCoord = [0,0]
        amount = 0
        for i in range(len(self.particleList)):
            if xRegion[0] <= self.particleList[i].x <= xRegion[1] and\
                    yRegion[0] <= self.particleList[i].y  <= yRegion[1]\
                    and self.particleList[i].y <= proxyRegiony[1]\
            and self.particleList[i].x - xRegion[0] <= proxyRegionX[1]:
                    candidateCoord[0] += self.particleList[i].x
                    candidateCoord[1] += self.particleList[i].y
                    amount += 1
        if amount > 0:
            meanCoord = [candidateCoord[0]/amount,candidateCoord[1]/amount]
        return meanCoord

    '''
    Method to initiate centroids to the systems.
    '''

    def intiateCentroids(self, centroids):
        xValues =[]
        yValues =[]
        for i in range(len(self.particleList)):
            xValues.append(self.particleList[i].x)
            yValues.append(self.particleList[i].y)
        xValue = [min(xValues), max(xValues)]
        yValue = [min(yValues), max(yValues)]

        xStep = (max(xValues) -min(xValues))/centroids
        yStep = (max(xValues) - min(xValues))/centroids

        for j in range(len(self.centroidList)):
            distance = 99999999999999
            self.centroidList[j].x = xValue[0]+ j*xStep
            self.centroidList[j].y = yValue[0] + j*yStep
            centroidCandidate = self.centroidList[j]
            for k in range(len(self.particleList)):
                newDist = pow((pow(self.centroidList[j].x-self.particleList[k].x,2)+
                            pow(self.centroidList[j].y-self.particleList[k].y,2)),0.5)
                if newDist < distance:
                    distance = newDist
                    centroidCandidate = Centroid(self.particleList[k].x, self.particleList[k].y)
            self.centroidList[j] = centroidCandidate

        self.centroidList = self.filterCentroid()

        #print(xValue)
        #print(yValue)
        print(self.printCentroids())


    '''
    We want a unique centroid list...
    '''

    def filterCentroid(self):
        newList = [Centroid(0,0)]
        newList[0] = self.centroidList[0]
        for i in range(1,len(self.centroidList)):
            for j in range(len(newList)):
                if newList[j].x == self.centroidList[i].x and newList[j].y == self.centroidList[i].y:
                    break
                elif j is (len(newList)-1):
                    newList.append(self.centroidList[i])
        return newList


class Particle:
    def __init__(self, xPos, yPos, xVel, yVel):
        self.x = xPos
        self.y = yPos
        self.xV = xVel
        self.yV = yVel


class Centroid:
    def __init__(self ,xPos, yPos):
        self.x = xPos
        self.y = yPos

'''
Pre-Process the input file to get the Velocity as well as the initial positions of the particles.
'''

def preProcess(dataString):
    # Position is determined by
    # example "position=<-31684, -53051> velocity=< 3,  5>"
    dataSplit = re.split('<|>|, |=<', dataString )
    xPos = dataSplit[1]
    yPos = dataSplit[2]
    xVol = dataSplit[4]
    yVol = dataSplit[5]
    return int(xPos), int(yPos), int(xVol), int(yVol)


'''
Now we need a function to setup or particle map, by using a fixed information file base.
'''


def setupParticles(filepath, centroids):
    lengthOfFile = file_len(filepath)
    visionMap = Playmap(lengthOfFile, centroids)
    with open(filepath) as fp:
        for cnt in range(lengthOfFile):
            line = fp.readline()
            [x, y, vx, vy] = preProcess(line)
            visionMap.particleList[cnt] = Particle(x , y , vx, vy)
        visionMap.intiateCentroids(len(visionMap.centroidList))

    return visionMap


'''
Next part is that we need a step function, that works through the velocity saved in each particle.
'''


def step(playMap):
    size = 45
    status = 0
    for i in range(len(playMap.particleList)):
        particle = playMap.particleList[i]
        playMap.particleList[i].x += particle.xV
        playMap.particleList[i].y += particle.yV
    for j in range(len(playMap.centroidList)):
        xRegion = [playMap.centroidList[j].x - size, playMap.centroidList[j].x +size]
        yRegion = [playMap.centroidList[j].y - size, playMap.centroidList[j].y + size]
        oldCoords = [playMap.centroidList[j].x, playMap.centroidList[j].y]
        playMap.centroidList[j] = playMap.moveCentroid(xRegion,yRegion, oldCoords)
        if playMap.countPotential(xRegion,yRegion) > 150:
            playMap.paintMap(xRegion, yRegion)
            playMap.print()
            status = 1
            break
    playMap.centroidList = playMap.filterCentroid()
    return playMap, status

'''
And then it is the test...
'''


def playTest(filepath ,timeSteps, centroids):
    start = timeit.default_timer()
    status = 0
    signMap = setupParticles(filepath, centroids)
    signMap.intiateCentroids(centroids)
    for time in range(timeSteps):
        if status == 1:
            print(time)

        [signMap, status] = step(signMap)
        if time%100 == 0:
            print("-----------------------End of the step "+ str(time)+"!----------------------")
    print("Done")

    stop = timeit.default_timer()
    Time = stop - start

    print("Time taken to find the message is: "+ str(Time)+ " seconds!")


#playTest("../day10/example.txt",4, 2)
playTest("../day10/input.txt", 12000, 2)
