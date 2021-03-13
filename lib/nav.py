from enum import Enum, IntEnum
from cc import import_file,turtle
fuel = import_file('/lib/fuel.py')

class DIRS(Enum):
	UP='UP'
	DOWN='DOWN'
	FORWARD='FORWARD'

class OPS(Enum):
	DIG='DIG'
	MOVE='MOVE'
	TURN='TURN'
        
class TURNS(Enum):
	LEFT='LEFT'
	RIGHT='RIGHT'

class AXIS(IntEnum):
	X=0
	Y=1
	Z=2

class CARDINALS(IntEnum):
	NORTH=0
	EAST=1
	SOUTH=2
	WEST=3

ACTIONS = {
	OPS.MOVE: {
		DIRS.UP:turtle.up,
		DIRS.DOWN:turtle.down,
		DIRS.FORWARD:turtle.forward,
	},
	OPS.DIG: {
		DIRS.UP:turtle.digUp,
		DIRS.DOWN:turtle.digDown,
		DIRS.FORWARD:turtle.dig,
	},
	OPS.TURN: {
		TURNS.LEFT:turtle.turnLeft,
		TURNS.RIGHT:turtle.turnRight,
	},
}

# destructively move n blocks
def force_dir(dir, n=1):
	for i in range(n):
		ACTIONS[OPS.DIG][dir]()

		while True:
			# keep trying until success
			# used to deal w/falling gravel etc.
			fuel.fuel()
			if ACTIONS[OPS.MOVE][dir]():
				break
			ACTIONS[OPS.DIG][dir]()

# move n blocks
def dir(dir, n=1):
	for i in range(n):
		fuel.fuel()
		if not ACTIONS[OPS.MOVE][dir]():
			return False
	return True

# turn a by a given direction
def turn(turn_dir):
	ACTIONS[OPS.TURN][turn_dir]()

class Navigator:
	def __init__(self, location=[0,0,0], direction=CARDINALS.NORTH):
		self.location=location
		self.direction=direction
	### GETTERS
	def get_location(self):
		return self.location.copy()
	def get_direction(self):
		return CARDINALS(self.direction)

	### SETTERS
	# change location depending on given direction
	def set_location(self, dir):
		if dir == DIRS.UP:
			axis = 2
			direction = 1
		elif dir == DIRS.DOWN:
			axis = 2
			direction = -1
		else:
			axis = 0 if self.get_direction() % 2 else 1
			direction = - 1 if self.get_direction() > 1 else 1
		self.location[axis]+=direction

	# change direction given a turn direction
	def set_direction(self, turn_dir):
		turn_dir = -1 if turn_dir == TURNS.LEFT else 1
		self.direction = CARDINALS((self.direction + turn_dir) % 4)

	## MOVERS
	# move in the given direction
	def dir(self, move_dir, n=1, to_do=None):
		for i in range(n):
			if to_do:
				to_do[0](to_do[1])
			if not dir(move_dir):
				return False
			self.set_location(move_dir)
		return True

	# force move
	def force_dir(self, move_dir, n=1, to_do=None):
		for i in range(n):
			if to_do:
				to_do[0](to_do[1])
			force_dir(move_dir)
			self.set_location(move_dir)

	## TURNERS
	# turn RIGHT or LEFT
	def turn(self, turn_dir):
		turn(turn_dir)
		self.set_direction(turn_dir)

	# turn to cardinal
	def turn_to(self, target):
		difference = target - self.direction
		direction = 1 if difference > 0 else -1
		turns = {-1:TURNS.LEFT, 1:TURNS.RIGHT}

		if abs(difference) > 2:
			self.turn(turns[-1 * direction])
		else:
			while difference:
				self.turn(turns[direction])
				difference -= direction

	## PATHERS
	# move once in any direction
	def step(self, axis, direction, n=1, do = None, force=False):
		move = self.force_dir if force else self.dir

		if axis == 3:
			move_dir = {1:DIRS.UP, -1:DIRS.DOWN}
			move(move_dir, n, do)
		else:
			if axis:
				target_cardinal = 0 if direction == 1 else 2
			else:
				target_cardinal = 1 if direction == 1 else 3

			initial_cardinal = self.get_direction()
			self.turn_to(target_cardinal)
			move(DIRS.FORWARD, n, do)
			self.turn_to(initial_cardinal)

	def pathing_brute(self, target, do=None, prefered_axis=0):

		while(self.location != target):
			difference = [a-b for a,b in zip(target, self.location)]
			direction = [1 if x > 0 else -1 for x in difference]
			print(difference)
			print(direction)

			for i in range(3):
				axis = prefered_axis + i % 3
				if difference[axis]:
					print(axis)
					print(difference[axis])
					self.step(axis, direction[axis], abs(difference[axis]), do, False)

	def go_to(self, target, do=False):
		self.pathing_brute(target, do)

