from __future__ import print_function
import string
import timeit

# Very good tools for small changes in stacks and queues
from collections import deque, defaultdict



# Add a global value as current marble indicates as a index

# Create a player class
class Player:
  def __init__(self, number):
    self.name = "player" + str(number)
    self.points = 0


class Board:
    def __init__(self, name, list, active):
        self.name = name
        self.list = list
        self.active = active

    '''
    Make a class function that contains the rules of marbles.
    '''

    def rules(self, newMarble):
        points = 0
        if newMarble % 23 == 0 and newMarble >1:
            if self.active -7 >= 0:
                    pointCollecter = self.list[self.active -7]
                    self.list = self.list[0:self.active - 7] + self.list[self.active - 6:len(self.list)]
                    self.active -= 7
            else:
                    pointCollecter = self.list[len(self.list)-self.active -7]
                    self.active = len(self.list) + self.active - 7
                    self.list = self.list[0:self.active]+self.list[self.active+1:len(self.list)]
            points += (newMarble +pointCollecter)
        elif newMarble <= 1:
            self.list += [newMarble]
            self.active += 1
        else:
            if not wallCheck(self.list,self.active+1) and not wallCheck(self.list,self.active+2):
                #print('hej!')
                self.list = self.list[0:self.active+2]+[newMarble]+self.list[self.active+2:len(self.list)]
                self.active += 2
            elif wallCheck(self.list , self.active+2) and not wallCheck(self.list , self.active+1):
                #print('hej!!')
                self.list += [newMarble]
                self.active += 2

            else:
                self.list = [self.list[0]] +[newMarble] + self.list[1:len(self.list)]
                self.active = 1
        return points




'''
Make a wall function, to check if we need to go around the circle
'''

def wallCheck(marbleList, index):
    state = False
    try:
        value = marbleList[index]
    except:
        state = True
    return state

def test(players, marbleLimit):
    start = timeit.default_timer()
    board = Board("marbleBoard",[0,1], 1)
    playerList = [Player(0)]*players
    for k in range(len(playerList)):
        playerList[k] = Player(k)
    max = 0
    turn = 0
    for i in range(2,marbleLimit+1):
        playerList[turn].points += board.rules(i)
        turn += 1
        if turn >= players:
            turn = 0

    for j in range(len(playerList)):
        if playerList[j].points > max:
            max = playerList[j].points
            name = playerList[j].name
    stop = timeit.default_timer()
    Time = stop - start
    print('The max amount of points is:', max, ' , With ', players, "amount of players and a total of ",
          marbleLimit, ' amount of marbles. With the winner being ',name , 'And time taken is',Time)


'''

Here is a smart solution that I cannot be credited for..., works simply about very very faster than the standard version.


'''


def play_game(max_players, last_marble):
    scores = defaultdict(int)
    circle = deque([0])

    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[marble % max_players] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)

    return max(scores.values()) if scores else 0

#Normal version
start = timeit.default_timer()
test(411, 72059)
#brutal version if you want to waste time
#test(411, 7205900)
#Good version if you wanna do it quickly
play_game(411, 7205900)

