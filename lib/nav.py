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

class CARDINALS(Enum):
	NORTH='NORTH'
	EAST='EAST'
	SOUTH='SOUTH'
	WEST='WEST'

# maps a direction to an axis
DIRS_TO_AXIS = {
	DIRS.UP: {
		'AXIS':AXIS.Z,
		'DIRECTION':1,
	},
	DIRS.DOWN: {
		'AXIS':AXIS.Z,
		'DIRECTION':-1,
	},
	DIRS.FORWARD: {
		CARDINALS.NORTH: {
			'AXIS':AXIS.Y,
			'DIRECTION':1,
		},
		CARDINALS.EAST: {
			'AXIS':AXIS.X,
			'DIRECTION':1,
		},
		CARDINALS.SOUTH: {
			'AXIS':AXIS.Y,
			'DIRECTION':-1,
		},
		CARDINALS.WEST: {
			'AXIS':AXIS.X,
			'DIRECTION':-1,
		},
	},
}

# maps cardinal direction and a turn to a resulting cardinal direction
TURN_TO_DIR = {
	CARDINALS.NORTH: {
		TURNS.LEFT:CARDINALS.WEST,
		TURNS.RIGHT:CARDINALS.EAST,
	},
	CARDINALS.EAST: {
		TURNS.LEFT:CARDINALS.NORTH,
		TURNS.RIGHT:CARDINALS.SOUTH,
	},
	CARDINALS.SOUTH: {
		TURNS.LEFT:CARDINALS.EAST,
		TURNS.RIGHT:CARDINALS.WEST,
	},
	CARDINALS.WEST: {
		TURNS.LEFT:CARDINALS.SOUTH,
		TURNS.RIGHT:CARDINALS.NORTH,
	},
}
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
	# getters
	def get_location(self):
		return self.location.copy()
	def get_direction(self):
		direction = self.direction
		if direction == CARDINALS.NORTH:
			return CARDINALS.NORTH
		elif direction == CARDINALS.EAST:
			return CARDINALS.EAST
		elif direction == CARDINALS.WEST:
			return CARDINALS.WEST
		else:
			return CARDINALS.SOUTH
	# change location depending on given direction
	def set_location(self, dir):
		if dir != DIRS.FORWARD:
			axis = DIRS_TO_AXIS[dir]['AXIS']
			direction = DIRS_TO_AXIS[dir]['DIRECTION']
		else:
			axis = DIRS_TO_AXIS[dir][self.direction]['AXIS']
			direction = DIRS_TO_AXIS[dir][self.direction]['DIRECTION']
		self.location[axis]+=direction

	# change direction given a turn direction
	def set_direction(self, turn_dir):
		self.direction = TURN_TO_DIR[self.direction][turn_dir]

	# move in the given direction
	def dir(self, move_dir, n=1):
		for i in range(n):
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

	# turn RIGHT or LEFT
	def turn(self, turn_dir):
		turn(turn_dir)
		self.set_direction(turn_dir)

	# turn to cardinal
	def turn_to(self, cardinal):
		if self.direction == cardinal:
			return
		elif DIRS_TO_AXIS[DIRS.FORWARD][self.direction]['AXIS'] == DIRS_TO_AXIS[DIRS.FORWARD][cardinal]['AXIS']:
			# change axis to be diffrent then desired axis
			self.turn(TURNS.LEFT)
		self.turn(TURNS.LEFT) if TURN_TO_DIR[self.direction][TURNS.LEFT] == cardinal else self.turn(TURNS.RIGHT)

	def go_to(self, location):
		# move z
		to_go = location[2] - self.location[2]
		if to_go > 0:
			self.force_dir(DIRS.UP, to_go)
		elif to_go < 0:
			self.force_dir(DIRS.DOWN, to_go * -1)
		# mov x
		to_go = location[0] - self.location[0]
		if to_go > 0:
			self.turn_to(CARDINALS.EAST)
			self.force_dir(DIRS.FORWARD, to_go)
		elif to_go < 0:
			self.turn_to(CARDINALS.WEST)
			self.force_dir(DIRS.FORWARD, to_go * -1)

		# mov y
		to_go = location[1] - self.location[1]
		if to_go > 0:
			self.turn_to(CARDINALS.NORTH)
			self.force_dir(DIRS.FORWARD, to_go)
		elif to_go < 0:
			self.turn_to(CARDINALS.SOUTH)
			self.force_dir(DIRS.FORWARD, to_go * -1)

		return True if self.location == location else False

