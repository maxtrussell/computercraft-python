from enum import Enum
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
	}
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
	ACTIONS[OPS.TURN][turn_dir]
