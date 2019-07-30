from itertools import count
import fileinput
import heapq

'''

This Methods is in whole learned from  Michael Fogleman and is different 
from my current method which utilizes arrowmaps to find the distance. 
My own methods is significant slower for more complex types of dungeons,
however it can be even fast if it uses smart mapping techniques.

His website is https://www.michaelfogleman.com/aoc18/ great read... 
to learn techniques and stuff.

'''

# General methods which are not class based

# Shortest path chooses the shortest path from a target and its enemies.
def shortest_paths(source, targets, occupied):
    result = []
    best = None
    visited = set(occupied)
    queue = [(0, [source])]
    while queue:
        distance, path = heapq.heappop(queue)
        if best and len(path) > best:
            return result
        node = path[-1]
        if node in targets:
            result.append(path)
            best = len(path)
            continue
        if node in visited:
            continue
        visited.add(node)
        for neighbor in adjacent({node}):
            if neighbor in visited:
                continue
            heapq.heappush(queue, (distance + 1, path + [neighbor]))
    return result

# Manhattan distance nuf said
def manhattan_distance(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1])

# adjacent returns all cells adjacent to the position
def adjacent(positions):
    return set((y + dy, x + dx)
        for y, x in positions
            for dy, dx in [(-1, 0), (0, -1), (0, 1), (1, 0)])

# choose_target determines which tile to move forward to
def choose_target(position, targets, occupied):
    if not targets:
        return None
    if position in targets:
        return position
    paths = shortest_paths(position, targets, occupied)
    ends = [x[-1] for x in paths]
    return min(ends) if ends else None

# choose_move chooses the move, that the unit moves by
def choose_move(position, target, occupied):
	if position == target:
		return position
	paths = shortest_paths(position, {target}, occupied)
	starts = [x[1] for x in paths]
	return min(starts) if starts else None

# A unit can either be an Elf (E) or Goblin (G) dependable on postion.
class Unit:
	def __init__(self, team, position):
		self.team = team
		self.position = position 
		self.hp = 200

# Then we need a model of the game which includes the models, units and round etc.
# Elf damage is specific for part 2
class Model:
	def __init__(self, lines, elf_attack=None):
		self.elf_attack = elf_attack
		self.walls = set()
		self.units = []
		self.rounds = 0
		for y, line in enumerate(lines):
			for x, c in enumerate(line.strip()):
				if c == "#":
					self.walls.add((y,x))
				elif c in 'EG':
					# Seperate c as character, y and x as coordinates
					self.units.append(Unit(c, (y,x)))

	def total_hp(self):
		return sum(x.hp for x in self.units if x.hp > 0)

	# Occupied function return set of occupied squares 	
	def occupied(self, unit=None):
		units = set(x.position for x in self.units
					if x != unit and x.hp > 0)
		return self.walls | units
	
	# get_move returns a new position for the unit during their turn
	def get_move(self, unit):
		occupied = self.occupied(unit)
		targets = set(x.position for x in self.units
					  if x.team != unit.team and x.hp > 0)
		if not targets:
			return None
		in_range = adjacent(targets) - occupied
		target = choose_target(unit.position, in_range, occupied)
		if target is None:
			return unit.position
		move = choose_move(unit.position, target, occupied)
		return move

	# choose_attack choose the target to attack given an attacker
	def get_attack(self, unit):
		units = [[x.hp, x.position, x] for x in self.units
			if x.team != unit.team and x.hp > 0 and
				manhattan_distance(unit.position, x.position) ==1]
		return min(units)[-1] if units else None

	# The step method that goes through each round
	def step(self):
		units = sorted(self.units, key=lambda x: x.position)
		for unit in units:
			if unit.hp <= 0:
				continue
			move = self.get_move(unit)
			if move is None:
				return False
			unit.position = move
			attack = self.get_attack(unit)
			if attack:
				if self.elf_attack:
					if unit.team == 'G':
						attack.hp -= 3
						if attack.hp <= 0:
							raise Exception
					else:
						attack.hp -= self.elf_attack
				else:
					attack.hp -= 3
		self.rounds += 1
		return True
	# After that there is a run method, to check if round is over or not
	def run(self):
		while True:
			if not self.step():
				return self.rounds, self.total_hp()
	
# Read in the lines 
lines = list(fileinput.input())

# part 1
rounds, hp = Model(lines).run()
print( "The total score for part 1 is: " + str(rounds * hp))

# part 2
for elf_attack in count(4):
	try:
		rounds, hp = Model(lines, elf_attack).run()
		print("The total score for part 2 is: " + str(rounds * hp))
		break
	except Exception:
		pass 
