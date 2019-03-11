from __future__ import print_function
import string
import timeit
import re

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from usefulFunctions import *


'''
Create a player map class consisting of a 2D list
'''


class Playmap:
    def __init__(self, width, length, particleSize, centroidSize):
        self.playmap = [["." for x in range(length)] for z in range(width)]
        self.particleList = particleSize * [None]
        self.centroidList = centroidSize * [Centroid(0,0)]

    def print(self):
        for i in range(len(self.playmap)):
            stringOut =""
            for j in range(len(self.playmap)):
                stringOut += self.playmap[j][i]
            print(stringOut)

    def printRegion(self, xRegion, yRegion):
        for i in range(xRegion[0],xRegion[1]):
            stringOut =""
            for j in range(yRegion[0], yRegion[1]):
                stringOut += self.playmap[j][i]
            print(stringOut)

    def countPixel(self,xRegion, yRegion):
        amount = 0
        for i in range(xRegion[0],xRegion[1]):
            for j in range(yRegion[0], yRegion[1]):
                if self.playmap[j][i] == "#":
                    amount+=1
        print("The amount of pixels are "+str(amount))
        return amount


    def printRegionInterest(self,xRegion, yRegion, minPixels):
        if minPixels < self.countPixel(xRegion, yRegion):
            self.printRegion(xRegion, yRegion)

    def printCentroids(self):
        for i in range(len(self.centroidList)):
            print("Centroid number " +str(i)+ "is ["+str(self.centroidList[i].x)+", "+str(self.centroidList[i].y)+"].")


    def meanCoordinate(self, xRegion, yRegion):
        meanCoord = [xRegion[1]-xRegion[0]/2, yRegion[1]-yRegion[0]/2]
        candidateCoord = [0,0]
        amount = 0
        for i in range(xRegion[0],xRegion[1]):
            for j in range(yRegion[0], yRegion[1]):
                if self.playmap[j][i] == "#":
                    candidateCoord[0] += j
                    candidateCoord[1] += i
                    amount += 1
        if amount > 0:
            meanCoord = [candidateCoord[0]/amount,candidateCoord[1]/amount]
            print("New centroid is at [" +str(meanCoord[0])+ ", "+str(meanCoord[1])+"]")
        return meanCoord

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

        stepIndex = 0

        for j in range(len(self.centroidList)):
            distance = 999999
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


def setupParticles(filepath, width, length, centroids):
    lengthOfFile = file_len(filepath)
    visionMap = Playmap(width, length, lengthOfFile, centroids)
    with open(filepath) as fp:
        for cnt in range(lengthOfFile):
            line = fp.readline()
            [x, y, vx, vy] = preProcess(line)
            visionMap.particleList[cnt] = Particle(x + width/2, y+ length/2, vx, vy)
            #visionMap.particleList[cnt].x += width/2
            #visionMap.particleList[cnt].y += length/2
            particle = visionMap.particleList[cnt]
            visionMap.playmap[particle.x][particle.y] = "#"
    visionMap.intiateCentroids(len(visionMap.centroidList))
    return visionMap


'''
Next part is that we need a step function, that works through the velocity saved in each particle.
'''


def step(playMap):
    size = 10
    print(len(playMap.playmap))
    for i in range(len(playMap.particleList)):
        particle = playMap.particleList[i]
        playMap.playmap[particle.x][particle.y] = "."
        playMap.particleList[i].x += particle.xV
        playMap.particleList[i].y += particle.yV
        playMap.playmap[playMap.particleList[i].x][playMap.particleList[i].y] = "#"
    for j in range(len(playMap.centroidList)):
        xRegion = [playMap.centroidList[j].x - size, playMap.centroidList[j].x +size]
        yRegion = [playMap.centroidList[j].y - size, playMap.centroidList[j].x + size]

        meanCoord = playMap.meanCoordinate(xRegion,yRegion)
        playMap.centroidList[j].x = meanCoord[0]
        playMap.centroidList[j].y = meanCoord[1]
        centroid = [[meanCoord[0]-size,meanCoord[0]+size],[meanCoord[1]-size,meanCoord[1]+size]]
        playMap.printRegionInterest(centroid[0], centroid[1], 26)
    print("-----------------------End of the step!----------------------")
    return playMap


def playTest(filepath ,width, length, centroids):
    signMap = setupParticles(filepath, width, length, centroids)
    signMap.intiateCentroids(centroids)
    for time in range(3):
        signMap = step(signMap)
    print("Done")


def test(testString):
    [x,y,vx,vy] = preProcess(testString)
    test = "The Position is [%s, %s] and the Velocity is [%s, %s]." %(x, y ,vx , vy)
    print(test)


#playTest("../day10/example.txt", 50, 50, 8)
playTest("../day10/input.txt", 100000, 100000, 8)

#test("position=<-31684, -53051> velocity=< 3,  5>")